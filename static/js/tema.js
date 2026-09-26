// ============================================================
// FLASHMATTY - SISTEMA GLOBAL DE TEMAS
// ============================================================

(function () {

    const TEMAS = {

        dark: {
            primaria: "#6366f1",
            fundo: "#0f172a",
            card: "#1e293b",
            superficie: "#334155",
            texto: "#f8fafc",
            secundario: "#94a3b8",
            borda: "#334155"
        },

        light: {
            primaria: "#4f46e5",
            fundo: "#f8fafc",
            card: "#ffffff",
            superficie: "#f1f5f9",
            texto: "#0f172a",
            secundario: "#64748b",
            borda: "#e2e8f0"
        }

    };


    // ========================================================
    // COR PERSONALIZADA
    // ========================================================

    function obterPersonalizado() {

        return {

            primaria:
                localStorage.getItem(
                    "flashmatty_cor_primaria"
                ) || "#8b5cf6",

            fundo:
                localStorage.getItem(
                    "flashmatty_cor_fundo"
                ) || "#111827",

            card:
                localStorage.getItem(
                    "flashmatty_cor_card"
                ) || "#1f2937",

            superficie:
                localStorage.getItem(
                    "flashmatty_cor_superficie"
                ) || "#374151",

            texto:
                localStorage.getItem(
                    "flashmatty_cor_texto"
                ) || "#f9fafb",

            secundario:
                localStorage.getItem(
                    "flashmatty_cor_secundaria"
                ) || "#9ca3af",

            borda:
                localStorage.getItem(
                    "flashmatty_cor_borda"
                ) || "#374151"

        };

    }


    // ========================================================
    // LUMINOSIDADE
    // ========================================================

    function corEhEscura(hex) {

        if (
            typeof hex !== "string"
            ||
            !/^#[0-9a-f]{6}$/i.test(hex)
        ) {
            return true;
        }


        const r =
            parseInt(
                hex.slice(1, 3),
                16
            );

        const g =
            parseInt(
                hex.slice(3, 5),
                16
            );

        const b =
            parseInt(
                hex.slice(5, 7),
                16
            );


        const luminancia =
            (
                r * 299
                +
                g * 587
                +
                b * 114
            )
            /
            1000;


        return luminancia < 128;

    }


    // ========================================================
    // APLICAR CORES
    // ========================================================

    function aplicarCores(
        cores
    ) {

        const raiz =
            document.documentElement;


        raiz.style.setProperty(
            "--fm-primary",
            cores.primaria
        );

        raiz.style.setProperty(
            "--fm-bg",
            cores.fundo
        );

        raiz.style.setProperty(
            "--fm-card",
            cores.card
        );

        raiz.style.setProperty(
            "--fm-surface",
            cores.superficie
        );

        raiz.style.setProperty(
            "--fm-text",
            cores.texto
        );

        raiz.style.setProperty(
            "--fm-muted",
            cores.secundario
        );

        raiz.style.setProperty(
            "--fm-border",
            cores.borda
        );


        raiz.style.colorScheme =
            corEhEscura(
                cores.fundo
            )
                ? "dark"
                : "light";

    }


    // ========================================================
    // APLICAR TEMA
    // ========================================================

    function aplicarTema(
        nome
    ) {

        if (
            ![
                "dark",
                "light",
                "custom"
            ].includes(nome)
        ) {

            nome = "dark";

        }


        let cores;


        if (
            nome === "custom"
        ) {

            cores =
                obterPersonalizado();

        } else {

            cores =
                TEMAS[nome];

        }


        document.documentElement.dataset.theme =
            nome;


        aplicarCores(
            cores
        );


        localStorage.setItem(
            "flashmatty_tema",
            nome
        );


        window.dispatchEvent(
            new CustomEvent(
                "flashmatty:tema-alterado",
                {
                    detail: {
                        tema: nome,
                        cores: cores
                    }
                }
            )
        );

    }


    // ========================================================
    // SALVAR PERSONALIZADO
    // ========================================================

    function salvarPersonalizado(
        cores
    ) {

        const mapa = {

            primaria:
                "flashmatty_cor_primaria",

            fundo:
                "flashmatty_cor_fundo",

            card:
                "flashmatty_cor_card",

            superficie:
                "flashmatty_cor_superficie",

            texto:
                "flashmatty_cor_texto",

            secundario:
                "flashmatty_cor_secundaria",

            borda:
                "flashmatty_cor_borda"

        };


        Object.entries(
            mapa
        ).forEach(
            ([chave, armazenamento]) => {

                if (
                    cores[chave]
                ) {

                    localStorage.setItem(
                        armazenamento,
                        cores[chave]
                    );

                }

            }
        );


        aplicarTema(
            "custom"
        );

    }


    // ========================================================
    // RESTAURAR PERSONALIZADO
    // ========================================================

    function restaurarPersonalizado() {

        const padrao = {
            primaria: "#8b5cf6",
            fundo: "#111827",
            card: "#1f2937",
            superficie: "#374151",
            texto: "#f9fafb",
            secundario: "#9ca3af",
            borda: "#374151"
        };


        salvarPersonalizado(
            padrao
        );


        return padrao;

    }


    // ========================================================
    // API GLOBAL
    // ========================================================

    window.FlashMattyTema = {

        aplicar:
            aplicarTema,

        salvarPersonalizado:
            salvarPersonalizado,

        obterPersonalizado:
            obterPersonalizado,

        restaurarPersonalizado:
            restaurarPersonalizado,

        get atual() {

            return (
                localStorage.getItem(
                    "flashmatty_tema"
                )
                ||
                "dark"
            );

        }

    };


    // ========================================================
    // APLICAR IMEDIATAMENTE
    // ========================================================

    aplicarTema(

        localStorage.getItem(
            "flashmatty_tema"
        )
        ||
        "dark"

    );

})();