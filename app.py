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

# ============================================================
# MULTIPLAYER
# ============================================================

from multiplayer import socketio
from multiplayer.routes import multiplayer_bp


# ============================================================
# APP
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "matematica-kids-desenvolvimento"

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///matematica.db"

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False


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

login_manager.login_message = (
    "Faça login para continuar."
)


@login_manager.user_loader
def carregar_usuario(user_id):

    try:

        return db.session.get(
            Usuario,
            int(user_id)
        )

    except (
        ValueError,
        TypeError
    ):

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

# IMPORTANTE:
# eventos somente depois de configurar SocketIO
import multiplayer.socket_events


# ============================================================
# CRIAR TABELAS
# ============================================================

with app.app_context():

    db.create_all()


# ============================================================
# BUSCAR ANO
# ============================================================

def buscar_ano(ano_id):

    ano = CURRICULO.get(
        ano_id
    )

    if not ano:

        abort(404)

    return ano


# ============================================================
# BUSCAR TEMA
# ============================================================

def buscar_tema(
    ano,
    tema_id
):

    tema = (
        ano
        .get(
            "temas",
            {}
        )
        .get(
            tema_id
        )
    )

    if not tema:

        abort(404)

    return tema


# ============================================================
# BUSCAR ASSUNTO
# ============================================================

def buscar_assunto(
    tema,
    assunto_id
):

    assunto = (
        tema
        .get(
            "assuntos",
            {}
        )
        .get(
            assunto_id
        )
    )

    if not assunto:

        abort(404)

    return assunto


# ============================================================
# BUSCAR ETAPA
# ============================================================

def buscar_etapa(
    assunto,
    etapa_id
):

    etapa = (
        assunto
        .get(
            "etapas",
            {}
        )
        .get(
            etapa_id
        )
    )

    if not etapa:

        abort(404)

    return etapa


# ============================================================
# CORRIGIR VALORES NULOS DO USUÁRIO
# ============================================================

def corrigir_usuario(
    usuario
):

    usuario.xp = (
        usuario.xp
        or 0
    )

    usuario.moedas = (
        usuario.moedas
        or 0
    )

    usuario.acertos = (
        usuario.acertos
        or 0
    )

    usuario.erros = (
        usuario.erros
        or 0
    )


