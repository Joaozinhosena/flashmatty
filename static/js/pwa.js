// ============================================================
// FLASHMATTY PWA
// Registro do Service Worker + suporte ao prompt de instalação
// ============================================================

(() => {
    "use strict";

    let installPrompt = null;

    window.addEventListener("beforeinstallprompt", event => {
        event.preventDefault();
        installPrompt = event;
        window.dispatchEvent(new CustomEvent("flashmatty:pwa-install-ready"));
    });

    window.instalarFlashMatty = async function () {
        if (!installPrompt) {
            return false;
        }

        installPrompt.prompt();
        const escolha = await installPrompt.userChoice;
        installPrompt = null;
        return escolha.outcome === "accepted";
    };

    window.addEventListener("appinstalled", () => {
        installPrompt = null;
        window.dispatchEvent(new CustomEvent("flashmatty:pwa-installed"));
    });

    if (!("serviceWorker" in navigator)) {
        return;
    }

    window.addEventListener("load", async () => {
        try {
            await navigator.serviceWorker.register(
                "/service-worker.js",
                { scope: "/" }
            );
        } catch (erro) {
            console.error("FlashMatty: falha ao registrar Service Worker.", erro);
        }
    });
})();
