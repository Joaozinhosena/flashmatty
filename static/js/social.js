(() => {

    "use strict";


    // ========================================================
    // EVITA INICIALIZAÇÃO DUPLICADA
    // ========================================================

    if (window.__flashMattySocialCarregado) {

        console.warn(
            "⚠️ social.js já foi carregado."
        );

        return;
    }


    window.__flashMattySocialCarregado =
        true;


    // ========================================================
    // STATUS ONLINE
    // ========================================================

    function atualizarStatus(
        usuarioId,
        online
    ) {

        document
            .querySelectorAll(
                `[data-online-user="${usuarioId}"]`
            )
            .forEach(
                elemento => {

                    elemento.dataset.online =
                        online
                            ? "1"
                            : "0";


                    elemento.textContent =
                        online
                            ? "● Online"
                            : "● Offline";

                }
            );

    }


    // ========================================================
    // TOAST
    // ========================================================

    function criarToast(
        mensagem,
        opcoes = {}
    ) {

        const toast =
            document.createElement(
                "div"
            );


        toast.className =
            "flash-social-toast";


        Object.assign(
            toast.style,
            {

                position:
                    "fixed",

                right:
                    "18px",

                bottom:
                    "18px",

                zIndex:
                    "99999",

                width:
                    "min(390px, calc(100vw - 36px))",

                background:
                    "var(--fm-card, #0f172a)",

                color:
                    "var(--fm-text, #ffffff)",

                border:
                    "1px solid var(--fm-border, #334155)",

                borderRadius:
                    "18px",

                padding:
                    "16px",

                boxShadow:
                    "0 20px 50px rgba(0,0,0,.35)",

                fontFamily:
                    "system-ui, sans-serif"

            }
        );


        // ====================================================
        // TEXTO
        // ====================================================

        const texto =
            document.createElement(
                "div"
            );


        texto.className =
            "flash-social-toast-texto";


        texto.textContent =
            mensagem;


        texto.style.fontWeight =
            "800";


        toast.appendChild(
            texto
        );


        // ====================================================
        // BOTÃO
        // ====================================================

        let botao = null;


        if (
            opcoes.textoBotao
            &&
            typeof opcoes.aoClicar
            ===
            "function"
        ) {

            botao =
                document.createElement(
                    "button"
                );


            botao.type =
                "button";


            botao.textContent =
                opcoes.textoBotao;


            Object.assign(
                botao.style,
                {

                    marginTop:
                        "12px",

                    background:
                        "var(--fm-primary, #4f46e5)",

                    color:
                        "#ffffff",

                    border:
                        "0",

                    borderRadius:
                        "12px",

                    padding:
                        "10px 14px",

                    fontWeight:
                        "900",

                    cursor:
                        "pointer"

                }
            );


            botao.addEventListener(
                "click",
                () => {

                    if (
                        botao.dataset.processando
                        ===
                        "true"
                    ) {

                        return;

                    }


                    botao.dataset.processando =
                        "true";


                    botao.disabled =
                        true;


                    botao.textContent =
                        opcoes.textoProcessando
                        ||
                        "Aguarde...";


                    try {

                        opcoes.aoClicar(
                            botao,
                            toast
                        );

                    } catch (erro) {

                        console.error(
                            "Erro no botão do toast:",
                            erro
                        );


                        botao.dataset.processando =
                            "false";


                        botao.disabled =
                            false;


                        botao.textContent =
                            opcoes.textoBotao;

                    }

                }
            );


            toast.appendChild(
                botao
            );

        }


        // ====================================================
        // ADICIONAR NA TELA
        // ====================================================

        document.body.appendChild(
            toast
        );


        // ====================================================
        // REMOÇÃO AUTOMÁTICA
        // ====================================================

        const duracao =
            Number(
                opcoes.duracao
                ??
                6000
            );


        let temporizador = null;


        if (
            Number.isFinite(
                duracao
            )
            &&
            duracao > 0
        ) {

            temporizador =
                setTimeout(
                    () => {

                        if (
                            toast.isConnected
                        ) {

                            toast.remove();

                        }

                    },
                    duracao
                );

        }


        // ====================================================
        // API DO TOAST
        // ====================================================

        return {

            elemento:
                toast,

            texto:
                texto,

            botao:
                botao,

            remover() {

                if (
                    temporizador
                ) {

                    clearTimeout(
                        temporizador
                    );

                }


                if (
                    toast.isConnected
                ) {

                    toast.remove();

                }

            },

            alterarTexto(
                novaMensagem
            ) {

                texto.textContent =
                    novaMensagem;

            },

            liberarBotao(
                textoBotao = null
            ) {

                if (
                    !botao
                ) {

                    return;

                }


                botao.dataset.processando =
                    "false";


                botao.disabled =
                    false;


                if (
                    textoBotao
                ) {

                    botao.textContent =
                        textoBotao;

                }

            }

        };

    }


    // ========================================================
    // DOCUMENTO CARREGADO
    // ========================================================

    document.addEventListener(
        "DOMContentLoaded",
        () => {


            // =================================================
            // SOCKET.IO
            // =================================================

            if (
                typeof window.io
                !==
                "function"
            ) {

                console.warn(
                    "⚠️ Socket.IO não foi carregado. Sistema social desativado."
                );

                return;

            }


            // =================================================
            // SOCKET SOCIAL
            // =================================================

            const socket =
                window.io();


            window.flashSocialSocket =
                socket;


            console.log(
                "👥 Sistema social iniciado."
            );


            // =================================================
            // ESTADO
            // =================================================

            let redirecionandoParaDesafio =
                false;


            let desafioSendoAceito =
                null;


            // =================================================
            // HEARTBEAT
            // =================================================

            function enviarHeartbeat() {

                if (
                    !socket.connected
                ) {

                    return;

                }


                socket.emit(
                    "social_presenca"
                );

            }


            // =================================================
            // USUÁRIOS VISÍVEIS
            // =================================================

            function idsVisiveis() {

                return [

                    ...new Set(

                        Array
                            .from(
                                document.querySelectorAll(
                                    "[data-online-user]"
                                )
                            )
                            .map(
                                elemento =>
                                    Number(
                                        elemento.dataset.onlineUser
                                    )
                            )
                            .filter(
                                numero =>
                                    Number.isFinite(
                                        numero
                                    )
                            )

                    )

                ];

            }


            // =================================================
            // CONSULTAR PRESENÇA
            // =================================================

            function consultarPresenca() {

                if (
                    !socket.connected
                ) {

                    return;

                }


                const usuarios =
                    idsVisiveis();


                if (
                    !usuarios.length
                ) {

                    return;

                }


                socket.emit(

                    "social_consultar_presenca",

                    {

                        usuarios:
                            usuarios

                    }

                );

            }


            // =================================================
            // CONECTADO
            // =================================================

            socket.on(
                "connect",
                () => {

                    console.log(
                        "🟢 Social conectado:",
                        socket.id
                    );


                    enviarHeartbeat();

                    consultarPresenca();

                }
            );


            // =================================================
            // DESCONECTADO
            // =================================================

            socket.on(
                "disconnect",
                motivo => {

                    console.log(
                        "🔴 Social desconectado:",
                        motivo
                    );

                }
            );


            // =================================================
            // ERRO
            // =================================================

            socket.on(
                "connect_error",
                erro => {

                    console.error(
                        "❌ Erro de conexão social:",
                        erro
                    );

                }
            );


            // =================================================
            // HEARTBEATS
            // =================================================

            const heartbeatInterval =
                setInterval(
                    enviarHeartbeat,
                    20000
                );


            const presencaInterval =
                setInterval(
                    consultarPresenca,
                    25000
                );


            // =================================================
            // LIMPEZA DA PÁGINA
            // =================================================

            window.addEventListener(
                "pagehide",
                () => {

                    clearInterval(
                        heartbeatInterval
                    );


                    clearInterval(
                        presencaInterval
                    );

                },
                {
                    once:
                        true
                }
            );


            // =================================================
            // STATUS ONLINE/OFFLINE
            // =================================================

            socket.on(
                "social_status",
                dados => {

                    if (
                        !dados
                        ||
                        dados.usuario_id
                        ===
                        undefined
                    ) {

                        return;

                    }


                    atualizarStatus(

                        dados.usuario_id,

                        Boolean(
                            dados.online
                        )

                    );

                }
            );


            // =================================================
            // RESULTADO DA CONSULTA DE PRESENÇA
            // =================================================

            socket.on(
                "social_presenca_resultado",
                resultado => {

                    Object
                        .entries(
                            resultado
                            ||
                            {}
                        )
                        .forEach(
                            (
                                [
                                    usuarioId,
                                    online
                                ]
                            ) => {

                                atualizarStatus(

                                    usuarioId,

                                    Boolean(
                                        online
                                    )

                                );

                            }
                        );

                }
            );


            // =================================================
            // BOTÕES DE DESAFIAR
            // =================================================

            document
                .querySelectorAll(
                    "[data-desafiar-usuario]"
                )
                .forEach(
                    botao => {

                        botao.addEventListener(
                            "click",
                            () => {

                                if (
                                    !socket.connected
                                ) {

                                    criarToast(
                                        "Não foi possível enviar o desafio: conexão indisponível."
                                    );

                                    return;

                                }


                                const usuarioId =
                                    Number(
                                        botao.dataset.desafiarUsuario
                                    );


                                if (
                                    !Number.isFinite(
                                        usuarioId
                                    )
                                ) {

                                    return;

                                }


                                if (
                                    botao.dataset.enviando
                                    ===
                                    "true"
                                ) {

                                    return;

                                }


                                if (
                                    typeof window.somClique
                                    ===
                                    "function"
                                ) {

                                    window.somClique();

                                }


                                const textoOriginal =
                                    botao.textContent;


                                botao.dataset.enviando =
                                    "true";


                                botao.disabled =
                                    true;


                                botao.textContent =
                                    "⏳ Enviando...";


                                socket.emit(

                                    "social_desafiar",

                                    {

                                        usuario_id:
                                            usuarioId

                                    }

                                );


                                setTimeout(
                                    () => {

                                        if (
                                            !botao.isConnected
                                        ) {

                                            return;

                                        }


                                        botao.dataset.enviando =
                                            "false";


                                        botao.disabled =
                                            false;


                                        botao.textContent =
                                            textoOriginal;

                                    },
                                    2000
                                );

                            }
                        );

                    }
                );


            // =================================================
            // RESULTADO DE DESAFIO
            // =================================================

            socket.on(
                "social_desafio_resultado",
                dados => {

                    dados =
                        dados
                        ||
                        {};


                    console.log(
                        "🎮 Resultado do desafio:",
                        dados
                    );


                    // =========================================
                    // CASO ESTEJA TENTANDO ACEITAR UM DESAFIO
                    // E O SERVIDOR TENHA RETORNADO ERRO
                    // =========================================

                    if (
                        desafioSendoAceito
                        &&
                        dados.ok === false
                    ) {

                        if (
                            desafioSendoAceito.timeout
                        ) {

                            clearTimeout(
                                desafioSendoAceito.timeout
                            );

                        }


                        desafioSendoAceito.toast
                            ?.alterarTexto(
                                dados.mensagem
                                ||
                                "Não foi possível aceitar o desafio."
                            );


                        desafioSendoAceito.toast
                            ?.liberarBotao(
                                "Tentar novamente"
                            );


                        desafioSendoAceito =
                            null;


                        return;

                    }


                    criarToast(

                        dados.mensagem
                        ||
                        "Desafio processado."

                    );

                }
            );


            // =================================================
            // DESAFIO RECEBIDO
            // =================================================

            socket.on(
                "social_desafio_recebido",
                dados => {

                    if (
                        !dados
                        ||
                        !dados.desafiante_id
                    ) {

                        return;

                    }


                    console.log(
                        "🎮 Desafio recebido:",
                        dados
                    );


                    if (
                        typeof window.somConcluido
                        ===
                        "function"
                    ) {

                        window.somConcluido();

                    }


                    const toast =
                        criarToast(

                            (
                                `${dados.nome} desafiou você `
                                +
                                "para uma partida! 🎮"
                            ),

                            {

                                textoBotao:
                                    "Aceitar desafio",

                                textoProcessando:
                                    "Criando sala...",

                                duracao:
                                    120000,

                                aoClicar:
                                    (
                                        botao,
                                        toastElemento
                                    ) => {

                                        if (
                                            !socket.connected
                                        ) {

                                            botao.dataset.processando =
                                                "false";


                                            botao.disabled =
                                                false;


                                            botao.textContent =
                                                "Aceitar desafio";


                                            criarToast(
                                                "A conexão com o servidor foi perdida."
                                            );


                                            return;

                                        }


                                        // =================================
                                        // NÃO REDIRECIONA AQUI
                                        // =================================
                                        //
                                        // O servidor primeiro:
                                        //
                                        // 1. valida o desafio
                                        // 2. cria a sala
                                        // 3. adiciona host
                                        // 4. adiciona o amigo
                                        // 5. envia a URL aos dois
                                        //
                                        // =================================

                                        socket.emit(

                                            "social_desafio_aceito",

                                            {

                                                desafiante_id:
                                                    dados.desafiante_id

                                            }

                                        );


                                        const objetoToast = {

                                            elemento:
                                                toastElemento,

                                            alterarTexto(
                                                texto
                                            ) {

                                                const alvo =
                                                    toastElemento
                                                        .querySelector(
                                                            ".flash-social-toast-texto"
                                                        );


                                                if (
                                                    alvo
                                                ) {

                                                    alvo.textContent =
                                                        texto;

                                                }

                                            },

                                            liberarBotao(
                                                texto
                                            ) {

                                                botao.dataset.processando =
                                                    "false";


                                                botao.disabled =
                                                    false;


                                                botao.textContent =
                                                    texto;

                                            }

                                        };


                                        objetoToast.alterarTexto(
                                            "🎮 Criando a sala do desafio..."
                                        );


                                        // =================================
                                        // TIMEOUT
                                        // =================================

                                        const timeout =
                                            setTimeout(
                                                () => {

                                                    if (
                                                        redirecionandoParaDesafio
                                                    ) {

                                                        return;

                                                    }


                                                    objetoToast
                                                        .alterarTexto(
                                                            "O servidor demorou para criar a sala. Tente novamente."
                                                        );


                                                    objetoToast
                                                        .liberarBotao(
                                                            "Tentar novamente"
                                                        );


                                                    desafioSendoAceito =
                                                        null;

                                                },
                                                12000
                                            );


                                        desafioSendoAceito = {

                                            desafianteId:
                                                Number(
                                                    dados.desafiante_id
                                                ),

                                            toast:
                                                objetoToast,

                                            timeout:
                                                timeout

                                        };

                                    }

                            }

                        );


                    console.log(
                        "Toast do desafio criado:",
                        toast
                    );

                }
            );


            // =================================================
            // DESAFIO ACEITO / SALA CRIADA
            // =================================================
            //
            // ESTE É O EVENTO PRINCIPAL.
            //
            // O servidor só deve dispará-lo depois de:
            //
            // criar_sala(...)
            // adicionar_jogador(...)
            //
            // =================================================

            socket.on(
                "social_desafio_aceito",
                dados => {

                    console.log(
                        "🎮 Desafio aceito / sala criada:",
                        dados
                    );


                    if (
                        !dados
                    ) {

                        return;

                    }


                    const destino =
                        dados.url_multiplayer;


                    if (
                        !destino
                    ) {

                        console.error(
                            "❌ O servidor não retornou url_multiplayer.",
                            dados
                        );


                        if (
                            desafioSendoAceito
                        ) {

                            clearTimeout(
                                desafioSendoAceito.timeout
                            );


                            desafioSendoAceito.toast
                                ?.alterarTexto(
                                    "A sala foi criada, mas a URL não foi recebida."
                                );


                            desafioSendoAceito.toast
                                ?.liberarBotao(
                                    "Tentar novamente"
                                );


                            desafioSendoAceito =
                                null;

                        }


                        return;

                    }


                    // =========================================
                    // EVITA REDIRECIONAMENTO DUPLO
                    // =========================================

                    if (
                        redirecionandoParaDesafio
                    ) {

                        return;

                    }


                    redirecionandoParaDesafio =
                        true;


                    // =========================================
                    // CANCELA TIMEOUT DE ACEITAÇÃO
                    // =========================================

                    if (
                        desafioSendoAceito
                        &&
                        desafioSendoAceito.timeout
                    ) {

                        clearTimeout(
                            desafioSendoAceito.timeout
                        );

                    }


                    desafioSendoAceito =
                        null;


                    // =========================================
                    // SOM
                    // =========================================

                    if (
                        typeof window.somConcluido
                        ===
                        "function"
                    ) {

                        window.somConcluido();

                    }


                    // =========================================
                    // AVISO
                    // =========================================

                    criarToast(

                        dados.mensagem
                        ||
                        "🎮 Desafio aceito! Entrando na sala...",

                        {

                            duracao:
                                1800

                        }

                    );


                    console.log(
                        "➡️ Redirecionando para:",
                        destino
                    );


                    // =========================================
                    // REDIRECIONAR SOMENTE AGORA
                    // =========================================

                    setTimeout(
                        () => {

                            window.location.href =
                                destino;

                        },
                        500
                    );

                }
            );


            // =================================================
            // COMPATIBILIDADE COM EVENTO ANTIGO
            // =================================================

            socket.on(
                "social_sala_desafio_criada",
                dados => {

                    console.log(
                        "🎮 Evento compatível de sala:",
                        dados
                    );


                    if (
                        !dados
                        ||
                        !dados.codigo
                    ) {

                        return;

                    }


                    if (
                        redirecionandoParaDesafio
                    ) {

                        return;

                    }


                    const destino =

                        dados.url

                        ||

                        (
                            "/multiplayer/desafio/"
                            +
                            encodeURIComponent(
                                dados.codigo
                            )
                        );


                    redirecionandoParaDesafio =
                        true;


                    if (
                        desafioSendoAceito
                        &&
                        desafioSendoAceito.timeout
                    ) {

                        clearTimeout(
                            desafioSendoAceito.timeout
                        );

                    }


                    desafioSendoAceito =
                        null;


                    setTimeout(
                        () => {

                            window.location.href =
                                destino;

                        },
                        400
                    );

                }
            );


            // =================================================
            // ERROS SOCIAIS
            // =================================================

            socket.on(
                "social_erro",
                dados => {

                    console.error(
                        "❌ Erro social:",
                        dados
                    );


                    const mensagem =

                        dados?.mensagem

                        ||

                        "Ocorreu um erro no sistema social.";


                    if (
                        desafioSendoAceito
                    ) {

                        if (
                            desafioSendoAceito.timeout
                        ) {

                            clearTimeout(
                                desafioSendoAceito.timeout
                            );

                        }


                        desafioSendoAceito.toast
                            ?.alterarTexto(
                                mensagem
                            );


                        desafioSendoAceito.toast
                            ?.liberarBotao(
                                "Tentar novamente"
                            );


                        desafioSendoAceito =
                            null;


                        return;

                    }


                    criarToast(
                        mensagem
                    );

                }
            );


        }
    );

})();