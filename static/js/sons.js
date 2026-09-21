// ============================================================
// FLASHMATTY - SISTEMA GLOBAL DE SONS
// ============================================================

let contextoAudio = null;
let audioAtivo = false;


// ============================================================
// CRIAR / LIBERAR AUDIOCONTEXT
// ============================================================

async function ativarAudio() {

    try {

        if (!contextoAudio) {

            const AudioContext =
                window.AudioContext ||
                window.webkitAudioContext;


            if (!AudioContext) {

                console.warn(
                    "Web Audio API não suportada."
                );

                return false;
            }


            contextoAudio =
                new AudioContext();
        }


        if (
            contextoAudio.state ===
            "suspended"
        ) {

            await contextoAudio.resume();
        }


        audioAtivo = true;

        return true;

    } catch (erro) {

        console.warn(
            "Erro ao ativar áudio:",
            erro
        );

        return false;
    }
}


// ============================================================
// PRIMEIRA INTERAÇÃO DO USUÁRIO
// ============================================================

document.addEventListener(
    "pointerdown",
    async () => {

        if (!audioAtivo) {

            await ativarAudio();
        }
    },
    {
        passive: true
    }
);


// ============================================================
// GERAR UM TOM
// ============================================================

async function tocarTom({
    frequencia = 440,
    duracao = 0.08,
    volume = 0.05,
    tipo = "sine",
    atraso = 0
} = {}) {

    const liberado =
        await ativarAudio();


    if (
        !liberado ||
        !contextoAudio
    ) {

        return;
    }


    const oscilador =
        contextoAudio.createOscillator();


    const ganho =
        contextoAudio.createGain();


    const inicio =
        contextoAudio.currentTime +
        atraso;


    const fim =
        inicio +
        duracao;


    oscilador.type =
        tipo;


    oscilador.frequency.setValueAtTime(
        frequencia,
        inicio
    );


    ganho.gain.setValueAtTime(
        0.0001,
        inicio
    );


    ganho.gain.exponentialRampToValueAtTime(
        volume,
        inicio + 0.01
    );


    ganho.gain.exponentialRampToValueAtTime(
        0.0001,
        fim
    );


    oscilador.connect(
        ganho
    );


    ganho.connect(
        contextoAudio.destination
    );


    oscilador.start(
        inicio
    );


    oscilador.stop(
        fim + 0.03
    );
}


// ============================================================
// CLIQUE
// ============================================================

function somClique() {

    tocarTom({
        frequencia: 430,
        duracao: 0.045,
        volume: 0.04,
        tipo: "sine"
    });


    tocarTom({
        frequencia: 620,
        duracao: 0.045,
        volume: 0.035,
        tipo: "sine",
        atraso: 0.035
    });
}


// ============================================================
// SELEÇÃO
// ============================================================

function somSelecao() {

    tocarTom({
        frequencia: 650,
        duracao: 0.07,
        volume: 0.05
    });


    tocarTom({
        frequencia: 780,
        duracao: 0.06,
        volume: 0.04,
        atraso: 0.055
    });
}


// ============================================================
// ACERTO
// ============================================================

function somAcerto() {

    tocarTom({
        frequencia: 523.25,
        duracao: 0.10,
        volume: 0.08,
        atraso: 0
    });


    tocarTom({
        frequencia: 659.25,
        duracao: 0.10,
        volume: 0.08,
        atraso: 0.09
    });


    tocarTom({
        frequencia: 783.99,
        duracao: 0.18,
        volume: 0.09,
        atraso: 0.18
    });
}


// ============================================================
// ERRO
// ============================================================

function somErro() {

    tocarTom({
        frequencia: 240,
        duracao: 0.13,
        volume: 0.055,
        tipo: "square"
    });


    tocarTom({
        frequencia: 175,
        duracao: 0.18,
        volume: 0.045,
        tipo: "square",
        atraso: 0.12
    });
}


// ============================================================
// MOEDA
// ============================================================

function somMoeda() {

    tocarTom({
        frequencia: 950,
        duracao: 0.06,
        volume: 0.06
    });


    tocarTom({
        frequencia: 1350,
        duracao: 0.10,
        volume: 0.065,
        atraso: 0.055
    });
}


// ============================================================
// ETAPA CONCLUÍDA
// ============================================================

function somConcluido() {

    const notas = [
        523.25,
        659.25,
        783.99,
        1046.50
    ];


    notas.forEach(
        (nota, indice) => {

            tocarTom({
                frequencia: nota,

                duracao:
                    indice === 3
                        ? 0.35
                        : 0.12,

                volume: 0.085,

                atraso:
                    indice * 0.11
            });
        }
    );
}


// ============================================================
// TENTAR NOVAMENTE
// ============================================================

function somTentarNovamente() {

    tocarTom({
        frequencia: 392,
        duracao: 0.10,
        volume: 0.05
    });


    tocarTom({
        frequencia: 330,
        duracao: 0.12,
        volume: 0.05,
        atraso: 0.1
    });


    tocarTom({
        frequencia: 294,
        duracao: 0.18,
        volume: 0.05,
        atraso: 0.21
    });
}


// ============================================================
// NAVEGAÇÃO GLOBAL
// ============================================================

document.addEventListener(
    "click",
    async event => {

        const elemento =
            event.target.closest(
                "a, button"
            );


        if (!elemento) {

            return;
        }


        // Elemento pode pedir silêncio.
        if (
            elemento.dataset.semSom ===
            "true"
        ) {

            return;
        }


        // O botão de conferir já possui
        // efeitos próprios no exercicio.js.
        if (
            elemento.id ===
            "botaoResponder"
        ) {

            return;
        }


        await ativarAudio();


        // ====================================================
        // LINKS
        // ====================================================

        if (
            elemento.tagName === "A"
        ) {

            const href =
                elemento.getAttribute(
                    "href"
                );


            if (
                !href ||
                href === "#" ||
                href.startsWith(
                    "javascript:"
                )
            ) {

                somClique();

                return;
            }


            // Não interfere em Ctrl+Clique,
            // Shift+Clique etc.
            if (
                event.ctrlKey ||
                event.metaKey ||
                event.shiftKey ||
                event.altKey
            ) {

                somClique();

                return;
            }


            // Downloads / nova aba
            if (
                elemento.hasAttribute(
                    "download"
                ) ||
                elemento.target === "_blank"
            ) {

                somClique();

                return;
            }


            // Impede a navegação por alguns
            // milissegundos para o som tocar.
            event.preventDefault();


            somClique();


            setTimeout(
                () => {

                    window.location.href =
                        elemento.href;

                },
                100
            );


            return;
        }


        // ====================================================
        // BOTÕES NORMAIS
        // ====================================================

        somClique();

    }
);


// ============================================================
// DEBUG
// ============================================================

console.log(
    " Sistema de sons FlashMatty carregado."
);