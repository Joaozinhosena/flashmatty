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
        // PERSONALIZAÇÃO DO JOGADOR
        // ====================================================

        function cosmeticosDe(
            jogador
        ) {

            if (
                jogador
                &&
                jogador.cosmeticos
                &&
                typeof jogador.cosmeticos
                ===
                "object"
            ) {

                return jogador.cosmeticos;

            }

            return {};

        }


        function idCosmetico(
            cosmeticos,
            tipo
        ) {

            return (
                cosmeticos?.[tipo]?.id
                ||
                ""
            );

        }


        function classesFundo(
            itemId
        ) {

            const mapa = {

                fundo_ceu_noturno:
                    "bg-gradient-to-br from-slate-950 via-blue-950 to-indigo-950",

                fundo_sunset:
                    "bg-gradient-to-br from-orange-950 via-rose-900 to-indigo-950",

                fundo_neon:
                    "bg-gradient-to-br from-cyan-950 via-violet-950 to-fuchsia-950",

                fundo_galaxia:
                    "bg-gradient-to-br from-slate-950 via-indigo-950 to-purple-950",

                fundo_esmeralda:
                    "bg-gradient-to-br from-emerald-950 via-teal-950 to-slate-950"

            };

            return (
                mapa[itemId]
                ||
                "bg-gradient-to-br from-slate-900 to-slate-800"
            );

        }


        function classesCard(
            itemId
        ) {

            const mapa = {

                card_vidro:
                    "bg-slate-900/70 backdrop-blur-xl border-slate-500/30",

                card_neon:
                    "bg-slate-950 border-violet-500 shadow-[0_0_28px_rgba(139,92,246,0.30)]",

                card_ouro:
                    "bg-gradient-to-br from-amber-950 to-slate-950 border-yellow-400 shadow-[0_0_28px_rgba(245,158,11,0.28)]",

                card_galactico:
                    "bg-gradient-to-br from-indigo-950 via-purple-950 to-slate-950 border-purple-400 shadow-[0_0_32px_rgba(168,85,247,0.30)]"

            };

            return (
                mapa[itemId]
                ||
                "bg-slate-900 border-slate-700"
            );

        }


        function classesMoldura(
            itemId
        ) {

            const mapa = {

                moldura_indigo:
                    "ring-4 ring-indigo-400 shadow-[0_0_22px_rgba(99,102,241,0.60)]",

                moldura_fogo:
                    "ring-4 ring-orange-400 shadow-[0_0_24px_rgba(239,68,68,0.66)]",

                moldura_gelo:
                    "ring-4 ring-cyan-300 shadow-[0_0_24px_rgba(14,165,233,0.64)]",

                moldura_ouro:
                    "ring-4 ring-yellow-400 shadow-[0_0_26px_rgba(245,158,11,0.72)]",

                moldura_arco_iris:
                    "ring-4 ring-fuchsia-400 shadow-[0_0_28px_rgba(34,211,238,0.58)]"

            };

            return (
                mapa[itemId]
                ||
                "ring-2 ring-slate-500"
            );

        }


        function classesNome(
            itemId
        ) {

            const mapa = {

                nome_ciano:
                    "text-cyan-300 drop-shadow-[0_0_8px_rgba(34,211,238,0.48)]",

                nome_dourado:
                    "text-yellow-300 drop-shadow-[0_0_8px_rgba(250,204,21,0.48)]",

                nome_gradiente:
                    "bg-gradient-to-r from-cyan-400 via-violet-400 to-pink-400 bg-clip-text text-transparent",

                nome_esmeralda:
                    "text-emerald-300 drop-shadow-[0_0_8px_rgba(16,185,129,0.45)]",

                nome_lendario:
                    "bg-gradient-to-r from-yellow-200 via-orange-400 to-fuchsia-400 bg-clip-text text-transparent"

            };

            return (
                mapa[itemId]
                ||
                "text-white"
            );

        }


        function criarAvatar(
            jogador,
            cosmeticos
        ) {

            const wrapper =
                document.createElement(
                    "div"
                );


            wrapper.className = `
                relative
                mx-auto
                w-20
                h-20
                rounded-full
                ${classesMoldura(
                    idCosmetico(
                        cosmeticos,
                        "moldura"
                    )
                )}
            `;


            const usuarioId =
                Number(
                    jogador.usuario_id
                );


            if (
                Number.isFinite(
                    usuarioId
                )
                &&
                usuarioId > 0
            ) {

                const imagem =
                    document.createElement(
                        "img"
                    );


                imagem.src =
                    `/social/foto/${usuarioId}`;

                imagem.alt =
                    `Foto de ${
                        jogador.nome
                        ||
                        "Jogador"
                    }`;

                imagem.className = `
                    w-full
                    h-full
                    rounded-full
                    object-cover
                    bg-slate-800
                `;


                wrapper.appendChild(
                    imagem
                );

            } else {

                const fallback =
                    document.createElement(
                        "div"
                    );


                fallback.className = `
                    w-full
                    h-full
                    rounded-full
                    bg-slate-800
                    flex
                    items-center
                    justify-center
                    text-3xl
                `;

                fallback.textContent =
                    "";


                wrapper.appendChild(
                    fallback
                );

            }


            const badge =
                cosmeticos?.badge;


            if (
                badge?.valor?.simbolo
            ) {

                const selo =
                    document.createElement(
                        "span"
                    );


                selo.className = `
                    absolute
                    -right-2
                    bottom-0
                    min-w-9
                    h-9
                    px-1
                    rounded-full
                    flex
                    items-center
                    justify-center
                    bg-slate-950
                    border-2
                    border-white/20
                    text-lg
                    shadow-lg
                `;


                selo.textContent =
                    badge.valor.simbolo;


                wrapper.appendChild(
                    selo
                );

            }


            return wrapper;

        }


        function adicionarEfeito(
            card,
            efeitoId
        ) {

            if (!efeitoId) {
                return;
            }


            const efeito =
                document.createElement(
                    "div"
                );


            efeito.className = `
                absolute
                inset-0
                pointer-events-none
                overflow-hidden
                rounded-2xl
            `;


            if (
                efeitoId
                ===
                "efeito_estrelas"
            ) {

                efeito.innerHTML = `
                    <span class="absolute top-4 left-[15%] w-2 h-2 rounded-full bg-white/80 animate-pulse"></span>
                    <span class="absolute top-10 right-[18%] w-2 h-2 rounded-full bg-cyan-200/80 animate-ping"></span>
                    <span class="absolute bottom-6 left-[38%] w-1.5 h-1.5 rounded-full bg-violet-200/80 animate-pulse"></span>
                `;

            }

            else if (
                efeitoId
                ===
                "efeito_grade"
            ) {

                efeito.innerHTML = `
                    <span class="absolute inset-3 rounded-xl border border-cyan-400/20 bg-cyan-400/5 animate-pulse"></span>
                `;

            }

            else if (
                efeitoId
                ===
                "efeito_aurora"
            ) {

                efeito.innerHTML = `
                    <span class="absolute -top-10 -left-10 w-32 h-32 rounded-full bg-cyan-500/20 blur-2xl animate-pulse"></span>
                    <span class="absolute -bottom-10 -right-10 w-36 h-36 rounded-full bg-fuchsia-500/20 blur-2xl animate-pulse"></span>
                `;

            }

            else if (
                efeitoId
                ===
                "efeito_scan"
            ) {

                efeito.innerHTML = `
                    <span class="absolute inset-x-5 top-1/2 h-px bg-cyan-300 shadow-[0_0_18px_rgba(103,232,249,0.85)] animate-pulse"></span>
                `;

            }


            card.appendChild(
                efeito
            );

        }


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


                        const cosmeticos =
                            cosmeticosDe(
                                jogador
                            );


                        const fundoId =
                            idCosmetico(
                                cosmeticos,
                                "fundo"
                            );


                        const cardId =
                            idCosmetico(
                                cosmeticos,
                                "card"
                            );


                        const nomeId =
                            idCosmetico(
                                cosmeticos,
                                "nome"
                            );


                        const efeitoId =
                            idCosmetico(
                                cosmeticos,
                                "efeito"
                            );


                        elemento.className = `
                            relative
                            overflow-hidden
                            border
                            rounded-2xl
                            p-4
                            text-center
                            transition
                            duration-200
                            hover:-translate-y-1
                            hover:shadow-xl
                            ${classesCard(
                                cardId
                            )}
                        `;


                        adicionarEfeito(
                            elemento,
                            efeitoId
                        );


                        const conteudo =
                            document.createElement(
                                "div"
                            );


                        conteudo.className = `
                            relative
                            z-10
                        `;


                        const faixa =
                            document.createElement(
                                "div"
                            );


                        faixa.className = `
                            -mx-4
                            -mt-4
                            mb-4
                            h-16
                            ${classesFundo(
                                fundoId
                            )}
                            opacity-90
                        `;


                        conteudo.appendChild(
                            faixa
                        );


                        const avatar =
                            criarAvatar(
                                jogador,
                                cosmeticos
                            );


                        avatar.classList.add(
                            "-mt-12"
                        );


                        conteudo.appendChild(
                            avatar
                        );


                        const status =
                            document.createElement(
                                "div"
                            );


                        status.className = `
                            mt-3
                            text-xs
                            font-black
                            ${
                                jogador.online
                                    ?
                                    "text-emerald-400"
                                    :
                                    "text-slate-500"
                            }
                        `;


                        status.textContent =
                            jogador.online
                                ?
                                "● Online"
                                :
                                "● Desconectado";


                        conteudo.appendChild(
                            status
                        );


                        const nome =
                            document.createElement(
                                "div"
                            );


                        nome.className = `
                            mt-1
                            text-lg
                            font-black
                            truncate
                            ${classesNome(
                                nomeId
                            )}
                        `;


                        nome.textContent =
                            jogador.nome
                            ||
                            "Jogador";


                        conteudo.appendChild(
                            nome
                        );


                        const titulo =
                            cosmeticos?.titulo;


                        if (
                            titulo?.valor?.texto
                        ) {

                            const tituloElemento =
                                document.createElement(
                                    "div"
                                );


                            tituloElemento.className = `
                                inline-flex
                                items-center
                                gap-1
                                mt-2
                                px-3
                                py-1
                                rounded-full
                                border
                                border-white/10
                                bg-slate-950/60
                                text-slate-200
                                text-xs
                                font-black
                            `;


                            tituloElemento.textContent =
                                `${
                                    titulo.icone
                                    ||
                                    "✨"
                                } ${
                                    titulo.valor.texto
                                }`;


                            conteudo.appendChild(
                                tituloElemento
                            );

                        }


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
                                ml-1
                                px-3
                                py-1
                                rounded-full
                                bg-amber-400/10
                                border
                                border-amber-300/20
                                text-amber-300
                                text-xs
                                font-black
                            `;


                            etiquetaHost.textContent =
                                " Anfitrião";


                            conteudo.appendChild(
                                etiquetaHost
                            );

                        }


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
                                z-20
                                bg-indigo-500
                                text-white
                                rounded-full
                                px-2
                                py-1
                                text-[10px]
                                font-black
                                shadow-lg
                            `;


                            voce.textContent =
                                "VOCÊ";


                            elemento.appendChild(
                                voce
                            );

                        }


                        elemento.appendChild(
                            conteudo
                        );


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
                        " Iniciando partida...";


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
                        " Iniciar partida";

                }

            }
        );

    }
);