
// FLASHMATTY - NOTIFICAÇÕES WEB PUSH
// ============================================================

// Evita inicialização duplicada caso o arquivo seja incluído
// mais de uma vez por engano.
if (window.__flashMattyNotificacoesCarregado) {
    console.warn("🔔 notificacoes.js já foi carregado.");
} else {

    window.__flashMattyNotificacoesCarregado = true;

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        console.log(
            "🔔 notificacoes.js carregado"
        );


        // ====================================================
        // ELEMENTOS
        // ====================================================

        const botaoAtivar =
            document.getElementById(
                "ativarNotificacoes"
            );


        const botaoTestar =
            document.getElementById(
                "testarNotificacao"
            );


        const status =
            document.getElementById(
                "notificacaoStatus"
            );


        const preferencias = {

            amizades:
                document.getElementById(
                    "prefNotificacaoAmizades"
                ),

            desafios:
                document.getElementById(
                    "prefNotificacaoDesafios"
                ),

            conquistas:
                document.getElementById(
                    "prefNotificacaoConquistas"
                ),

            recompensas:
                document.getElementById(
                    "prefNotificacaoRecompensas"
                ),

            lembretes:
                document.getElementById(
                    "prefNotificacaoLembretes"
                )

        };


        // ====================================================
        // VERIFICAR HTML
        // ====================================================

        if (!status) {

            console.error(
                "Elemento #notificacaoStatus não encontrado."
            );

            return;

        }


        // ====================================================
        // STATUS
        // ====================================================

        function mostrarStatus(
            mensagem,
            tipo = "normal"
        ) {

            status.textContent =
                mensagem;


            status.classList.remove(
                "text-green-400",
                "text-red-400",
                "text-yellow-400",
                "text-slate-400"
            );


            if (tipo === "ok") {

                status.classList.add(
                    "text-green-400"
                );

            } else if (tipo === "erro") {

                status.classList.add(
                    "text-red-400"
                );

            } else if (tipo === "aviso") {

                status.classList.add(
                    "text-yellow-400"
                );

            } else {

                status.classList.add(
                    "text-slate-400"
                );

            }

        }


        // ====================================================
        // FETCH JSON
        // ====================================================

        async function fetchJson(
            url,
            opcoes = {}
        ) {

            const resposta =
                await fetch(
                    url,
                    {
                        credentials:
                            "same-origin",

                        ...opcoes
                    }
                );


            let dados = {};


            try {

                dados =
                    await resposta.json();

            } catch {

                // resposta não era JSON
            }


            if (!resposta.ok) {

                throw new Error(
                    dados.erro
                    ||
                    `Erro HTTP ${resposta.status}`
                );

            }


            return dados;

        }


        // ====================================================
        // SUPORTE
        // ====================================================

        function navegadorSuportaPush() {

            return (

                "serviceWorker"
                in
                navigator

                &&

                "PushManager"
                in
                window

                &&

                "Notification"
                in
                window

            );

        }


        // ====================================================
        // TIMEOUT
        // ====================================================

        function comTimeout(
            promessa,
            milissegundos,
            mensagem
        ) {

            return Promise.race([

                promessa,

                new Promise(
                    (
                        _resolve,
                        reject
                    ) => {

                        setTimeout(
                            () => {

                                reject(
                                    new Error(
                                        mensagem
                                    )
                                );

                            },
                            milissegundos
                        );

                    }
                )

            ]);

        }


        // ====================================================
        // REGISTRAR SERVICE WORKER
        // ====================================================

        async function obterServiceWorker() {

            if (
                !navegadorSuportaPush()
            ) {

                throw new Error(
                    "Este navegador não oferece suporte a Web Push."
                );

            }


            const registroInicial =
                await navigator
                    .serviceWorker
                    .register(
                        "/service-worker.js",
                        {
                            scope:
                                "/"
                        }
                    );


            console.log(
                "🔧 Service Worker registrado:",
                registroInicial.scope
            );


            const registro =
                await comTimeout(

                    navigator
                        .serviceWorker
                        .ready,

                    10000,

                    (
                        "O Service Worker não ficou pronto. "
                        +
                        "Verifique /service-worker.js."
                    )

                );


            return registro;

        }


        // ====================================================
        // BASE64 VAPID
        // ====================================================

        function urlBase64ParaUint8Array(
            base64String
        ) {

            const padding =
                "=".repeat(
                    (
                        4
                        -
                        base64String.length
                        %
                        4
                    )
                    %
                    4
                );


            const base64 =
                (
                    base64String
                    +
                    padding
                )
                .replace(
                    /-/g,
                    "+"
                )
                .replace(
                    /_/g,
                    "/"
                );


            const rawData =
                window.atob(
                    base64
                );


            return Uint8Array.from(

                [...rawData]
                    .map(
                        caractere =>
                            caractere
                                .charCodeAt(0)
                    )

            );

        }


        // ====================================================
        // SINCRONIZAR ASSINATURA
        // ====================================================

        async function enviarAssinaturaServidor(
            assinatura
        ) {

            const dadosAssinatura =
                assinatura.toJSON();


            const opcoesBase = {

                method:
                    "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                }

            };


            // Primeiro tenta o formato cru:
            // { endpoint, expirationTime, keys }
            try {

                return await fetchJson(
                    "/notificacoes/assinar",
                    {
                        ...opcoesBase,

                        body:
                            JSON.stringify(
                                dadosAssinatura
                            )
                    }
                );

            } catch (erroFormatoCru) {

                console.warn(
                    "Formato cru da assinatura não aceito; tentando formato encapsulado.",
                    erroFormatoCru
                );

            }


            // Compatibilidade com backend que espera:
            // { subscription: { endpoint, keys, ... } }
            return fetchJson(
                "/notificacoes/assinar",
                {
                    ...opcoesBase,

                    body:
                        JSON.stringify({

                            subscription:
                                dadosAssinatura

                        })
                }
            );

        }


        // ====================================================
        // ATUALIZAR BOTÕES
        // ====================================================

        function atualizarInterface(
            ativo
        ) {

            if (botaoAtivar) {

                botaoAtivar.dataset.ativo =
                    ativo
                        ?
                        "true"
                        :
                        "false";


                botaoAtivar.textContent =
                    ativo
                        ?
                        "🔔 Desativar notificações"
                        :
                        "🔕 Ativar notificações";

            }


            if (botaoTestar) {

                botaoTestar.disabled =
                    !ativo;


                botaoTestar.classList.toggle(
                    "opacity-50",
                    !ativo
                );


                botaoTestar.classList.toggle(
                    "cursor-not-allowed",
                    !ativo
                );

            }

        }


        // ====================================================
        // VERIFICAR ESTADO
        // ====================================================

        async function verificarEstado() {

            mostrarStatus(
                "Verificando notificações..."
            );


            if (
                !navegadorSuportaPush()
            ) {

                atualizarInterface(
                    false
                );


                mostrarStatus(
                    "Web Push não é suportado neste navegador.",
                    "erro"
                );


                return;

            }


            try {

                const registro =
                    await obterServiceWorker();


                const assinatura =
                    await registro
                        .pushManager
                        .getSubscription();


                if (assinatura) {

                    try {

                        await enviarAssinaturaServidor(
                            assinatura
                        );

                    } catch (erro) {

                        console.warn(
                            "Falha ao sincronizar assinatura:",
                            erro
                        );

                    }


                    atualizarInterface(
                        true
                    );


                    mostrarStatus(
                        "🔔 Notificações ativadas neste dispositivo.",
                        "ok"
                    );

                } else {

                    atualizarInterface(
                        false
                    );


                    if (
                        Notification.permission
                        ===
                        "denied"
                    ) {

                        mostrarStatus(
                            (
                                "As notificações estão bloqueadas "
                                +
                                "nas configurações do navegador."
                            ),
                            "erro"
                        );

                    } else {

                        mostrarStatus(
                            "Notificações ainda não ativadas neste dispositivo."
                        );

                    }

                }

            } catch (erro) {

                console.error(
                    "Erro ao verificar notificações:",
                    erro
                );


                atualizarInterface(
                    false
                );


                mostrarStatus(
                    `Erro: ${erro.message}`,
                    "erro"
                );

            }

        }


        // ====================================================
        // ATIVAR PUSH
        // ====================================================

        async function ativarNotificacoes() {

            mostrarStatus(
                "Solicitando permissão..."
            );


            if (
                Notification.permission
                ===
                "denied"
            ) {

                throw new Error(
                    (
                        "As notificações foram bloqueadas. "
                        +
                        "Libere-as nas configurações do navegador."
                    )
                );

            }


            const permissao =
                await Notification
                    .requestPermission();


            if (
                permissao
                !==
                "granted"
            ) {

                throw new Error(
                    "Permissão para notificações não concedida."
                );

            }


            const registro =
                await obterServiceWorker();


            let assinatura =
                await registro
                    .pushManager
                    .getSubscription();


            if (!assinatura) {

                mostrarStatus(
                    "Preparando o dispositivo..."
                );


                const dados =
                    await fetchJson(
                        "/notificacoes/chave-publica"
                    );


                const chavePublica =

                    dados.chave
                    ||
                    dados.publicKey
                    ||
                    dados.public_key;


                if (!chavePublica) {

                    throw new Error(
                        "A chave VAPID pública não foi retornada pelo servidor."
                    );

                }


                assinatura =
                    await registro
                        .pushManager
                        .subscribe({

                            userVisibleOnly:
                                true,

                            applicationServerKey:
                                urlBase64ParaUint8Array(
                                    chavePublica
                                )

                        });

            }


            await enviarAssinaturaServidor(
                assinatura
            );


            atualizarInterface(
                true
            );


            mostrarStatus(
                "🔔 Notificações ativadas com sucesso.",
                "ok"
            );

        }


        // ====================================================
        // DESATIVAR
        // ====================================================

        async function desativarNotificacoes() {

            mostrarStatus(
                "Desativando..."
            );


            const registro =
                await obterServiceWorker();


            const assinatura =
                await registro
                    .pushManager
                    .getSubscription();


            if (assinatura) {

                try {

                    await fetchJson(
                        "/notificacoes/desassinar",
                        {

                            method:
                                "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"

                            },

                            body:
                                JSON.stringify({

                                    endpoint:
                                        assinatura.endpoint

                                })

                        }
                    );

                } catch (erro) {

                    console.warn(
                        "Erro removendo assinatura do servidor:",
                        erro
                    );

                }


                await assinatura
                    .unsubscribe();

            }


            atualizarInterface(
                false
            );


            mostrarStatus(
                "🔕 Notificações desativadas neste dispositivo."
            );

        }


        // ====================================================
        // BOTÃO PRINCIPAL
        // ====================================================

        botaoAtivar
            ?.addEventListener(
                "click",
                async () => {

                    botaoAtivar.disabled =
                        true;


                    try {

                        const ativo =
                            botaoAtivar
                                .dataset
                                .ativo
                            ===
                            "true";


                        if (ativo) {

                            await desativarNotificacoes();

                        } else {

                            await ativarNotificacoes();

                        }

                    } catch (erro) {

                        console.error(
                            "Erro Push:",
                            erro
                        );


                        mostrarStatus(
                            `Erro: ${erro.message}`,
                            "erro"
                        );

                    } finally {

                        botaoAtivar.disabled =
                            false;

                    }

                }
            );


        // ====================================================
        // TESTE
        // ====================================================

        botaoTestar
            ?.addEventListener(
                "click",
                async () => {

                    botaoTestar.disabled =
                        true;


                    try {

                        mostrarStatus(
                            "Enviando notificação de teste..."
                        );


                        const dados =
                            await fetchJson(
                                "/notificacoes/testar",
                                {

                                    method:
                                        "POST",

                                    headers: {

                                        "Content-Type":
                                            "application/json"

                                    }

                                }
                            );


                        const quantidadeEnviada =
                            Number(

                                dados.enviados
                                ??
                                dados.enviadas
                                ??
                                dados.resultado?.enviadas
                                ??
                                dados.resultado?.enviados
                                ??
                                0

                            );


                        if (
                            quantidadeEnviada
                            <=
                            0
                        ) {

                            throw new Error(
                                (
                                    "O servidor não encontrou "
                                    +
                                    "nenhuma assinatura ativa."
                                )
                            );

                        }


                        mostrarStatus(
                            "✅ Notificação de teste enviada.",
                            "ok"
                        );

                    } catch (erro) {

                        console.error(
                            erro
                        );


                        mostrarStatus(
                            `Erro: ${erro.message}`,
                            "erro"
                        );

                    } finally {

                        botaoTestar.disabled =
                            false;

                    }

                }
            );


        // ====================================================
        // CARREGAR PREFERÊNCIAS
        // ====================================================

        async function carregarPreferencias() {

            try {

                const dados =
                    await fetchJson(
                        "/notificacoes/preferencias"
                    );


                const dadosPreferencias =
                    dados.preferencias
                    ??
                    dados;


                Object.entries(
                    preferencias
                )
                .forEach(
                    ([chave, elemento]) => {

                        if (elemento) {

                            elemento.checked =
                                Boolean(
                                    dadosPreferencias[
                                        chave
                                    ]
                                );

                        }

                    }
                );

            } catch (erro) {

                console.error(
                    "Erro carregando preferências:",
                    erro
                );

            }

        }


        // ====================================================
        // SALVAR PREFERÊNCIAS
        // ====================================================

        async function salvarPreferencias() {

            const dados = {};


            Object.entries(
                preferencias
            )
            .forEach(
                ([chave, elemento]) => {

                    if (elemento) {

                        dados[chave] =
                            elemento.checked;

                    }

                }
            );


            try {

                const opcoesBase = {

                    method:
                        "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    }

                };


                try {

                    await fetchJson(
                        "/notificacoes/preferencias",
                        {
                            ...opcoesBase,

                            body:
                                JSON.stringify(
                                    dados
                                )
                        }
                    );

                } catch (erroFormatoPlano) {

                    console.warn(
                        "Formato plano das preferências não aceito; tentando formato encapsulado.",
                        erroFormatoPlano
                    );


                    await fetchJson(
                        "/notificacoes/preferencias",
                        {
                            ...opcoesBase,

                            body:
                                JSON.stringify({

                                    preferencias:
                                        dados

                                })
                        }
                    );

                }


                console.log(
                    "🔔 Preferências salvas:",
                    dados
                );

            } catch (erro) {

                console.error(
                    "Erro salvando preferências:",
                    erro
                );


                mostrarStatus(
                    (
                        "Não foi possível salvar "
                        +
                        "as preferências."
                    ),
                    "erro"
                );

            }

        }


        Object.values(
            preferencias
        )
        .forEach(
            elemento => {

                elemento
                    ?.addEventListener(
                        "change",
                        salvarPreferencias
                    );

            }
        );


        // ====================================================
        // INICIALIZAÇÃO
        // ====================================================

        try {

            await carregarPreferencias();

        } catch (erro) {

            console.error(
                erro
            );

        }


        await verificarEstado();

    }
);

}
