document.addEventListener("DOMContentLoaded", () => {

    // ============================================================
    // ELEMENTOS PRINCIPAIS
    // ============================================================

    const app =
        document.getElementById("exercicio-app");

    const questaoInicialEl =
        document.getElementById("questao-inicial");

    const perguntaEl =
        document.getElementById("pergunta");

    const visualEl =
        document.getElementById("visual");

    const respostaAreaEl =
        document.getElementById("resposta-area");

    const feedbackEl =
        document.getElementById("feedback");

    const botaoResponder =
        document.getElementById("botaoResponder");

    const barraProgresso =
        document.getElementById("barra-progresso");

    const textoProgresso =
        document.getElementById("texto-progresso");

    const xpEl =
        document.getElementById("xp-atual");

    const moedasEl =
        document.getElementById("moedas");


    // ============================================================
    // VERIFICAÇÃO DA PÁGINA
    // ============================================================

    if (
        !app ||
        !questaoInicialEl ||
        !perguntaEl ||
        !visualEl ||
        !respostaAreaEl ||
        !feedbackEl ||
        !botaoResponder
    ) {

        console.error(
            "ERRO: elementos da página de exercício não foram encontrados."
        );

        console.log({
            app,
            questaoInicialEl,
            perguntaEl,
            visualEl,
            respostaAreaEl,
            feedbackEl,
            botaoResponder
        });

        return;
    }


    // ============================================================
    // ESTADO DO EXERCÍCIO
    // ============================================================

    let questaoAtual = null;

    let respostaAtual = null;

    let enviando = false;

    let associacoes = {};

    let associacaoSelecionada = null;

    let ordemSelecionada = [];

    let quantidadeAssociacoes = 0;

    let quantidadeOrdenacao = 0;


    // ============================================================
    // CARREGAR QUESTÃO INICIAL
    // ============================================================

    try {

        questaoAtual =
            JSON.parse(
                questaoInicialEl.textContent
            );

    } catch (erro) {

        console.error(
            "Erro ao carregar questão inicial:",
            erro
        );

        mostrarMensagem(
            "Não foi possível carregar a atividade.",
            "erro"
        );

        return;
    }


    // ============================================================
    // UTILITÁRIOS
    // ============================================================

    function escapar(valor) {

        const elemento =
            document.createElement("div");

        elemento.textContent =
            String(valor ?? "");

        return elemento.innerHTML;
    }


    function esperar(ms) {

        return new Promise(
            resolve =>
                setTimeout(resolve, ms)
        );
    }


    function mostrarMensagem(
        texto,
        tipo = ""
    ) {

        feedbackEl.textContent =
            texto || "";

        feedbackEl.className =
            "mt-5 min-h-10 text-center text-lg font-black";


        if (tipo === "sucesso") {

            feedbackEl.classList.add(
                "text-green-600"
            );

        } else if (tipo === "erro") {

            feedbackEl.classList.add(
                "text-red-500"
            );

        } else if (tipo === "aviso") {

            feedbackEl.classList.add(
                "text-orange-500"
            );

        } else {

            feedbackEl.classList.add(
                "text-slate-500"
            );
        }
    }


    function limparEstadoQuestao() {

        respostaAtual = null;

        associacoes = {};

        associacaoSelecionada = null;

        ordemSelecionada = [];

        quantidadeAssociacoes = 0;

        quantidadeOrdenacao = 0;

        mostrarMensagem("");

        botaoResponder.disabled = false;

        botaoResponder.textContent =
            "Conferir 🚀";
    }


    function selecionarCard(
        elemento
    ) {

        respostaAreaEl
            .querySelectorAll(
                "[data-resposta]"
            )
            .forEach(item => {

                item.classList.remove(
                    "border-indigo-500",
                    "bg-indigo-50",
                    "ring-4",
                    "ring-indigo-100"
                );
            });


        elemento.classList.add(
            "border-indigo-500",
            "bg-indigo-50",
            "ring-4",
            "ring-indigo-100"
        );
    }


    // ============================================================
    // RENDERIZAR VISUAL
    // ============================================================

    function renderizarVisual(
        dados
    ) {

        visualEl.innerHTML = "";


        if (!dados) {

            return;
        }


        // ========================================================
        // GRUPOS
        // ========================================================

        if (
            dados.tipo === "grupos"
        ) {

            visualEl.innerHTML = `

                <div
                    class="
                        flex
                        flex-wrap
                        justify-center
                        gap-5
                    "
                >

                    ${
                        (dados.grupos || [])
                            .map(quantidade => `

                                <div
                                    class="
                                        max-w-64
                                        rounded-2xl
                                        border-2
                                        border-indigo-100
                                        bg-indigo-50
                                        p-4
                                    "
                                >

                                    <div
                                        class="
                                            flex
                                            flex-wrap
                                            justify-center
                                            gap-2
                                        "
                                    >

                                        ${
                                            Array.from(
                                                {
                                                    length:
                                                        Number(
                                                            quantidade
                                                        )
                                                },
                                                () => `
                                                    <span class="text-3xl">
                                                        ${escapar(
                                                            dados.icone || "⭐"
                                                        )}
                                                    </span>
                                                `
                                            ).join("")
                                        }

                                    </div>

                                </div>

                            `)
                            .join("")
                    }

                </div>
            `;

            return;
        }


        // ========================================================
        // SUBTRAÇÃO COM OBJETOS
        // ========================================================

        if (
            dados.tipo ===
            "subtracao_objetos"
        ) {

            let html = "";

            const total =
                Number(
                    dados.total || 0
                );

            const retirados =
                Number(
                    dados.retirados || 0
                );


            for (
                let i = 0;
                i < total;
                i++
            ) {

                const retirado =
                    i < retirados;


                html += `

                    <span
                        class="
                            text-4xl
                            ${
                                retirado
                                    ? "opacity-25 line-through"
                                    : ""
                            }
                        "
                    >
                        ${escapar(
                            dados.icone || "🎈"
                        )}
                    </span>
                `;
            }


            visualEl.innerHTML = `

                <div
                    class="
                        flex
                        flex-wrap
                        justify-center
                        gap-3
                    "
                >
                    ${html}
                </div>
            `;

            return;
        }


        // ========================================================
        // MULTIPLICAÇÃO COM GRUPOS
        // ========================================================

        if (
            dados.tipo ===
            "multiplicacao_grupos"
        ) {

            const grupos =
                Number(
                    dados.grupos || 0
                );

            const itens =
                Number(
                    dados.itens || 0
                );


            visualEl.innerHTML = `

                <div
                    class="
                        flex
                        flex-wrap
                        justify-center
                        gap-4
                    "
                >

                    ${
                        Array.from(
                            { length: grupos },
                            () => `

                                <div
                                    class="
                                        max-w-52
                                        rounded-2xl
                                        border-2
                                        border-indigo-100
                                        bg-white
                                        p-4
                                        shadow-sm
                                    "
                                >

                                    <div
                                        class="
                                            flex
                                            flex-wrap
                                            justify-center
                                            gap-2
                                        "
                                    >

                                        ${
                                            Array.from(
                                                { length: itens },
                                                () => `
                                                    <span class="text-3xl">
                                                        ${escapar(
                                                            dados.icone || "🔵"
                                                        )}
                                                    </span>
                                                `
                                            ).join("")
                                        }

                                    </div>

                                </div>
                            `
                        ).join("")
                    }

                </div>
            `;

            return;
        }


        // ========================================================
        // DIVISÃO
        // ========================================================

        if (
            dados.tipo === "divisao"
        ) {

            const grupos =
                Number(
                    dados.grupos || 1
                );

            const total =
                Number(
                    dados.total || 0
                );

            const porGrupo =
                Math.floor(
                    total / grupos
                );


            visualEl.innerHTML = `

                <div
                    class="
                        flex
                        flex-wrap
                        justify-center
                        gap-4
                    "
                >

                    ${
                        Array.from(
                            { length: grupos },
                            (_, indice) => `

                                <div
                                    class="
                                        min-w-28
                                        rounded-2xl
                                        border-2
                                        border-indigo-200
                                        bg-indigo-50
                                        p-4
                                        text-center
                                    "
                                >

                                    <div
                                        class="
                                            mb-2
                                            text-xs
                                            font-bold
                                            text-indigo-500
                                        "
                                    >
                                        Grupo ${indice + 1}
                                    </div>

                                    <div class="text-2xl">

                                        ${
                                            Array.from(
                                                { length: porGrupo },
                                                () =>
                                                    escapar(
                                                        dados.icone || "🍬"
                                                    )
                                            ).join(" ")
                                        }

                                    </div>

                                </div>
                            `
                        ).join("")
                    }

                </div>
            `;

            return;
        }


        // ========================================================
        // MATERIAL DOURADO
        // ========================================================

        if (
            dados.tipo ===
            "material_dourado"
        ) {

            const dezenas =
                Number(
                    dados.dezenas || 0
                );

            const unidades =
                Number(
                    dados.unidades || 0
                );


            visualEl.innerHTML = `

                <div
                    class="
                        flex
                        flex-wrap
                        items-end
                        justify-center
                        gap-4
                    "
                >

                    ${
                        Array.from(
                            { length: dezenas },
                            () => `

                                <div
                                    class="
                                        grid
                                        grid-cols-2
                                        gap-1
                                        rounded-lg
                                        bg-yellow-400
                                        p-2
                                    "
                                >

                                    ${
                                        Array.from(
                                            { length: 10 },
                                            () => `
                                                <span
                                                    class="
                                                        h-3
                                                        w-3
                                                        rounded-sm
                                                        bg-yellow-100
                                                    "
                                                ></span>
                                            `
                                        ).join("")
                                    }

                                </div>
                            `
                        ).join("")
                    }


                    ${
                        Array.from(
                            { length: unidades },
                            () => `
                                <span
                                    class="
                                        h-8
                                        w-8
                                        rounded-md
                                        bg-yellow-400
                                    "
                                ></span>
                            `
                        ).join("")
                    }

                </div>
            `;

            return;
        }


        // ========================================================
        // FORMA GEOMÉTRICA
        // ========================================================

        if (
            dados.tipo === "forma"
        ) {

            let formaSvg = "";


            switch (
                dados.forma
            ) {

                case "triangulo":

                    formaSvg = `
                        <polygon
                            points="100,20 180,170 20,170"
                            fill="#6366f1"
                        />
                    `;

                    break;


                case "retangulo":

                    formaSvg = `
                        <rect
                            x="20"
                            y="55"
                            width="160"
                            height="100"
                            rx="8"
                            fill="#6366f1"
                        />
                    `;

                    break;


                case "pentagono":

                    formaSvg = `
                        <polygon
                            points="
                                100,15
                                180,75
                                150,175
                                50,175
                                20,75
                            "
                            fill="#6366f1"
                        />
                    `;

                    break;


                case "hexagono":

                    formaSvg = `
                        <polygon
                            points="
                                55,20
                                145,20
                                190,100
                                145,180
                                55,180
                                10,100
                            "
                            fill="#6366f1"
                        />
                    `;

                    break;


                case "circulo":

                    formaSvg = `
                        <circle
                            cx="100"
                            cy="100"
                            r="75"
                            fill="#6366f1"
                        />
                    `;

                    break;


                default:

                    formaSvg = `
                        <rect
                            x="35"
                            y="35"
                            width="130"
                            height="130"
                            rx="8"
                            fill="#6366f1"
                        />
                    `;
            }


            visualEl.innerHTML = `

                <svg
                    viewBox="0 0 200 200"
                    class="
                        mx-auto
                        h-52
                        w-52
                    "
                >
                    ${formaSvg}
                </svg>
            `;

            return;
        }


        // ========================================================
        // FRAÇÃO
        // ========================================================

        if (
            dados.tipo === "fracao"
        ) {

            const numerador =
                Number(
                    dados.numerador || 0
                );

            const denominador =
                Number(
                    dados.denominador || 1
                );


            let partes = "";


            for (
                let i = 0;
                i < denominador;
                i++
            ) {

                partes += `

                    <div
                        class="
                            h-28
                            flex-1
                            border-r
                            border-indigo-300
                            last:border-r-0
                            ${
                                i < numerador
                                    ? "bg-indigo-500"
                                    : "bg-white"
                            }
                        "
                    ></div>
                `;
            }


            visualEl.innerHTML = `

                <div
                    class="
                        mx-auto
                        max-w-md
                        text-center
                    "
                >

                    <div
                        class="
                            flex
                            overflow-hidden
                            rounded-2xl
                            border-2
                            border-indigo-300
                        "
                    >
                        ${partes}
                    </div>

                    <div
                        class="
                            mt-3
                            text-sm
                            font-bold
                            text-slate-500
                        "
                    >
                        Observe as partes pintadas.
                    </div>

                </div>
            `;

            return;
        }


        // ========================================================
        // RELÓGIO
        // ========================================================

        if (
            dados.tipo === "relogio"
        ) {

            const hora =
                Number(
                    dados.hora || 0
                );

            const minuto =
                Number(
                    dados.minuto || 0
                );


            const anguloMinuto =
                minuto * 6;

            const anguloHora =
                (hora % 12) * 30 +
                minuto * 0.5;


            visualEl.innerHTML = `

                <div
                    class="
                        relative
                        mx-auto
                        h-60
                        w-60
                        rounded-full
                        border-8
                        border-slate-800
                        bg-white
                        shadow-lg
                    "
                >

                    <span
                        class="
                            absolute
                            left-1/2
                            top-2
                            -translate-x-1/2
                            font-black
                        "
                    >
                        12
                    </span>

                    <span
                        class="
                            absolute
                            right-3
                            top-1/2
                            -translate-y-1/2
                            font-black
                        "
                    >
                        3
                    </span>

                    <span
                        class="
                            absolute
                            bottom-2
                            left-1/2
                            -translate-x-1/2
                            font-black
                        "
                    >
                        6
                    </span>

                    <span
                        class="
                            absolute
                            left-3
                            top-1/2
                            -translate-y-1/2
                            font-black
                        "
                    >
                        9
                    </span>


                    <div
                        class="
                            absolute
                            left-1/2
                            top-1/2
                            h-16
                            w-2
                            origin-bottom
                            rounded-full
                            bg-slate-900
                        "

                        style="
                            transform:
                                translate(-50%, -100%)
                                rotate(${anguloHora}deg);
                        "
                    ></div>


                    <div
                        class="
                            absolute
                            left-1/2
                            top-1/2
                            h-20
                            w-1
                            origin-bottom
                            rounded-full
                            bg-indigo-500
                        "

                        style="
                            transform:
                                translate(-50%, -100%)
                                rotate(${anguloMinuto}deg);
                        "
                    ></div>


                    <div
                        class="
                            absolute
                            left-1/2
                            top-1/2
                            h-4
                            w-4
                            -translate-x-1/2
                            -translate-y-1/2
                            rounded-full
                            bg-slate-900
                        "
                    ></div>

                </div>
            `;

            return;
        }


        // ========================================================
        // DINHEIRO
        // ========================================================

        if (
            dados.tipo === "dinheiro"
        ) {

            visualEl.innerHTML = `

                <div
                    class="
                        flex
                        flex-wrap
                        justify-center
                        gap-4
                    "
                >

                    ${
                        (dados.valores || [])
                            .map(valor => `

                                <div
                                    class="
                                        min-w-28
                                        rounded-2xl
                                        border-4
                                        border-emerald-500
                                        bg-emerald-50
                                        px-5
                                        py-5
                                        text-center
                                        text-xl
                                        font-black
                                        text-emerald-700
                                        shadow-sm
                                    "
                                >
                                    R$ ${escapar(valor)}
                                </div>
                            `)
                            .join("")
                    }

                </div>
            `;

            return;
        }


        // ========================================================
        // GRÁFICO DE BARRAS
        // ========================================================

        if (
            dados.tipo ===
            "grafico_barras"
        ) {

            const valores =
                dados.dados || {};

            const maior =
                Math.max(
                    ...Object.values(
                        valores
                    ).map(Number),
                    1
                );


            visualEl.innerHTML = `

                <div
                    class="
                        mx-auto
                        max-w-xl
                        space-y-4
                    "
                >

                    ${
                        Object.entries(
                            valores
                        )
                            .map(
                                ([nome, valor]) => `

                                    <div>

                                        <div
                                            class="
                                                mb-1
                                                flex
                                                justify-between
                                                font-bold
                                            "
                                        >
                                            <span>
                                                ${escapar(nome)}
                                            </span>

                                            <span>
                                                ${escapar(valor)}
                                            </span>
                                        </div>

                                        <div
                                            class="
                                                h-8
                                                overflow-hidden
                                                rounded-lg
                                                bg-slate-100
                                            "
                                        >

                                            <div
                                                class="
                                                    h-full
                                                    rounded-lg
                                                    bg-indigo-500
                                                "

                                                style="
                                                    width:
                                                    ${
                                                        (
                                                            Number(valor) /
                                                            maior
                                                        ) * 100
                                                    }%;
                                                "
                                            ></div>

                                        </div>

                                    </div>
                                `
                            )
                            .join("")
                    }

                </div>
            `;

            return;
        }


        // ========================================================
        // RÉGUA
        // ========================================================

        if (
            dados.tipo === "regua"
        ) {

            visualEl.innerHTML = `

                <div
                    class="
                        mx-auto
                        max-w-lg
                        rounded-2xl
                        bg-yellow-200
                        p-6
                        text-center
                    "
                >

                    <div class="text-7xl">
                        📏
                    </div>

                    <div
                        class="
                            mt-3
                            text-2xl
                            font-black
                        "
                    >
                        ${escapar(
                            dados.metros || ""
                        )} m
                    </div>

                </div>
            `;

            return;
        }


        // ========================================================
        // BALANÇA
        // ========================================================

        if (
            dados.tipo === "balanca"
        ) {

            visualEl.innerHTML = `

                <div class="text-center">

                    <div class="text-8xl">
                        ⚖️
                    </div>

                    <div
                        class="
                            mt-3
                            text-2xl
                            font-black
                        "
                    >
                        ${escapar(
                            dados.kg || ""
                        )} kg
                    </div>

                </div>
            `;

            return;
        }


        // ========================================================
        // MOEDA
        // ========================================================

        if (
            dados.tipo === "moeda"
        ) {

            visualEl.innerHTML = `

                <div
                    class="
                        text-center
                        text-8xl
                    "
                >
                    🪙
                </div>
            `;

            return;
        }


        // ========================================================
        // DADO
        // ========================================================

        if (
            dados.tipo === "dado"
        ) {

            visualEl.innerHTML = `

                <div
                    class="
                        text-center
                        text-8xl
                    "
                >
                    🎲
                </div>
            `;

            return;
        }


        // ========================================================
        // SÓLIDO
        // ========================================================

        if (
            dados.tipo === "solido"
        ) {

            const mapa = {

                esfera:
                    "⚽",

                cubo:
                    "🧊",

                cilindro:
                    "🥫",

                cone:
                    "🔺"
            };


            visualEl.innerHTML = `

                <div
                    class="
                        text-center
                        text-8xl
                    "
                >
                    ${
                        mapa[
                            dados.forma
                        ] ||
                        "🧊"
                    }
                </div>
            `;

            return;
        }


        // ========================================================
        // TERMÔMETRO
        // ========================================================

        if (
            dados.tipo ===
            "termometro"
        ) {

            const temperatura =
                Number(
                    dados.valor || 0
                );


            visualEl.innerHTML = `

                <div
                    class="
                        mx-auto
                        flex
                        max-w-xs
                        items-center
                        justify-center
                        gap-6
                    "
                >

                    <div
                        class="
                            text-8xl
                        "
                    >
                        🌡️
                    </div>

                    <div
                        class="
                            text-4xl
                            font-black
                        "
                    >
                        ${temperatura} °C
                    </div>

                </div>
            `;

            return;
        }


        // ========================================================
        // ÂNGULO
        // ========================================================

        if (
            dados.tipo === "angulo"
        ) {

            const graus =
                Number(
                    dados.graus || 0
                );


            const radiano =
                -graus *
                Math.PI /
                180;


            const x =
                100 +
                75 *
                Math.cos(
                    radiano
                );


            const y =
                150 +
                75 *
                Math.sin(
                    radiano
                );


            visualEl.innerHTML = `

                <svg
                    viewBox="0 0 220 190"
                    class="
                        mx-auto
                        w-64
                    "
                >

                    <line
                        x1="100"
                        y1="150"
                        x2="190"
                        y2="150"
                        stroke="#0f172a"
                        stroke-width="7"
                        stroke-linecap="round"
                    />

                    <line
                        x1="100"
                        y1="150"
                        x2="${x}"
                        y2="${y}"
                        stroke="#6366f1"
                        stroke-width="7"
                        stroke-linecap="round"
                    />

                    <circle
                        cx="100"
                        cy="150"
                        r="7"
                        fill="#0f172a"
                    />

                    <text
                        x="110"
                        y="135"
                        font-size="18"
                        font-weight="700"
                    >
                        ${graus}°
                    </text>

                </svg>
            `;

            return;
        }


        // ========================================================
        // RETÂNGULO - PERÍMETRO / ÁREA
        // ========================================================

        if (
            dados.tipo ===
            "retangulo_medidas"
        ) {

            let grade = "";


            if (dados.grade) {

                for (
                    let x = 60;
                    x <= 260;
                    x += 20
                ) {

                    grade += `

                        <line
                            x1="${x}"
                            y1="35"
                            x2="${x}"
                            y2="155"
                            stroke="#c7d2fe"
                        />
                    `;
                }


                for (
                    let y = 35;
                    y <= 155;
                    y += 20
                ) {

                    grade += `

                        <line
                            x1="60"
                            y1="${y}"
                            x2="260"
                            y2="${y}"
                            stroke="#c7d2fe"
                        />
                    `;
                }
            }


            visualEl.innerHTML = `

                <svg
                    viewBox="0 0 320 200"
                    class="
                        mx-auto
                        w-full
                        max-w-md
                    "
                >

                    <rect
                        x="60"
                        y="35"
                        width="200"
                        height="120"
                        rx="6"
                        fill="#eef2ff"
                        stroke="#6366f1"
                        stroke-width="5"
                    />

                    ${grade}

                    <text
                        x="160"
                        y="25"
                        text-anchor="middle"
                        font-size="20"
                        font-weight="900"
                    >
                        ${escapar(
                            dados.largura
                        )}
                    </text>

                    <text
                        x="280"
                        y="102"
                        font-size="20"
                        font-weight="900"
                    >
                        ${escapar(
                            dados.altura
                        )}
                    </text>

                </svg>
            `;

            return;
        }


        // ========================================================
        // PLANO CARTESIANO
        // ========================================================

        if (
            dados.tipo ===
            "plano_cartesiano"
        ) {

            const x =
                Number(
                    dados.x || 0
                );

            const y =
                Number(
                    dados.y || 0
                );


            const origemX = 50;

            const origemY = 250;

            const passo = 25;


            const pontoX =
                origemX +
                x *
                passo;

            const pontoY =
                origemY -
                y *
                passo;


            let grade = "";

            let numerosX = "";

            let numerosY = "";


            for (
                let i = 0;
                i <= 8;
                i++
            ) {

                const posX =
                    origemX +
                    i *
                    passo;

                const posY =
                    origemY -
                    i *
                    passo;


                grade += `

                    <line
                        x1="${posX}"
                        y1="40"
                        x2="${posX}"
                        y2="${origemY}"
                        stroke="#e2e8f0"
                        stroke-width="1"
                    />

                    <line
                        x1="${origemX}"
                        y1="${posY}"
                        x2="260"
                        y2="${posY}"
                        stroke="#e2e8f0"
                        stroke-width="1"
                    />
                `;


                numerosX += `

                    <text
                        x="${posX}"
                        y="${origemY + 23}"
                        text-anchor="middle"
                        font-size="12"
                        font-weight="700"
                        fill="#475569"
                    >
                        ${i}
                    </text>
                `;


                if (i > 0) {

                    numerosY += `

                        <text
                            x="${origemX - 15}"
                            y="${posY + 4}"
                            text-anchor="middle"
                            font-size="12"
                            font-weight="700"
                            fill="#475569"
                        >
                            ${i}
                        </text>
                    `;
                }
            }


            visualEl.innerHTML = `

                <div
                    class="
                        mx-auto
                        max-w-md
                        rounded-3xl
                        border
                        border-slate-200
                        bg-white
                        p-4
                        shadow-sm
                    "
                >

                    <svg
                        viewBox="0 0 300 290"
                        class="w-full"
                    >

                        ${grade}

                        <line
                            x1="${origemX}"
                            y1="${origemY}"
                            x2="275"
                            y2="${origemY}"
                            stroke="#0f172a"
                            stroke-width="3"
                        />

                        <polygon
                            points="
                                275,250
                                265,244
                                265,256
                            "
                            fill="#0f172a"
                        />

                        <line
                            x1="${origemX}"
                            y1="${origemY}"
                            x2="${origemX}"
                            y2="20"
                            stroke="#0f172a"
                            stroke-width="3"
                        />

                        <polygon
                            points="
                                50,20
                                44,30
                                56,30
                            "
                            fill="#0f172a"
                        />

                        ${numerosX}

                        ${numerosY}

                        <text
                            x="280"
                            y="${origemY + 5}"
                            font-size="16"
                            font-weight="900"
                        >
                            X
                        </text>

                        <text
                            x="${origemX - 5}"
                            y="16"
                            font-size="16"
                            font-weight="900"
                        >
                            Y
                        </text>

                        <circle
                            cx="${pontoX}"
                            cy="${pontoY}"
                            r="14"
                            fill="#c7d2fe"
                        />

                        <circle
                            cx="${pontoX}"
                            cy="${pontoY}"
                            r="9"
                            fill="#4f46e5"
                        />

                        <text
                            x="${pontoX + 14}"
                            y="${pontoY - 12}"
                            font-size="17"
                            font-weight="900"
                            fill="#4338ca"
                        >
                            P
                        </text>

                    </svg>

                    <p
                        class="
                            mt-2
                            text-center
                            text-sm
                            font-bold
                            text-slate-500
                        "
                    >
                        Observe a posição do ponto P.
                    </p>

                </div>
            `;

            return;
        }


        // ========================================================
        // BLOCO / VOLUME
        // ========================================================

        if (
            dados.tipo === "bloco"
        ) {

            visualEl.innerHTML = `

                <div
                    class="
                        mx-auto
                        max-w-md
                        rounded-3xl
                        bg-indigo-50
                        p-8
                        text-center
                    "
                >

                    <div class="text-7xl">
                        🧊
                    </div>

                    <div
                        class="
                            mt-4
                            text-2xl
                            font-black
                        "
                    >
                        ${escapar(dados.a)}
                        ×
                        ${escapar(dados.b)}
                        ×
                        ${escapar(dados.c)}
                    </div>

                </div>
            `;

            return;
        }
    }


    // ============================================================
    // CAMPO PARA DIGITAR
    // ============================================================

    function renderizarNumero() {

        respostaAreaEl.innerHTML = `

            <div
                class="
                    mx-auto
                    max-w-md
                "
            >

                <input
                    id="resposta"

                    type="text"

                    inputmode="decimal"

                    autocomplete="off"

                    placeholder="Digite sua resposta"

                    class="
                        w-full
                        rounded-2xl
                        border-2
                        border-slate-200
                        bg-white
                        px-6
                        py-5
                        text-center
                        text-3xl
                        font-black
                        outline-none
                        transition

                        focus:border-indigo-500
                        focus:ring-4
                        focus:ring-indigo-100
                    "
                >

            </div>
        `;


        const input =
            document.getElementById(
                "resposta"
            );


        input.addEventListener(
            "input",
            () => {

                respostaAtual =
                    input.value;
            }
        );


        input.addEventListener(
            "keydown",
            evento => {

                if (
                    evento.key === "Enter"
                ) {

                    evento.preventDefault();

                    enviarResposta();
                }
            }
        );


        setTimeout(
            () => input.focus(),
            50
        );
    }


    // ============================================================
    // MÚLTIPLA ESCOLHA
    // ============================================================

    function renderizarMultiplaEscolha(
        dados
    ) {

        const alternativas =
            dados.alternativas || [];


        respostaAreaEl.innerHTML = `

            <div
                class="
                    mx-auto
                    grid
                    max-w-3xl
                    grid-cols-1
                    gap-4

                    sm:grid-cols-2
                "
            >

                ${
                    alternativas
                        .map(alternativa => `

                            <button
                                type="button"

                                data-resposta="${
                                    escapar(
                                        alternativa.id
                                    )
                                }"

                                class="
                                    min-h-24
                                    rounded-2xl
                                    border-2
                                    border-slate-200
                                    bg-white
                                    p-5
                                    text-xl
                                    font-black
                                    shadow-sm
                                    transition

                                    hover:-translate-y-1
                                    hover:border-indigo-400
                                    hover:shadow-md
                                "
                            >
                                ${
                                    escapar(
                                        alternativa.texto
                                    )
                                }
                            </button>
                        `)
                        .join("")
                }

            </div>
        `;


        respostaAreaEl
            .querySelectorAll(
                "[data-resposta]"
            )
            .forEach(elemento => {

                elemento.addEventListener(
                    "click",
                    () => {

                        respostaAtual =
                            elemento.dataset
                                .resposta;


                        selecionarCard(
                            elemento
                        );
                    }
                );
            });
    }


    // ============================================================
    // ESCOLHA POR IMAGEM REAL
    // ============================================================

    function renderizarImagemEscolha(
        dados
    ) {

        respostaAreaEl.innerHTML = `

            <div
                class="
                    mx-auto
                    grid
                    max-w-5xl
                    grid-cols-2
                    gap-4

                    md:grid-cols-4
                "
            >

                ${
                    (dados.alternativas || [])
                        .map(alternativa => `

                            <button
                                type="button"

                                data-resposta="${
                                    escapar(
                                        alternativa.id
                                    )
                                }"

                                class="
                                    overflow-hidden
                                    rounded-2xl
                                    border-2
                                    border-slate-200
                                    bg-white
                                    p-2
                                    shadow-sm
                                    transition

                                    hover:-translate-y-1
                                    hover:border-indigo-400
                                    hover:shadow-lg
                                "
                            >

                                <div
                                    class="
                                        relative
                                        aspect-square
                                        overflow-hidden
                                        rounded-xl
                                        bg-slate-100
                                    "
                                >

                                    <img
                                        src="${
                                            escapar(
                                                alternativa.imagem
                                            )
                                        }"

                                        alt="${
                                            escapar(
                                                alternativa.texto || ""
                                            )
                                        }"

                                        loading="lazy"

                                        class="
                                            h-full
                                            w-full
                                            object-cover
                                        "
                                    >


                                    <div
                                        class="
                                            imagem-fallback
                                            absolute
                                            inset-0
                                            hidden
                                            items-center
                                            justify-center
                                            bg-slate-100
                                            text-7xl
                                        "
                                    >
                                        ${
                                            escapar(
                                                alternativa.fallback ||
                                                "🖼️"
                                            )
                                        }
                                    </div>

                                </div>


                                <div
                                    class="
                                        py-3
                                        text-center
                                        font-black
                                    "
                                >
                                    ${
                                        escapar(
                                            alternativa.texto || ""
                                        )
                                    }
                                </div>

                            </button>
                        `)
                        .join("")
                }

            </div>
        `;


        respostaAreaEl
            .querySelectorAll("img")
            .forEach(imagem => {

                imagem.addEventListener(
                    "error",
                    () => {

                        imagem.style.display =
                            "none";


                        const fallback =
                            imagem
                                .parentElement
                                .querySelector(
                                    ".imagem-fallback"
                                );


                        if (fallback) {

                            fallback.classList.remove(
                                "hidden"
                            );

                            fallback.classList.add(
                                "flex"
                            );
                        }
                    }
                );
            });


        respostaAreaEl
            .querySelectorAll(
                "[data-resposta]"
            )
            .forEach(elemento => {

                elemento.addEventListener(
                    "click",
                    () => {

                        respostaAtual =
                            elemento.dataset
                                .resposta;


                        selecionarCard(
                            elemento
                        );
                    }
                );
            });
    }


    // ============================================================
    // ASSOCIAÇÃO
    // ============================================================

    function renderizarAssociacao(
        dados
    ) {

        quantidadeAssociacoes =
            (dados.esquerda || [])
                .length;


        respostaAreaEl.innerHTML = `

            <div
                class="
                    mx-auto
                    max-w-4xl
                "
            >

                <p
                    class="
                        mb-5
                        text-center
                        font-bold
                        text-slate-500
                    "
                >
                    Escolha um item da esquerda e depois
                    o correspondente da direita.
                </p>


                <div
                    class="
                        grid
                        grid-cols-2
                        gap-5
                    "
                >

                    <div class="space-y-3">

                        ${
                            (dados.esquerda || [])
                                .map(item => `

                                    <button
                                        type="button"

                                        data-esquerda="${
                                            escapar(
                                                item.id
                                            )
                                        }"

                                        class="
                                            w-full
                                            rounded-2xl
                                            border-2
                                            border-slate-200
                                            bg-white
                                            p-5
                                            text-xl
                                            font-black
                                            transition
                                        "
                                    >
                                        ${
                                            escapar(
                                                item.texto
                                            )
                                        }
                                    </button>
                                `)
                                .join("")
                        }

                    </div>


                    <div class="space-y-3">

                        ${
                            (dados.direita || [])
                                .map(item => `

                                    <button
                                        type="button"

                                        data-direita="${
                                            escapar(
                                                item.id
                                            )
                                        }"

                                        class="
                                            w-full
                                            rounded-2xl
                                            border-2
                                            border-slate-200
                                            bg-white
                                            p-5
                                            text-xl
                                            font-black
                                            transition
                                        "
                                    >
                                        ${
                                            escapar(
                                                item.texto
                                            )
                                        }
                                    </button>
                                `)
                                .join("")
                        }

                    </div>

                </div>


                <div
                    id="status-associacao"

                    class="
                        mt-5
                        text-center
                        font-bold
                        text-slate-500
                    "
                ></div>

            </div>
        `;


        const status =
            document.getElementById(
                "status-associacao"
            );


        respostaAreaEl
            .querySelectorAll(
                "[data-esquerda]"
            )
            .forEach(elemento => {

                elemento.addEventListener(
                    "click",
                    () => {

                        associacaoSelecionada =
                            elemento.dataset
                                .esquerda;


                        respostaAreaEl
                            .querySelectorAll(
                                "[data-esquerda]"
                            )
                            .forEach(item => {

                                item.classList.remove(
                                    "border-indigo-500",
                                    "bg-indigo-50",
                                    "ring-4",
                                    "ring-indigo-100"
                                );
                            });


                        elemento.classList.add(
                            "border-indigo-500",
                            "bg-indigo-50",
                            "ring-4",
                            "ring-indigo-100"
                        );
                    }
                );
            });


        respostaAreaEl
            .querySelectorAll(
                "[data-direita]"
            )
            .forEach(elemento => {

                elemento.addEventListener(
                    "click",
                    () => {

                        if (
                            !associacaoSelecionada
                        ) {

                            mostrarMensagem(
                                "Escolha primeiro um item da esquerda.",
                                "aviso"
                            );

                            return;
                        }


                        const idEsquerda =
                            associacaoSelecionada;

                        const idDireita =
                            elemento.dataset
                                .direita;


                        associacoes[
                            idEsquerda
                        ] =
                            idDireita;


                        respostaAtual = {
                            ...associacoes
                        };


                        const esquerda =
                            respostaAreaEl
                                .querySelector(
                                    `[data-esquerda="${CSS.escape(
                                        idEsquerda
                                    )}"]`
                                );


                        if (esquerda) {

                            esquerda.classList.remove(
                                "border-indigo-500",
                                "ring-4",
                                "ring-indigo-100"
                            );

                            esquerda.classList.add(
                                "border-green-500",
                                "bg-green-50"
                            );
                        }


                        elemento.classList.add(
                            "border-green-500",
                            "bg-green-50"
                        );


                        associacaoSelecionada =
                            null;


                        const feitas =
                            Object.keys(
                                associacoes
                            ).length;


                        status.textContent =
                            `${feitas}/${quantidadeAssociacoes} associações realizadas.`;


                        mostrarMensagem("");
                    }
                );
            });
    }


    // ============================================================
    // ORDENAÇÃO
    // ============================================================

    function renderizarOrdenacao(
        dados
    ) {

        quantidadeOrdenacao =
            (dados.itens || [])
                .length;


        respostaAreaEl.innerHTML = `

            <div
                class="
                    mx-auto
                    max-w-4xl
                "
            >

                <p
                    class="
                        mb-5
                        text-center
                        font-bold
                        text-slate-500
                    "
                >
                    Clique nos itens na ordem correta.
                </p>


                <div
                    id="ordem-origem"

                    class="
                        flex
                        min-h-24
                        flex-wrap
                        items-center
                        justify-center
                        gap-3
                        rounded-2xl
                        border-2
                        border-dashed
                        border-slate-300
                        bg-slate-50
                        p-4
                    "
                >

                    ${
                        (dados.itens || [])
                            .map(item => `

                                <button
                                    type="button"

                                    data-ordem="${
                                        escapar(
                                            item.id
                                        )
                                    }"

                                    class="
                                        rounded-xl
                                        border-2
                                        border-slate-200
                                        bg-white
                                        px-6
                                        py-4
                                        text-xl
                                        font-black
                                        shadow-sm
                                        transition

                                        hover:border-indigo-400
                                    "
                                >
                                    ${
                                        escapar(
                                            item.texto
                                        )
                                    }
                                </button>
                            `)
                            .join("")
                    }

                </div>


                <div
                    class="
                        my-4
                        text-center
                        text-3xl
                    "
                >
                    ↓
                </div>


                <div
                    id="ordem-destino"

                    class="
                        flex
                        min-h-24
                        flex-wrap
                        items-center
                        justify-center
                        gap-3
                        rounded-2xl
                        border-2
                        border-indigo-200
                        bg-indigo-50
                        p-4
                    "
                ></div>


                <button
                    id="limpar-ordem"

                    type="button"

                    class="
                        mx-auto
                        mt-4
                        block
                        rounded-xl
                        bg-slate-200
                        px-5
                        py-3
                        font-black
                        text-slate-700

                        hover:bg-slate-300
                    "
                >
                    Limpar ordem
                </button>

            </div>
        `;


        const destino =
            document.getElementById(
                "ordem-destino"
            );


        respostaAreaEl
            .querySelectorAll(
                "[data-ordem]"
            )
            .forEach(elemento => {

                elemento.addEventListener(
                    "click",
                    () => {

                        const valor =
                            elemento.dataset
                                .ordem;


                        if (
                            ordemSelecionada
                                .includes(
                                    valor
                                )
                        ) {

                            return;
                        }


                        ordemSelecionada.push(
                            valor
                        );


                        respostaAtual = [
                            ...ordemSelecionada
                        ];


                        const copia =
                            elemento.cloneNode(
                                true
                            );


                        copia.removeAttribute(
                            "data-ordem"
                        );


                        copia.disabled =
                            true;


                        copia.classList.add(
                            "border-indigo-500",
                            "bg-white"
                        );


                        destino.appendChild(
                            copia
                        );


                        elemento.disabled =
                            true;


                        elemento.classList.add(
                            "opacity-30"
                        );
                    }
                );
            });


        document
            .getElementById(
                "limpar-ordem"
            )
            .addEventListener(
                "click",
                () => {

                    ordemSelecionada = [];

                    respostaAtual = [];

                    destino.innerHTML = "";


                    respostaAreaEl
                        .querySelectorAll(
                            "[data-ordem]"
                        )
                        .forEach(elemento => {

                            elemento.disabled =
                                false;

                            elemento.classList.remove(
                                "opacity-30"
                            );
                        });
                }
            );
    }


    // ============================================================
    // RENDERIZAR QUESTÃO
    // ============================================================

    function renderizarQuestao(
        dados
    ) {

        if (
            !dados ||
            typeof dados !== "object"
        ) {

            console.error(
                "Questão inválida:",
                dados
            );

            mostrarMensagem(
                "O servidor enviou uma questão inválida.",
                "erro"
            );

            return;
        }


        limparEstadoQuestao();


        questaoAtual =
            dados;


        perguntaEl.textContent =
            dados.pergunta ||
            "Resolva a questão.";


        renderizarVisual(
            dados.visual
        );


        switch (
            dados.tipo_ui
        ) {

            case "multipla_escolha":

                renderizarMultiplaEscolha(
                    dados
                );

                break;


            case "verdadeiro_falso":

                renderizarMultiplaEscolha(
                    dados
                );

                break;


            case "imagem_escolha":

                renderizarImagemEscolha(
                    dados
                );

                break;


            case "associacao":

                renderizarAssociacao(
                    dados
                );

                break;


            case "ordenacao":

                renderizarOrdenacao(
                    dados
                );

                break;


            case "numero":

                renderizarNumero();

                break;


            default:

                console.warn(
                    "tipo_ui desconhecido:",
                    dados.tipo_ui
                );

                renderizarNumero();

                break;
        }
    }


    // ============================================================
    // VERIFICAR SE RESPOSTA ESTÁ COMPLETA
    // ============================================================

    function validarRespostaAntesDeEnviar() {

        if (
            respostaAtual === null ||
            respostaAtual === ""
        ) {

            mostrarMensagem(
                "Escolha ou digite uma resposta.",
                "aviso"
            );

            return false;
        }


        if (
            questaoAtual.tipo_ui ===
            "associacao"
        ) {

            const realizadas =
                Object.keys(
                    associacoes
                ).length;


            if (
                realizadas <
                quantidadeAssociacoes
            ) {

                mostrarMensagem(
                    `Complete todas as associações (${realizadas}/${quantidadeAssociacoes}).`,
                    "aviso"
                );

                return false;
            }
        }


        if (
            questaoAtual.tipo_ui ===
            "ordenacao"
        ) {

            if (
                ordemSelecionada.length <
                quantidadeOrdenacao
            ) {

                mostrarMensagem(
                    `Coloque todos os itens em ordem (${ordemSelecionada.length}/${quantidadeOrdenacao}).`,
                    "aviso"
                );

                return false;
            }
        }


        if (
            Array.isArray(
                respostaAtual
            ) &&
            respostaAtual.length === 0
        ) {

            mostrarMensagem(
                "Escolha uma resposta.",
                "aviso"
            );

            return false;
        }


        if (
            typeof respostaAtual ===
                "object" &&
            respostaAtual !== null &&
            !Array.isArray(
                respostaAtual
            ) &&
            Object.keys(
                respostaAtual
            ).length === 0
        ) {

            mostrarMensagem(
                "Complete a resposta.",
                "aviso"
            );

            return false;
        }


        return true;
    }


    // ============================================================
    // ATUALIZAR PROGRESSO
    // ============================================================

    function atualizarProgresso(
        respondidas,
        quantidade
    ) {

        respondidas =
            Number(
                respondidas || 0
            );

        quantidade =
            Number(
                quantidade || 1
            );


        const porcentagem =
            Math.min(
                100,
                Math.round(
                    (
                        respondidas /
                        quantidade
                    ) *
                    100
                )
            );


        if (barraProgresso) {

            barraProgresso.style.width =
                `${porcentagem}%`;
        }


        if (textoProgresso) {

            textoProgresso.textContent =
                `${respondidas}/${quantidade}`;
        }
    }


    // ============================================================
    // ENVIAR RESPOSTA
    // ============================================================

    async function enviarResposta() {

        if (enviando) {

            return;
        }


        if (
            !validarRespostaAntesDeEnviar()
        ) {

            return;
        }


        enviando = true;

        botaoResponder.disabled = true;

        botaoResponder.textContent =
            "Verificando...";


        console.log(
            "Resposta enviada:",
            respostaAtual
        );


        try {

            const respostaServidor =
                await fetch(
                    "/api/responder",
                    {

                        method:
                            "POST",

                        headers: {

                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                {
                                    resposta:
                                        respostaAtual
                                }
                            )
                    }
                );


            const texto =
                await respostaServidor.text();


            let dados;


            try {

                dados =
                    JSON.parse(
                        texto
                    );

            } catch (erro) {

                console.error(
                    "Resposta não JSON:",
                    texto
                );

                throw new Error(
                    "O servidor retornou uma resposta inválida."
                );
            }


            console.log(
                "Resposta da API:",
                dados
            );


            if (
                !respostaServidor.ok
            ) {

                throw new Error(
                    dados.erro ||
                    "Erro ao verificar resposta."
                );
            }


            // ====================================================
            // FEEDBACK
            // ====================================================

            if (dados.correto) {

                mostrarMensagem(
                    dados.mensagem ||
                    "Muito bem! 🎉",
                    "sucesso"
                );

            } else {

                mostrarMensagem(
                    dados.mensagem ||
                    "Resposta incorreta.",
                    "erro"
                );
            }


            // ====================================================
            // XP
            // ====================================================

            if (
                xpEl &&
                dados.xp !== undefined
            ) {

                xpEl.textContent =
                    dados.xp;
            }


            // ====================================================
            // MOEDAS
            // ====================================================

            if (
                moedasEl &&
                dados.moedas !== undefined
            ) {

                moedasEl.textContent =
                    dados.moedas;
            }


            // ====================================================
            // FINAL DA ETAPA
            // ====================================================

            if (dados.terminou) {

                atualizarProgresso(
                    dados.quantidade,
                    dados.quantidade
                );


                await esperar(
                    1000
                );


                mostrarResultadoFinal(
                    dados
                );


                return;
            }


            // ====================================================
            // PROGRESSO NORMAL
            // ====================================================

            atualizarProgresso(
                dados.respondidas,
                dados.quantidade
            );


            // ====================================================
            // PRÓXIMA QUESTÃO
            // ====================================================

            await esperar(
                1000
            );


            if (!dados.questao) {

                throw new Error(
                    "O servidor não enviou a próxima questão."
                );
            }


            renderizarQuestao(
                dados.questao
            );

        } catch (erro) {

            console.error(
                "Erro ao verificar resposta:",
                erro
            );


            mostrarMensagem(
                erro.message ||
                "Não foi possível acessar o servidor.",
                "erro"
            );

        } finally {

            enviando = false;


            if (
                document.body.contains(
                    botaoResponder
                )
            ) {

                botaoResponder.disabled =
                    false;

                botaoResponder.textContent =
                    "Conferir 🚀";
            }
        }
    }


    // ============================================================
    // RESULTADO FINAL
    // ============================================================

    function mostrarResultadoFinal(
        dados
    ) {

        const passou =
            Boolean(
                dados.passou
            );


        const assuntoConcluido =
            Boolean(
                dados.assunto_concluido
            );


        app.innerHTML = `

            <div
                class="
                    mx-auto
                    max-w-xl
                    py-12
                    text-center
                "
            >

                <div class="text-8xl">

                    ${
                        passou
                            ? "🏆"
                            : "💪"
                    }

                </div>


                <h1
                    class="
                        mt-5
                        text-3xl
                        font-black
                        text-slate-900
                    "
                >

                    ${
                        passou
                            ? "Etapa concluída!"
                            : "Continue praticando!"
                    }

                </h1>


                <p
                    class="
                        mt-4
                        text-lg
                        text-slate-600
                    "
                >

                    Você acertou

                    <strong>
                        ${escapar(
                            dados.acertos
                        )}
                    </strong>

                    de

                    <strong>
                        ${escapar(
                            dados.quantidade
                        )}
                    </strong>

                    questões.

                </p>


                <div
                    class="
                        mx-auto
                        mt-7
                        flex
                        h-36
                        w-36
                        items-center
                        justify-center
                        rounded-full
                        border-8
                        text-3xl
                        font-black

                        ${
                            passou
                                ? "border-green-500 text-green-600"
                                : "border-orange-400 text-orange-500"
                        }
                    "
                >
                    ${escapar(
                        dados.pontuacao
                    )}%
                </div>


                <p
                    class="
                        mt-5
                        font-bold
                        text-slate-500
                    "
                >

                    ${
                        passou
                            ? "Você atingiu a pontuação necessária para avançar."
                            : "Você precisa atingir pelo menos 80% para concluir esta etapa."
                    }

                </p>


                ${
                    assuntoConcluido
                        ? `

                            <div
                                class="
                                    mt-6
                                    rounded-2xl
                                    border
                                    border-yellow-300
                                    bg-yellow-100
                                    p-5
                                    font-black
                                    text-yellow-800
                                "
                            >
                                🏆 Assunto completamente concluído!
                            </div>
                        `
                        : ""
                }


                <div
                    class="
                        mt-8
                        flex
                        flex-col
                        gap-3

                        sm:flex-row
                        sm:justify-center
                    "
                >

                    <button
                        id="repetir-etapa"

                        type="button"

                        class="
                            rounded-2xl
                            bg-indigo-600
                            px-6
                            py-4
                            font-black
                            text-white
                            shadow-lg

                            hover:bg-indigo-700
                        "
                    >

                        ${
                            passou
                                ? "Praticar novamente"
                                : "Tentar novamente"
                        }

                    </button>


                    <button
                        id="voltar-trilha"

                        type="button"

                        class="
                            rounded-2xl
                            bg-slate-200
                            px-6
                            py-4
                            font-black
                            text-slate-700

                            hover:bg-slate-300
                        "
                    >
                        Voltar para a trilha
                    </button>

                </div>

            </div>
        `;


        document
            .getElementById(
                "repetir-etapa"
            )
            ?.addEventListener(
                "click",
                () => {

                    window.location.reload();
                }
            );


        document
            .getElementById(
                "voltar-trilha"
            )
            ?.addEventListener(
                "click",
                () => {

                    window.history.back();
                }
            );
    }


    // ============================================================
    // BOTÃO PRINCIPAL
    // ============================================================

    botaoResponder.addEventListener(
        "click",
        enviarResposta
    );


    // ============================================================
    // INICIAR EXERCÍCIO
    // ============================================================

    console.log(
        "Questão inicial:",
        questaoAtual
    );


    renderizarQuestao(
        questaoAtual
    );

});