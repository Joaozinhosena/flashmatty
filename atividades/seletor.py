import json
from datetime import datetime

from sqlalchemy import or_

from models import db
from .models import QuestaoBanco, HistoricoQuestao


PREFIXO_QUESTAO_REAL = "IM-"


def _data_ingenua_utc():
    return datetime.utcnow()


def _filtro_base(
    ano_id,
    tema_id,
    assunto_id,
    etapa_id,
    tipo,
):
    """
    Consulta-base do novo acervo.

    Só aceita questões:
    - IM-*
    - revisadas
    - ativas
    - compatíveis com ano/tema/assunto/etapa/tipo
    """
    return (
        QuestaoBanco.query
        .filter(
            QuestaoBanco.ano == str(ano_id),
            QuestaoBanco.tema == str(tema_id),
            QuestaoBanco.assunto == str(assunto_id),
            QuestaoBanco.tipo == str(tipo),
            QuestaoBanco.revisada.is_(True),
            QuestaoBanco.ativa.is_(True),
            QuestaoBanco.codigo.like(
                f"{PREFIXO_QUESTAO_REAL}%"
            ),
        )
        .filter(
            or_(
                QuestaoBanco.etapa == str(etapa_id),
                QuestaoBanco.etapa.is_(None),
                QuestaoBanco.etapa == "",
            )
        )
    )


def contar_questoes_disponiveis(
    ano_id,
    tema_id,
    assunto_id,
    etapa_id,
    tipo,
):
    """
    Quantidade de questões IM-* disponíveis para esta etapa.

    O app.py usa isso para não exigir 8 questões quando,
    por exemplo, o banco real ainda possui somente 3.
    """
    return _filtro_base(
        ano_id=ano_id,
        tema_id=tema_id,
        assunto_id=assunto_id,
        etapa_id=etapa_id,
        tipo=tipo,
    ).count()


def _converter_questao_banco(questao):
    alternativas = []

    for alternativa in questao.alternativas:
        item = {
            "id": str(alternativa.valor),
            "texto": str(alternativa.texto),
        }

        if alternativa.imagem:
            item["imagem"] = alternativa.imagem

        alternativas.append(item)

    dados = {
        "id_questao": questao.id,
        "codigo": questao.codigo,
        "origem": "fonte_real",
        "tipo_ui": questao.tipo_ui,
        "pergunta": questao.enunciado,
        "resposta": str(questao.resposta_correta),
        "dificuldade": questao.dificuldade,
        "habilidade": questao.habilidade_bncc or "",
        "explicacao": questao.explicacao or "",
        "autor": questao.autor or "",
        "instituicao": questao.instituicao or "",
        "fonte": questao.fonte or "",
        "licenca": questao.licenca or "",
    }

    if alternativas:
        dados["alternativas"] = alternativas

    if questao.instrucao:
        dados["instrucao"] = questao.instrucao

    if questao.visual_json:
        try:
            dados["visual"] = json.loads(
                questao.visual_json
            )
        except (
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ):
            pass

    return dados


def _pontuacao_candidata(
    questao_id,
    historicos_por_questao,
):
    historicos = historicos_por_questao.get(
        questao_id,
        [],
    )

    if not historicos:
        return 1_000_000

    historicos = sorted(
        historicos,
        key=lambda h: h.respondida_em,
        reverse=True,
    )

    ultimo = historicos[0]
    vezes = len(historicos)

    erros = sum(
        1
        for historico in historicos
        if not historico.acertou
    )

    agora = _data_ingenua_utc()

    dias = max(
        0,
        (agora - ultimo.respondida_em).days,
    )

    score = 0

    if not ultimo.acertou:
        score += 5_000

    score += erros * 500
    score += min(dias, 30) * 100
    score -= vezes * 250

    if ultimo.acertou and dias <= 1:
        score -= 10_000

    return score


def selecionar_questao_banco(
    usuario_id,
    ano_id,
    tema_id,
    assunto_id,
    etapa_id,
    tipo,
    ids_evitar=None,
):
    ids_evitar = {
        int(item)
        for item in (ids_evitar or [])
        if str(item).isdigit()
    }

    consulta = _filtro_base(
        ano_id=ano_id,
        tema_id=tema_id,
        assunto_id=assunto_id,
        etapa_id=etapa_id,
        tipo=tipo,
    )

    candidatos = [
        questao
        for questao in consulta.all()
        if questao.id not in ids_evitar
    ]

    if not candidatos:
        return None

    ids = [
        questao.id
        for questao in candidatos
    ]

    historicos = (
        HistoricoQuestao.query
        .filter(
            HistoricoQuestao.usuario_id == usuario_id,
            HistoricoQuestao.questao_id.in_(ids),
        )
        .all()
    )

    historicos_por_questao = {}

    for historico in historicos:
        historicos_por_questao.setdefault(
            historico.questao_id,
            [],
        ).append(
            historico
        )

    candidatos.sort(
        key=lambda questao: (
            _pontuacao_candidata(
                questao.id,
                historicos_por_questao,
            ),
            -questao.id,
        ),
        reverse=True,
    )

    return candidatos[0]


def obter_questao_para_usuario(
    usuario_id,
    ano_id,
    tema_id,
    assunto_id,
    etapa_id,
    tipo,
    interacoes=None,
    nivel=None,
    ano_numero=None,
    complexidade=None,
    operacoes=None,
    desafio=False,
    ids_evitar=None,
):
    """
    Novo comportamento:
    - usa somente IM-*;
    - nunca chama game.py;
    - retorna None quando não existe questão real compatível.
    """

    questao_banco = selecionar_questao_banco(
        usuario_id=usuario_id,
        ano_id=ano_id,
        tema_id=tema_id,
        assunto_id=assunto_id,
        etapa_id=etapa_id,
        tipo=tipo,
        ids_evitar=ids_evitar,
    )

    if questao_banco is None:
        return None

    return _converter_questao_banco(
        questao_banco
    )


def registrar_resposta_banco(
    usuario_id,
    questao_id,
    resposta_usuario,
    acertou,
):
    if not questao_id:
        return None

    questao = db.session.get(
        QuestaoBanco,
        int(questao_id),
    )

    if questao is None:
        return None

    if not str(
        questao.codigo or ""
    ).startswith(
        PREFIXO_QUESTAO_REAL
    ):
        return None

    registro = HistoricoQuestao(
        usuario_id=usuario_id,
        questao_id=questao.id,
        resposta_usuario=str(
            resposta_usuario
        ),
        acertou=bool(
            acertou
        ),
        respondida_em=_data_ingenua_utc(),
    )

    db.session.add(
        registro
    )

    return registro
