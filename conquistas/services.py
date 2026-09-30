from collections import defaultdict

from sqlalchemy import (
    and_,
    or_,
)

from models import (
    db,
    Usuario,
    ProgressoAssunto,
    ProgressoEtapa,
)

from social.models import (
    Amizade,
)

from .catalogo import (
    CATEGORIAS,
    CONQUISTAS,
)

from .models import (
    ConquistaUsuario,
    HistoricoMultiplayer,
)


def _int(valor):
    try:
        return int(valor or 0)
    except (TypeError, ValueError):
        return 0


def _usuario_id_seguro(
    jogador
):
    """
    Tenta obter o ID real da conta.

    Em salas comuns, o jogador_id pode ser algo como:
        7-a18b32c1

    O ID real da conta é guardado em usuario_id. O fallback
    abaixo permite registrar partidas antigas caso necessário.
    """

    usuario_id = jogador.get(
        "usuario_id"
    )

    if usuario_id is not None:

        try:
            return int(
                usuario_id
            )
        except (
            TypeError,
            ValueError
        ):
            pass


    jogador_id = str(
        jogador.get(
            "id",
            ""
        )
        or
        ""
    ).strip()


    primeiro = (
        jogador_id
        .split(
            "-",
            1
        )[0]
    )


    try:
        candidato = int(
            primeiro
        )
    except (
        TypeError,
        ValueError
    ):
        return None


    usuario = db.session.get(
        Usuario,
        candidato
    )


    if not usuario:
        return None


    return candidato


def estatisticas_usuario(
    usuario_id
):

    usuario_id = int(
        usuario_id
    )


    usuario = db.session.get(
        Usuario,
        usuario_id
    )


    if not usuario:

        return None


    xp = _int(
        getattr(
            usuario,
            "xp",
            0
        )
    )


    acertos = _int(
        getattr(
            usuario,
            "acertos",
            0
        )
    )


    erros = _int(
        getattr(
            usuario,
            "erros",
            0
        )
    )


    total_respostas = (
        acertos
        +
        erros
    )


    precisao = (
        (
            acertos
            /
            total_respostas
            *
            100
        )
        if total_respostas
        else
        0
    )


    etapas_concluidas = (

        ProgressoEtapa.query

        .filter_by(
            usuario_id=
                usuario_id,

            concluida=
                True
        )

        .count()
    )


    assuntos_concluidos = (

        ProgressoAssunto.query

        .filter_by(
            usuario_id=
                usuario_id,

            concluido=
                True
        )

        .count()
    )


    amigos = (

        Amizade.query

        .filter(
            Amizade.status
            ==
            "aceita",

            or_(
                Amizade.solicitante_id
                ==
                usuario_id,

                Amizade.destinatario_id
                ==
                usuario_id
            )
        )

        .count()
    )


    historico = (

        HistoricoMultiplayer.query

        .filter_by(
            usuario_id=
                usuario_id
        )

        .order_by(
            HistoricoMultiplayer.id.asc()
        )

        .all()
    )


    partidas = len(
        historico
    )


    vitorias = sum(
        1
        for item
        in historico
        if item.venceu
    )


    podios = sum(
        1
        for item
        in historico
        if (
            item.posicao
            and
            item.posicao <= 3
        )
    )


    perfeitas = sum(
        1
        for item
        in historico
        if item.perfeita
    )


    max_pontos = max(
        (
            item.pontos
            for item
            in historico
        ),
        default=0
    )


    sequencia_atual = 0
    melhor_sequencia = 0


    for item in historico:

        if item.venceu:

            sequencia_atual += 1

            melhor_sequencia = max(
                melhor_sequencia,
                sequencia_atual
            )

        else:

            sequencia_atual = 0


    return {
        "xp":
            xp,

        "acertos":
            acertos,

        "erros":
            erros,

        "total_respostas":
            total_respostas,

        "precisao":
            precisao,

        "etapas_concluidas":
            etapas_concluidas,

        "assuntos_concluidos":
            assuntos_concluidos,

        "amigos":
            amigos,

        "multiplayer_partidas":
            partidas,

        "multiplayer_vitorias":
            vitorias,

        "multiplayer_podios":
            podios,

        "multiplayer_perfeitas":
            perfeitas,

        "multiplayer_max_pontos":
            max_pontos,

        "multiplayer_melhor_sequencia":
            melhor_sequencia,
    }


