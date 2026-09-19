document.addEventListener("DOMContentLoaded", () => {

    // =========================================================
    // ELEMENTOS DA PÁGINA
    // =========================================================

    const app = document.getElementById("exercicio-app");
    const jsonInicial = document.getElementById("questao-inicial");

    const pergunta = document.getElementById("pergunta");
    const visual = document.getElementById("visual");
    const respostaArea = document.getElementById("resposta-area");

    const botao = document.getElementById("botaoResponder");
    const feedback = document.getElementById("feedback");

    const barra = document.getElementById("barra-progresso");
    const textoProgresso = document.getElementById("texto-progresso");

    const xp = document.getElementById("xp-atual");


    // =========================================================
    // VERIFICAÇÃO
    // =========================================================

    if (
        !app ||
        !jsonInicial ||
        !pergunta ||
        !visual ||
        !respostaArea ||
        !botao ||
        !feedback
    ) {

        console.error(
            "Erro: elementos necessários do exercício não foram encontrados."
        );

        return;
    }


    // =========================================================
    // CARREGAR QUESTÃO INICIAL
    // =========================================================

    let questaoAtual;

    try {

        questaoAtual = JSON.parse(
            jsonInicial.textContent
        );

    } catch (erro) {

        console.error(
            "Erro ao carregar questão:",
            erro
        );

        feedback.textContent =
            "Não foi possível carregar o exercício.";

        return;
    }


    // =========================================================
    // ESTADO
    // =========================================================

    let enviando = false;

    let respostaAtual = null;

    let associacoes = {};

    let associacaoSelecionada = null;

    let ordemSelecionada = [];


    // =========================================================
    // SEGURANÇA HTML
    // =========================================================

    function escapar(valor) {

        const div =
            document.createElement("div");

        div.textContent =
            String(valor ?? "");

        return div.innerHTML;
    }


    // =========================================================
    // LIMPAR ESTADO
    // =========================================================

    function resetarEstado() {

        respostaAtual = null;

        associacoes = {};

        associacaoSelecionada = null;

        ordemSelecionada = [];

        feedback.textContent = "";

        feedback.className =
            "mt-5 min-h-12 text-center font-black";

        botao.disabled = false;

        botao.textContent = "Conferir";
    }


    // =========================================================
    // FORMAS SVG
    // =========================================================

    function criarForma(nome) {

        const formas = {

            triangulo: `
                <polygon
                    points="100,20 180,170 20,170"
                    fill="#6366f1"
                />
            `,

            quadrado: `
                <rect
                    x="35"
                    y="35"
                    width="130"
                    height="130"
                    rx="8"
                    fill="#6366f1"
                />
            `,

            retangulo: `
                <rect
                    x="20"
                    y="55"
                    width="160"
                    height="100"
                    rx="8"
                    fill="#6366f1"
                />
            `,

            pentagono: `
                <polygon
                    points="100,18 180,76 150,170 50,170 20,76"
                    fill="#6366f1"
                />
            `,

            hexagono: `
                <polygon
                    points="55,25 145,25 190,100 145,175 55,175 10,100"
                    fill="#6366f1"
                />
            `
        };


        return `
            <svg
                viewBox="0 0 200 200"
                class="mx-auto w-48 h-48"
            >

                ${
                    formas[nome] ||
                    formas.quadrado
                }

            </svg>
        `;
    }


    // =========================================================
    // VISUAL DA QUESTÃO
    // =========================================================

    function renderizarVisual(dados) {

        visual.innerHTML = "";


        if (!dados) {

            return;
        }


        // =====================================================
        // ADIÇÃO COM OBJETOS
        // =====================================================

        if (dados.tipo === "grupos") {

            visual.innerHTML = `

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
                        .map(
                            quantidade => `

                                <div
                                    class="
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
                                            max-w-48
                                            text-3xl
                                        "
                                    >

                                        ${
                                            Array.from(
                                                {
                                                    length:
                                                        Math.min(
                                                            Number(
                                                                quantidade
                                                            ),
                                                            30
                                                        )
                                                },
                                                () => `

                                                    <span>
                                                        ${
                                                            dados.icone ||
                                                            "⭐"
                                                        }
                                                    </span>

                                                `
                                            ).join("")
                                        }

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


        // =====================================================
        // SUBTRAÇÃO VISUAL
        // =====================================================

        if (
            dados.tipo ===
            "subtracao_objetos"
        ) {

            let html = "";


            for (
                let i = 0;
                i < Number(dados.total || 0);
                i++
            ) {

                const retirado =
                    i <
                    Number(
                        dados.retirados || 0
                    );


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

                        ${
                            dados.icone ||
                            "🎈"
                        }

                    </span>

                `;
            }


            visual.innerHTML = `

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


        // =====================================================
        // MULTIPLICAÇÃO COM GRUPOS
        // =====================================================

        if (
            dados.tipo ===
            "multiplicacao_grupos"
        ) {

            visual.innerHTML = `

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
                            {
                                length:
                                    Number(
                                        dados.grupos ||
                                        0
                                    )
                            },

                            () => `

                                <div
                                    class="
                                        rounded-2xl
                                        border-2
                                        border-indigo-100
                                        bg-white
                                        p-4
                                        shadow
                                    "
                                >

                                    <div
                                        class="
                                            flex
                                            flex-wrap
                                            justify-center
                                            gap-2
                                            max-w-40
                                            text-2xl
                                        "
                                    >

                                        ${
                                            Array.from(
                                                {
                                                    length:
                                                        Number(
                                                            dados.itens ||
                                                            0
                                                        )
                                                },

                                                () => `

                                                    <span>
                                                        ${
                                                            dados.icone ||
                                                            "🔵"
                                                        }
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


        // =====================================================
        // DIVISÃO
        // =====================================================

        if (
            dados.tipo ===
            "divisao"
        ) {

            const grupos =
                Number(
                    dados.grupos ||
                    1
                );

            const total =
                Number(
                    dados.total ||
                    0
                );

            const porGrupo =
                Math.floor(
                    total /
                    grupos
                );


            visual.innerHTML = `

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
                            {
                                length:
                                    grupos
                            },

                            () => `

                                <div
                                    class="
                                        min-w-24
                                        rounded-2xl
                                        border-2
                                        border-indigo-100
                                        bg-white
                                        p-4
                                        text-center
                                        text-2xl
                                        shadow
                                    "
                                >

                                    ${
                                        Array.from(
                                            {
                                                length:
                                                    porGrupo
                                            },

                                            () =>
                                                dados.icone ||
                                                "🍬"

                                        ).join(" ")
                                    }

                                </div>

                            `
                        ).join("")
                    }

                </div>
            `;

            return;
        }


        // =====================================================
        // MATERIAL DOURADO
        // =====================================================

        if (
            dados.tipo ===
            "material_dourado"
        ) {

            visual.innerHTML = `

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
                            {
                                length:
                                    Number(
                                        dados.dezenas ||
                                        0
                                    )
                            },

                            () => `

                                <div
                                    class="
                                        grid
                                        grid-cols-2
                                        gap-1
                                        rounded-lg
                                        bg-amber-400
                                        p-2
                                    "
                                >

                                    ${
                                        Array.from(
                                            {
                                                length: 10
                                            },

                                            () => `

                                                <span
                                                    class="
                                                        h-3
                                                        w-3
                                                        rounded-sm
                                                        bg-amber-100
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
                            {
                                length:
                                    Number(
                                        dados.unidades ||
                                        0
                                    )
                            },

                            () => `

                                <span
                                    class="
                                        h-7
                                        w-7
                                        rounded-md
                                        bg-amber-400
                                    "
                                ></span>

                            `

                        ).join("")
                    }

                </div>
            `;

            return;
        }


        // =====================================================
        // FORMA GEOMÉTRICA
        // =====================================================

        if (
            dados.tipo ===
            "forma"
        ) {

            visual.innerHTML =
                criarForma(
                    dados.forma
                );

            return;
        }


        // =====================================================
        // FRAÇÃO
        // =====================================================

        if (
            dados.tipo ===
            "fracao"
        ) {

            const numerador =
                Number(
                    dados.numerador
                );

            const denominador =
                Number(
                    dados.denominador
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
                            h-24
                            flex-1
                            border-r
                            border-indigo-200
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


            visual.innerHTML = `

                <div
                    class="
                        mx-auto
                        flex
                        max-w-md
                        overflow-hidden
                        rounded-2xl
                        border-2
                        border-indigo-300
                    "
                >

                    ${partes}

                </div>
            `;

            return;
        }


        // =====================================================
        // RELÓGIO
        // =====================================================

        if (
            dados.tipo ===
            "relogio"
        ) {

            const hora =
                Number(
                    dados.hora
                );

            const minuto =
                Number(
                    dados.minuto
                );


            const anguloMinuto =
                minuto * 6;


            const anguloHora =
                (
                    (hora % 12) *
                    30
                )
                +
                (
                    minuto *
                    0.5
                );


            visual.innerHTML = `

                <div
                    class="
                        relative
                        mx-auto
                        h-56
                        w-56
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
                                translate(
                                    -50%,
                                    -100%
                                )
                                rotate(
                                    ${anguloHora}deg
                                );
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
                                translate(
                                    -50%,
                                    -100%
                                )
                                rotate(
                                    ${anguloMinuto}deg
                                );
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


        // =====================================================
        // GRÁFICO DE BARRAS
        // =====================================================

        if (
            dados.tipo ===
            "grafico_barras"
        ) {

            const valores =
                dados.dados ||
                {};


            const maior =
                Math.max(
                    ...Object.values(
                        valores
                    ),
                    1
                );


            visual.innerHTML = `

                <div
                    class="
                        mx-auto
                        max-w-xl
                        space-y-3
                    "
                >

                    ${
                        Object.entries(
                            valores
                        )
                        .map(
                            ([nome, valor]) => `

                                <div
                                    class="
                                        grid
                                        grid-cols-[90px_1fr_40px]
                                        items-center
                                        gap-3
                                    "
                                >

                                    <span
                                        class="
                                            font-bold
                                        "
                                    >
                                        ${
                                            escapar(
                                                nome
                                            )
                                        }
                                    </span>


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
                                                        Number(
                                                            valor
                                                        )
                                                        /
                                                        maior
                                                    )
                                                    *
                                                    100
                                                }%;
                                            "
                                        ></div>

                                    </div>


                                    <span
                                        class="
                                            font-black
                                        "
                                    >
                                        ${valor}
                                    </span>

                                </div>

                            `
                        )
                        .join("")
                    }

                </div>
            `;

            return;
        }


        // =====================================================
        // DINHEIRO
        // =====================================================

        if (
            dados.tipo ===
            "dinheiro"
        ) {

            visual.innerHTML = `

                <div
                    class="
                        flex
                        flex-wrap
                        justify-center
                        gap-4
                    "
                >

                    ${
                        (
                            dados.valores ||
                            []
                        )
                        .map(
                            valor => `

                                <div
                                    class="
                                        flex
                                        min-w-28
                                        items-center
                                        justify-center
                                        rounded-2xl
                                        border-4
                                        border-emerald-500
                                        bg-emerald-50
                                        px-5
                                        py-5
                                        text-xl
                                        font-black
                                        text-emerald-700
                                        shadow
                                    "
                                >
                                    R$ ${valor}
                                </div>

                            `
                        )
                        .join("")
                    }

                </div>
            `;

            return;
        }


        // =====================================================
        // ÂNGULO
        // =====================================================

        if (
            dados.tipo ===
            "angulo"
        ) {

            const graus =
                Number(
                    dados.graus
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


            visual.innerHTML = `

                <svg
                    viewBox="0 0 220 190"
                    class="mx-auto w-64"
                >

                    <line
                        x1="100"
                        y1="150"
                        x2="190"
                        y2="150"

                        stroke="#1e293b"
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


        // =====================================================
        // RETÂNGULO
        // =====================================================

        if (
            dados.tipo ===
            "retangulo_medidas"
        ) {

            visual.innerHTML = `

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


                    <text
                        x="160"
                        y="25"

                        text-anchor="middle"

                        font-size="18"
                        font-weight="700"
                    >

                        ${dados.largura}

                    </text>


                    <text
                        x="280"
                        y="100"

                        text-anchor="middle"

                        font-size="18"
                        font-weight="700"
                    >

                        ${dados.altura}

                    </text>

                </svg>
            `;

            return;
        }


        // =====================================================
        // PLANO CARTESIANO
        // =====================================================

        if (
            dados.tipo ===
            "plano_cartesiano"
        ) {

            const x =
                Number(
                    dados.x
                );

            const y =
                Number(
                    dados.y
                );


            const px =
                35 +
                x *
                23;


            const py =
                220 -
                y *
                23;


            let linhas = "";


            for (
                let i = 0;
                i <= 8;
                i++
            ) {

                linhas += `

                    <line
                        x1="${
                            35 +
                            i * 23
                        }"

                        y1="25"

                        x2="${
                            35 +
                            i * 23
                        }"

                        y2="220"

                        stroke="#e2e8f0"
                    />


                    <line
                        x1="35"

                        y1="${
                            220 -
                            i * 23
                        }"

                        x2="230"

                        y2="${
                            220 -
                            i * 23
                        }"

                        stroke="#e2e8f0"
                    />

                `;
            }


            visual.innerHTML = `

                <svg
                    viewBox="0 0 260 250"

                    class="
                        mx-auto
                        w-full
                        max-w-sm
                        rounded-2xl
                        bg-white
                    "
                >

                    ${linhas}


                    <line
                        x1="35"
                        y1="220"

                        x2="235"
                        y2="220"

                        stroke="#0f172a"

                        stroke-width="3"
                    />


                    <line
                        x1="35"
                        y1="225"

                        x2="35"
                        y2="20"

                        stroke="#0f172a"

                        stroke-width="3"
                    />


                    <circle
                        cx="${px}"
                        cy="${py}"

                        r="8"

                        fill="#6366f1"
                    />


                    <text
                        x="${px + 10}"
                        y="${py - 10}"

                        font-size="14"

                        font-weight="700"
                    >
                        P
                    </text>

                </svg>
            `;

            return;
        }


        // =====================================================
        // TERMÔMETRO
        // =====================================================

        if (
            dados.tipo ===
            "termometro"
        ) {

            const altura =
                Math.max(
                    25,

                    Math.min(
                        90,

                        Number(
                            dados.valor
                        )
                        *
                        2
                    )
                );


            visual.innerHTML = `

                <div
                    class="
                        mx-auto
                        flex
                        w-fit
                        items-center
                        gap-5
                    "
                >

                    <div
                        class="
                            relative
                            h-52
                            w-12
                            rounded-full
                            border-4
                            border-slate-300
                            bg-white
                        "
                    >

                        <div
                            class="
                                absolute
                                bottom-2
                                left-1/2
                                w-5
                                -translate-x-1/2
                                rounded-full
                                bg-red-500
                            "

                            style="
                                height:
                                ${altura}%;
                            "
                        ></div>

                    </div>


                    <div
                        class="
                            text-4xl
                            font-black
                        "
                    >

                        ${dados.valor}°C

                    </div>

                </div>
            `;

            return;
        }


        // =====================================================
        // VISUAIS SIMPLES
        // =====================================================

        if (
            dados.tipo ===
            "moeda"
        ) {

            visual.innerHTML = `

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


        if (
            dados.tipo ===
            "dado"
        ) {

            visual.innerHTML = `

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


        if (
            dados.tipo ===
            "solido"
        ) {

            const mapa = {

                esfera:
                    "⚪",

                cubo:
                    "🧊",

                cilindro:
                    "🥫"
            };


            visual.innerHTML = `

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


        if (
            dados.tipo ===
            "regua"
        ) {

            visual.innerHTML = `

                <div
                    class="
                        mx-auto
                        max-w-lg
                        rounded-xl
                        bg-yellow-200
                        p-5
                        text-center
                        text-2xl
                        font-black
                    "
                >

                    📏 ${dados.metros} m

                </div>
            `;

            return;
        }


        if (
            dados.tipo ===
            "balanca"
        ) {

            visual.innerHTML = `

                <div
                    class="
                        text-center
                        text-7xl
                    "
                >
                    ⚖️
                </div>


                <div
                    class="
                        mt-3
                        text-center
                        text-2xl
                        font-black
                    "
                >

                    ${dados.kg} kg

                </div>
            `;

            return;
        }


        if (
            dados.tipo ===
            "bloco"
        ) {

            visual.innerHTML = `

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

                    <div
                        class="
                            text-7xl
                        "
                    >
                        🧊
                    </div>


                    <div
                        class="
                            mt-4
                            text-xl
                            font-black
                        "
                    >

                        ${dados.a}
                        ×
                        ${dados.b}
                        ×
                        ${dados.c}

                    </div>

                </div>
            `;
        }
    }


    // =========================================================
    // RESPOSTA NUMÉRICA / TEXTO
    // =========================================================

    function renderizarNumero() {

        respostaArea.innerHTML = `

            <div
                class="
                    mx-auto
                    max-w-md
                "
            >

                <input
                    id="campo-resposta"

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


        const campo =
            document.getElementById(
                "campo-resposta"
            );


        campo.addEventListener(
            "input",

            () => {

                respostaAtual =
                    campo.value;
            }
        );


        campo.addEventListener(
            "keydown",

            event => {

                if (
                    event.key ===
                    "Enter"
                ) {

                    event.preventDefault();

                    enviarResposta();
                }
            }
        );


        setTimeout(
            () => campo.focus(),
            100
        );
    }


    // =========================================================
    // MÚLTIPLA ESCOLHA
    // =========================================================

    function renderizarMultiplaEscolha(
        dados
    ) {

        respostaArea.innerHTML = `

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
                    (
                        dados.alternativas ||
                        []
                    )
                    .map(
                        alternativa => `

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
                                    hover:border-indigo-300
                                    hover:shadow-md
                                "
                            >

                                ${
                                    escapar(
                                        alternativa.texto
                                    )
                                }

                            </button>

                        `
                    )
                    .join("")
                }

            </div>
        `;


        respostaArea
            .querySelectorAll(
                "[data-resposta]"
            )
            .forEach(

                elemento => {

                    elemento.addEventListener(
                        "click",

                        () => {

                            respostaAtual =
                                elemento.dataset
                                    .resposta;


                            respostaArea
                                .querySelectorAll(
                                    "[data-resposta]"
                                )
                                .forEach(

                                    item => {

                                        item.classList.remove(
                                            "border-indigo-500",
                                            "bg-indigo-50",
                                            "ring-4",
                                            "ring-indigo-200"
                                        );
                                    }
                                );


                            elemento.classList.add(
                                "border-indigo-500",
                                "bg-indigo-50",
                                "ring-4",
                                "ring-indigo-200"
                            );
                        }
                    );
                }
            );
    }


    // =========================================================
    // ASSOCIAÇÃO
    // =========================================================

    function renderizarAssociacao(
        dados
    ) {

        respostaArea.innerHTML = `

            <div
                class="
                    mx-auto
                    grid
                    max-w-3xl
                    grid-cols-2
                    gap-5
                "
            >

                <div
                    class="
                        space-y-3
                    "
                >

                    ${
                        (
                            dados.esquerda ||
                            []
                        )
                        .map(
                            item => `

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
                                        text-2xl
                                        font-black
                                    "
                                >

                                    ${
                                        escapar(
                                            item.texto
                                        )
                                    }

                                </button>

                            `
                        )
                        .join("")
                    }

                </div>


                <div
                    class="
                        space-y-3
                    "
                >

                    ${
                        (
                            dados.direita ||
                            []
                        )
                        .map(
                            item => `

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
                                        text-lg
                                        font-black
                                    "
                                >

                                    ${
                                        escapar(
                                            item.texto
                                        )
                                    }

                                </button>

                            `
                        )
                        .join("")
                    }

                </div>

            </div>


            <div
                id="associacao-status"

                class="
                    mt-5
                    text-center
                    font-bold
                    text-slate-500
                "
            ></div>
        `;


        const status =
            document.getElementById(
                "associacao-status"
            );


        respostaArea
            .querySelectorAll(
                "[data-esquerda]"
            )
            .forEach(

                elemento => {

                    elemento.addEventListener(
                        "click",

                        () => {

                            associacaoSelecionada =
                                elemento.dataset
                                    .esquerda;


                            respostaArea
                                .querySelectorAll(
                                    "[data-esquerda]"
                                )
                                .forEach(

                                    item => {

                                        item.classList.remove(
                                            "border-indigo-500",
                                            "bg-indigo-50"
                                        );
                                    }
                                );


                            elemento.classList.add(
                                "border-indigo-500",
                                "bg-indigo-50"
                            );
                        }
                    );
                }
            );


        respostaArea
            .querySelectorAll(
                "[data-direita]"
            )
            .forEach(

                elemento => {

                    elemento.addEventListener(
                        "click",

                        () => {

                            if (
                                !associacaoSelecionada
                            ) {

                                status.textContent =
                                    "Primeiro escolha um item da esquerda.";

                                return;
                            }


                            associacoes[
                                associacaoSelecionada
                            ] =
                                elemento.dataset
                                    .direita;


                            respostaAtual = {
                                ...associacoes
                            };


                            status.textContent =
                                `${
                                    Object.keys(
                                        associacoes
                                    ).length
                                } associação(ões) feita(s).`;


                            associacaoSelecionada =
                                null;
                        }
                    );
                }
            );
    }


    // =========================================================
    // ORDENAÇÃO
    // =========================================================

    function renderizarOrdenacao(
        dados
    ) {

        respostaArea.innerHTML = `

            <div
                class="
                    mx-auto
                    max-w-3xl
                "
            >

                <p
                    class="
                        mb-4
                        text-center
                        font-bold
                        text-slate-500
                    "
                >

                    Toque nos números na ordem correta.

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
                        (
                            dados.itens ||
                            []
                        )
                        .map(
                            item => `

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
                                        px-5
                                        py-4
                                        text-xl
                                        font-black
                                        shadow
                                    "
                                >

                                    ${
                                        escapar(
                                            item.texto
                                        )
                                    }

                                </button>

                            `
                        )
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
                        px-4
                        py-2
                        font-black
                        text-slate-700
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


        respostaArea
            .querySelectorAll(
                "[data-ordem]"
            )
            .forEach(

                elemento => {

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


                            copia.disabled =
                                true;


                            copia.classList.add(
                                "border-indigo-500"
                            );


                            destino.appendChild(
                                copia
                            );


                            elemento.classList.add(
                                "opacity-30"
                            );
                        }
                    );
                }
            );


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


                    respostaArea
                        .querySelectorAll(
                            "[data-ordem]"
                        )
                        .forEach(

                            elemento => {

                                elemento.classList.remove(
                                    "opacity-30"
                                );
                            }
                        );
                }
            );
    }


    // =========================================================
    // RENDERIZAR QUESTÃO
    // =========================================================

    function renderizarQuestao(
        dados
    ) {

        resetarEstado();


        questaoAtual =
            dados;


        pergunta.textContent =
            dados.pergunta ||
            "Resolva o exercício.";


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

            default:

                renderizarNumero();

                break;
        }
    }


    // =========================================================
    // VERIFICAR SE HÁ RESPOSTA
    // =========================================================

    function respostaVazia() {

        if (
            respostaAtual === null ||
            respostaAtual === ""
        ) {

            return true;
        }


        if (
            Array.isArray(
                respostaAtual
            )
        ) {

            return (
                respostaAtual.length ===
                0
            );
        }


        if (
            typeof respostaAtual ===
                "object"
            &&
            respostaAtual !== null
        ) {

            return (
                Object.keys(
                    respostaAtual
                ).length ===
                0
            );
        }


        return false;
    }


    // =========================================================
    // ENVIAR RESPOSTA
    // =========================================================

    async function enviarResposta() {

        if (enviando) {

            return;
        }


        if (
            respostaVazia()
        ) {

            feedback.textContent =
                "Escolha ou digite uma resposta.";

            feedback.className =
                "mt-5 min-h-12 text-center font-black text-orange-500";

            return;
        }


        enviando = true;

        botao.disabled = true;

        botao.textContent =
            "Verificando...";


        try {

            const requisicao =
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
                await requisicao.text();


            let dados;


            try {

                dados =
                    JSON.parse(
                        texto
                    );

            } catch {

                throw new Error(
                    "O servidor retornou uma resposta inválida."
                );
            }


            if (
                !requisicao.ok
            ) {

                throw new Error(
                    dados.erro ||
                    "Erro ao verificar resposta."
                );
            }


            // =================================================
            // FEEDBACK
            // =================================================

            feedback.textContent =
                dados.mensagem ||
                "";


            if (
                dados.correto
            ) {

                feedback.className =
                    "mt-5 min-h-12 text-center font-black text-green-600";

            } else {

                feedback.className =
                    "mt-5 min-h-12 text-center font-black text-red-500";
            }


            // =================================================
            // XP
            // =================================================

            if (
                xp &&
                dados.xp !==
                undefined
            ) {

                xp.textContent =
                    dados.xp;
            }


            // =================================================
            // TERMINOU
            // =================================================

            if (
                dados.terminou
            ) {

                if (barra) {

                    barra.style.width =
                        "100%";
                }


                await esperar(
                    850
                );


                mostrarResultado(
                    dados
                );

                return;
            }


            // =================================================
            // PROGRESSO
            // =================================================

            const respondidas =
                Number(
                    dados.respondidas ||
                    0
                );


            const quantidade =
                Number(
                    dados.quantidade ||
                    1
                );


            const porcentagem =
                Math.min(
                    100,

                    Math.round(
                        (
                            respondidas /
                            quantidade
                        )
                        *
                        100
                    )
                );


            if (barra) {

                barra.style.width =
                    `${porcentagem}%`;
            }


            if (
                textoProgresso
            ) {

                textoProgresso.textContent =
                    `${respondidas}/${quantidade}`;
            }


            await esperar(
                850
            );


            // =================================================
            // PRÓXIMA QUESTÃO
            // =================================================

            renderizarQuestao(
                dados.questao
            );

        }

        catch (erro) {

            console.error(
                erro
            );


            feedback.textContent =
                erro.message;


            feedback.className =
                "mt-5 min-h-12 text-center font-black text-red-500";

        }

        finally {

            enviando = false;


            if (
                document.body.contains(
                    botao
                )
            ) {

                botao.disabled =
                    false;

                botao.textContent =
                    "Conferir";
            }
        }
    }


    // =========================================================
    // ESPERA
    // =========================================================

    function esperar(
        tempo
    ) {

        return new Promise(
            resolve => {

                setTimeout(
                    resolve,
                    tempo
                );
            }
        );
    }


    // =========================================================
    // RESULTADO DA ETAPA
    // =========================================================

    function mostrarResultado(
        dados
    ) {

        const passou =
            Boolean(
                dados.passou
            );


        app.innerHTML = `

            <div
                class="
                    mx-auto
                    max-w-xl
                    py-10
                    text-center
                "
            >

                <div
                    class="
                        text-7xl
                    "
                >

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
                        : "Quase lá!"
                    }

                </h1>


                <p
                    class="
                        mt-4
                        text-lg
                        text-slate-500
                    "
                >

                    Você acertou

                    <strong>
                        ${dados.acertos}
                    </strong>

                    de

                    <strong>
                        ${dados.quantidade}
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

                    ${dados.pontuacao}%

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

                        ? "A próxima etapa foi liberada."

                        : "Você precisa atingir 80% para avançar."
                    }

                </p>


                ${
                    dados.assunto_concluido

                    ? `

                        <div
                            class="
                                mt-6
                                rounded-2xl
                                border
                                border-yellow-300
                                bg-yellow-100
                                p-4
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
                        type="button"

                        onclick="
                            location.reload()
                        "

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
                        type="button"

                        onclick="
                            history.back()
                        "

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
    }


    // =========================================================
    // BOTÃO
    // =========================================================

    botao.addEventListener(
        "click",
        enviarResposta
    );


    // =========================================================
    // INICIAR
    // =========================================================

    renderizarQuestao(
        questaoAtual
    );

});