# ============================================================
# PROGRESSO DA ETAPA
# ============================================================

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

            usuario_id=
                current_user.id,

            ano=
                ano_id,

            tema=
                tema_id,

            assunto=
                assunto_id,

            etapa=
                etapa_id

        )
        .first()
    )


    if (
        not progresso
        and
        criar
    ):

        progresso = ProgressoEtapa(

            usuario_id=
                current_user.id,

            ano=
                ano_id,

            tema=
                tema_id,

            assunto=
                assunto_id,

            etapa=
                etapa_id,

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


# ============================================================
# PROGRESSO DO ASSUNTO
# ============================================================

def obter_progresso_assunto(
    ano_id,
    tema_id,
    assunto_id,
    criar=False
):

    progresso = (
        ProgressoAssunto.query
        .filter_by(

            usuario_id=
                current_user.id,

            ano=
                ano_id,

            tema=
                tema_id,

            assunto=
                assunto_id

        )
        .first()
    )


    if (
        not progresso
        and
        criar
    ):

        progresso = (
            ProgressoAssunto(

                usuario_id=
                    current_user.id,

                ano=
                    ano_id,

                tema=
                    tema_id,

                assunto=
                    assunto_id,

                concluido=False
            )
        )


        db.session.add(
            progresso
        )


    return progresso


# ============================================================
# VERIFICAR SE ETAPA ESTÁ LIBERADA
# ============================================================

def etapa_liberada(
    assunto,
    ano_id,
    tema_id,
    assunto_id,
    etapa_id
):

    ids = list(
        assunto[
            "etapas"
        ].keys()
    )


    if etapa_id not in ids:

        return False


    indice = ids.index(
        etapa_id
    )


    # PRIMEIRA ETAPA SEMPRE LIBERADA

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


# ============================================================
# ATUALIZAR CONCLUSÃO DO ASSUNTO
# ============================================================

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


    # Uma vez concluído, permanece concluído

    if todas_concluidas:

        progresso_assunto.concluido = True


    return progresso_assunto


# ============================================================
# QUESTÃO PÚBLICA
# ============================================================

def questao_publica(
    questao
):

    """
    Remove a resposta correta antes de
    enviar a questão para o navegador.
    """

    if not isinstance(
        questao,
        dict
    ):

        return {}


    return {

        chave:
            valor

        for chave, valor
        in questao.items()

        if chave != "resposta"
    }


# ============================================================
# NORMALIZAR RESPOSTA
# ============================================================

def normalizar_resposta(
    valor
):

    # --------------------------------------------------------
    # ASSOCIAÇÃO
    # --------------------------------------------------------

    if isinstance(
        valor,
        dict
    ):

        return {

            str(chave)
            .strip()
            .casefold():

                normalizar_resposta(
                    conteudo
                )

            for chave, conteudo
            in sorted(

                valor.items(),

                key=lambda item:
                    str(
                        item[0]
                    )
            )
        }


    # --------------------------------------------------------
    # ORDENAÇÃO
    # --------------------------------------------------------

    if isinstance(
        valor,
        list
    ):

        return [

            normalizar_resposta(
                item
            )

            for item
            in valor
        ]


    # --------------------------------------------------------
    # NULO
    # --------------------------------------------------------

    if valor is None:

        return ""


    # --------------------------------------------------------
    # TEXTO / NÚMERO
    # --------------------------------------------------------

    return (

        str(valor)

        .strip()

        .casefold()

        .replace(
            ",",
            "."
        )
    )


# ============================================================
# COMPARAR RESPOSTAS
# ============================================================

def respostas_iguais(
    resposta_usuario,
    resposta_correta
):

    return (

        normalizar_resposta(
            resposta_usuario
        )

        ==

        normalizar_resposta(
            resposta_correta
        )
    )


# ============================================================
# CONVERTER RESPOSTA PARA TEXTO
# ============================================================

def resposta_para_texto(
    valor
):

    if isinstance(
        valor,
        dict
    ):

        return "; ".join(

            f"{chave} → {conteudo}"

            for chave, conteudo
            in valor.items()
        )


    if isinstance(
        valor,
        list
    ):

        return " → ".join(

            str(item)

            for item
            in valor
        )


    return str(
        valor
    )


# ============================================================
# VERIFICAR RESPOSTA VAZIA
# ============================================================

def resposta_vazia(
    valor
):

    if valor is None:

        return True


    if isinstance(
        valor,
        str
    ):

        return not valor.strip()


    if isinstance(
        valor,
        list
    ):

        return (
            len(valor)
            ==
            0
        )


    if isinstance(
        valor,
        dict
    ):

        return (
            len(valor)
            ==
            0
        )


    return False


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    if current_user.is_authenticated:

        return redirect(
            url_for(
                "dashboard"
            )
        )


    return redirect(
        url_for(
            "login"
        )
    )


# ============================================================
# CADASTRO
# ============================================================

@app.route(
    "/cadastro",
    methods=[
        "GET",
        "POST"
    ]
)
def cadastro():

    if current_user.is_authenticated:

        return redirect(
            url_for(
                "dashboard"
            )
        )


    if request.method == "POST":

        nome = (
            request.form
            .get(
                "nome",
                ""
            )
            .strip()
        )


        username = (
            request.form
            .get(
                "username",
                ""
            )
            .strip()
        )


        senha = request.form.get(
            "senha",
            ""
        )


        confirmar = request.form.get(
            "confirmar_senha",
            ""
        )


        if (
            not nome
            or
            not username
            or
            not senha
        ):

            flash(
                "Preencha todos os campos."
            )


            return redirect(
                url_for(
                    "cadastro"
                )
            )


        if senha != confirmar:

            flash(
                "As senhas não são iguais."
            )


            return redirect(
                url_for(
                    "cadastro"
                )
            )


        existente = (
            Usuario.query
            .filter_by(
                username=
                    username
            )
            .first()
        )


        if existente:

            flash(
                "Usuário já existe."
            )


            return redirect(
                url_for(
                    "cadastro"
                )
            )


        usuario = Usuario(

            nome=
                nome,

            username=
                username,

            senha=
                generate_password_hash(
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
            url_for(
                "dashboard"
            )
        )


    return render_template(
        "cadastro.html"
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=[
        "GET",
        "POST"
    ]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for(
                "dashboard"
            )
        )


    if request.method == "POST":

        username = (
            request.form
            .get(
                "username",
                ""
            )
            .strip()
        )


        senha = request.form.get(
            "senha",
            ""
        )


        usuario = (
            Usuario.query
            .filter_by(
                username=
                    username
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
                url_for(
                    "login"
                )
            )


        corrigir_usuario(
            usuario
        )


        db.session.commit()


        login_user(
            usuario
        )


        return redirect(
            url_for(
                "dashboard"
            )
        )


    return render_template(
        "login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route(
    "/logout"
)
@login_required
def logout():

    logout_user()


    session.clear()


    return redirect(
        url_for(
            "login"
        )
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route(
    "/dashboard"
)
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

@app.route(
    "/jornada"
)
@login_required
def jornada():

    anos = sorted(

        CURRICULO.items(),

        key=lambda item:
            item[1][
                "ordem"
            ]
    )


    progresso_anos = {}


    for ano_id, ano in anos:

        total = 0

        concluidos = 0


        for tema_id, tema in ano[
            "temas"
        ].items():

            for assunto_id in tema[
                "assuntos"
            ]:

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


        if total:

            progresso_anos[
                ano_id
            ] = round(

                concluidos
                /
                total
                *
                100
            )

        else:

            progresso_anos[
                ano_id
            ] = 0


    return render_template(

        "jornada.html",

        anos=
            anos,

        progresso_anos=
            progresso_anos
    )


# ============================================================
# ANO
# ============================================================

@app.route(
    "/ano/<ano_id>"
)
@login_required
def ano(
    ano_id
):

    dados_ano = buscar_ano(
        ano_id
    )


    return render_template(

        "ano.html",

        ano=
            dados_ano,

        ano_id=
            ano_id
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

        ano=
            dados_ano,

        ano_id=
            ano_id,

        tema=
            dados_tema,

        tema_id=
            tema_id,

        progressos=
            progressos
    )


# ============================================================
# ASSUNTO / TRILHA
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

            "progresso":
                progresso,

            "liberada":
                etapa_liberada(

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

        ano=
            dados_ano,

        ano_id=
            ano_id,

        tema=
            dados_tema,

        tema_id=
            tema_id,

        assunto=
            dados_assunto,

        assunto_id=
            assunto_id,

        progressos=
            progressos,

        progresso_assunto=
            progresso_assunto
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


    dados_etapa = buscar_etapa(

        dados_assunto,

        etapa_id
    )


    # --------------------------------------------------------
    # VERIFICAR LIBERAÇÃO
    # --------------------------------------------------------

    if not etapa_liberada(

        dados_assunto,

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

                ano_id=
                    ano_id,

                tema_id=
                    tema_id,

                assunto_id=
                    assunto_id
            )
        )


    # --------------------------------------------------------
    # TIPOS DE INTERAÇÃO DA ETAPA
    # --------------------------------------------------------

    interacoes = (
        dados_etapa.get(
            "interacoes",
            []
        )
    )


    # --------------------------------------------------------
    # GERAR PRIMEIRA QUESTÃO
    # --------------------------------------------------------

    nova_questao = gerar_questao(

        dados_etapa[
            "tipo"
        ],

        interacoes
    )


    if (
        not isinstance(
            nova_questao,
            dict
        )
        or
        "pergunta" not in nova_questao
        or
        "resposta" not in nova_questao
    ):

        abort(
            500,
            description=
                "O gerador retornou uma questão inválida."
        )


    # --------------------------------------------------------
    # CRIAR TENTATIVA
    # --------------------------------------------------------

    session[
        "tentativa"
    ] = {

        "ano":
            ano_id,

        "tema":
            tema_id,

        "assunto":
            assunto_id,

        "etapa":
            etapa_id,

        "respondidas":
            0,

        "acertos":
            0,

        "quantidade":
            dados_etapa[
                "quantidade"
            ],

        "pergunta":
            nova_questao[
                "pergunta"
            ],

        "resposta":
            nova_questao[
                "resposta"
            ],

        "tipo":
            dados_etapa[
                "tipo"
            ],

        "interacoes":
            interacoes
    }


    session.modified = True


    # --------------------------------------------------------
    # NÃO ENVIA RESPOSTA CORRETA AO NAVEGADOR
    # --------------------------------------------------------

    return render_template(

        "etapa.html",

        ano=
            dados_ano,

        tema=
            dados_tema,

        assunto=
            dados_assunto,

        etapa=
            dados_etapa,

        etapa_id=
            etapa_id,

        questao_publica=
            questao_publica(
                nova_questao
            )
    )


# ============================================================
# API RESPONDER
# ============================================================

@app.route(
    "/api/responder",
    methods=[
        "POST"
    ]
)
@login_required
def responder():

    try:

        # ====================================================
        # RECEBER JSON
        # ====================================================

        dados = (

            request.get_json(
                silent=True
            )

            or {}
        )


        if "resposta" not in dados:

            return jsonify(

                erro=
                    "Escolha ou digite uma resposta."

            ), 400


        resposta_usuario = dados.get(
            "resposta"
        )


        if resposta_vazia(
            resposta_usuario
        ):

            return jsonify(

                erro=
                    "Escolha ou digite uma resposta."

            ), 400


        # ====================================================
        # TENTATIVA
        # ====================================================

        tentativa = session.get(
            "tentativa"
        )


        if not tentativa:

            return jsonify(

                erro=
                    "A tentativa expirou."

            ), 400


        correta = tentativa[
            "resposta"
        ]


        # ====================================================
        # COMPARAR RESPOSTA
        # ====================================================

        acertou = respostas_iguais(

            resposta_usuario,

            correta
        )


        corrigir_usuario(
            current_user
        )


        # ====================================================
        # PROGRESSO
        # ====================================================

        progresso = (
            obter_progresso_etapa(

                tentativa[
                    "ano"
                ],

                tentativa[
                    "tema"
                ],

                tentativa[
                    "assunto"
                ],

                tentativa[
                    "etapa"
                ],

                criar=True
            )
        )


        progresso.acertos = (
            progresso.acertos
            or 0
        )

        progresso.erros = (
            progresso.erros
            or 0
        )

        progresso.xp = (
            progresso.xp
            or 0
        )

        progresso.tentativas = (
            progresso.tentativas
            or 0
        )

        progresso.melhor_pontuacao = (
            progresso.melhor_pontuacao
            or 0
        )


        # ====================================================
        # ACERTO
        # ====================================================

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
                "Muito bem! "
            )


        # ====================================================
        # ERRO
        # ====================================================

        else:

            progresso.erros += 1


            current_user.erros += 1


            mensagem = (

                "Quase! A resposta correta era "

                f"{resposta_para_texto(correta)}."
            )


        tentativa[
            "respondidas"
        ] += 1


        # ====================================================
        # SALVAR HISTÓRICO
        # ====================================================

        registro = Resposta(

            usuario_id=
                current_user.id,

            ano=
                tentativa[
                    "ano"
                ],

            tema=
                tentativa[
                    "tema"
                ],

            assunto=
                tentativa[
                    "assunto"
                ],

            etapa=
                tentativa[
                    "etapa"
                ],

            pergunta=
                tentativa[
                    "pergunta"
                ],

            resposta_usuario=
                resposta_para_texto(
                    resposta_usuario
                ),

            resposta_correta=
                resposta_para_texto(
                    correta
                ),

            acertou=
                acertou
        )


        db.session.add(
            registro
        )


        # ====================================================
        # TERMINOU?
        # ====================================================

        terminou = (

            tentativa[
                "respondidas"
            ]

            >=

            tentativa[
                "quantidade"
            ]
        )


        # ====================================================
        # FINAL DA ETAPA
        # ====================================================

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


            progresso.melhor_pontuacao = max(

                progresso.melhor_pontuacao,

                pontuacao
            )


            passou = (
                pontuacao >= 80
            )


            # ------------------------------------------------
            # EVITA GANHAR BÔNUS REPETIDO
            # ------------------------------------------------

            ja_estava_concluida = bool(
                progresso.concluida
            )


            if passou:

                progresso.concluida = True


                if not ja_estava_concluida:

                    current_user.xp += 20

                    current_user.moedas += 5


            # ------------------------------------------------
            # VERIFICAR ASSUNTO
            # ------------------------------------------------

            dados_ano = buscar_ano(

                tentativa[
                    "ano"
                ]
            )


            dados_tema = buscar_tema(

                dados_ano,

                tentativa[
                    "tema"
                ]
            )


            dados_assunto = buscar_assunto(

                dados_tema,

                tentativa[
                    "assunto"
                ]
            )


            progresso_assunto = (
                atualizar_assunto(

                    tentativa[
                        "ano"
                    ],

                    tentativa[
                        "tema"
                    ],

                    tentativa[
                        "assunto"
                    ],

                    dados_assunto
                )
            )


            db.session.commit()


            session.pop(
                "tentativa",
                None
            )


            session.modified = True


            return jsonify(

                terminou=
                    True,

                correto=
                    acertou,

                mensagem=
                    mensagem,

                passou=
                    passou,

                pontuacao=
                    pontuacao,

                acertos=
                    acertos_tentativa,

                quantidade=
                    quantidade,

                xp=
                    current_user.xp,

                moedas=
                    current_user.moedas,

                assunto_concluido=
                    bool(
                        progresso_assunto.concluido
                    )
            )


        # ====================================================
        # GERAR PRÓXIMA QUESTÃO
        # ====================================================

        nova_questao = gerar_questao(

            tentativa[
                "tipo"
            ],

            tentativa.get(
                "interacoes",
                []
            )
        )


        # ====================================================
        # VALIDAR QUESTÃO
        # ====================================================

        if (
            not isinstance(
                nova_questao,
                dict
            )
            or
            "pergunta" not in nova_questao
            or
            "resposta" not in nova_questao
        ):

            raise ValueError(

                "O game.py retornou uma questão inválida."
            )


        # ====================================================
        # ATUALIZAR SESSÃO
        # ====================================================

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


        # ====================================================
        # DEVOLVER QUESTÃO SEM RESPOSTA
        # ====================================================

        return jsonify(

            terminou=
                False,

            correto=
                acertou,

            mensagem=
                mensagem,

            xp=
                current_user.xp,

            moedas=
                current_user.moedas,

            respondidas=
                tentativa[
                    "respondidas"
                ],

            quantidade=
                tentativa[
                    "quantidade"
                ],

            questao=
                questao_publica(
                    nova_questao
                )
        )


    # ========================================================
    # ERRO
    # ========================================================

    except Exception as erro:

        db.session.rollback()


        print(
            "ERRO /api/responder:",
            erro
        )


        return jsonify(

            erro=
                str(
                    erro
                )

        ), 500


# ============================================================
# BIBLIOTECA
# ============================================================

@app.route(
    "/biblioteca"
)
@login_required
def biblioteca():

    corrigir_usuario(
        current_user
    )


    progressos = (
        ProgressoAssunto.query
        .filter_by(

            usuario_id=
                current_user.id
        )
        .all()
    )


    etapas = (
        ProgressoEtapa.query
        .filter_by(

            usuario_id=
                current_user.id
        )
        .all()
    )


    total_assuntos = sum(

        len(
            tema[
                "assuntos"
            ]
        )

        for ano
        in CURRICULO.values()

        for tema
        in ano[
            "temas"
        ].values()
    )


    assuntos_concluidos = sum(

        1

        for progresso
        in progressos

        if progresso.concluido
    )


    etapas_concluidas = sum(

        1

        for progresso
        in etapas

        if progresso.concluida
    )


    if total_assuntos:

        progresso_geral = round(

            assuntos_concluidos

            /

            total_assuntos

            *

            100
        )

    else:

        progresso_geral = 0


    historico = (
        Resposta.query

        .filter_by(

            usuario_id=
                current_user.id
        )

        .order_by(

            Resposta.criado_em.desc()
        )

        .limit(
            10
        )

        .all()
    )


    return render_template(

        "biblioteca.html",

        total_assuntos=
            total_assuntos,

        assuntos_concluidos=
            assuntos_concluidos,

        etapas_concluidas=
            etapas_concluidas,

        progresso_geral=
            progresso_geral,

        historico=
            historico
    )


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == "__main__":

    print("")
    print("==========================================")
    print(" flashmatty")
    print(" http://127.0.0.1:5000")
    print("==========================================")
    print("")


    socketio.run(

        app,

        debug=True,

        host="0.0.0.0",

        port=5000,

        allow_unsafe_werkzeug=True
    )