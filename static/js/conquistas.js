(() => {

    "use strict";


    if (
        window.__flashMattyConquistas
    ) {

        return;

    }


    window.__flashMattyConquistas =
        true;


    function iniciar() {

        const modal =
            document.getElementById(
                "conquistaModal"
            );


        if (!modal) {
            return;
        }


        const imagem =
            document.getElementById(
                "conquistaModalImagem"
            );

        const categoria =
            document.getElementById(
                "conquistaModalCategoria"
            );

        const nome =
            document.getElementById(
                "conquistaModalNome"
            );

        const curta =
            document.getElementById(
                "conquistaModalCurta"
            );

        const biografia =
            document.getElementById(
                "conquistaModalBiografia"
            );

        const status =
            document.getElementById(
                "conquistaModalStatus"
            );

        const progresso =
            document.getElementById(
                "conquistaModalProgresso"
            );

        const data =
            document.getElementById(
                "conquistaModalData"
            );


        let focoAnterior =
            null;


        function abrir(
            botao
        ) {

            focoAnterior =
                document.activeElement;


            imagem.src =
                botao.dataset
                    .conquistaImagem
                ||
                "";


            imagem.alt =
                botao.dataset
                    .conquistaNome
                ||
                "Conquista";


            categoria.textContent =
                botao.dataset
                    .conquistaCategoria
                ||
                "Conquista";


            nome.textContent =
                botao.dataset
                    .conquistaNome
                ||
                "Conquista";


            curta.textContent =
                botao.dataset
                    .conquistaCurta
                ||
                "";


            biografia.textContent =
                botao.dataset
                    .conquistaBiografia
                ||
                "";


            const desbloqueada =
                (
                    botao.dataset
                        .conquistaStatus
                    ===
                    "Desbloqueada"
                );


            status.textContent =
                desbloqueada
                    ?
                    "✓ Desbloqueada"
                    :
                    "🔒 Bloqueada";


            status.className =
                desbloqueada
                    ?
                    "block mt-1 text-emerald-300"
                    :
                    "block mt-1 text-slate-400";


            progresso.textContent =
                botao.dataset
                    .conquistaProgresso
                ||
                "";


            const dataValor =
                botao.dataset
                    .conquistaData
                ||
                "";


            data.textContent =
                dataValor
                    ?
                    `Conquistada em ${dataValor}`
                    :
                    "";


            modal.classList.remove(
                "hidden"
            );


            modal.classList.add(
                "flex"
            );


            modal.setAttribute(
                "aria-hidden",
                "false"
            );


            document.body.classList.add(
                "overflow-hidden"
            );


            const fechar =
                modal.querySelector(
                    "[data-conquista-close]"
                );


            fechar?.focus();

        }


        function fechar() {

            modal.classList.add(
                "hidden"
            );


            modal.classList.remove(
                "flex"
            );


            modal.setAttribute(
                "aria-hidden",
                "true"
            );


            document.body.classList.remove(
                "overflow-hidden"
            );


            if (
                focoAnterior
                &&
                typeof focoAnterior.focus
                ===
                "function"
            ) {

                focoAnterior.focus();

            }

        }


        document
            .querySelectorAll(
                "[data-conquista-open]"
            )
            .forEach(
                botao => {

                    botao.addEventListener(
                        "click",
                        () => {

                            abrir(
                                botao
                            );

                        }
                    );

                }
            );


        modal
            .querySelectorAll(
                "[data-conquista-close], [data-conquista-backdrop]"
            )
            .forEach(
                elemento => {

                    elemento.addEventListener(
                        "click",
                        fechar
                    );

                }
            );


        document.addEventListener(
            "keydown",
            evento => {

                if (
                    evento.key
                    ===
                    "Escape"
                    &&
                    modal.getAttribute(
                        "aria-hidden"
                    )
                    ===
                    "false"
                ) {

                    fechar();

                }

            }
        );

    }


    if (
        document.readyState
        ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            iniciar,
            {
                once:
                    true
            }
        );

    } else {

        iniciar();

    }

})();
