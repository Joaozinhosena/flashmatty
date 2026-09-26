// ============================================================
// FLASHMATTY - SISTEMA GLOBAL DE SONS
// ============================================================

let contextoAudio = null;
let audioAtivo = false;


// ============================================================
// CONFIGURAÇÕES
// ============================================================

function sonsAtivados() {

    // Usa a configuração global criada no base.html
    if (
        window.FlashMattyConfig
        &&
        typeof window.FlashMattyConfig.sonsAtivados !== "undefined"
    ) {

        return Boolean(
            window.FlashMattyConfig.sonsAtivados
        );

    }


    // Fallback caso o objeto global não exista
    return (
        localStorage.getItem(
            "flashmatty_sons"
        )
        !==
        "false"
    );

}


function obterVolume() {

    let volume = 70;


    if (
        window.FlashMattyConfig
        &&
        typeof window.FlashMattyConfig.volume !== "undefined"
    ) {

        volume = Number(
            window.FlashMattyConfig.volume
        );

    } else {

        volume = Number(
            localStorage.getItem(
                "flashmatty_volume"
            )
            ??
            70
        );

    }


    if (
        !Number.isFinite(
            volume
        )
    ) {

        volume = 70;

    }


    return Math.max(
        0,
        Math.min(
            100,
            volume
        )
    );

}


function obterVolumeNormalizado() {

    return (
        obterVolume()
        /
        100
    );

}


function audioPermitido() {

    return (
        sonsAtivados()
        &&
        obterVolume() > 0
    );

}


// ============================================================
// CRIAR / LIBERAR AUDIOCONTEXT
// ============================================================

async function ativarAudio() {

    /*
    Se o usuário desligou o áudio,
    não há necessidade de criar AudioContext.
    */

    if (
        !audioPermitido()
    ) {

        return false;

    }


    try {

        if (!contextoAudio) {

            const AudioContext =
                window.AudioContext
                ||
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
            contextoAudio.state
            ===
            "suspended"
        ) {

            await contextoAudio.resume();

        }


        if (
            contextoAudio.state
            ===
            "closed"
        ) {

            contextoAudio = null;
            audioAtivo = false;

            return ativarAudio();

        }


        audioAtivo = true;

        return true;

    } catch (erro) {

        console.warn(
            "Erro ao ativar áudio:",
            erro
        );

        audioAtivo = false;

        return false;

    }

}


// ============================================================
// PRIMEIRA INTERAÇÃO DO USUÁRIO
// ============================================================

