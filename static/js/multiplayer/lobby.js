document.addEventListener(
    "DOMContentLoaded",
    () => {

        const lobby =
            document.getElementById(
                "lobby"
            );

        if (!lobby) {
            return;
        }


        const codigo =
            lobby.dataset.codigo;

        const jogadorId =
            lobby.dataset.jogador;

        const host =
            lobby.dataset.host ===
            "true";


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


        const socket =
            io();


        socket.on(
            "connect",
            () => {

                socket.emit(
                    "entrar_socket",
                    {
                        codigo: codigo,
                        jogador_id:
                            jogadorId
                    }
                );
            }
        );


        socket.on(
            "jogadores_atualizados",
            dados => {

                lista.innerHTML = "";

                quantidade.textContent =
                    dados.jogadores.length;


                dados.jogadores.forEach(
                    jogador => {

                        const elemento =
                            document.createElement(
                                "div"
                            );

                        elemento.className =
                            `
                            bg-slate-100
                            rounded-2xl
                            p-4
                            text-center
                            font-black
                            `;


                        elemento.innerHTML =
                            `
                            <div class="text-3xl">
                                ${
                                    jogador.online
                                    ? "🟢"
                                    : "⚫"
                                }
                            </div>

                            <div class="mt-2">
                                ${
                                    jogador.nome
                                }
                            </div>
                            `;


                        lista.appendChild(
                            elemento
                        );
                    }
                );
            }
        );


        if (
            host &&
            iniciar
        ) {

            iniciar.addEventListener(
                "click",
                () => {

                    iniciar.disabled =
                        true;

                    iniciar.textContent =
                        "Iniciando...";


                    socket.emit(
                        "iniciar_partida",
                        {
                            codigo:
                                codigo
                        }
                    );
                }
            );
        }


        socket.on(
            "partida_iniciada",
            () => {

                window.location.href =
                    `/multiplayer/jogo/${codigo}`;
            }
        );


        socket.on(
            "erro_sala",
            dados => {

                alert(
                    dados.mensagem
                );
            }
        );
    }
);