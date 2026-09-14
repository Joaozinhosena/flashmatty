document.addEventListener(
    "DOMContentLoaded",
    () => {

        const jogo =
            document.getElementById(
                "multiplayerGame"
            );

        if (!jogo) {
            return;
        }


        const codigo =
            jogo.dataset.codigo;

        const jogadorId =
            jogo.dataset.jogador;

        const host =
            jogo.dataset.host ===
            "true";


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


        const socket =
            io();


        let timer = null;

        let respondeu = false;

        let rodadaEncerrada = false;


        socket.on(
            "connect",
            () => {

                socket.emit(
                    "entrar_socket",
                    {
                        codigo:
                            codigo,

                        jogador_id:
                            jogadorId
                    }
                );


                if (host) {

                    setTimeout(
                        () => {

                            socket.emit(
                                "proxima_questao",
                                {
                                    codigo:
                                        codigo
                                }
                            );

                        },
                        800
                    );
                }
            }
        );


        socket.on(
            "nova_questao",
            dados => {

                respondeu = false;

                rodadaEncerrada = false;

                rodada.textContent =
                    dados.rodada;

                total.textContent =
                    dados.total;


                area.innerHTML = `
                    <h1
                        class="
                        text-2xl
                        md:text-4xl
                        font-black
                        text-center
                        "
                    >
                        ${dados.pergunta}
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
                    ></div>
                `;


                const container =
                    document.getElementById(
                        "alternativas"
                    );


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

                        botao.className =
                            `
                            min-h-28
                            border-2
                            rounded-3xl
                            p-5
                            text-2xl
                            font-black
                            bg-white
                            hover:border-indigo-500
                            `;


                        const simbolos = [
                            "▲",
                            "◆",
                            "●",
                            "■"
                        ];


                        botao.textContent =
                            `${simbolos[indice]} ${alternativa}`;


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


                                botao.classList.add(
                                    "border-indigo-600",
                                    "bg-indigo-50"
                                );


                                socket.emit(
                                    "responder",
                                    {
                                        codigo:
                                            codigo,

                                        resposta:
                                            alternativa
                                    }
                                );
                            }
                        );


                        container.appendChild(
                            botao
                        );
                    }
                );


                iniciarTimer(
                    dados.tempo
                );
            }
        );


        socket.on(
            "resposta_recebida",
            dados => {

                if (dados.correto) {

                    area.insertAdjacentHTML(
                        "beforeend",
                        `
                        <div
                            class="
                            mt-6
                            text-center
                            bg-green-100
                            text-green-700
                            rounded-2xl
                            p-4
                            font-black
                            text-xl
                            "
                        >
                            ✓ Correto!
                            +${dados.pontos}
                            pontos
                        </div>
                        `
                    );

                } else {

                    area.insertAdjacentHTML(
                        "beforeend",
                        `
                        <div
                            class="
                            mt-6
                            text-center
                            bg-red-100
                            text-red-600
                            rounded-2xl
                            p-4
                            font-black
                            text-xl
                            "
                        >
                            ✕ Resposta incorreta
                        </div>
                        `
                    );
                }
            }
        );


        socket.on(
            "rodada_finalizada",
            dados => {

                rodadaEncerrada =
                    true;

                clearInterval(
                    timer
                );


                let rankingHtml = "";


                dados.ranking
                    .slice(
                        0,
                        5
                    )
                    .forEach(
                        jogador => {

                            rankingHtml += `
                                <div
                                    class="
                                    flex
                                    justify-between
                                    gap-4
                                    bg-slate-100
                                    rounded-xl
                                    p-3
                                    "
                                >
                                    <span class="font-bold">
                                        ${jogador.posicao}º
                                        ${jogador.nome}
                                    </span>

                                    <strong>
                                        ${jogador.pontos}
                                    </strong>
                                </div>
                            `;
                        }
                    );


                area.innerHTML = `
                    <div class="text-center">

                        <div class="text-5xl">
                            🏆
                        </div>

                        <h2
                            class="
                            text-3xl
                            font-black
                            mt-3
                            "
                        >
                            Ranking
                        </h2>

                        <p class="text-slate-500 mt-2">
                            Resposta:
                            <strong>
                                ${dados.correta}
                            </strong>
                        </p>

                    </div>

                    <div class="space-y-2 mt-7">
                        ${rankingHtml}
                    </div>
                `;


                if (host) {

                    const proximo =
                        document.createElement(
                            "button"
                        );

                    proximo.type =
                        "button";

                    proximo.className =
                        `
                        w-full
                        bg-indigo-600
                        text-white
                        rounded-2xl
                        p-4
                        font-black
                        mt-7
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
                                dados.terminou
                            ) {

                                window.location.href =
                                    `/multiplayer/resultado/${codigo}`;

                                return;
                            }


                            socket.emit(
                                "proxima_questao",
                                {
                                    codigo:
                                        codigo
                                }
                            );
                        }
                    );


                    area.appendChild(
                        proximo
                    );

                } else {

                    area.insertAdjacentHTML(
                        "beforeend",
                        `
                        <p
                            class="
                            text-center
                            text-slate-500
                            font-bold
                            mt-7
                            "
                        >
                            Aguardando o anfitrião...
                        </p>
                        `
                    );


                    if (
                        dados.terminou
                    ) {

                        setTimeout(
                            () => {

                                window.location.href =
                                    `/multiplayer/resultado/${codigo}`;

                            },
                            3500
                        );
                    }
                }
            }
        );


        socket.on(
            "partida_finalizada",
            () => {

                window.location.href =
                    `/multiplayer/resultado/${codigo}`;
            }
        );


        function iniciarTimer(
            segundos
        ) {

            clearInterval(
                timer
            );


            let restante =
                segundos;


            cronometro.textContent =
                `⏱️ ${restante}`;


            barra.style.width =
                "100%";


            timer = setInterval(
                () => {

                    restante -= 1;


                    cronometro.textContent =
                        `⏱️ ${Math.max(0, restante)}`;


                    const porcentagem =
                        Math.max(
                            0,
                            restante /
                            segundos *
                            100
                        );


                    barra.style.width =
                        `${porcentagem}%`;


                    if (
                        restante <= 0
                    ) {

                        clearInterval(
                            timer
                        );


                        if (
                            host
                            &&
                            !rodadaEncerrada
                        ) {

                            socket.emit(
                                "tempo_esgotado",
                                {
                                    codigo:
                                        codigo
                                }
                            );
                        }
                    }

                },
                1000
            );
        }
    }
);