from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    session,
    abort
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import (
    db,
    Usuario,
    ProgressoAssunto,
    ProgressoEtapa,
    Resposta
)

from curriculum import CURRICULO
from game import gerar_questao

# MULTIPLAYER
from multiplayer import socketio
from multiplayer.routes import multiplayer_bp


# ============================================================
# APP
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "matematica-kids-desenvolvimento"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///matematica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# ============================================================
# BANCO
# ============================================================

db.init_app(app)

# ============================================================
# LOGIN
# ============================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = "Faça login para continuar."


@login_manager.user_loader
def carregar_usuario(user_id):
    """
    Informa ao Flask-Login como recuperar o usuário
    salvo na sessão.
    """

    try:
        return db.session.get(
            Usuario,
            int(user_id)
        )

    except (ValueError, TypeError):
        return None


# ============================================================
# MULTIPLAYER
# ============================================================

socketio.init_app(
    app,
    cors_allowed_origins="*"
)

app.register_blueprint(
    multiplayer_bp
)

# Importa os eventos somente depois de
# SocketIO e Blueprint estarem configurados.
import multiplayer.socket_events


# ============================================================
# BANCO - CRIA TABELAS
# ============================================================

with app.app_context():
    db.create_all()



    
# ============================================================
# FUNÇÕES
# ============================================================

def buscar_ano(ano_id):

    ano = CURRICULO.get(ano_id)

    if not ano:
        abort(404)

    return ano


def buscar_tema(
    ano,
    tema_id
):

    tema = ano.get(
        "temas",
        {}
    ).get(
        tema_id
    )

    if not tema:
        abort(404)

    return tema


def buscar_assunto(
    tema,
    assunto_id
):

    assunto = tema.get(
        "assuntos",
        {}
    ).get(
        assunto_id
    )

    if not assunto:
        abort(404)

    return assunto


def buscar_etapa(
    assunto,
    etapa_id
):

    etapa = assunto.get(
        "etapas",
        {}
    ).get(
        etapa_id
    )

    if not etapa:
        abort(404)

    return etapa


def corrigir_usuario(usuario):

    usuario.xp = usuario.xp or 0
    usuario.moedas = usuario.moedas or 0
    usuario.acertos = usuario.acertos or 0
    usuario.erros = usuario.erros or 0


def obter_progresso_etapa(
    ano_id,
    tema_id,
    assunto_id,
    etapa_id,
    criar=False
):

    progresso = (
        ProgressoEtapa.query
        .filter_by(
            usuario_id=current_user.id,
            ano=ano_id,
            tema=tema_id,
            assunto=assunto_id,
            etapa=etapa_id
        )
        .first()
    )

    if not progresso and criar:

        progresso = ProgressoEtapa(

            usuario_id=current_user.id,

            ano=ano_id,

            tema=tema_id,

            assunto=assunto_id,

            etapa=etapa_id,

            acertos=0,

            erros=0,

            xp=0,

            tentativas=0,

            melhor_pontuacao=0,

            concluida=False
        )

        db.session.add(
            progresso
        )

    return progresso


def obter_progresso_assunto(
    ano_id,
    tema_id,
    assunto_id,
    criar=False
):

    progresso = (
        ProgressoAssunto.query
        .filter_by(
            usuario_id=current_user.id,
            ano=ano_id,
            tema=tema_id,
            assunto=assunto_id
        )
        .first()
    )

    if not progresso and criar:

        progresso = ProgressoAssunto(

            usuario_id=current_user.id,

            ano=ano_id,

            tema=tema_id,

            assunto=assunto_id,

            concluido=False
        )

        db.session.add(
            progresso
        )

    return progresso


def etapa_liberada(
    assunto,
    ano_id,
    tema_id,
    assunto_id,
    etapa_id
):

    ids = list(
        assunto["etapas"].keys()
    )

    indice = ids.index(
        etapa_id
    )

    # Primeira etapa sempre liberada
    if indice == 0:
        return True

    etapa_anterior = ids[
        indice - 1
    ]

    progresso_anterior = (
        obter_progresso_etapa(
            ano_id,
            tema_id,
            assunto_id,
            etapa_anterior
        )
    )

    return bool(
        progresso_anterior
        and
        progresso_anterior.concluida
    )


def atualizar_assunto(
    ano_id,
    tema_id,
    assunto_id,
    assunto
):

    progresso_assunto = (
        obter_progresso_assunto(
            ano_id,
            tema_id,
            assunto_id,
            criar=True
        )
    )

    todas_concluidas = True

    for etapa_id in assunto[
        "etapas"
    ].keys():

        progresso = (
            obter_progresso_etapa(
                ano_id,
                tema_id,
                assunto_id,
                etapa_id
            )
        )

        if (
            not progresso
            or
            not progresso.concluida
        ):

            todas_concluidas = False
            break

    # Uma vez concluído, permanece concluído.
    if todas_concluidas:

        progresso_assunto.concluido = True

    return progresso_assunto


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


