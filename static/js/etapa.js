document.addEventListener("DOMContentLoaded", () => {

    const jogo =
        document.getElementById("jogo");

    const pergunta =
        document.getElementById("pergunta");

    const resposta =
        document.getElementById("resposta");

    const botao =
        document.getElementById("botaoResponder");

    const feedback =
        document.getElementById("feedback");

    const barra =
        document.getElementById("barraProgresso");

    const xp =
        document.getElementById("xp");


    if (
        !jogo ||
        !pergunta ||
        !resposta ||
        !botao
    ) {
        return;
    }


    let enviando = false;


    async function responder() {

        if (enviando) {
            return;
        }


        const valor =
            resposta.value.trim();


        if (!valor) {

            feedback.textContent =
                "Digite uma resposta.";

            feedback.className =
                "mt-5 min-h-12 font-black text-red-500";

            resposta.focus();

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
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            resposta: valor
                        })
                    }
                );


            const texto =
                await requisicao.text();


            let dados;


            try {

                dados =
                    JSON.parse(texto);

            } catch {

                throw new Error(
                    "O servidor retornou uma resposta inválida."
                );
            }


            if (!requisicao.ok) {

                throw new Error(
                    dados.erro ||
                    "Erro ao verificar resposta."
                );
            }


            // ================================================
            // FEEDBACK
            // ================================================

            feedback.textContent =
                dados.mensagem;


            if (dados.correto) {

                feedback.className =
                    "mt-5 min-h-12 font-black text-green-600";

            } else {

                feedback.className =
                    "mt-5 min-h-12 font-black text-red-500";
            }


            // ================================================
            // XP
            // ================================================

            if (xp) {

                xp.textContent =
                    dados.xp;
            }


            // ================================================
            // TERMINOU ETAPA
            // ================================================

            if (dados.terminou) {

                barra.style.width =
                    "100%";


                await new Promise(
                    resolve =>
                        setTimeout(
                            resolve,
                            1000
                        )
                );


                jogo.innerHTML = `
                    <div class="text-center py-10">

                        <div class="text-7xl mb-6">
                            ${
                                dados.passou
                                ? "🏆"
                                : "💪"
                            }
                        </div>

                        <h1 class="text-3xl font-black">

                            ${
                                dados.passou
                                ? "Etapa concluída!"
                                : "Quase lá!"
                            }

                        </h1>

                        <p class="text-slate-500 mt-3">

                            Você acertou
                            ${dados.acertos}
                            de
                            ${dados.quantidade}
                            questões.

                        </p>

                        <div
                            class="
                            text-5xl
                            font-black
                            mt-6
                            ${
                                dados.passou
                                ? "text-green-600"
                                : "text-orange-500"
                            }
                            "
                        >
                            ${dados.pontuacao}%
                        </div>

                        <p class="mt-4 text-slate-500">

                            ${
                                dados.passou
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
                                    bg-yellow-100
                                    border
                                    border-yellow-300
                                    rounded-2xl
                                    p-4
                                    font-black
                                    "
                                >
                                    🏆 Assunto completamente concluído!
                                </div>
                            `

                            : ""
                        }

                        <a
                            href="${jogo.dataset.voltar}"
                            class="
                            block
                            mt-8
                            bg-indigo-600
                            text-white
                            rounded-2xl
                            p-4
                            font-black
                            "
                        >
                            Voltar para a trilha
                        </a>

                    </div>
                `;

                return;
            }


            // ================================================
            // PROGRESSO
            // ================================================

            const porcentagem =
                (
                    dados.respondidas /
                    dados.quantidade
                )
                * 100;


            barra.style.width =
                `${porcentagem}%`;


            // ================================================
            // ESPERAR FEEDBACK
            // ================================================

            await new Promise(
                resolve =>
                    setTimeout(
                        resolve,
                        900
                    )
            );


            // ================================================
            // PRÓXIMA QUESTÃO
            // ================================================

            pergunta.textContent =
                dados.questao.pergunta;


            resposta.value = "";

            resposta.focus();


            feedback.textContent = "";

        }

        catch (erro) {

            feedback.textContent =
                erro.message;

            feedback.className =
                "mt-5 min-h-12 font-black text-red-500";
        }

        finally {

            enviando = false;

            botao.disabled = false;

            botao.textContent =
                "Conferir";
        }
    }


    botao.addEventListener(
        "click",
        responder
    );


    resposta.addEventListener(
        "keydown",
        event => {

            if (event.key === "Enter") {

                event.preventDefault();

                responder();
            }
        }
    );


    resposta.focus();

});