def avaliar_conquista(
    conquista,
    estatisticas
):

    tipo = conquista[
        "tipo"
    ]

    meta = float(
        conquista.get(
            "meta",
            1
        )
        or
        1
    )


    if tipo == "precisao":

        precisao = float(
            estatisticas.get(
                "precisao",
                0
            )
            or
            0
        )


        total = _int(
            estatisticas.get(
                "total_respostas",
                0
            )
        )


        minimo = _int(
            conquista.get(
                "minimo",
                0
            )
        )


        concluiu = (
            precisao >= meta
            and
            total >= minimo
        )


        parte_precisao = min(
            1,
            precisao
            /
            max(
                1,
                meta
            )
        )


        parte_volume = min(
            1,
            total
            /
            max(
                1,
                minimo
            )
        )


        percentual = round(
            min(
                parte_precisao,
                parte_volume
            )
            *
            100
        )


        texto = (
            f"{precisao:.0f}% de precisão"
            f" • {total}/{minimo} respostas"
        )


        return {
            "concluiu":
                concluiu,

            "valor":
                precisao,

            "percentual":
                percentual,

            "texto":
                texto,
        }


    valor = float(
        estatisticas.get(
            tipo,
            0
        )
        or
        0
    )


    concluiu = (
        valor >= meta
    )


    percentual = round(
        min(
            100,
            (
                valor
                /
                max(
                    1,
                    meta
                )
                *
                100
            )
        )
    )


    inteiro = (
        int(valor)
        if valor.is_integer()
        else round(
            valor,
            1
        )
    )


    meta_inteira = (
        int(meta)
        if meta.is_integer()
        else meta
    )


    texto = (
        f"{inteiro}/{meta_inteira}"
    )


    return {
        "concluiu":
            concluiu,

        "valor":
            valor,

        "percentual":
            percentual,

        "texto":
            texto,
    }


def sincronizar_conquistas(
    usuario_id,
    commit=True
):

    usuario_id = int(
        usuario_id
    )


    estatisticas = (
        estatisticas_usuario(
            usuario_id
        )
    )


    if not estatisticas:

        return []


    existentes = {

        registro.conquista_id:
            registro

        for registro
        in (
            ConquistaUsuario.query

            .filter_by(
                usuario_id=
                    usuario_id
            )

            .all()
        )
    }


    novas = []


    for conquista in CONQUISTAS:

        conquista_id = (
            conquista[
                "id"
            ]
        )


        if conquista_id in existentes:
            continue


        avaliacao = avaliar_conquista(
            conquista,
            estatisticas
        )


        if not avaliacao[
            "concluiu"
        ]:
            continue


        registro = ConquistaUsuario(
            usuario_id=
                usuario_id,

            conquista_id=
                conquista_id,

            valor_desbloqueio=
                avaliacao[
                    "valor"
                ],
        )


        db.session.add(
            registro
        )


        existentes[
            conquista_id
        ] = registro


        novas.append(
            conquista_id
        )


    if (
        commit
        and
        novas
    ):

        db.session.commit()


    return novas


