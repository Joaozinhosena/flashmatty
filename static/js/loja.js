(() => {

    "use strict";


    // ========================================================
    // EVITA DUPLICIDADE
    // ========================================================

    if (
        window.__flashMattyLojaCarregada
    ) {

        return;

    }


    window.__flashMattyLojaCarregada =
        true;


    document.addEventListener(
        "DOMContentLoaded",
        () => {


            // =================================================
            // FILTROS
            // =================================================

            const botoes = [

                ...document
                    .querySelectorAll(
                        "[data-store-filter]"
                    )

            ];


            const secoes = [

                ...document
                    .querySelectorAll(
                        "[data-store-section]"
                    )

            ];


            botoes.forEach(
                botao => {

                    botao.addEventListener(
                        "click",
                        () => {

                            const filtro =
                                botao.dataset
                                    .storeFilter
                                ||
                                "todos";


                            botoes.forEach(
                                outro => {

                                    outro.dataset.active =
                                        (
                                            outro
                                                ===
                                            botao
                                        )
                                        ?
                                        "1"
                                        :
                                        "0";

                                }
                            );


                            secoes.forEach(
                                secao => {

                                    const mostrar =
                                        (
                                            filtro
                                            ===
                                            "todos"
                                        )
                                        ||
                                        (
                                            secao
                                                .dataset
                                                .storeSection
                                            ===
                                            filtro
                                        );


                                    secao.hidden =
                                        !mostrar;

                                }
                            );

                        }
                    );

                }
            );


            // =================================================
            // CONFIRMAÇÃO DE COMPRA
            // =================================================

            document
                .querySelectorAll(
                    "[data-store-purchase]"
                )
                .forEach(
                    formulario => {

                        formulario
                            .addEventListener(
                                "submit",
                                evento => {

                                    const nome =
                                        formulario
                                            .dataset
                                            .itemName
                                        ||
                                        "este item";


                                    const preco =
                                        formulario
                                            .dataset
                                            .itemPrice
                                        ||
                                        "?";


                                    const confirmar =
                                        window.confirm(
                                            (
                                                `Comprar ${nome} `
                                                +
                                                `por ${preco} moedas?`
                                            )
                                        );


                                    if (!confirmar) {

                                        evento
                                            .preventDefault();

                                    }

                                }
                            );

                    }
                );

        }
    );

})();
