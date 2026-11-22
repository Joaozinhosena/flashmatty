
 // ============================================================
 // FLASHMATTY SERVICE WORKER
 // VERSÃO 2.0
 //
 // PWA + CACHE ATUALIZÁVEL + PUSH
 // NOTIFICAÇÕES + PROTEÇÃO DE DADOS
 // ============================================================

const CACHE_VERSION = "flashmatty-static-v2";

const PRECACHE = [
    "/static/manifest.json",
    "/static/js/pwa.js",
    "/static/img/icons/icon-192.png",
    "/static/img/icons/icon-512.png",
    "/static/img/icons/icon-maskable-192.png",
    "/static/img/icons/icon-maskable-512.png",
    "/static/img/icons/favicon-48.png",
    "/static/img/icons/apple-touch-icon-180.png",
    "/static/img/icons/badge-96.png"
];

// ============================================================
// IDENTIFICAÇÃO DOS ARQUIVOS VISUAIS
// ============================================================

function arquivoVisual(url) {

    return (
        url.pathname === "/static/manifest.json" ||
        url.pathname.startsWith("/static/img/icons/")
    );

}

// ============================================================
// INSTALAÇÃO DO SERVICE WORKER
// ============================================================

self.addEventListener("install", event => {

    event.waitUntil(

        caches.open(CACHE_VERSION)
            .then(async cache => {

                // Atualiza o precache diretamente da rede.
                // Não reutiliza respostas do cache HTTP.

                const arquivos = PRECACHE.map(caminho =>
                    new Request(caminho, {
                        cache: "reload"
                    })
                );

                await cache.addAll(arquivos);

            })
            .then(() => self.skipWaiting())

    );

});

// ============================================================
// ATIVAÇÃO E LIMPEZA DOS CACHES ANTIGOS
// ============================================================

self.addEventListener("activate", event => {

    event.waitUntil(

        caches.keys()
            .then(nomes =>

                Promise.all(

                    nomes.map(nome => {

                        if (
                            nome.startsWith("flashmatty-") &&
                            nome !== CACHE_VERSION
                        ) {

                            return caches.delete(nome);

                        }

                        return Promise.resolve(false);

                    })

                )

            )
            .then(() => self.clients.claim())

    );

});

// ============================================================
// INTERCEPTAÇÃO DE REQUISIÇÕES
// ============================================================

self.addEventListener("fetch", event => {

    const requisicao = event.request;

    // Apenas GET.
    if (requisicao.method !== "GET") {
        return;
    }

    const url = new URL(requisicao.url);

    // Não interceptar outros domínios.
    if (url.origin !== self.location.origin) {
        return;
    }

    // Não armazenar páginas autenticadas.
    if (requisicao.mode === "navigate") {
        return;
    }

    // Apenas arquivos estáticos.
    if (!url.pathname.startsWith("/static/")) {
        return;
    }

    // ========================================================
    // ÍCONES E MANIFESTO
    // NETWORK FIRST
    // ========================================================

    if (arquivoVisual(url)) {

        event.respondWith(

            (async () => {

                const cache = await caches.open(
                    CACHE_VERSION
                );

                try {

                    const resposta = await fetch(
                        requisicao,
                        {
                            cache: "no-store"
                        }
                    );

                    if (resposta.ok) {

                        await cache.put(
                            requisicao,
                            resposta.clone()
                        );

                    }

                    return resposta;

                } catch (erro) {

                    const salva = await cache.match(
                        requisicao
                    );

                    if (salva) {
                        return salva;
                    }

                    return Response.error();

                }

            })()

        );

        return;

    }

    // ========================================================
    // DEMAIS ARQUIVOS ESTÁTICOS
    // STALE WHILE REVALIDATE
    // ========================================================

    event.respondWith(

        (async () => {

            const cache = await caches.open(
                CACHE_VERSION
            );

            const salva = await cache.match(
                requisicao
            );

            const atualiza = fetch(requisicao)

                .then(async resposta => {

                    if (resposta && resposta.ok) {

                        await cache.put(
                            requisicao,
                            resposta.clone()
                        );

                    }

                    return resposta;

                });

            if (salva) {

                event.waitUntil(
                    atualiza.catch(() => undefined)
                );

                return salva;

            }

            try {

                return await atualiza;

            } catch (erro) {

                return Response.error();

            }

        })()

    );

});

// ============================================================
// NOTIFICAÇÕES PUSH
// ============================================================

self.addEventListener("push", event => {

    let dados = {};

    try {

        dados = event.data
            ? event.data.json()
            : {};

    } catch {

        dados = {

            titulo: "FlashMatty",

            corpo: event.data
                ? event.data.text()
                : ""

        };

    }

    const titulo = dados.titulo || "FlashMatty";

    const opcoes = {

        body:
            dados.corpo ||
            "Você recebeu uma nova notificação.",

        icon:
            "/static/img/icons/icon-192.png",

        badge:
            "/static/img/icons/badge-96.png",

        tag:
            dados.tag ||
            "flashmatty",

        renotify: true,

        data: {

            url:
                dados.url ||
                "/dashboard"

        }

    };

    event.waitUntil(

        self.registration.showNotification(
            titulo,
            opcoes
        )

    );

});

// ============================================================
// CLIQUE NA NOTIFICAÇÃO
// ============================================================

self.addEventListener("notificationclick", event => {

    event.notification.close();

    const destino =
        event.notification?.data?.url ||
        "/dashboard";

    let urlDestino;

    try {

        urlDestino = new URL(
            destino,
            self.location.origin
        );

    } catch {

        urlDestino = new URL(
            "/dashboard",
            self.location.origin
        );

    }

    // Impede redirecionamento externo.
    if (urlDestino.origin !== self.location.origin) {

        urlDestino = new URL(
            "/dashboard",
            self.location.origin
        );

    }

    event.waitUntil(

        clients.matchAll({

            type: "window",

            includeUncontrolled: true

        }).then(async janelas => {

            for (const janela of janelas) {

                if ("navigate" in janela) {

                    try {

                        const cliente = await janela.navigate(
                            urlDestino.href
                        );

                        if (cliente) {
                            return await cliente.focus();
                        }

                    } catch (erro) {

                        // Tenta outra janela.

                    }

                }

            }

            return clients.openWindow(
                urlDestino.href
            );

        })

    );

});

// ============================================================
// FIM DO SERVICE WORKER FLASHMATTY
// ============================================================
