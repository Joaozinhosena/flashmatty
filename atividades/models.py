from datetime import datetime

from models import db


# ============================================================
# BANCO PEDAGÓGICO DE QUESTÕES
# ============================================================

class QuestaoBanco(db.Model):

    __tablename__ = "questao_banco"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    codigo = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
        index=True
    )

    # IDs usados pelo curriculum.py.
    ano = db.Column(
        db.String(30),
        nullable=False,
        index=True
    )

    tema = db.Column(
        db.String(60),
        nullable=False,
        index=True
    )

    assunto = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    # Pode ficar vazio para uma questão válida em qualquer
    # etapa daquele assunto/tipo.
    etapa = db.Column(
        db.String(30),
        nullable=True,
        index=True
    )

    # Mesmo identificador usado em dados_etapa["tipo"].
    tipo = db.Column(
        db.String(60),
        nullable=False,
        index=True
    )

    # numero, multipla_escolha, verdadeiro_falso etc.
    tipo_ui = db.Column(
        db.String(40),
        nullable=False,
        default="multipla_escolha"
    )

    enunciado = db.Column(
        db.Text,
        nullable=False
    )

    resposta_correta = db.Column(
        db.String(255),
        nullable=False
    )

    explicacao = db.Column(
        db.Text,
        nullable=True
    )

    instrucao = db.Column(
        db.Text,
        nullable=True
    )

    habilidade_bncc = db.Column(
        db.String(80),
        nullable=True,
        index=True
    )

    dificuldade = db.Column(
        db.Integer,
        nullable=False,
        default=2,
        index=True
    )

    # JSON opcional compatível com a chave "visual" do game.py.
    visual_json = db.Column(
        db.Text,
        nullable=True
    )

    autor = db.Column(
        db.String(150),
        nullable=True
    )

    instituicao = db.Column(
        db.String(150),
        nullable=True
    )

    fonte = db.Column(
        db.String(500),
        nullable=True
    )

    licenca = db.Column(
        db.String(120),
        nullable=True
    )

    revisada = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        index=True
    )

    ativa = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        index=True
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    alternativas = db.relationship(
        "AlternativaQuestao",
        backref="questao",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="AlternativaQuestao.ordem"
    )


# ============================================================
# ALTERNATIVAS
# ============================================================

class AlternativaQuestao(db.Model):

    __tablename__ = "alternativa_questao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    questao_id = db.Column(
        db.Integer,
        db.ForeignKey("questao_banco.id"),
        nullable=False,
        index=True
    )

    valor = db.Column(
        db.String(255),
        nullable=False
    )

    texto = db.Column(
        db.Text,
        nullable=False
    )

    imagem = db.Column(
        db.String(500),
        nullable=True
    )

    ordem = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    __table_args__ = (
        db.UniqueConstraint(
            "questao_id",
            "valor",
            name="uq_alternativa_questao_valor"
        ),
    )


# ============================================================
# ATIVIDADES MONTADAS POR PROFESSORES
# ============================================================

class Atividade(db.Model):

    __tablename__ = "atividade"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    codigo = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
        index=True
    )

    titulo = db.Column(
        db.String(180),
        nullable=False
    )

    descricao = db.Column(
        db.Text,
        nullable=True
    )

    ano = db.Column(
        db.String(30),
        nullable=False,
        index=True
    )

    tema = db.Column(
        db.String(60),
        nullable=True,
        index=True
    )

    assunto = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    autor = db.Column(
        db.String(150),
        nullable=True
    )

    instituicao = db.Column(
        db.String(150),
        nullable=True
    )

    publicada = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    ativa = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    questoes = db.relationship(
        "AtividadeQuestao",
        backref="atividade",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="AtividadeQuestao.ordem"
    )


class AtividadeQuestao(db.Model):

    __tablename__ = "atividade_questao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    atividade_id = db.Column(
        db.Integer,
        db.ForeignKey("atividade.id"),
        nullable=False,
        index=True
    )

    questao_id = db.Column(
        db.Integer,
        db.ForeignKey("questao_banco.id"),
        nullable=False,
        index=True
    )

    ordem = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    questao = db.relationship(
        "QuestaoBanco"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "atividade_id",
            "questao_id",
            name="uq_atividade_questao"
        ),
    )


# ============================================================
# HISTÓRICO DO ALUNO POR QUESTÃO FIXA
# ============================================================

class HistoricoQuestao(db.Model):

    __tablename__ = "historico_questao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False,
        index=True
    )

    questao_id = db.Column(
        db.Integer,
        db.ForeignKey("questao_banco.id"),
        nullable=False,
        index=True
    )

    atividade_id = db.Column(
        db.Integer,
        db.ForeignKey("atividade.id"),
        nullable=True,
        index=True
    )

    resposta_usuario = db.Column(
        db.String(255),
        nullable=True
    )

    acertou = db.Column(
        db.Boolean,
        nullable=False,
        index=True
    )

    respondida_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )

    questao = db.relationship(
        "QuestaoBanco"
    )

    atividade = db.relationship(
        "Atividade"
    )

    __table_args__ = (
        db.Index(
            "ix_historico_usuario_questao",
            "usuario_id",
            "questao_id"
        ),
    )



# ============================================================
# REVISÃO HUMANA DA QUESTÃO
# ============================================================

class RevisaoQuestao(db.Model):

    __tablename__ = "revisao_questao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    questao_id = db.Column(
        db.Integer,
        db.ForeignKey("questao_banco.id"),
        nullable=False,
        index=True
    )

    revisor = db.Column(
        db.String(150),
        nullable=False
    )

    instituicao = db.Column(
        db.String(150),
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    observacao = db.Column(
        db.Text,
        nullable=True
    )

    revisado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )

    questao = db.relationship(
        "QuestaoBanco"
    )