document.addEventListener(
    "pointerdown",
    async () => {

        if (
            !audioAtivo
            &&
            audioPermitido()
        ) {

            await ativarAudio();

        }

    },
    {
        passive: true,
        once: false
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

    // --------------------------------------------------------
    // SOM DESATIVADO
    // --------------------------------------------------------

    if (
        !audioPermitido()
    ) {

        return false;

    }


    const liberado =
        await ativarAudio();


    if (
        !liberado
        ||
        !contextoAudio
    ) {

        return false;

    }


    // --------------------------------------------------------
    // APLICAR VOLUME MESTRE
    // --------------------------------------------------------

    const volumeMestre =
        obterVolumeNormalizado();


    const volumeFinal =
        volume
        *
        volumeMestre;


    if (
        volumeFinal <= 0
    ) {

        return false;

    }


    try {

        const oscilador =
            contextoAudio.createOscillator();


        const ganho =
            contextoAudio.createGain();


        const inicio =
            contextoAudio.currentTime
            +
            Math.max(
                0,
                atraso
            );


        const fim =
            inicio
            +
            Math.max(
                0.01,
                duracao
            );


        oscilador.type =
            tipo;


        oscilador.frequency.setValueAtTime(
            frequencia,
            inicio
        );


        /*
        exponentialRampToValueAtTime não aceita zero.
        Por isso usamos 0.0001 como mínimo.
        */

        ganho.gain.setValueAtTime(
            0.0001,
            inicio
        );


        ganho.gain.exponentialRampToValueAtTime(
            Math.max(
                0.0001,
                volumeFinal
            ),
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


        return true;

    } catch (erro) {

        console.warn(
            "Erro ao reproduzir som:",
            erro
        );

        return false;

    }

}


// ============================================================
// CLIQUE
// ============================================================

function somClique() {

    if (
        !audioPermitido()
    ) {

        return;

    }


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

    if (
        !audioPermitido()
    ) {

        return;

    }


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

    if (
        !audioPermitido()
    ) {

        return;

    }


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

    if (
        !audioPermitido()
    ) {

        return;

    }


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

    if (
        !audioPermitido()
    ) {

        return;

    }


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

    if (
        !audioPermitido()
    ) {

        return;

    }


    const notas = [
        523.25,
        659.25,
        783.99,
        1046.50
    ];


    notas.forEach(
        (nota, indice) => {

            tocarTom({

                frequencia:
                    nota,

                duracao:
                    indice === 3
                        ? 0.35
                        : 0.12,

                volume:
                    0.085,

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

    if (
        !audioPermitido()
    ) {

        return;

    }


    tocarTom({
        frequencia: 392,
        duracao: 0.10,
        volume: 0.05
    });


    tocarTom({
        frequencia: 330,
        duracao: 0.12,
        volume: 0.05,
        atraso: 0.10
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


        // ====================================================
        // ELEMENTO SEM SOM
        // ====================================================

        if (
            elemento.dataset.semSom
            ===
            "true"
        ) {

            return;

        }


        // ====================================================
        // BOTÃO DE RESPOSTA POSSUI SOM PRÓPRIO
        // ====================================================

        if (
            elemento.id
            ===
            "botaoResponder"
        ) {

            return;

        }


        /*
        Se som estiver desligado ou volume for 0,
        não interferimos no clique nem na navegação.
        */

        if (
            !audioPermitido()
        ) {

            return;

        }


        await ativarAudio();


        // ====================================================
        // LINKS
        // ====================================================

        if (
            elemento.tagName
            ===
            "A"
        ) {

            const href =
                elemento.getAttribute(
                    "href"
                );


            // ------------------------------------------------
            // LINK SEM DESTINO
            // ------------------------------------------------

            if (
                !href
                ||
                href === "#"
                ||
                href.startsWith(
                    "javascript:"
                )
            ) {

                somClique();

                return;

            }


            // ------------------------------------------------
            // ÂNCORA DA MESMA PÁGINA
            // ------------------------------------------------

            if (
                href.startsWith(
                    "#"
                )
            ) {

                somClique();

                return;

            }


            // ------------------------------------------------
            // CTRL / SHIFT / ALT / CMD
            // ------------------------------------------------

            if (
                event.ctrlKey
                ||
                event.metaKey
                ||
                event.shiftKey
                ||
                event.altKey
            ) {

                somClique();

                return;

            }


            // ------------------------------------------------
            // NOVA ABA / DOWNLOAD
            // ------------------------------------------------

            if (
                elemento.hasAttribute(
                    "download"
                )
                ||
                elemento.target
                ===
                "_blank"
            ) {

                somClique();

                return;

            }


            /*
            Pequeno atraso apenas quando o áudio realmente
            está habilitado.
            */

            event.preventDefault();


            somClique();


            setTimeout(
                () => {

                    window.location.href =
                        elemento.href;

                },
                90
            );


            return;

        }


        // ====================================================
        // BOTÕES
        // ====================================================

        somClique();

    }
);


// ============================================================
// ATUALIZAR CONFIGURAÇÕES EM TEMPO REAL
// ============================================================

window.addEventListener(
    "storage",
    event => {

        if (
            event.key
            ===
            "flashmatty_sons"
            ||
            event.key
            ===
            "flashmatty_volume"
        ) {

            console.log(
                "🔊 Configuração de áudio atualizada."
            );

        }

    }
);


// ============================================================
// API GLOBAL
// ============================================================

window.ativarAudio =
    ativarAudio;

window.tocarTom =
    tocarTom;

window.somClique =
    somClique;

window.somSelecao =
    somSelecao;

window.somAcerto =
    somAcerto;

window.somErro =
    somErro;

window.somMoeda =
    somMoeda;

window.somConcluido =
    somConcluido;

window.somTentarNovamente =
    somTentarNovamente;


// ============================================================
// API DE CONFIGURAÇÃO DE SOM
// ============================================================

window.FlashMattySons = {

    get ativo() {

        return sonsAtivados();

    },


    get volume() {

        return obterVolume();

    },


    get volumeNormalizado() {

        return obterVolumeNormalizado();

    },


    tocarClique() {

        somClique();

    },


    tocarAcerto() {

        somAcerto();

    },


    tocarErro() {

        somErro();

    },


    tocarMoeda() {

        somMoeda();

    }

};


// ============================================================
// DEBUG
// ============================================================

console.log(
    "🔊 Sistema de sons FlashMatty carregado."
);

console.log(
    "🔊 Sons:",
    sonsAtivados()
        ? "ativados"
        : "desativados"
);

console.log(
    "🔊 Volume:",
    `${obterVolume()}%`
);