def conquistas_perfil(
    usuario_id
):
    """
    Retorna as conquistas prontas para o template de perfil.
    Conquistas já desbloqueadas permanecem desbloqueadas mesmo
    se uma estatística não monotônica (ex.: amigos) diminuir.
    """

    usuario_id = int(
        usuario_id
    )


    sincronizar_conquistas(
        usuario_id,
        commit=True
    )


    estatisticas = (
        estatisticas_usuario(
            usuario_id
        )
        or
        {}
    )


    desbloqueios = {

        item.conquista_id:
            item

        for item
        in (
            ConquistaUsuario.query

            .filter_by(
                usuario_id=
                    usuario_id
            )

            .all()
        )
    }


    lista = []


    for conquista in CONQUISTAS:

        conquista_id = (
            conquista[
                "id"
            ]
        )


        registro = (
            desbloqueios.get(
                conquista_id
            )
        )


        avaliacao = avaliar_conquista(
            conquista,
            estatisticas
        )


        item = dict(
            conquista
        )


        item[
            "imagem"
        ] = (
            "img/conquistas/"
            f"{conquista_id}.png"
        )


        item[
            "desbloqueada"
        ] = bool(
            registro
        )


        item[
            "desbloqueada_em"
        ] = (
            registro.desbloqueada_em
            if registro
            else None
        )


        item[
            "percentual"
        ] = (
            100
            if registro
            else avaliacao[
                "percentual"
            ]
        )


        item[
            "progresso_texto"
        ] = (
            "Conquista desbloqueada"
            if registro
            else avaliacao[
                "texto"
            ]
        )


        categoria = (
            CATEGORIAS.get(
                item[
                    "categoria"
                ],
                {}
            )
        )


        item[
            "categoria_nome"
        ] = categoria.get(
            "nome",
            item[
                "categoria"
            ]
        )


        lista.append(
            item
        )


    grupos = defaultdict(
        list
    )


    for item in lista:

        grupos[
            item[
                "categoria"
            ]
        ].append(
            item
        )


    desbloqueadas = sum(
        1
        for item
        in lista
        if item[
            "desbloqueada"
        ]
    )


    return {
        "lista":
            lista,

        "grupos":
            dict(
                grupos
            ),

        "categorias":
            CATEGORIAS,

        "desbloqueadas":
            desbloqueadas,

        "total":
            len(
                lista
            ),
    }


def registrar_resultado_multiplayer(
    codigo,
    sala,
    classificacao
):
    """
    Persiste o resultado de uma sala apenas uma vez por conta
    e sincroniza conquistas multiplayer imediatamente.
    """

    if (
        not sala
        or
        not classificacao
    ):

        return


    criada_em = float(
        sala.get(
            "criada_em",
            0
        )
        or
        0
    )


    partida_id = (
        f"{codigo}:"
        f"{int(criada_em * 1000)}"
    )


    total_questoes = len(
        sala.get(
            "questoes",
            []
        )
    )


    usuarios_processados = set()


    for posicao_item in classificacao:

        jogador_id = str(
            posicao_item.get(
                "id",
                ""
            )
        )


        jogador = (
            sala.get(
                "jogadores",
                {}
            )
            .get(
                jogador_id
            )
        )


        if not jogador:
            continue


        usuario_id = (
            _usuario_id_seguro(
                jogador
            )
        )


        if (
            not usuario_id
            or
            usuario_id
            in usuarios_processados
        ):

            continue


        usuarios_processados.add(
            usuario_id
        )


        existente = (

            HistoricoMultiplayer.query

            .filter_by(
                partida_id=
                    partida_id,

                usuario_id=
                    usuario_id
            )

            .first()
        )


        if existente:
            continue


        posicao = _int(
            posicao_item.get(
                "posicao",
                0
            )
        )


        pontos = _int(
            posicao_item.get(
                "pontos",
                0
            )
        )


        acertos = _int(
            posicao_item.get(
                "acertos",
                0
            )
        )


        erros = _int(
            posicao_item.get(
                "erros",
                0
            )
        )


        perfeita = (
            total_questoes > 0
            and
            acertos >= total_questoes
            and
            erros == 0
        )


        registro = HistoricoMultiplayer(
            partida_id=
                partida_id,

            usuario_id=
                usuario_id,

            sala_codigo=
                str(
                    codigo
                ),

            posicao=
                posicao,

            pontos=
                pontos,

            acertos=
                acertos,

            erros=
                erros,

            total_questoes=
                total_questoes,

            venceu=
                (
                    posicao
                    ==
                    1
                ),

            perfeita=
                perfeita,
        )


        db.session.add(
            registro
        )


    try:

        db.session.flush()


        for usuario_id in usuarios_processados:

            sincronizar_conquistas(
                usuario_id,
                commit=False
            )


        db.session.commit()


    except Exception:

        db.session.rollback()

        raise
