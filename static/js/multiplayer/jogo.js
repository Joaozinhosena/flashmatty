document.addEventListener(
    "DOMContentLoaded",
    () => {

        // ====================================================
        // ELEMENTO PRINCIPAL
        // ====================================================

        const jogo =
            document.getElementById(
                "multiplayerGame"
            );

        if (!jogo) {
            return;
        }


        // ====================================================
        // DADOS DA PARTIDA
        // ====================================================

        const codigo =
            jogo.dataset.codigo || "";

        const jogadorId =
            jogo.dataset.jogador || "";

        const host =
            jogo.dataset.host === "true";


        // ====================================================
        // ELEMENTOS
        // ====================================================

        const area =
            document.getElementById(
                "areaPergunta"
            );

        const rodada =
            document.getElementById(
                "rodada"
            );

        const total =
            document.getElementById(
                "total"
            );

        const cronometro =
            document.getElementById(
                "cronometro"
            );

        const barra =
            document.getElementById(
                "tempoBarra"
            );


        // ====================================================
        // SOCKET.IO
        // ====================================================

        const socket = io();


        // ====================================================
        // ESTADO LOCAL
        // ====================================================

        let timer = null;

        let respondeu = false;

        let rodadaEncerrada = false;

        let redirecionando =
            false;


        // ====================================================
        // SEGURANÇA
        // ====================================================

        function escaparHtml(valor) {

            const elemento =
                document.createElement(
                    "div"
                );

            elemento.textContent =
                valor ?? "";

            return elemento.innerHTML;
        }


        // ====================================================
        // CONECTOU
        // ====================================================

        socket.on(
            "connect",
            () => {

                console.log(
                    "Conectado ao multiplayer:",
                    socket.id
                );


                // Entra novamente na room Socket.IO.
                socket.emit(
                    "entrar_socket",
                    {
                        codigo: codigo,
                        jogador_id: jogadorId
                    }
                );


                /*
                Somente o host solicita a primeira
                questão.

                O servidor impede duplicação caso
                já exista uma questão ativa.
                */

                if (host) {

                    setTimeout(
                        () => {

                            if (
                                socket.connected
                                &&
                                !rodadaEncerrada
                            ) {

                                socket.emit(
                                    "proxima_questao",
                                    {
                                        codigo:
                                            codigo,

                                        jogador_id:
                                            jogadorId
                                    }
                                );

                            }

                        },
                        1500
                    );

                }

            }
        );


        // ====================================================
        // ERRO DE CONEXÃO
        // ====================================================

        socket.on(
            "connect_error",
            erro => {

                console.error(
                    "Erro Socket.IO:",
                    erro
                );

            }
        );


        // ====================================================
        // NOVA QUESTÃO
        // ====================================================

        socket.on(
            "nova_questao",
            dados => {

                if (!dados) {
                    return;
                }


                respondeu =
                    false;

                rodadaEncerrada =
                    false;


                rodada.textContent =
                    dados.rodada ?? "-";

                total.textContent =
                    dados.total ?? "-";


                // ============================================
                // DADOS DO MODO ESPECIAL
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
                    dados.efeito || "";

                const multiplicador =
                    Number(
                        dados.multiplicador ||
                        1
                    );


                let avisoModo = "";


                // Não precisa ocupar muito espaço
                // no modo clássico.
                if (
                    modo !== "classico"
                    ||
                    efeito
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
                                        mt-2
                                        px-3
                                        py-1
                                        rounded-full
                                        bg-indigo-600
                                        text-white
                                        text-xs
                                        font-black
                                    "
                                >
                                    ${multiplicador}x PONTOS
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
                            dados.pergunta
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

                `;


                const container =
                    document.getElementById(
                        "alternativas"
                    );


                if (
                    !container
                    ||
                    !Array.isArray(
                        dados.alternativas
                    )
                ) {
                    return;
                }


                // ============================================
                // ALTERNATIVAS
                // ============================================

                const simbolos = [
                    "▲",
                    "◆",
                    "●",
                    "■"
                ];


                dados.alternativas.forEach(
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
                            disabled:cursor-not-allowed
                            disabled:opacity-70
                        `;


                        botao.textContent =
                            `${simbolos[indice] || "●"} ${alternativa}`;


                        botao.addEventListener(
                            "click",
                            () => {

                                if (
                                    respondeu
                                    ||
                                    rodadaEncerrada
                                ) {
                                    return;
                                }


                                respondeu =
                                    true;


                                // Desativa todas.
                                const botoes =
                                    container
                                    .querySelectorAll(
                                        "button"
                                    );


                                botoes.forEach(
                                    b => {

                                        b.disabled =
                                            true;

                                    }
                                );


                                // Marca a selecionada.
                                botao.classList.add(
                                    "border-indigo-600",
                                    "bg-indigo-50"
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
                    Number(
                        dados.tempo || 20
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

                if (!dados) {
                    return;
                }


                // Evita mensagens duplicadas.
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

                if (dados.correto) {

                    feedback.className = `
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
                        Number(
                            dados.pontos || 0
                        );


                    const totalPontos =
                        Number(
                            dados.total_pontos || 0
                        );


                    const sequencia =
                        Number(
                            dados.sequencia || 0
                        );


                    feedback.innerHTML = `

                        <div
                            class="
                                text-xl
                                md:text-2xl
                            "
                        >
                            ✓ Correto!
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

                    feedback.className = `
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
                        Number(
                            dados.pontos || 0
                        );


                    let penalidade = "";


                    // Dobro ou Nada pode retornar
                    // pontuação negativa.
                    if (pontos < 0) {

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
                        <div class="text-xl">
                            ✕ Resposta incorreta
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

                if (!dados) {
                    return;
                }


                rodadaEncerrada =
                    true;


                respondeu =
                    true;


                pararTimer();


                cronometro.textContent =
                    "⏱️ 0";


                barra.style.width =
                    "0%";


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

                            let medalha =
                                `${jogador.posicao}º`;


                            if (
                                Number(
                                    jogador.posicao
                                )
                                ===
                                1
                            ) {

                                medalha =
                                    "🥇";

                            }

                            else if (
                                Number(
                                    jogador.posicao
                                )
                                ===
                                2
                            ) {

                                medalha =
                                    "🥈";

                            }

                            else if (
                                Number(
                                    jogador.posicao
                                )
                                ===
                                3
                            ) {

                                medalha =
                                    "🥉";

                            }


                            rankingHtml += `

                                <div
                                    class="
                                        flex
                                        items-center
                                        justify-between
                                        gap-4
                                        bg-slate-100
                                        border
                                        border-slate-200
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
                                        </span>

                                    </div>


                                    <strong
                                        class="
                                            text-indigo-600
                                            shrink-0
                                        "
                                    >
                                        ${
                                            Number(
                                                jogador.pontos
                                            )
                                            ||
                                            0
                                        }
                                    </strong>

                                </div>

                            `;

                        }
                    );


                // ============================================
                // MOTIVO DO FIM
                // ============================================

                let mensagemFim =
                    "";


                if (
                    dados.motivo === "tempo"
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
                                    dados.correta
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

                `;


                // ============================================
                // HOST
                // ============================================

                if (host) {

                    const proximo =
                        document.createElement(
                            "button"
                        );


                    proximo.type =
                        "button";


                    proximo.className = `
                        w-full
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

                            proximo.disabled =
                                true;


                            if (
                                dados.terminou
                            ) {

                                irResultado();

                                return;
                            }


                            proximo.textContent =
                                "Carregando...";


                            socket.emit(
                                "proxima_questao",
                                {
                                    codigo:
                                        codigo,

                                    jogador_id:
                                        jogadorId
                                }
                            );

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
                            "Preparando o pódio..."
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
                            1500
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
            () => {

                /*
                Pequeno atraso para o jogador enxergar
                a finalização antes do pódio.
                */

                setTimeout(
                    irResultado,
                    900
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
                    mensagem
                );


                alert(
                    mensagem
                );

            }
        );


        // ====================================================
        // IR PARA RESULTADO
        // ====================================================

        function irResultado() {

            if (redirecionando) {
                return;
            }


            redirecionando =
                true;


            pararTimer();


            window.location.href =
                `/multiplayer/resultado/${
                    encodeURIComponent(
                        codigo
                    )
                }`;

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
        // PARAR TIMER
        // ====================================================

        function pararTimer() {

            if (timer) {

                clearInterval(
                    timer
                );

                timer =
                    null;

            }

        }


        // ====================================================
        // CRONÔMETRO
        // ====================================================

        function iniciarTimer(
            segundos
        ) {

            pararTimer();


            segundos =
                Number(
                    segundos
                );


            if (
                !Number.isFinite(
                    segundos
                )
                ||
                segundos <= 0
            ) {

                segundos =
                    20;

            }


            const inicio =
                Date.now();


            const fim =
                inicio
                +
                (
                    segundos
                    *
                    1000
                );


            cronometro.textContent =
                `⏱️ ${segundos}`;


            barra.style.width =
                "100%";


            function atualizar() {

                const agora =
                    Date.now();


                const milissegundosRestantes =
                    Math.max(
                        0,
                        fim - agora
                    );


                const restante =
                    Math.ceil(
                        milissegundosRestantes
                        /
                        1000
                    );


                const porcentagem =
                    Math.max(
                        0,
                        Math.min(
                            100,
                            (
                                milissegundosRestantes
                                /
                                (
                                    segundos
                                    *
                                    1000
                                )
                            )
                            *
                            100
                        )
                    );


                cronometro.textContent =
                    `⏱️ ${restante}`;


                barra.style.width =
                    `${porcentagem}%`;


                // --------------------------------------------
                // AVISOS VISUAIS
                // --------------------------------------------

                if (
                    porcentagem <= 25
                ) {

                    cronometro.classList.add(
                        "text-red-600"
                    );

                }

                else {

                    cronometro.classList.remove(
                        "text-red-600"
                    );

                }


                // --------------------------------------------
                // ACABOU
                // --------------------------------------------

                if (
                    milissegundosRestantes
                    <=
                    0
                ) {

                    pararTimer();


                    rodadaEncerrada =
                        true;


                    desabilitarAlternativas();


                    /*
                    O servidor possui seu próprio
                    temporizador.

                    O evento abaixo serve como
                    confirmação adicional quando
                    este navegador é o host.
                    */

                    if (host) {

                        socket.emit(
                            "tempo_esgotado",
                            {
                                codigo:
                                    codigo,

                                jogador_id:
                                    jogadorId
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

    }
);