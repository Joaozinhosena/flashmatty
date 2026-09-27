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


class CompraCosmetico(db.Model):

    __tablename__ = (
        "compra_cosmetico"
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

    item_id = db.Column(
        db.String(80),
        nullable=False,
        index=True
    )

    comprado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow
    )

    __table_args__ = (

        db.UniqueConstraint(
            "usuario_id",
            "item_id",
            name=(
                "uq_compra_cosmetico_"
                "usuario_item"
            )
        ),

    )


class PersonalizacaoPerfil(db.Model):

    __tablename__ = (
        "personalizacao_perfil"
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey(
            f"{USUARIO_TABLE}.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    titulo_id = db.Column(
        db.String(80),
        nullable=True
    )

    fundo_id = db.Column(
        db.String(80),
        nullable=True
    )

    moldura_id = db.Column(
        db.String(80),
        nullable=True
    )

    badge_id = db.Column(
        db.String(80),
        nullable=True
    )

    nome_id = db.Column(
        db.String(80),
        nullable=True
    )

    card_id = db.Column(
        db.String(80),
        nullable=True
    )

    efeito_id = db.Column(
        db.String(80),
        nullable=True
    )

    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow,
        onupdate=utcnow
    )

    @classmethod
    def obter(
        cls,
        usuario_id,
        criar=False
    ):

        usuario_id = int(
            usuario_id
        )

        registro = (
            db.session.get(
                cls,
                usuario_id
            )
        )

        if (
            registro is None
            and
            criar
        ):

            registro = cls(
                usuario_id=
                    usuario_id
            )

            db.session.add(
                registro
            )

        return registro
