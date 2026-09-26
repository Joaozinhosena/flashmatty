from flask import (
    Blueprint,
    jsonify,
    request,
)

from flask_login import (
    current_user,
    login_required,
)

from models import db

from .models import (
    AssinaturaPush,
    PreferenciaNotificacao,
)

from .push import (
    obter_chave_publica,
    push_configurado,
    enviar_push_usuario,
)


notificacoes_bp = Blueprint(
    "notificacoes",
    __name__,
    url_prefix="/notificacoes"
)


# ============================================================
# CHAVE PÚBLICA
# ============================================================

@notificacoes_bp.route(
    "/chave-publica"
)
@login_required
def chave_publica():

    if not push_configurado():

        return jsonify(
            erro=
                "Web Push ainda não foi configurado."
        ), 503


    return jsonify(
        chave=
            obter_chave_publica()
    )


# ============================================================
# SALVAR ASSINATURA
# ============================================================

@notificacoes_bp.route(
    "/assinar",
    methods=[
        "POST"
    ]
)
@login_required
def assinar():

    dados = (
        request.get_json(
            silent=True
        )
        or
        {}
    )


    assinatura = (
        dados.get(
            "subscription"
        )
        or
        {}
    )


    endpoint = (
        assinatura.get(
            "endpoint",
            ""
        )
        .strip()
    )


    chaves = (
        assinatura.get(
            "keys"
        )
        or
        {}
    )


    p256dh = (
        chaves.get(
            "p256dh",
            ""
        )
        .strip()
    )


    auth = (
        chaves.get(
            "auth",
            ""
        )
        .strip()
    )


    if (
        not endpoint
        or
        not p256dh
        or
        not auth
    ):

        return jsonify(
            erro=
                "Assinatura Push inválida."
        ), 400


    registro = (

        AssinaturaPush.query

        .filter_by(
            endpoint=endpoint
        )

        .first()
    )


    if not registro:

        registro = AssinaturaPush(

            usuario_id=
                current_user.id,

            endpoint=
                endpoint,

            p256dh=
                p256dh,

            auth=
                auth,

            user_agent=
                request.headers.get(
                    "User-Agent",
                    ""
                )[:500]

        )


        db.session.add(
            registro
        )

    else:

        registro.usuario_id = (
            current_user.id
        )

        registro.p256dh = (
            p256dh
        )

        registro.auth = (
            auth
        )

        registro.user_agent = (
            request.headers.get(
                "User-Agent",
                ""
            )[:500]
        )


    PreferenciaNotificacao.obter(
        current_user.id,
        criar=True
    )


    db.session.commit()


    


    return jsonify(
        ok=True
    )


# ============================================================
# CANCELAR ASSINATURA
# ============================================================

@notificacoes_bp.route(
    "/desassinar",
    methods=[
        "POST"
    ]
)
@login_required
def desassinar():

    dados = (
        request.get_json(
            silent=True
        )
        or
        {}
    )


    endpoint = (
        dados.get(
            "endpoint",
            ""
        )
        .strip()
    )


    if endpoint:

        registros = (

            AssinaturaPush.query

            .filter_by(
                usuario_id=
                    current_user.id,

                endpoint=
                    endpoint
            )

            .all()
        )


        for registro in registros:

            db.session.delete(
                registro
            )


        db.session.commit()


    return jsonify(
        ok=True
    )


# ============================================================
# PREFERÊNCIAS
# ============================================================

@notificacoes_bp.route(
    "/preferencias",
    methods=[
        "GET",
        "POST"
    ]
)
@login_required
def preferencias():

    preferencia = (
        PreferenciaNotificacao.obter(
            current_user.id,
            criar=True
        )
    )


    if request.method == "POST":

        dados = (
            request.get_json(
                silent=True
            )
            or
            {}
        )


        for campo in (
            "amizades",
            "desafios",
            "conquistas",
            "recompensas",
            "lembretes"
        ):

            if campo in dados:

                setattr(
                    preferencia,
                    campo,
                    bool(
                        dados[campo]
                    )
                )


        db.session.commit()


    else:

        db.session.commit()


    return jsonify(

        amizades=
            bool(
                preferencia.amizades
            ),

        desafios=
            bool(
                preferencia.desafios
            ),

        conquistas=
            bool(
                preferencia.conquistas
            ),

        recompensas=
            bool(
                preferencia.recompensas
            ),

        lembretes=
            bool(
                preferencia.lembretes
            )

    )


# ============================================================
# TESTE
# ============================================================

@notificacoes_bp.route(
    "/testar",
    methods=[
        "POST"
    ]
)
@login_required
def testar():

    quantidade = (
        enviar_push_usuario(

            current_user.id,

            "🔔 FlashMatty",

            "As notificações estão funcionando!",

            url="/dashboard",

            tag="teste"

        )
    )


    return jsonify(
        ok=True,
        enviados=quantidade
    )