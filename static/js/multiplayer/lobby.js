document.addEventListener(
    "DOMContentLoaded",
    () => {

        "use strict";


        // ====================================================
        // ELEMENTO PRINCIPAL
        // ====================================================

        const lobby =
            document.getElementById(
                "lobby"
            );


        if (!lobby) {

            console.warn(
                "[LOBBY] Elemento #lobby não encontrado."
            );

            return;
        }


        // ====================================================
        // HELPERS
        // ====================================================

        function booleano(valor) {

            return [
                "true",
                "1",
                "sim",
                "yes"
            ].includes(
                String(
                    valor ?? ""
                )
                    .trim()
                    .toLowerCase()
            );
        }


        function tocarSom(nome) {

            try {

                const funcao =
                    window[nome];


                if (
                    typeof funcao ===
                    "function"
                ) {

                    funcao();
                }

            } catch (erro) {

                console.warn(
                    `[LOBBY] Erro ao tocar ${nome}:`,
                    erro
                );
            }
        }


        // ====================================================
        // DADOS DA SALA
        // ====================================================

        const codigo =
            String(
                lobby.dataset.codigo ||
                ""
            )
                .trim();


        const jogadorId =
            String(
                lobby.dataset.jogador ||
                ""
            )
                .trim();


        /*
        Usamos let porque podemos corrigir
        a informação quando o servidor enviar
        jogadores_atualizados.
        */

        let ehHost =
            booleano(
                lobby.dataset.host
            );


        // ====================================================
        // ELEMENTOS
        // ====================================================

        const lista =
            document.getElementById(
                "listaJogadores"
            );


        const quantidade =
            document.getElementById(
                "quantidadeJogadores"
            );


        const iniciar =
            document.getElementById(
                "iniciarPartida"
            );


        const mensagemListaVazia =
            document.getElementById(
                "mensagemListaVazia"
            );


        // ====================================================
        // DEBUG INICIAL
        // ====================================================

        console.log(
            "====================================="
        );

        console.log(
            "🎮 FLASHMATTY - LOBBY"
        );

        console.log(
            "Sala:",
            codigo
        );

        console.log(
            "Jogador:",
            jogadorId
        );

        console.log(
            "Host informado pelo HTML:",
            ehHost
        );

        console.log(
            "====================================="
        );


        // ====================================================
        // VALIDAÇÃO
        // ====================================================

        if (!codigo) {

            console.error(
                "[LOBBY] Código da sala não informado."
            );

            return;
        }


        if (!jogadorId) {

            console.error(
                "[LOBBY] ID do jogador não informado."
            );

            return;
        }


        if (
            typeof window.io !==
            "function"
        ) {

            console.error(
                "[LOBBY] Socket.IO não foi carregado."
            );


            mostrarAviso(
                "Não foi possível conectar ao multiplayer.",
                "erro"
            );

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
        // ESTADO
        // ====================================================

        let redirecionando =
            false;


        let timeoutInicio =
            null;


        let quantidadeOnline =
            0;


        // ====================================================
        // STATUS DE CONEXÃO
        // ====================================================

        function obterStatus() {

            let elemento =
                document.getElementById(
                    "statusLobbySocket"
                );


            if (elemento) {

                return elemento;
            }


            elemento =
                document.createElement(
                    "div"
                );


            elemento.id =
                "statusLobbySocket";


            elemento.className = `
                fixed
                right-4
                bottom-4
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
                elemento
            );


            return elemento;
        }


        function mostrarStatus(
            mensagem,
            tipo = "normal"
        ) {

            const elemento =
                obterStatus();


            elemento.style.display =
                "block";


            elemento.style.opacity =
                "1";


            elemento.textContent =
                mensagem;


            elemento.className = `
                fixed
                right-4
                bottom-4
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

                elemento.classList.add(
                    "bg-green-600",
                    "text-white"
                );

            }

            else if (
                tipo ===
                "erro"
            ) {

                elemento.classList.add(
                    "bg-red-600",
                    "text-white"
                );

            }

            else {

                elemento.classList.add(
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

                        elemento.style.opacity =
                            "0";

                    },
                    1700
                );


                setTimeout(
                    () => {

                        elemento.style.display =
                            "none";

                    },
                    2100
                );
            }
        }


        // ====================================================
        // AVISO NA TELA
        // ====================================================

        function mostrarAviso(
            mensagem,
            tipo = "erro"
        ) {

            const anterior =
                document.getElementById(
                    "avisoLobby"
                );


            if (anterior) {

                anterior.remove();
            }


            const aviso =
                document.createElement(
                    "div"
                );


            aviso.id =
                "avisoLobby";


            aviso.className = `
                max-w-xl
                mx-auto

                mt-5

                rounded-2xl

                p-4

                text-center
                font-bold
            `;


            if (
                tipo ===
                "sucesso"
            ) {

                aviso.classList.add(
                    "bg-green-100",
                    "border",
                    "border-green-200",
                    "text-green-700"
                );

            } else {

                aviso.classList.add(
                    "bg-red-100",
                    "border",
                    "border-red-200",
                    "text-red-700"
                );
            }


            aviso.textContent =
                mensagem;


            lobby.appendChild(
                aviso
            );
        }


        // ====================================================
        // ESTADO DO BOTÃO
        // ====================================================

        function definirBotaoInicio(
            estado
        ) {

            if (!iniciar) {

                return;
            }


            if (
                estado ===
                "iniciando"
            ) {

                iniciar.dataset.iniciando =
                    "true";


                iniciar.disabled =
                    true;


                iniciar.textContent =
                    "⏳ Iniciando partida...";


                return;
            }


            iniciar.dataset.iniciando =
                "false";


            if (!ehHost) {

                iniciar.disabled =
                    true;


                return;
            }


            iniciar.disabled =
                false;


            iniciar.textContent =
                "▶ Iniciar partida";
        }


        // ====================================================
        // ENTRAR NA ROOM
        // ====================================================

        function entrarNaSalaSocket() {

            if (
                !socket.connected
            ) {

                return;
            }


            console.log(
                "[LOBBY] Entrando na room:",
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
        // CONEXÃO
        // ====================================================

        socket.on(
            "connect",
            () => {

                console.log(
                    "[LOBBY] Socket conectado:",
                    socket.id
                );


                mostrarStatus(
                    "● Conectado",
                    "online"
                );


                entrarNaSalaSocket();

            }
        );


        // ====================================================
        // DESCONEXÃO
        // ====================================================

        socket.on(
            "disconnect",
            motivo => {

                console.warn(
                    "[LOBBY] Socket desconectado:",
                    motivo
                );


                mostrarStatus(
                    "● Reconectando...",
                    "erro"
                );


                if (
                    iniciar
                    &&
                    iniciar.dataset.iniciando
                    ===
                    "true"
                ) {

                    definirBotaoInicio(
                        "normal"
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
                    "[LOBBY] Erro Socket.IO:",
                    erro
                );


                mostrarStatus(
                    "Falha na conexão",
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
                        "[LOBBY] Tentativa de reconexão:",
                        tentativa
                    );

                }
            );


            socket.io.on(
                "reconnect",
                tentativa => {

                    console.log(
                        "[LOBBY] Reconectado após",
                        tentativa,
                        "tentativas."
                    );

                }
            );
        }


        // ====================================================
        // JOGADORES ATUALIZADOS
        // ====================================================

        socket.on(
            "jogadores_atualizados",
            dados => {

                console.log(
                    "[LOBBY] Jogadores atualizados:",
                    dados
                );


                if (
                    !dados
                    ||
                    !Array.isArray(
                        dados.jogadores
                    )
                ) {

                    console.warn(
                        "[LOBBY] Lista inválida:",
                        dados
                    );

                    return;
                }


                const jogadores =
                    dados.jogadores;


                // ============================================
                // IDENTIFICA O JOGADOR ATUAL
                // ============================================

                const eu =
                    jogadores.find(
                        jogador =>

                            String(
                                jogador.id
                            )
                            ===
                            String(
                                jogadorId
                            )
                    );


                /*
                Se o HTML informou host incorretamente,
                usamos a informação vinda do servidor.
                */

                if (eu) {

                    const hostServidor =
                        Boolean(
                            eu.host
                        );


                    if (
                        hostServidor !==
                        ehHost
                    ) {

                        console.warn(
                            "[LOBBY] Host corrigido pelo servidor:",
                            hostServidor
                        );


                        ehHost =
                            hostServidor;
                    }
                }


                // ============================================
                // QUANTIDADE ONLINE
                // ============================================

                const jogadoresOnline =
                    jogadores.filter(
                        jogador =>
                            Boolean(
                                jogador.online
                            )
                    );


                quantidadeOnline =
                    jogadoresOnline.length;


                if (quantidade) {

                    quantidade.textContent =
                        quantidadeOnline;
                }


                // ============================================
                // LISTA VAZIA
                // ============================================

                if (
                    mensagemListaVazia
                ) {

                    mensagemListaVazia.style.display =
                        jogadores.length
                            ?
                            "none"
                            :
                            "block";
                }


                // ============================================
                // LIMPA LISTA
                // ============================================

                if (lista) {

                    lista.innerHTML =
                        "";
                }


                // ============================================
                // MONTA OS JOGADORES
                // ============================================

                jogadores.forEach(
                    jogador => {

                        if (!lista) {

                            return;
                        }


                        const elemento =
                            document.createElement(
                                "div"
                            );


                        const jogadorAtual =
                            String(
                                jogador.id
                            )
                            ===
                            String(
                                jogadorId
                            );


                        elemento.className = `
                            relative

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

                            text-center

                            transition
                            duration-200

                            hover:shadow-md
                            hover:-translate-y-0.5
                        `;


                        // ====================================
                        // STATUS
                        // ====================================

                        const status =
                            document.createElement(
                                "div"
                            );


                        status.className =
                            "text-3xl";


                        status.textContent =
                            jogador.online
                                ?
                                "🟢"
                                :
                                "⚫";


                        elemento.appendChild(
                            status
                        );


                        // ====================================
                        // NOME
                        // ====================================

                        const nome =
                            document.createElement(
                                "div"
                            );


                        nome.className = `
                            mt-2

                            font-black

                            text-slate-900

                            truncate
                        `;


                        nome.textContent =
                            jogador.nome ||
                            "Jogador";


                        elemento.appendChild(
                            nome
                        );


                        // ====================================
                        // HOST
                        // ====================================

                        if (
                            jogador.host
                        ) {

                            const etiquetaHost =
                                document.createElement(
                                    "div"
                                );


                            etiquetaHost.className = `
                                inline-flex

                                items-center
                                justify-center

                                mt-2

                                px-3
                                py-1

                                rounded-full

                                bg-amber-100
                                text-amber-700

                                text-xs
                                font-black
                            `;


                            etiquetaHost.textContent =
                                "👑 Anfitrião";


                            elemento.appendChild(
                                etiquetaHost
                            );
                        }


                        // ====================================
                        // OFFLINE
                        // ====================================

                        if (
                            !jogador.online
                        ) {

                            const offline =
                                document.createElement(
                                    "div"
                                );


                            offline.className = `
                                mt-2

                                text-xs
                                text-slate-400

                                font-bold
                            `;


                            offline.textContent =
                                "Desconectado";


                            elemento.appendChild(
                                offline
                            );
                        }


                        // ====================================
                        // VOCÊ
                        // ====================================

                        if (
                            jogadorAtual
                        ) {

                            const voce =
                                document.createElement(
                                    "div"
                                );


                            voce.className = `
                                absolute

                                top-2
                                right-2

                                bg-indigo-600
                                text-white

                                rounded-full

                                px-2
                                py-1

                                text-[10px]
                                font-black
                            `;


                            voce.textContent =
                                "VOCÊ";


                            elemento.appendChild(
                                voce
                            );
                        }


                        lista.appendChild(
                            elemento
                        );
                    }
                );


                // ============================================
                // BOTÃO DO HOST
                // ============================================

                if (
                    iniciar
                ) {

                    /*
                    Importante:
                    verificamos !== "true".

                    "false" é uma string e seria
                    considerada verdadeira em:
                    !iniciar.dataset.iniciando
                    */

                    const estaIniciando =
                        iniciar.dataset.iniciando
                        ===
                        "true";


                    if (
                        ehHost
                        &&
                        !estaIniciando
                    ) {

                        iniciar.disabled =
                            false;


                        iniciar.textContent =
                            "▶ Iniciar partida";

                    }

                    else if (
                        !ehHost
                    ) {

                        iniciar.disabled =
                            true;
                    }
                }

            }
        );


        // ====================================================
        // BOTÃO DE INICIAR
        // ====================================================

        if (
            iniciar
        ) {

            iniciar.dataset.iniciando =
                "false";


            iniciar.addEventListener(
                "click",
                () => {

                    // ========================================
                    // NÃO É HOST
                    // ========================================

                    if (
                        !ehHost
                    ) {

                        console.warn(
                            "[LOBBY] Jogador tentou iniciar sem ser host."
                        );


                        mostrarAviso(
                            "Somente o anfitrião pode iniciar a partida."
                        );


                        return;
                    }


                    // ========================================
                    // SOCKET DESCONECTADO
                    // ========================================

                    if (
                        !socket.connected
                    ) {

                        mostrarAviso(
                            "A conexão com o servidor foi perdida. Aguarde a reconexão."
                        );


                        return;
                    }


                    // ========================================
                    // CLIQUE DUPLO
                    // ========================================

                    if (
                        iniciar.dataset.iniciando
                        ===
                        "true"
                    ) {

                        return;
                    }


                    tocarSom(
                        "somClique"
                    );


                    definirBotaoInicio(
                        "iniciando"
                    );


                    console.log(
                        "[LOBBY] Solicitando início da partida:",
                        {
                            codigo:
                                codigo,

                            jogador_id:
                                jogadorId,

                            jogadores_online:
                                quantidadeOnline
                        }
                    );


                    socket.emit(
                        "iniciar_partida",
                        {
                            codigo:
                                codigo,

                            jogador_id:
                                jogadorId
                        }
                    );


                    /*
                    Se o backend não responder com
                    partida_iniciada ou erro_sala,
                    o botão não fica travado para sempre.
                    */

                    clearTimeout(
                        timeoutInicio
                    );


                    timeoutInicio =
                        setTimeout(
                            () => {

                                if (
                                    redirecionando
                                ) {

                                    return;
                                }


                                if (
                                    iniciar.dataset.iniciando
                                    !==
                                    "true"
                                ) {

                                    return;
                                }


                                console.warn(
                                    "[LOBBY] O servidor não respondeu ao iniciar_partida."
                                );


                                definirBotaoInicio(
                                    "normal"
                                );


                                mostrarAviso(
                                    "O servidor não respondeu ao pedido de início. Tente novamente."
                                );

                            },
                            8000
                        );

                }
            );

        }


        // ====================================================
        // PARTIDA INICIADA
        // ====================================================

        socket.on(
            "partida_iniciada",
            dados => {

                console.log(
                    "[LOBBY] Partida iniciada:",
                    dados
                );


                if (
                    redirecionando
                ) {

                    return;
                }


                redirecionando =
                    true;


                clearTimeout(
                    timeoutInicio
                );


                tocarSom(
                    "somConcluido"
                );


                const codigoPartida =
                    String(
                        dados?.codigo ||
                        codigo
                    );


                mostrarStatus(
                    "Partida iniciada! 🎮",
                    "online"
                );


                setTimeout(
                    () => {

                        window.location.href =
                            `/multiplayer/jogo/${
                                encodeURIComponent(
                                    codigoPartida
                                )
                            }`;

                    },
                    250
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
                    "Ocorreu um erro na sala.";


                console.error(
                    "[LOBBY] erro_sala:",
                    mensagem,
                    dados
                );


                clearTimeout(
                    timeoutInicio
                );


                tocarSom(
                    "somErro"
                );


                mostrarAviso(
                    mensagem
                );


                if (
                    iniciar
                ) {

                    definirBotaoInicio(
                        "normal"
                    );
                }

            }
        );


        // ====================================================
        // SAÍDA DA PÁGINA
        // ====================================================

        window.addEventListener(
            "beforeunload",
            () => {

                clearTimeout(
                    timeoutInicio
                );

            }
        );

    }
);