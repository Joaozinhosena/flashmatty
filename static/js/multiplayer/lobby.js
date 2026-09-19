document.addEventListener(
    "DOMContentLoaded",
    () => {

        // ====================================================
        // ELEMENTO PRINCIPAL
        // ====================================================

        const lobby =
            document.getElementById(
                "lobby"
            );


        if (!lobby) {
            return;
        }


        // ====================================================
        // DADOS DA SALA
        // ====================================================

        const codigo =
            lobby.dataset.codigo || "";


        const jogadorId =
            lobby.dataset.jogador || "";


        const host =
            lobby.dataset.host === "true";


        // ====================================================
        // ELEMENTOS DA TELA
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
        // SOCKET.IO
        // ====================================================

        const socket = io();


        // ====================================================
        // CONECTOU
        // ====================================================

        socket.on(
            "connect",
            () => {

                console.log(
                    "Socket conectado:",
                    socket.id
                );


                socket.emit(
                    "entrar_socket",
                    {
                        codigo: codigo,
                        jogador_id: jogadorId
                    }
                );

            }
        );


        // ====================================================
        // DESCONEXÃO
        // ====================================================

        socket.on(
            "disconnect",
            motivo => {

                console.log(
                    "Socket desconectado:",
                    motivo
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
                    "Erro ao conectar Socket.IO:",
                    erro
                );

            }
        );


        // ====================================================
        // JOGADORES ATUALIZADOS
        // ====================================================

        socket.on(
            "jogadores_atualizados",
            dados => {

                if (
                    !dados ||
                    !Array.isArray(
                        dados.jogadores
                    )
                ) {
                    return;
                }


                const jogadores =
                    dados.jogadores;


                // --------------------------------------------
                // LIMPA LISTA
                // --------------------------------------------

                if (lista) {
                    lista.innerHTML = "";
                }


                // --------------------------------------------
                // QUANTIDADE
                // --------------------------------------------

                const online =
                    jogadores.filter(
                        jogador =>
                            jogador.online
                    );


                if (quantidade) {

                    quantidade.textContent =
                        online.length;

                }


                // --------------------------------------------
                // MENSAGEM DE LISTA VAZIA
                // --------------------------------------------

                if (
                    mensagemListaVazia
                ) {

                    mensagemListaVazia.style.display =
                        jogadores.length > 0
                            ? "none"
                            : "block";

                }


                // --------------------------------------------
                // MONTA JOGADORES
                // --------------------------------------------

                jogadores.forEach(
                    jogador => {

                        if (!lista) {
                            return;
                        }


                        const elemento =
                            document.createElement(
                                "div"
                            );


                        elemento.className = `
                            relative
                            bg-slate-100
                            border
                            border-slate-200
                            rounded-2xl
                            p-4
                            text-center
                            transition
                            duration-200
                            hover:shadow-md
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
                                ? "🟢"
                                : "⚫";


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


                        /*
                        Usamos textContent em vez de
                        innerHTML para impedir que um
                        apelido seja interpretado como HTML.
                        */

                        nome.textContent =
                            jogador.nome ||
                            "Jogador";


                        elemento.appendChild(
                            nome
                        );


                        // ====================================
                        // HOST
                        // ====================================

                        if (jogador.host) {

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

                        if (!jogador.online) {

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
                            String(jogador.id)
                            ===
                            String(jogadorId)
                        ) {

                            const voce =
                                document.createElement(
                                    "div"
                                );


                            voce.className = `
                                absolute
                                top-2
                                right-2
                                bg-indigo-100
                                text-indigo-700
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


                // --------------------------------------------
                // BOTÃO DO HOST
                // --------------------------------------------

                if (
                    host &&
                    iniciar &&
                    !iniciar.dataset.iniciando
                ) {

                    iniciar.disabled = false;

                }

            }
        );


        // ====================================================
        // INICIAR PARTIDA
        // ====================================================

        if (
            host &&
            iniciar
        ) {

            iniciar.addEventListener(
                "click",
                () => {

                    // Impede clique duplo.
                    if (
                        iniciar.dataset.iniciando
                        ===
                        "true"
                    ) {
                        return;
                    }


                    iniciar.dataset.iniciando =
                        "true";


                    iniciar.disabled =
                        true;


                    iniciar.textContent =
                        "⏳ Iniciando partida...";


                    socket.emit(
                        "iniciar_partida",
                        {
                            codigo: codigo,
                            jogador_id: jogadorId
                        }
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

                const codigoPartida =
                    dados?.codigo ||
                    codigo;


                window.location.href =
                    `/multiplayer/jogo/${encodeURIComponent(
                        codigoPartida
                    )}`;

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


                alert(
                    mensagem
                );


                // Se o host tentou iniciar
                // e ocorreu erro, libera novamente.
                if (
                    host &&
                    iniciar
                ) {

                    iniciar.dataset.iniciando =
                        "false";


                    iniciar.disabled =
                        false;


                    iniciar.textContent =
                        "▶ Iniciar partida";

                }

            }
        );

    }
);