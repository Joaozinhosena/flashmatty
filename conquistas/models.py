from datetime import datetime

from models import (
    db,
    Usuario,
)


USUARIO_TABLE = (
    Usuario.__tablename__
)


def utcnow():
    return datetime.utcnow()


class ConquistaUsuario(db.Model):

    __tablename__ = (
        "conquista_usuario"
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey(
            f"{USUARIO_TABLE}.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    conquista_id = db.Column(
        db.String(80),
        nullable=False,
        index=True
    )

    valor_desbloqueio = db.Column(
        db.Float,
        nullable=True
    )

    desbloqueada_em = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow
    )

    __table_args__ = (

        db.UniqueConstraint(
            "usuario_id",
            "conquista_id",
            name=(
                "uq_conquista_usuario_"
                "usuario_conquista"
            )
        ),

    )


class HistoricoMultiplayer(db.Model):

    __tablename__ = (
        "historico_multiplayer"
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    partida_id = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey(
            f"{USUARIO_TABLE}.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    sala_codigo = db.Column(
        db.String(12),
        nullable=False
    )

    posicao = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    pontos = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    acertos = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    erros = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    total_questoes = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    venceu = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    perfeita = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    jogada_em = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow,
        index=True
    )

    __table_args__ = (

        db.UniqueConstraint(
            "partida_id",
            "usuario_id",
            name=(
                "uq_historico_multiplayer_"
                "partida_usuario"
            )
        ),

    )
