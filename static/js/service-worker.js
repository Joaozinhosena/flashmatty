// ============================================================
// FLASHMATTY SERVICE WORKER
// ============================================================

self.addEventListener(
    "push",
    event => {

        let dados = {};


        try {

            dados =
                event.data
                    ? event.data.json()
                    : {};

        } catch {

            dados = {
                titulo:
                    "FlashMatty",

                corpo:
                    event.data
                        ? event.data.text()
                        : ""
            };

        }


        const titulo =
            dados.titulo
            ||
            "FlashMatty";


        const opcoes = {

            body:
                dados.corpo
                ||
                "Você recebeu uma nova notificação.",

            tag:
                dados.tag
                ||
                "flashmatty",

            renotify:
                true,

            data: {

                url:
                    dados.url
                    ||
                    "/dashboard"

            }

        };


        event.waitUntil(

            self.registration
                .showNotification(
                    titulo,
                    opcoes
                )

        );

    }
);


// ============================================================
// CLICAR NA NOTIFICAÇÃO
// ============================================================

self.addEventListener(
    "notificationclick",
    event => {

        event.notification.close();


        const destino =
            event.notification
                ?.data
                ?.url
            ||
            "/dashboard";


        event.waitUntil(

            clients
                .matchAll({
                    type:
                        "window",

                    includeUncontrolled:
                        true
                })

                .then(
                    janelas => {

                        for (
                            const janela
                            of
                            janelas
                        ) {

                            if (
                                "focus"
                                in
                                janela
                            ) {

                                janela.navigate(
                                    destino
                                );

                                return janela.focus();

                            }

                        }


                        return clients.openWindow(
                            destino
                        );

                    }
                )

        );

    }
);