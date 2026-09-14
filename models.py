from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()








# ============================================================
# USUÁRIO
# ============================================================

class Usuario(UserMixin, db.Model):

    __tablename__ = "usuario"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(80),
        nullable=False
    )

    username = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )

    xp = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    moedas = db.Column(
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

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    @property
    def nivel(self):

        return ((self.xp or 0) // 100) + 1

    @property
    def progresso_nivel(self):

        return (self.xp or 0) % 100

    @property
    def total_respostas(self):

        return (
            (self.acertos or 0)
            +
            (self.erros or 0)
        )

    @property
    def precisao(self):

        if self.total_respostas == 0:
            return 0

        return round(
            (self.acertos or 0)
            /
            self.total_respostas
            *
            100
        )


# ============================================================
# PROGRESSO DO ASSUNTO
# ============================================================

class ProgressoAssunto(db.Model):

    __tablename__ = "progresso_assunto"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    ano = db.Column(
        db.String(30),
        nullable=False
    )

    tema = db.Column(
        db.String(60),
        nullable=False
    )

    assunto = db.Column(
        db.String(100),
        nullable=False
    )

    concluido = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    __table_args__ = (

        db.UniqueConstraint(
            "usuario_id",
            "ano",
            "tema",
            "assunto",
            name="uq_progresso_assunto"
        ),

    )


# ============================================================
# PROGRESSO DAS ETAPAS
# ============================================================

class ProgressoEtapa(db.Model):

    __tablename__ = "progresso_etapa"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    ano = db.Column(
        db.String(30),
        nullable=False
    )

    tema = db.Column(
        db.String(60),
        nullable=False
    )

    assunto = db.Column(
        db.String(100),
        nullable=False
    )

    etapa = db.Column(
        db.String(30),
        nullable=False
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

    xp = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    tentativas = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    melhor_pontuacao = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    concluida = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    __table_args__ = (

        db.UniqueConstraint(
            "usuario_id",
            "ano",
            "tema",
            "assunto",
            "etapa",
            name="uq_progresso_etapa"
        ),

    )

    @property
    def total(self):

        return (
            (self.acertos or 0)
            +
            (self.erros or 0)
        )

    @property
    def dominio(self):

        if self.total == 0:
            return 0

        return round(
            (self.acertos or 0)
            /
            self.total
            *
            100
        )


# ============================================================
# HISTÓRICO
# ============================================================

class Resposta(db.Model):

    __tablename__ = "resposta"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    ano = db.Column(
        db.String(30),
        nullable=False
    )

    tema = db.Column(
        db.String(60),
        nullable=False
    )

    assunto = db.Column(
        db.String(100),
        nullable=False
    )

    etapa = db.Column(
        db.String(30),
        nullable=False
    )

    pergunta = db.Column(
        db.Text,
        nullable=False
    )

    resposta_usuario = db.Column(
        db.String(100)
    )

    resposta_correta = db.Column(
        db.String(100),
        nullable=False
    )

    acertou = db.Column(
        db.Boolean,
        nullable=False
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )