const input = document.getElementById("resposta");

let bloqueado = false;


input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        responder();
    }

});


async function responder() {

    if (bloqueado) {
        return;
    }


    const valor = input.value.trim();


    if (valor === "") {

        mostrarFeedback(
            "Digite uma resposta ",
            "text-orange-500"
        );

        return;
    }


    bloqueado = true;


    try {

        const response = await fetch(
            "/api/responder",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    resposta: valor
                })
            }
        );


        const dados = await response.json();


        if (!response.ok) {

            mostrarFeedback(
                dados.erro || "Ocorreu um erro.",
                "text-red-500"
            );

            bloqueado = false;

            return;
        }


        if (dados.correto) {

            mostrarFeedback(
                `${dados.mensagem}
                +${dados.xp_ganho} XP
                ⭐`,
                "text-green-500"
            );

        } else {

            mostrarFeedback(
                dados.mensagem,
                "text-red-500"
            );

        }


        atualizarStatus(dados);


        setTimeout(() => {

            atualizarQuestao(
                dados.questao
            );

            input.value = "";

            input.focus();

            mostrarFeedback("", "");

            bloqueado = false;

        }, 1200);


    } catch (erro) {

        console.error(erro);

        mostrarFeedback(
            "Não foi possível enviar a resposta.",
            "text-red-500"
        );

        bloqueado = false;
    }

}


function atualizarQuestao(questao) {

    document.getElementById(
        "tituloQuestao"
    ).innerText = questao.titulo;

    document.getElementById(
        "pergunta"
    ).innerText = questao.pergunta;

}

function atualizarStatus(dados) {

    document.getElementById("xp").innerText =
        dados.xp;

    document.getElementById("nivel").innerText =
        dados.nivel;

    document.getElementById("moedas").innerText =
        dados.moedas;

    document.getElementById("sequencia").innerText =
        "🔥 " + dados.sequencia;

}


function mostrarFeedback(texto, classe) {

    const feedback =
        document.getElementById("feedback");

    feedback.className =
        "min-h-[70px] mt-6 text-xl font-black " +
        classe;

    feedback.innerText = texto;

}