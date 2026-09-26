from datetime import datetime

from models import db


# ============================================================
# ASSINATURA PUSH
# ============================================================

class AssinaturaPush(db.Model):

    __tablename__ = "assinaturas_push"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        nullable=False,
        index=True
    )

    endpoint = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    p256dh = db.Column(
        db.Text,
        nullable=False
    )

    auth = db.Column(
        db.Text,
        nullable=False
    )

    user_agent = db.Column(
        db.String(500),
        nullable=True
    )

    criada_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    atualizada_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# ============================================================
# PREFERÊNCIAS
# ============================================================

class PreferenciaNotificacao(db.Model):

    __tablename__ = "preferencias_notificacoes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
        index=True
    )

    amizades = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    desafios = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    conquistas = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    recompensas = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    lembretes = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )


    @classmethod
    def obter(
        cls,
        usuario_id,
        criar=True
    ):

        preferencia = (
            cls.query
            .filter_by(
                usuario_id=usuario_id
            )
            .first()
        )


        if (
            not preferencia
            and
            criar
        ):

            preferencia = cls(
                usuario_id=usuario_id
            )

            db.session.add(
                preferencia
            )


        return preferencia