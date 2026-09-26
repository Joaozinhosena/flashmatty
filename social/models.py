from datetime import datetime

from models import db, Usuario


def utcnow():
    return datetime.utcnow()


USUARIO_TABLE = Usuario.__tablename__


class PerfilUsuario(db.Model):
    __tablename__ = "perfil_usuario"

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{USUARIO_TABLE}.id", ondelete="CASCADE"),
        primary_key=True,
    )

    bio = db.Column(
        db.String(160),
        nullable=False,
        default="",
    )

    # Opções: todos | amigos | privado
    visibilidade_progresso = db.Column(
        db.String(20),
        nullable=False,
        default="amigos",
    )

    # A foto é salva no banco.
    foto_dados = db.Column(
        db.LargeBinary,
        nullable=True,
    )

    foto_mime = db.Column(
        db.String(50),
        nullable=True,
    )

    ultimo_acesso = db.Column(
        db.DateTime,
        nullable=True,
    )

    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
    )

    @classmethod
    def obter(cls, usuario_id, criar=False):
        perfil = db.session.get(cls, int(usuario_id))

        if perfil is None and criar:
            perfil = cls(
                usuario_id=int(usuario_id),
                bio="",
                visibilidade_progresso="amigos",
            )
            db.session.add(perfil)

        return perfil


class Amizade(db.Model):
    __tablename__ = "amizade"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    solicitante_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{USUARIO_TABLE}.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    destinatario_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{USUARIO_TABLE}.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # pendente | aceita | recusada
    status = db.Column(
        db.String(20),
        nullable=False,
        default="pendente",
        index=True,
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow,
    )

    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=utcnow,
        onupdate=utcnow,
    )

    __table_args__ = (
        db.CheckConstraint(
            "solicitante_id <> destinatario_id",
            name="ck_amizade_usuarios_diferentes",
        ),
    )
