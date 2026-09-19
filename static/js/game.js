// ============================================================
// GAME.JS
// ============================================================
//
// Arquivo auxiliar do sistema de exercícios.
//
// IMPORTANTE:
// A lógica principal das atividades agora fica em:
//
// static/js/exercicio.js
//
// Este arquivo NÃO deve:
// - enviar /api/responder
// - controlar o botão Conferir
// - criar listener no campo #resposta
// - trocar questões
//
// Isso evita conflito com o sistema dinâmico.
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "game.js carregado"
        );


        // ====================================================
        // VERIFICAR SE É A NOVA TELA DE EXERCÍCIOS
        // ====================================================

        const exercicioApp =
            document.getElementById(
                "exercicio-app"
            );


        if (exercicioApp) {

            console.log(
                "Sistema dinâmico detectado. " +
                "O controle da atividade será feito por exercicio.js."
            );

            return;
        }


        // ====================================================
        // OUTRAS PÁGINAS
        // ====================================================
        //
        // Se no futuro game.js for utilizado em outra tela,
        // o código específico poderá ser colocado aqui.
        //
        // ====================================================

    }
);


// ============================================================
// FUNÇÕES AUXILIARES GERAIS
// ============================================================

function atualizarElemento(
    id,
    valor
) {

    const elemento =
        document.getElementById(
            id
        );


    if (!elemento) {

        return;
    }


    elemento.textContent =
        valor ?? "";
}


// ============================================================
// XP
// ============================================================

function atualizarXP(
    valor
) {

    atualizarElemento(
        "xp-atual",
        valor
    );


    // Compatibilidade com páginas antigas
    atualizarElemento(
        "xp",
        valor
    );
}


// ============================================================
// MOEDAS
// ============================================================

function atualizarMoedas(
    valor
) {

    atualizarElemento(
        "moedas",
        valor
    );
}


// ============================================================
// PROGRESSO
// ============================================================

function atualizarBarraProgresso(
    respondidas,
    quantidade
) {

    const barra =
        document.getElementById(
            "barra-progresso"
        );


    const texto =
        document.getElementById(
            "texto-progresso"
        );


    const respondidasNumero =
        Number(
            respondidas || 0
        );


    const quantidadeNumero =
        Math.max(
            1,
            Number(
                quantidade || 1
            )
        );


    const percentual =
        Math.min(
            100,
            Math.round(
                (
                    respondidasNumero /
                    quantidadeNumero
                ) *
                100
            )
        );


    if (barra) {

        barra.style.width =
            `${percentual}%`;
    }


    if (texto) {

        texto.textContent =
            `${respondidasNumero}/${quantidadeNumero}`;
    }
}


// ============================================================
// FEEDBACK GENÉRICO
// ============================================================

function mostrarFeedbackGlobal(
    mensagem,
    tipo = ""
) {

    const feedback =
        document.getElementById(
            "feedback"
        );


    if (!feedback) {

        return;
    }


    feedback.textContent =
        mensagem || "";


    feedback.className =
        "mt-5 min-h-10 text-center text-lg font-black";


    switch (tipo) {

        case "sucesso":

            feedback.classList.add(
                "text-green-600"
            );

            break;


        case "erro":

            feedback.classList.add(
                "text-red-500"
            );

            break;


        case "aviso":

            feedback.classList.add(
                "text-orange-500"
            );

            break;


        default:

            feedback.classList.add(
                "text-slate-500"
            );

            break;
    }
}