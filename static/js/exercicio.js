document.addEventListener(
    "DOMContentLoaded",
    () => {

        const input =
            document.getElementById(
                "resposta"
            );

        const botao =
            document.getElementById(
                "botaoResponder"
            );

        const feedback =
            document.getElementById(
                "feedback"
            );


        if (!input || !botao) {
            return;
        }


        let bloqueado = false;


        botao.addEventListener(
            "click",
            enviarResposta
        );


        input.addEventListener(
            "keydown",
            (evento) => {

                if (
                    evento.key === "Enter"
                ) {

                    evento.preventDefault();

                    enviarResposta();
                }
            }
        );


        async function enviarResposta() {

            if (bloqueado) {
                return;
            }


            const resposta =
                input.value.trim();


            if (!resposta) {

                mostrarMensagem(
                    "Digite uma resposta 😊",
                    "text-orange-500"
                );

                return;
            }


            bloqueado = true;

            botao.disabled = true;

            botao.innerText =
                "Verificando...";


            try {

                const respostaServidor =
                    await fetch(
                        "/api/responder",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    resposta: resposta
                                })
                        }
                    );


                const texto =
                    await respostaServidor.text();


                let dados;


                try {

                    dados =
                        JSON.parse(texto);

                } catch {

                    console.error(
                        "Resposta recebida:",
                        texto
                    );

                    mostrarMensagem(
                        "O servidor retornou uma resposta inválida.",
                        "text-red-500"
                    );

                    liberar();

                    return;
                }


                if (
                    !respostaServidor.ok
                ) {

                    mostrarMensagem(
                        dados.erro ||
                        "Erro no servidor.",
                        "text-red-500"
                    );

                    liberar();

                    return;
                }


                if (dados.correto) {

                    mostrarMensagem(
                        dados.mensagem,
                        "text-green-600"
                    );

                } else {

                    mostrarMensagem(
                        dados.mensagem,
                        "text-red-500"
                    );
                }


                atualizar(
                    "xp",
                    dados.xp
                );

                atualizar(
                    "moedas",
                    dados.moedas
                );

                atualizar(
                    "dominio",
                    dados.dominio + "%"
                );


                setTimeout(
                    () => {

                        atualizar(
                            "pergunta",
                            dados.questao.pergunta
                        );

                        input.value = "";

                        input.focus();

                        mostrarMensagem(
                            "",
                            ""
                        );

                        liberar();

                    },
                    1500
                );


            } catch (erro) {

                console.error(
                    erro
                );

                mostrarMensagem(
                    "Não foi possível acessar o servidor.",
                    "text-red-500"
                );

                liberar();
            }
        }


        function atualizar(
            id,
            valor
        ) {

            const elemento =
                document.getElementById(
                    id
                );


            if (elemento) {

                elemento.innerText =
                    valor;
            }
        }


        function mostrarMensagem(
            texto,
            classe
        ) {

            if (!feedback) {
                return;
            }


            feedback.className =
                "min-h-16 mt-6 text-xl font-black " +
                classe;


            feedback.innerText =
                texto;
        }


        function liberar() {

            bloqueado = false;

            botao.disabled = false;

            botao.innerText =
                "Conferir 🚀";
        }
    }
);