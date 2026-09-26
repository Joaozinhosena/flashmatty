import json
import os

from flask import current_app

from pywebpush import (
    webpush,
    WebPushException,
)

from models import db

from .models import (
    AssinaturaPush,
    PreferenciaNotificacao,
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

def obter_configuracao_vapid():

    return {

        "publica":
            os.getenv(
                "VAPID_PUBLIC_KEY",
                ""
            ).strip(),

        "privada":
            os.getenv(
                "VAPID_PRIVATE_KEY",
                ""
            ).strip(),

        "subject":
            os.getenv(
                "VAPID_SUBJECT",
                ""
            ).strip()

    }


def push_configurado():

    configuracao = (
        obter_configuracao_vapid()
    )

    return bool(
        configuracao["publica"]
        and
        configuracao["privada"]
        and
        configuracao["subject"]
    )


def obter_chave_publica():

    return (
        obter_configuracao_vapid()[
            "publica"
        ]
    )


# ============================================================
# VERIFICAR PREFERÊNCIA
# ============================================================

def categoria_permitida(
    usuario_id,
    categoria
):

    preferencia = (
        PreferenciaNotificacao
        .query
        .filter_by(
            usuario_id=usuario_id
        )
        .first()
    )


    if not preferencia:

        return True


    mapa = {

        "amizades":
            "amizades",

        "desafios":
            "desafios",

        "conquistas":
            "conquistas",

        "recompensas":
            "recompensas",

        "lembretes":
            "lembretes",

    }


    campo = mapa.get(
        categoria
    )


    if not campo:

        return True


    return bool(
        getattr(
            preferencia,
            campo,
            True
        )
    )


# ============================================================
# ENVIAR PUSH
# ============================================================

def enviar_push_usuario(
    usuario_id,
    titulo,
    corpo,
    url="/dashboard",
    categoria=None,
    tag=None,
    ttl=3600
):

    if not push_configurado():

        current_app.logger.warning(
            "Web Push não configurado."
        )

        return 0


    if (
        categoria
        and
        not categoria_permitida(
            usuario_id,
            categoria
        )
    ):

        return 0


    assinaturas = (

        AssinaturaPush.query

        .filter_by(
            usuario_id=usuario_id
        )

        .all()
    )


    if not assinaturas:

        return 0


    configuracao = (
        obter_configuracao_vapid()
    )


    payload = json.dumps(
        {
            "titulo":
                titulo,

            "corpo":
                corpo,

            "url":
                url,

            "tag":
                tag
                or
                categoria
                or
                "flashmatty"
        },
        ensure_ascii=False
    )


    enviados = 0

    remover = []


    for assinatura in assinaturas:

        try:

            webpush(

                subscription_info={
                    "endpoint":
                        assinatura.endpoint,

                    "keys": {
                        "p256dh":
                            assinatura.p256dh,

                        "auth":
                            assinatura.auth
                    }
                },

                data=payload,

                vapid_private_key=
                    configuracao[
                        "privada"
                    ],

                vapid_claims={
                    "sub":
                        configuracao[
                            "subject"
                        ]
                },

                ttl=ttl

            )


            enviados += 1


        except WebPushException as erro:

            resposta = getattr(
                erro,
                "response",
                None
            )


            status = getattr(
                resposta,
                "status_code",
                None
            )


            # Assinatura deixou de existir.
            if status in (
                404,
                410
            ):

                remover.append(
                    assinatura
                )

            else:

                current_app.logger.warning(
                    "Erro Web Push: %s",
                    erro
                )


        except Exception as erro:

            current_app.logger.exception(
                "Erro ao enviar notificação: %s",
                erro
            )


    for assinatura in remover:

        db.session.delete(
            assinatura
        )


    if remover:

        db.session.commit()


    return enviados