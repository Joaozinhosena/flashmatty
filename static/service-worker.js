// ============================================================
// FLASHMATTY SERVICE WORKER
// PWA + CACHE SEGURO DE ARQUIVOS ESTÁTICOS + PUSH
// ============================================================

const CACHE_VERSION = "flashmatty-static-v1";

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

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_VERSION)
            .then(cache => cache.addAll(PRECACHE))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys()
            .then(nomes => Promise.all(
                nomes.map(nome => {
                    if (nome.startsWith("flashmatty-") && nome !== CACHE_VERSION) {
                        return caches.delete(nome);
                    }
                    return Promise.resolve(false);
                })
            ))
            .then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", event => {
    const requisicao = event.request;

    if (requisicao.method !== "GET") {
        return;
    }

    const url = new URL(requisicao.url);

    // Não intercepta CDN/outros domínios.
    if (url.origin !== self.location.origin) {
        return;
    }

    // Páginas autenticadas/HTML sempre vêm da rede.
    // Isso evita guardar conteúdo privado de uma conta em cache.
    if (requisicao.mode === "navigate") {
        return;
    }

    if (!url.pathname.startsWith("/static/")) {
        return;
    }

    // Static: stale-while-revalidate.
    event.respondWith(
        caches.open(CACHE_VERSION).then(async cache => {
            const salva = await cache.match(requisicao);

            const atualiza = fetch(requisicao)
                .then(resposta => {
                    if (resposta && resposta.ok) {
                        cache.put(requisicao, resposta.clone());
                    }
                    return resposta;
                });

            if (salva) {
                event.waitUntil(atualiza.catch(() => undefined));
                return salva;
            }

            return atualiza;
        })
    );
});

// ============================================================
// PUSH
// ============================================================

self.addEventListener("push", event => {
    let dados = {};

    try {
        dados = event.data ? event.data.json() : {};
    } catch {
        dados = {
            titulo: "FlashMatty",
            corpo: event.data ? event.data.text() : ""
        };
    }

    const titulo = dados.titulo || "FlashMatty";

    const opcoes = {
        body: dados.corpo || "Você recebeu uma nova notificação.",
        icon: "/static/img/icons/icon-192.png",
        badge: "/static/img/icons/badge-96.png",
        tag: dados.tag || "flashmatty",
        renotify: true,
        data: {
            url: dados.url || "/dashboard"
        }
    };

    event.waitUntil(
        self.registration.showNotification(titulo, opcoes)
    );
});

// ============================================================
// CLIQUE NA NOTIFICAÇÃO
// ============================================================

self.addEventListener("notificationclick", event => {
    event.notification.close();

    const destino = event.notification?.data?.url || "/dashboard";
    const urlDestino = new URL(destino, self.location.origin).href;

    event.waitUntil(
        clients.matchAll({
            type: "window",
            includeUncontrolled: true
        }).then(janelas => {
            for (const janela of janelas) {
                if ("navigate" in janela) {
                    janela.navigate(urlDestino);
                    return janela.focus();
                }
            }

            return clients.openWindow(urlDestino);
        })
    );
});