# ============================================================
# CADASTRO
# ============================================================

@app.route(
    "/cadastro",
    methods=["GET", "POST"]
)
def cadastro():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    if request.method == "POST":

        nome = request.form.get(
            "nome",
            ""
        ).strip()

        username = request.form.get(
            "username",
            ""
        ).strip()

        senha = request.form.get(
            "senha",
            ""
        )

        confirmar = request.form.get(
            "confirmar_senha",
            ""
        )

        if not nome or not username or not senha:

            flash(
                "Preencha todos os campos."
            )

            return redirect(
                url_for("cadastro")
            )

        if senha != confirmar:

            flash(
                "As senhas não são iguais."
            )

            return redirect(
                url_for("cadastro")
            )

        existente = (
            Usuario.query
            .filter_by(
                username=username
            )
            .first()
        )

        if existente:

            flash(
                "Usuário já existe."
            )

            return redirect(
                url_for("cadastro")
            )

        usuario = Usuario(

            nome=nome,

            username=username,

            senha=generate_password_hash(
                senha
            ),

            xp=0,
            moedas=0,
            acertos=0,
            erros=0
        )

        db.session.add(
            usuario
        )

        db.session.commit()

        login_user(
            usuario
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "cadastro.html"
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        senha = request.form.get(
            "senha",
            ""
        )

        usuario = (
            Usuario.query
            .filter_by(
                username=username
            )
            .first()
        )

        if (
            not usuario
            or
            not check_password_hash(
                usuario.senha,
                senha
            )
        ):

            flash(
                "Usuário ou senha incorretos."
            )

            return redirect(
                url_for("login")
            )

        corrigir_usuario(
            usuario
        )

        db.session.commit()

        login_user(
            usuario
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    corrigir_usuario(
        current_user
    )

    db.session.commit()

    return render_template(
        "dashboard.html"
    )


# ============================================================
# JORNADA
# ============================================================

@app.route("/jornada")
@login_required
def jornada():

    anos = sorted(
        CURRICULO.items(),
        key=lambda x: x[1]["ordem"]
    )

    progresso_anos = {}

    for ano_id, ano in anos:

        total = 0
        concluidos = 0

        for tema_id, tema in ano[
            "temas"
        ].items():

            for assunto_id, assunto in tema[
                "assuntos"
            ].items():

                total += 1

                progresso = (
                    obter_progresso_assunto(
                        ano_id,
                        tema_id,
                        assunto_id
                    )
                )

                if (
                    progresso
                    and
                    progresso.concluido
                ):

                    concluidos += 1

        progresso_anos[
            ano_id
        ] = round(
            concluidos / total * 100
        ) if total else 0

    return render_template(
        "jornada.html",
        anos=anos,
        progresso_anos=progresso_anos
    )


# ============================================================
# ANO
# ============================================================

@app.route(
    "/ano/<ano_id>"
)
@login_required
def ano(ano_id):

    dados_ano = buscar_ano(
        ano_id
    )

    return render_template(
        "ano.html",
        ano=dados_ano,
        ano_id=ano_id
    )


# ============================================================
# TEMA
# ============================================================

@app.route(
    "/ano/<ano_id>/tema/<tema_id>"
)
@login_required
def tema(
    ano_id,
    tema_id
):

    dados_ano = buscar_ano(
        ano_id
    )

    dados_tema = buscar_tema(
        dados_ano,
        tema_id
    )

    progressos = {}

    for assunto_id in dados_tema[
        "assuntos"
    ]:

        progressos[
            assunto_id
        ] = obter_progresso_assunto(
            ano_id,
            tema_id,
            assunto_id
        )

    return render_template(
        "tema.html",

        ano=dados_ano,
        ano_id=ano_id,

        tema=dados_tema,
        tema_id=tema_id,

        progressos=progressos
    )


# ============================================================
# TRILHA DO ASSUNTO
# ============================================================

@app.route(
    "/ano/<ano_id>/tema/<tema_id>/assunto/<assunto_id>"
)
@login_required
def assunto(
    ano_id,
    tema_id,
    assunto_id
):

    dados_ano = buscar_ano(
        ano_id
    )

    dados_tema = buscar_tema(
        dados_ano,
        tema_id
    )

    dados_assunto = buscar_assunto(
        dados_tema,
        assunto_id
    )

    progressos = {}

    for etapa_id in dados_assunto[
        "etapas"
    ]:

        progresso = (
            obter_progresso_etapa(
                ano_id,
                tema_id,
                assunto_id,
                etapa_id
            )
        )

        progressos[
            etapa_id
        ] = {

            "progresso": progresso,

            "liberada": etapa_liberada(
                dados_assunto,
                ano_id,
                tema_id,
                assunto_id,
                etapa_id
            )
        }

    progresso_assunto = (
        atualizar_assunto(
            ano_id,
            tema_id,
            assunto_id,
            dados_assunto
        )
    )

    db.session.commit()

    return render_template(
        "assunto.html",

        ano=dados_ano,
        ano_id=ano_id,

        tema=dados_tema,
        tema_id=tema_id,

        assunto=dados_assunto,
        assunto_id=assunto_id,

        progressos=progressos,

        progresso_assunto=progresso_assunto
    )


# ============================================================
# ETAPA
# ============================================================

@app.route(
    "/etapa/<ano_id>/<tema_id>/<assunto_id>/<etapa_id>"
)
@login_required
def etapa(
    ano_id,
    tema_id,
    assunto_id,
    etapa_id
):

    ano = buscar_ano(
        ano_id
    )

    tema = buscar_tema(
        ano,
        tema_id
    )

    assunto = buscar_assunto(
        tema,
        assunto_id
    )

    etapa = buscar_etapa(
        assunto,
        etapa_id
    )

    if not etapa_liberada(
        assunto,
        ano_id,
        tema_id,
        assunto_id,
        etapa_id
    ):

        flash(
            "Conclua a etapa anterior primeiro. 🔒"
        )

        return redirect(
            url_for(
                "assunto",
                ano_id=ano_id,
                tema_id=tema_id,
                assunto_id=assunto_id
            )
        )

    nova_questao = gerar_questao(
        etapa["tipo"]
    )

    # Cada acesso inicia uma tentativa
    session["tentativa"] = {

        "ano": ano_id,
        "tema": tema_id,
        "assunto": assunto_id,
        "etapa": etapa_id,

        "respondidas": 0,
        "acertos": 0,

        "quantidade":
            etapa["quantidade"],

        "pergunta":
            nova_questao["pergunta"],

        "resposta":
            nova_questao["resposta"],

        "tipo":
            etapa["tipo"]
    }

    session.modified = True

    return render_template(
        "etapa.html",

        ano=ano,

        tema=tema,

        assunto=assunto,

        etapa=etapa,

        etapa_id=etapa_id,

        questao=nova_questao
    )


# ============================================================
# API RESPONDER
# ============================================================

@app.route(
    "/api/responder",
    methods=["POST"]
)
@login_required
def responder():

    try:

        dados = (
            request.get_json(
                silent=True
            )
            or {}
        )

        resposta_usuario = str(
            dados.get(
                "resposta",
                ""
            )
        ).strip()

        if not resposta_usuario:

            return jsonify(
                erro="Digite uma resposta."
            ), 400

        tentativa = session.get(
            "tentativa"
        )

        if not tentativa:

            return jsonify(
                erro="A tentativa expirou."
            ), 400

        correta = str(
            tentativa["resposta"]
        ).strip()

        normal_usuario = (
            resposta_usuario
            .casefold()
            .replace(",", ".")
        )

        normal_correta = (
            correta
            .casefold()
            .replace(",", ".")
        )

        acertou = (
            normal_usuario
            ==
            normal_correta
        )

        corrigir_usuario(
            current_user
        )

        # ----------------------------------------------------
        # DADOS DO PROGRESSO
        # ----------------------------------------------------

        progresso = (
            obter_progresso_etapa(

                tentativa["ano"],
                tentativa["tema"],
                tentativa["assunto"],
                tentativa["etapa"],

                criar=True
            )
        )

        progresso.acertos = (
            progresso.acertos or 0
        )

        progresso.erros = (
            progresso.erros or 0
        )

        progresso.xp = (
            progresso.xp or 0
        )

        progresso.tentativas = (
            progresso.tentativas or 0
        )

        progresso.melhor_pontuacao = (
            progresso.melhor_pontuacao or 0
        )

        # ----------------------------------------------------
        # ACERTO / ERRO
        # ----------------------------------------------------

        if acertou:

            tentativa[
                "acertos"
            ] += 1

            progresso.acertos += 1

            progresso.xp += 10

            current_user.acertos += 1

            current_user.xp += 10

            current_user.moedas += 2

            mensagem = (
                "Muito bem! 🎉"
            )

        else:

            progresso.erros += 1

            current_user.erros += 1

            mensagem = (
                f"Quase! A resposta era {correta}."
            )

        tentativa[
            "respondidas"
        ] += 1

        # ----------------------------------------------------
        # HISTÓRICO
        # ----------------------------------------------------

        registro = Resposta(

            usuario_id=current_user.id,

            ano=tentativa["ano"],

            tema=tentativa["tema"],

            assunto=tentativa[
                "assunto"
            ],

            etapa=tentativa[
                "etapa"
            ],

            pergunta=tentativa[
                "pergunta"
            ],

            resposta_usuario=(
                resposta_usuario
            ),

            resposta_correta=correta,

            acertou=acertou
        )

        db.session.add(
            registro
        )

        # ----------------------------------------------------
        # TERMINOU A ETAPA?
        # ----------------------------------------------------

        terminou = (
            tentativa[
                "respondidas"
            ]
            >=
            tentativa[
                "quantidade"
            ]
        )

        if terminou:

            quantidade = tentativa[
                "quantidade"
            ]

            acertos_tentativa = tentativa[
                "acertos"
            ]

            pontuacao = round(
                acertos_tentativa
                /
                quantidade
                *
                100
            )

            progresso.tentativas += 1

            if (
                pontuacao
                >
                progresso.melhor_pontuacao
            ):

                progresso.melhor_pontuacao = (
                    pontuacao
                )

            # 80% para passar
            passou = (
                pontuacao >= 80
            )


            ja_estava_concluida = bool(progresso.concluida)

            # Nunca perde uma conclusão antiga
            if passou:

                progresso.concluida = True

                if not ja_estava_concluida:
                    
                    # bônus por concluir
                    current_user.xp += 20
                    
                    current_user.moedas += 5


            # ------------------------------------------------
            # VERIFICAR ASSUNTO
            # ------------------------------------------------

            ano = buscar_ano(
                tentativa["ano"]
            )

            tema = buscar_tema(
                ano,
                tentativa["tema"]
            )

            assunto = buscar_assunto(
                tema,
                tentativa["assunto"]
            )

            progresso_assunto = (
                atualizar_assunto(

                    tentativa["ano"],

                    tentativa["tema"],

                    tentativa[
                        "assunto"
                    ],

                    assunto
                )
            )

            assunto_concluido = bool(
                progresso_assunto.concluido
            )

            db.session.commit()

            session.pop(
                "tentativa",
                None
            )

            return jsonify(

                terminou=True,

                correto=acertou,

                mensagem=mensagem,

                passou=passou,

                pontuacao=pontuacao,

                acertos=acertos_tentativa,

                quantidade=quantidade,

                xp=current_user.xp,

                moedas=current_user.moedas,

                assunto_concluido=(
                    assunto_concluido
                )
            )

        # ----------------------------------------------------
        # PRÓXIMA QUESTÃO
        # ----------------------------------------------------

        nova_questao = gerar_questao(
            tentativa["tipo"]
        )

        tentativa[
            "pergunta"
        ] = nova_questao[
            "pergunta"
        ]

        tentativa[
            "resposta"
        ] = nova_questao[
            "resposta"
        ]

        session[
            "tentativa"
        ] = tentativa

        session.modified = True

        db.session.commit()

        return jsonify(

            terminou=False,

            correto=acertou,

            mensagem=mensagem,

            xp=current_user.xp,

            moedas=current_user.moedas,

            respondidas=tentativa[
                "respondidas"
            ],

            quantidade=tentativa[
                "quantidade"
            ],

            questao={
                "pergunta":
                    nova_questao[
                        "pergunta"
                    ]
            }
        )

    except Exception as erro:

        db.session.rollback()

        print(
            "ERRO /api/responder:",
            erro
        )

        return jsonify(
            erro=str(erro)
        ), 500


# ============================================================
# BIBLIOTECA
# ============================================================

@app.route("/biblioteca")
@login_required
def biblioteca():

    corrigir_usuario(
        current_user
    )

    progressos = (
        ProgressoAssunto.query
        .filter_by(
            usuario_id=current_user.id
        )
        .all()
    )

    etapas = (
        ProgressoEtapa.query
        .filter_by(
            usuario_id=current_user.id
        )
        .all()
    )

    total_assuntos = sum(

        len(
            tema["assuntos"]
        )

        for ano in CURRICULO.values()

        for tema in ano[
            "temas"
        ].values()
    )

    assuntos_concluidos = sum(

        1

        for progresso in progressos

        if progresso.concluido
    )

    etapas_concluidas = sum(

        1

        for progresso in etapas

        if progresso.concluida
    )

    progresso_geral = (

        round(
            assuntos_concluidos
            /
            total_assuntos
            *
            100
        )

        if total_assuntos

        else 0
    )

    historico = (
        Resposta.query
        .filter_by(
            usuario_id=current_user.id
        )
        .order_by(
            Resposta.criado_em.desc()
        )
        .limit(10)
        .all()
    )

    return render_template(

        "biblioteca.html",

        total_assuntos=total_assuntos,

        assuntos_concluidos=(
            assuntos_concluidos
        ),

        etapas_concluidas=(
            etapas_concluidas
        ),

        progresso_geral=(
            progresso_geral
        ),

        historico=historico
    )


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    socketio.run(
        app,
        debug=True,
        host="0.0.0.0",
        port=5000,
        allow_unsafe_werkzeug=True
    )