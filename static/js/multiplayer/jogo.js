document.addEventListener(
    "DOMContentLoaded",
    () => {

        "use strict";


        // ====================================================
        // ELEMENTO PRINCIPAL
        // ====================================================

        const jogo =
            document.getElementById(
                "multiplayerGame"
            );


        if (!jogo) {

            console.warn(
                "[MULTIPLAYER] #multiplayerGame não encontrado."
            );

            return;
        }


        // ====================================================
        // HELPERS
        // ====================================================

        function pegarElemento(id) {

            return document.getElementById(
                id
            );
        }


        function converterBoolean(valor) {

            const convertido =
                String(
                    valor ?? ""
                )
                .trim()
                .toLowerCase();


            return [
                "true",
                "1",
                "sim",
                "yes"
            ].includes(
                convertido
            );
        }


        function escaparHtml(valor) {

            const elemento =
                document.createElement(
                    "div"
                );


            elemento.textContent =
                valor ?? "";


            return elemento.innerHTML;
        }


        function numeroSeguro(
            valor,
            padrao = 0
        ) {

            const numero =
                Number(
                    valor
                );


            return Number.isFinite(
                numero
            )
                ?
                numero
                :
                padrao;
        }


        // ====================================================
        // DADOS DA PARTIDA
        // ====================================================

        const codigo =
            String(
                jogo.dataset.codigo ||
                ""
            )
            .trim();


        const jogadorId =
            String(
                jogo.dataset.jogador ||
                ""
            )
            .trim();


        const host =
            converterBoolean(
                jogo.dataset.host
            );


        // ====================================================
        // DEBUG INICIAL
        // ====================================================

        console.log(
            "========================================"
        );

        console.log(
            "🎮 FLASHMATTY MULTIPLAYER"
        );

        console.log(
            "Código:",
            codigo
        );

        console.log(
            "Jogador:",
            jogadorId
        );

        console.log(
            "Host:",
            host
        );

        console.log(
            "data-host:",
            jogo.dataset.host
        );

        console.log(
            "========================================"
        );


        // ====================================================
        // VERIFICAÇÃO DE DADOS
        // ====================================================

        if (!codigo) {

            console.error(
                "[MULTIPLAYER] Código da sala ausente."
            );

            return;
        }


        if (!jogadorId) {

            console.error(
                "[MULTIPLAYER] ID do jogador ausente."
            );

            return;
        }


        // ====================================================
        // ELEMENTOS DA PÁGINA
        // ====================================================

        const area =
            pegarElemento(
                "areaPergunta"
            );


        const rodada =
            pegarElemento(
                "rodada"
            );


        const total =
            pegarElemento(
                "total"
            );


        const cronometro =
            pegarElemento(
                "cronometro"
            );


        const barra =
            pegarElemento(
                "tempoBarra"
            );


        if (!area) {

            console.error(
                "[MULTIPLAYER] #areaPergunta não encontrado."
            );

            return;
        }


        // ====================================================
        // SOCKET.IO DISPONÍVEL?
        // ====================================================

        if (
            typeof window.io !==
            "function"
        ) {

            console.error(
                "[MULTIPLAYER] Socket.IO não foi carregado."
            );


            area.innerHTML = `

                <div
                    class="
                        text-center
                        bg-red-50
                        border
                        border-red-200
                        rounded-3xl
                        p-8
                    "
                >

                    <div class="text-5xl">
                        ⚠️
                    </div>

                    <h2
                        class="
                            text-2xl
                            font-black
                            text-red-700
                            mt-4
                        "
                    >
                        Falha no multiplayer
                    </h2>

                    <p
                        class="
                            text-red-600
                            mt-2
                        "
                    >
                        O Socket.IO não foi carregado.
                    </p>

                </div>

            `;


            return;
        }


        // ====================================================
        // SOCKET.IO
        // ====================================================

        const socket =
            window.io(
                {
                    transports: [
                        "websocket",
                        "polling"
                    ],

                    reconnection:
                        true,

                    reconnectionAttempts:
                        Infinity,

                    reconnectionDelay:
                        800,

                    reconnectionDelayMax:
                        4000,

                    timeout:
                        10000
                }
            );


        // ====================================================
        // ESTADO LOCAL
        // ====================================================

        let timer =
            null;


        let respondeu =
            false;


        let rodadaEncerrada =
            false;


        let redirecionando =
            false;


        let questaoAtiva =
            false;


        let solicitandoQuestao =
            false;


        let primeiraQuestaoSolicitada =
            false;


        let tempoEsgotadoEnviado =
            false;


        let ultimaRodada =
            null;


        // ====================================================
        // SONS
        // ====================================================

        function tocarSom(nome) {

            try {

                const funcao =
                    window[
                        nome
                    ];


                if (
                    typeof funcao ===
                    "function"
                ) {

                    funcao();
                }

            } catch (erro) {

                console.warn(
                    `[SOM] Falha em ${nome}:`,
                    erro
                );
            }
        }


        // ====================================================
        // STATUS DE CONEXÃO
        // ====================================================

        function obterStatusConexao() {

            let status =
                document.getElementById(
                    "statusMultiplayer"
                );


            if (status) {

                return status;
            }


            status =
                document.createElement(
                    "div"
                );


            status.id =
                "statusMultiplayer";


            status.className = `
                fixed
                bottom-4
                right-4
                z-50
                rounded-full
                px-4
                py-2
                text-xs
                font-black
                shadow-lg
                transition
                duration-300
            `;


            document.body.appendChild(
                status
            );


            return status;
        }


        function mostrarStatus(
            mensagem,
            tipo = "normal"
        ) {

            const status =
                obterStatusConexao();


            status.textContent =
                mensagem;


            status.className = `
                fixed
                bottom-4
                right-4
                z-50
                rounded-full
                px-4
                py-2
                text-xs
                font-black
                shadow-lg
                transition
                duration-300
            `;


            if (
                tipo ===
                "online"
            ) {

                status.classList.add(
                    "bg-green-600",
                    "text-white"
                );

            }

            else if (
                tipo ===
                "erro"
            ) {

                status.classList.add(
                    "bg-red-600",
                    "text-white"
                );

            }

            else {

                status.classList.add(
                    "bg-slate-800",
                    "text-white"
                );
            }


            if (
                tipo ===
                "online"
            ) {

                setTimeout(
                    () => {

                        if (
                            status.textContent ===
                            mensagem
                        ) {

                            status.style.opacity =
                                "0";

                        }

                    },
                    1800
                );


                setTimeout(
                    () => {

                        status.style.display =
                            "none";

                    },
                    2200
                );

            } else {

                status.style.display =
                    "block";

                status.style.opacity =
                    "1";
            }
        }


        // ====================================================
        // ALTERAR TEXTO COM SEGURANÇA
        // ====================================================

        function definirTexto(
            elemento,
            valor
        ) {

            if (!elemento) {
                return;
            }


            elemento.textContent =
                valor;
        }


        // ====================================================
        // BARRA DO TEMPO
        // ====================================================

        function definirBarra(
            porcentagem
        ) {

            if (!barra) {
                return;
            }


            const valor =
                Math.max(
                    0,
                    Math.min(
                        100,
                        numeroSeguro(
                            porcentagem
                        )
                    )
                );


            barra.style.width =
                `${valor}%`;
        }


        // ====================================================
        // DESABILITAR ALTERNATIVAS
        // ====================================================

        function desabilitarAlternativas() {

            const container =
                document.getElementById(
                    "alternativas"
                );


            if (!container) {
                return;
            }


            container
                .querySelectorAll(
                    "button"
                )
                .forEach(
                    botao => {

                        botao.disabled =
                            true;

                    }
                );
        }


        // ====================================================
        // PARAR CRONÔMETRO
        // ====================================================

        function pararTimer() {

            if (
                timer !==
                null
            ) {

                clearInterval(
                    timer
                );


                timer =
                    null;
            }
        }


        // ====================================================
        // ENTRAR NA SALA SOCKET
        // ====================================================

        function entrarNaSalaSocket() {

            if (
                !socket.connected
            ) {

                return;
            }


            console.log(
                "[MULTIPLAYER] Entrando na sala:",
                codigo,
                jogadorId
            );


            socket.emit(
                "entrar_socket",
                {
                    codigo:
                        codigo,

                    jogador_id:
                        jogadorId
                }
            );
        }


        // ====================================================
        // SOLICITAR PRÓXIMA QUESTÃO
        // ====================================================

        function solicitarProximaQuestao() {

            if (!host) {

                console.warn(
                    "[MULTIPLAYER] Apenas o host pode solicitar questão."
                );

                return;
            }


            if (
                !socket.connected
            ) {

                console.warn(
                    "[MULTIPLAYER] Socket desconectado."
                );

                mostrarStatus(
                    "Reconectando...",
                    "erro"
                );

                return;
            }


            if (
                solicitandoQuestao
            ) {

                console.log(
                    "[MULTIPLAYER] Já existe uma solicitação de questão."
                );

                return;
            }


            solicitandoQuestao =
                true;


            console.log(
                "[MULTIPLAYER] Solicitando próxima questão."
            );


            socket.emit(
                "proxima_questao",
                {
                    codigo:
                        codigo,

                    jogador_id:
                        jogadorId
                }
            );


            /*
            Se o servidor não responder,
            permitimos nova tentativa.
            */

            setTimeout(
                () => {

                    if (
                        solicitandoQuestao
                        &&
                        !questaoAtiva
                    ) {

                        console.warn(
                            "[MULTIPLAYER] Servidor não retornou questão."
                        );


                        solicitandoQuestao =
                            false;
                    }

                },
                6000
            );
        }


        // ====================================================
        // SOCKET CONECTADO
        // ====================================================

        socket.on(
            "connect",
            () => {

                console.log(
                    "[MULTIPLAYER] Socket conectado:",
                    socket.id
                );


                mostrarStatus(
                    "● Conectado",
                    "online"
                );


                entrarNaSalaSocket();


                /*
                O host solicita a primeira pergunta.

                Pequeno atraso garante que o evento
                entrar_socket chegue antes.
                */

                if (
                    host
                    &&
                    !questaoAtiva
                    &&
                    !primeiraQuestaoSolicitada
                ) {

                    primeiraQuestaoSolicitada =
                        true;


                    setTimeout(
                        () => {

                            if (
                                socket.connected
                                &&
                                !questaoAtiva
                                &&
                                !rodadaEncerrada
                            ) {

                                console.log(
                                    "[MULTIPLAYER] Host solicitando primeira questão."
                                );


                                solicitarProximaQuestao();
                            }

                        },
                        1000
                    );
                }

            }
        );


        // ====================================================
        // DESCONECTADO
        // ====================================================

        socket.on(
            "disconnect",
            motivo => {

                console.warn(
                    "[MULTIPLAYER] Socket desconectado:",
                    motivo
                );


                mostrarStatus(
                    "● Reconectando...",
                    "erro"
                );

            }
        );


        // ====================================================
        // ERRO DE CONEXÃO
        // ====================================================

        socket.on(
            "connect_error",
            erro => {

                console.error(
                    "[MULTIPLAYER] Erro Socket.IO:",
                    erro
                );


                mostrarStatus(
                    "Falha de conexão",
                    "erro"
                );

            }
        );


        // ====================================================
        // RECONEXÃO
        // ====================================================

        if (
            socket.io
        ) {

            socket.io.on(
                "reconnect_attempt",
                tentativa => {

                    console.log(
                        "[MULTIPLAYER] Tentando reconectar:",
                        tentativa
                    );


                    mostrarStatus(
                        "Reconectando...",
                        "erro"
                    );

                }
            );


            socket.io.on(
                "reconnect",
                tentativa => {

                    console.log(
                        "[MULTIPLAYER] Reconectado após",
                        tentativa,
                        "tentativas."
                    );

                }
            );
        }


        // ====================================================
        // NOVA QUESTÃO
        // ====================================================

        socket.on(
            "nova_questao",
            dados => {

                console.log(
                    "[MULTIPLAYER] Nova questão:",
                    dados
                );


                if (!dados) {

                    return;
                }


                pararTimer();


                solicitandoQuestao =
                    false;


                questaoAtiva =
                    true;


                respondeu =
                    false;


                rodadaEncerrada =
                    false;


                tempoEsgotadoEnviado =
                    false;


                ultimaRodada =
                    dados.rodada ??
                    ultimaRodada;


                definirTexto(
                    rodada,
                    dados.rodada ??
                    "-"
                );


                definirTexto(
                    total,
                    dados.total ??
                    "-"
                );


                // ============================================
                // DADOS DO MODO
                // ============================================

                const modo =
                    dados.modo ||
                    "classico";


                const modoNome =
                    dados.modo_nome ||
                    "Clássico";


                const modoIcone =
                    dados.modo_icone ||
                    "🎮";


                const efeito =
                    dados.efeito ||
                    "";


                const multiplicador =
                    numeroSeguro(
                        dados.multiplicador,
                        1
                    );


                let avisoModo =
                    "";


                if (
                    modo !==
                    "classico"
                    ||
                    efeito
                    ||
                    multiplicador > 1
                ) {

                    avisoModo = `

                        <div
                            class="
                                max-w-xl
                                mx-auto
                                mb-7

                                bg-indigo-50

                                border
                                border-indigo-100

                                rounded-2xl

                                p-4
                                text-center
                            "
                        >

                            <div
                                class="
                                    text-sm
                                    font-black
                                    text-indigo-700
                                "
                            >
                                ${escaparHtml(modoIcone)}
                                ${escaparHtml(modoNome)}
                            </div>


                            ${
                                efeito
                                    ?
                                    `
                                    <p
                                        class="
                                            text-sm
                                            text-indigo-600
                                            mt-1
                                        "
                                    >
                                        ${escaparHtml(efeito)}
                                    </p>
                                    `
                                    :
                                    ""
                            }


                            ${
                                multiplicador > 1
                                    ?
                                    `
                                    <div
                                        class="
                                            inline-flex

                                            mt-3

                                            px-3
                                            py-1

                                            rounded-full

                                            bg-indigo-600
                                            text-white

                                            text-xs
                                            font-black
                                        "
                                    >
                                        ⚡ ${multiplicador}x PONTOS
                                    </div>
                                    `
                                    :
                                    ""
                            }

                        </div>

                    `;
                }


                // ============================================
                // PERGUNTA
                // ============================================

                area.innerHTML = `

                    ${avisoModo}

                    <div
                        class="
                            max-w-3xl
                            mx-auto
                        "
                    >

                        <h1
                            class="
                                text-2xl
                                md:text-4xl

                                font-black
                                text-center
                                text-slate-900

                                leading-tight

                                px-2
                            "
                        >
                            ${escaparHtml(
                                dados.pergunta ||
                                "Questão"
                            )}
                        </h1>


                        <div
                            id="alternativas"

                            class="
                                grid
                                grid-cols-1
                                sm:grid-cols-2

                                gap-4

                                mt-10
                            "
                        >
                        </div>

                    </div>

                `;


                const container =
                    document.getElementById(
                        "alternativas"
                    );


                const alternativas =
                    Array.isArray(
                        dados.alternativas
                    )
                        ?
                        dados.alternativas
                        :
                        [];


                if (
                    !container
                ) {

                    console.error(
                        "[MULTIPLAYER] Container de alternativas ausente."
                    );

                    return;
                }


                if (
                    alternativas.length ===
                    0
                ) {

                    container.innerHTML = `

                        <div
                            class="
                                sm:col-span-2
                                text-center
                                bg-red-50
                                text-red-600
                                rounded-2xl
                                p-5
                                font-bold
                            "
                        >
                            Nenhuma alternativa foi recebida.
                        </div>

                    `;


                    console.error(
                        "[MULTIPLAYER] Questão sem alternativas:",
                        dados
                    );


                    return;
                }


                // ============================================
                // ALTERNATIVAS
                // ============================================

                const simbolos = [
                    "▲",
                    "◆",
                    "●",
                    "■",
                    "★",
                    "⬢"
                ];


                alternativas.forEach(
                    (
                        alternativa,
                        indice
                    ) => {

                        const botao =
                            document.createElement(
                                "button"
                            );


                        botao.type =
                            "button";


                        botao.dataset.resposta =
                            String(
                                alternativa
                            );


                        botao.className = `
                            min-h-28

                            border-2
                            border-slate-200

                            rounded-3xl

                            p-5

                            text-xl
                            md:text-2xl

                            font-black

                            bg-white
                            text-slate-900

                            shadow-sm

                            transition
                            duration-200

                            hover:border-indigo-500
                            hover:bg-indigo-50
                            hover:-translate-y-1

                            active:scale-[0.98]

                            disabled:cursor-not-allowed
                            disabled:opacity-70
                        `;


                        const simbolo =
                            simbolos[
                                indice
                            ]
                            ||
                            "●";


                        botao.textContent =
                            `${simbolo} ${alternativa}`;


                        botao.addEventListener(
                            "click",
                            () => {

                                if (
                                    respondeu
                                    ||
                                    rodadaEncerrada
                                    ||
                                    !questaoAtiva
                                ) {

                                    return;
                                }


                                tocarSom(
                                    "somSelecao"
                                );


                                respondeu =
                                    true;


                                const botoes =
                                    container
                                        .querySelectorAll(
                                            "button"
                                        );


                                botoes.forEach(
                                    outroBotao => {

                                        outroBotao.disabled =
                                            true;

                                    }
                                );


                                botao.classList.remove(
                                    "border-slate-200",
                                    "bg-white"
                                );


                                botao.classList.add(
                                    "border-indigo-600",
                                    "bg-indigo-100",
                                    "ring-4",
                                    "ring-indigo-100"
                                );


                                console.log(
                                    "[MULTIPLAYER] Resposta enviada:",
                                    alternativa
                                );


                                socket.emit(
                                    "responder",
                                    {
                                        codigo:
                                            codigo,

                                        jogador_id:
                                            jogadorId,

                                        resposta:
                                            String(
                                                alternativa
                                            )
                                    }
                                );

                            }
                        );


                        container.appendChild(
                            botao
                        );
                    }
                );


                // ============================================
                // CRONÔMETRO
                // ============================================

                iniciarTimer(
                    numeroSeguro(
                        dados.tempo,
                        20
                    )
                );

            }
        );


        // ====================================================
        // RESPOSTA RECEBIDA
        // ====================================================

        socket.on(
            "resposta_recebida",
            dados => {

                console.log(
                    "[MULTIPLAYER] Resposta recebida:",
                    dados
                );


                if (!dados) {

                    return;
                }


                const anterior =
                    document.getElementById(
                        "feedbackResposta"
                    );


                if (anterior) {

                    anterior.remove();
                }


                const feedback =
                    document.createElement(
                        "div"
                    );


                feedback.id =
                    "feedbackResposta";


                // ============================================
                // ACERTO
                // ============================================

                if (
                    dados.correto
                ) {

                    tocarSom(
                        "somAcerto"
                    );


                    feedback.className = `
                        max-w-xl
                        mx-auto

                        mt-6

                        text-center

                        bg-green-100

                        border
                        border-green-200

                        text-green-700

                        rounded-2xl

                        p-4

                        font-black
                    `;


                    const pontos =
                        numeroSeguro(
                            dados.pontos
                        );


                    const totalPontos =
                        numeroSeguro(
                            dados.total_pontos
                        );


                    const sequencia =
                        numeroSeguro(
                            dados.sequencia
                        );


                    feedback.innerHTML = `

                        <div
                            class="
                                text-xl
                                md:text-2xl
                            "
                        >
                            ✅ Correto!
                        </div>


                        <div
                            class="
                                text-2xl
                                md:text-3xl

                                mt-2
                            "
                        >
                            +${pontos} pontos
                        </div>


                        ${
                            sequencia > 1
                                ?
                                `
                                <div
                                    class="
                                        mt-2
                                        text-sm
                                        text-orange-600
                                    "
                                >
                                    🔥 ${sequencia}
                                    acertos seguidos
                                </div>
                                `
                                :
                                ""
                        }


                        ${
                            totalPontos > 0
                                ?
                                `
                                <div
                                    class="
                                        mt-2
                                        text-xs
                                        text-green-600
                                    "
                                >
                                    Total:
                                    ${totalPontos}
                                    pontos
                                </div>
                                `
                                :
                                ""
                        }

                    `;

                }

                // ============================================
                // ERRO
                // ============================================

                else {

                    tocarSom(
                        "somErro"
                    );


                    feedback.className = `
                        max-w-xl
                        mx-auto

                        mt-6

                        text-center

                        bg-red-100

                        border
                        border-red-200

                        text-red-600

                        rounded-2xl

                        p-4

                        font-black
                    `;


                    const pontos =
                        numeroSeguro(
                            dados.pontos
                        );


                    let penalidade =
                        "";


                    if (
                        pontos < 0
                    ) {

                        penalidade = `

                            <div
                                class="
                                    mt-2
                                    text-xl
                                "
                            >
                                ${pontos} pontos
                            </div>

                        `;
                    }


                    feedback.innerHTML = `

                        <div
                            class="
                                text-xl
                            "
                        >
                            ❌ Resposta incorreta
                        </div>

                        ${penalidade}

                    `;
                }


                area.appendChild(
                    feedback
                );

            }
        );


        // ====================================================
        // RODADA FINALIZADA
        // ====================================================

        socket.on(
            "rodada_finalizada",
            dados => {

                console.log(
                    "[MULTIPLAYER] Rodada finalizada:",
                    dados
                );


                if (!dados) {

                    return;
                }


                rodadaEncerrada =
                    true;


                respondeu =
                    true;


                questaoAtiva =
                    false;


                solicitandoQuestao =
                    false;


                pararTimer();


                definirTexto(
                    cronometro,
                    "⏱️ 0"
                );


                definirBarra(
                    0
                );


                desabilitarAlternativas();


                const ranking =
                    Array.isArray(
                        dados.ranking
                    )
                        ?
                        dados.ranking
                        :
                        [];


                let rankingHtml =
                    "";


                ranking
                    .slice(
                        0,
                        5
                    )
                    .forEach(
                        jogador => {

                            const posicao =
                                numeroSeguro(
                                    jogador.posicao
                                );


                            let medalha =
                                `${posicao}º`;


                            if (
                                posicao === 1
                            ) {

                                medalha =
                                    "🥇";

                            }

                            else if (
                                posicao === 2
                            ) {

                                medalha =
                                    "🥈";

                            }

                            else if (
                                posicao === 3
                            ) {

                                medalha =
                                    "🥉";
                            }


                            const jogadorAtual =
                                String(
                                    jogador.id ??
                                    ""
                                )
                                ===
                                String(
                                    jogadorId
                                );


                            rankingHtml += `

                                <div
                                    class="
                                        flex
                                        items-center
                                        justify-between

                                        gap-4

                                        ${
                                            jogadorAtual
                                                ?
                                                "bg-indigo-50 border-indigo-300"
                                                :
                                                "bg-slate-100 border-slate-200"
                                        }

                                        border

                                        rounded-2xl

                                        p-4
                                    "
                                >

                                    <div
                                        class="
                                            flex
                                            items-center
                                            gap-3
                                            min-w-0
                                        "
                                    >

                                        <span
                                            class="
                                                text-2xl
                                                shrink-0
                                            "
                                        >
                                            ${medalha}
                                        </span>


                                        <span
                                            class="
                                                font-bold
                                                truncate
                                            "
                                        >
                                            ${escaparHtml(
                                                jogador.nome ||
                                                "Jogador"
                                            )}

                                            ${
                                                jogadorAtual
                                                    ?
                                                    " (você)"
                                                    :
                                                    ""
                                            }
                                        </span>

                                    </div>


                                    <strong
                                        class="
                                            text-indigo-600
                                            shrink-0
                                        "
                                    >
                                        ${numeroSeguro(
                                            jogador.pontos
                                        )}
                                    </strong>

                                </div>

                            `;
                        }
                    );


                if (!rankingHtml) {

                    rankingHtml = `

                        <div
                            class="
                                text-center
                                text-slate-500
                                p-4
                            "
                        >
                            Ranking indisponível.
                        </div>

                    `;
                }


                // ============================================
                // MOTIVO
                // ============================================

                let mensagemFim =
                    "";


                if (
                    dados.motivo ===
                    "tempo"
                ) {

                    mensagemFim = `

                        <p
                            class="
                                text-orange-500
                                font-bold
                                mt-2
                            "
                        >
                            ⏱️ Tempo esgotado
                        </p>

                    `;
                }


                // ============================================
                // RANKING
                // ============================================

                area.innerHTML = `

                    <div
                        class="
                            max-w-2xl
                            mx-auto
                        "
                    >

                        <div class="text-center">

                            <div class="text-5xl">
                                🏆
                            </div>


                            <h2
                                class="
                                    text-3xl
                                    font-black
                                    text-slate-900

                                    mt-3
                                "
                            >
                                Ranking
                            </h2>


                            ${mensagemFim}


                            <p
                                class="
                                    text-slate-500
                                    mt-3
                                "
                            >
                                Resposta correta:

                                <strong
                                    class="
                                        text-green-600
                                    "
                                >
                                    ${escaparHtml(
                                        dados.correta ??
                                        "-"
                                    )}
                                </strong>

                            </p>

                        </div>


                        <div
                            class="
                                space-y-2
                                mt-7
                            "
                        >
                            ${rankingHtml}
                        </div>

                    </div>

                `;


                // ============================================
                // HOST
                // ============================================

                if (
                    host
                ) {

                    const proximo =
                        document.createElement(
                            "button"
                        );


                    proximo.type =
                        "button";


                    proximo.className = `
                        block

                        w-full
                        max-w-2xl
                        mx-auto

                        bg-indigo-600
                        hover:bg-indigo-700

                        active:scale-[0.99]

                        text-white

                        rounded-2xl

                        p-4

                        text-lg
                        font-black

                        mt-7

                        shadow-lg

                        transition

                        disabled:opacity-60
                        disabled:cursor-not-allowed
                    `;


                    proximo.textContent =
                        dados.terminou
                            ?
                            "Ver pódio 🏆"
                            :
                            "Próxima rodada →";


                    proximo.addEventListener(
                        "click",
                        () => {

                            if (
                                proximo.disabled
                            ) {

                                return;
                            }


                            tocarSom(
                                "somClique"
                            );


                            proximo.disabled =
                                true;


                            if (
                                dados.terminou
                            ) {

                                irResultado();

                                return;
                            }


                            proximo.textContent =
                                "⏳ Carregando...";


                            rodadaEncerrada =
                                false;


                            solicitarProximaQuestao();

                        }
                    );


                    area.appendChild(
                        proximo
                    );

                }

                // ============================================
                // OUTROS JOGADORES
                // ============================================

                else {

                    const espera =
                        document.createElement(
                            "p"
                        );


                    espera.className = `
                        text-center

                        text-slate-500
                        font-bold

                        mt-7
                    `;


                    espera.textContent =
                        dados.terminou
                            ?
                            "🏆 Preparando o pódio..."
                            :
                            "⏳ Aguardando o anfitrião...";


                    area.appendChild(
                        espera
                    );


                    if (
                        dados.terminou
                    ) {

                        setTimeout(
                            irResultado,
                            1800
                        );
                    }

                }

            }
        );


        // ====================================================
        // PARTIDA FINALIZADA
        // ====================================================

        socket.on(
            "partida_finalizada",
            dados => {

                console.log(
                    "[MULTIPLAYER] Partida finalizada:",
                    dados
                );


                questaoAtiva =
                    false;


                rodadaEncerrada =
                    true;


                pararTimer();


                tocarSom(
                    "somConcluido"
                );


                setTimeout(
                    irResultado,
                    1000
                );

            }
        );


        // ====================================================
        // ERRO DA SALA
        // ====================================================

        socket.on(
            "erro_sala",
            dados => {

                const mensagem =
                    dados?.mensagem ||
                    "Ocorreu um erro na partida.";


                console.error(
                    "[MULTIPLAYER] erro_sala:",
                    mensagem,
                    dados
                );


                solicitandoQuestao =
                    false;


                mostrarStatus(
                    mensagem,
                    "erro"
                );


                /*
                Não usamos apenas alert.
                A mensagem também aparece na tela.
                */

                const erroAnterior =
                    document.getElementById(
                        "erroMultiplayer"
                    );


                if (
                    erroAnterior
                ) {

                    erroAnterior.remove();
                }


                const aviso =
                    document.createElement(
                        "div"
                    );


                aviso.id =
                    "erroMultiplayer";


                aviso.className = `
                    max-w-xl
                    mx-auto

                    bg-red-100

                    border
                    border-red-200

                    text-red-700

                    rounded-2xl

                    p-4
                    mt-5

                    text-center
                    font-bold
                `;


                aviso.textContent =
                    mensagem;


                area.appendChild(
                    aviso
                );

            }
        );


        // ====================================================
        // IR PARA RESULTADO
        // ====================================================

        function irResultado() {

            if (
                redirecionando
            ) {

                return;
            }


            redirecionando =
                true;


            pararTimer();


            console.log(
                "[MULTIPLAYER] Indo para resultado."
            );


            window.location.href =
                `/multiplayer/resultado/${
                    encodeURIComponent(
                        codigo
                    )
                }`;

        }


        // ====================================================
        // CRONÔMETRO
        // ====================================================

        function iniciarTimer(
            segundos
        ) {

            pararTimer();


            segundos =
                numeroSeguro(
                    segundos,
                    20
                );


            if (
                segundos <= 0
            ) {

                segundos =
                    20;
            }


            tempoEsgotadoEnviado =
                false;


            const duracao =
                segundos * 1000;


            const inicio =
                Date.now();


            const fim =
                inicio + duracao;


            definirTexto(
                cronometro,
                `⏱️ ${segundos}`
            );


            definirBarra(
                100
            );


            if (
                cronometro
            ) {

                cronometro.classList.remove(
                    "text-red-600",
                    "text-orange-500"
                );
            }


            function atualizar() {

                const agora =
                    Date.now();


                const restanteMs =
                    Math.max(
                        0,
                        fim - agora
                    );


                const restante =
                    Math.ceil(
                        restanteMs /
                        1000
                    );


                const porcentagem =
                    (
                        restanteMs /
                        duracao
                    )
                    *
                    100;


                definirTexto(
                    cronometro,
                    `⏱️ ${restante}`
                );


                definirBarra(
                    porcentagem
                );


                // ============================================
                // CORES DO TEMPO
                // ============================================

                if (
                    cronometro
                ) {

                    cronometro.classList.remove(
                        "text-red-600",
                        "text-orange-500"
                    );


                    if (
                        porcentagem <=
                        25
                    ) {

                        cronometro.classList.add(
                            "text-red-600"
                        );

                    }

                    else if (
                        porcentagem <=
                        50
                    ) {

                        cronometro.classList.add(
                            "text-orange-500"
                        );
                    }

                }


                // ============================================
                // TEMPO ESGOTADO
                // ============================================

                if (
                    restanteMs <=
                    0
                ) {

                    pararTimer();


                    rodadaEncerrada =
                        true;


                    respondeu =
                        true;


                    desabilitarAlternativas();


                    /*
                    O servidor também pode possuir timer.

                    Esta flag garante que este navegador
                    nunca envie tempo_esgotado duas vezes.
                    */

                    if (
                        host
                        &&
                        !tempoEsgotadoEnviado
                        &&
                        socket.connected
                    ) {

                        tempoEsgotadoEnviado =
                            true;


                        console.log(
                            "[MULTIPLAYER] Host informou tempo esgotado."
                        );


                        socket.emit(
                            "tempo_esgotado",
                            {
                                codigo:
                                    codigo,

                                jogador_id:
                                    jogadorId,

                                rodada:
                                    ultimaRodada
                            }
                        );
                    }

                }

            }


            atualizar();


            timer =
                setInterval(
                    atualizar,
                    100
                );
        }


        // ====================================================
        // SAÍDA DA PÁGINA
        // ====================================================

        window.addEventListener(
            "beforeunload",
            () => {

                pararTimer();

            }
        );

    }
);