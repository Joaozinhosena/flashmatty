import time
from threading import RLock


_LOCK = RLock()

_CONEXOES = {}

TEMPO_EXPIRACAO = 50


# ============================================================
# TEMPO INTERNO
# ============================================================

def _agora():

    return time.monotonic()


# ============================================================
# LIMPAR CONEXÕES EXPIRADAS
# ============================================================

def _limpar_expirados_locked():

    limite = (
        _agora()
        -
        TEMPO_EXPIRACAO
    )


    usuarios_vazios = []


    for usuario_id, conexoes in list(
        _CONEXOES.items()
    ):

        sids_expirados = [

            sid

            for sid, ultima_atividade
            in list(
                conexoes.items()
            )

            if ultima_atividade
            <
            limite
        ]


        for sid in sids_expirados:

            conexoes.pop(
                sid,
                None
            )


        if not conexoes:

            usuarios_vazios.append(
                usuario_id
            )


    for usuario_id in usuarios_vazios:

        _CONEXOES.pop(
            usuario_id,
            None
        )


# ============================================================
# REGISTRAR / ATUALIZAR PRESENÇA
# ============================================================

def registrar_presenca(
    usuario_id,
    sid
):

    usuario_id = int(
        usuario_id
    )


    with _LOCK:

        _limpar_expirados_locked()


        conexoes = (
            _CONEXOES.setdefault(
                usuario_id,
                {}
            )
        )


        ja_estava_online = bool(
            conexoes
        )


        conexoes[
            sid
        ] = _agora()


        return (
            not ja_estava_online
        )


# ============================================================
# VERIFICAR ONLINE
# ============================================================

def esta_online(
    usuario_id
):

    try:

        usuario_id = int(
            usuario_id
        )

    except (
        TypeError,
        ValueError
    ):

        return False


    with _LOCK:

        _limpar_expirados_locked()


        return bool(
            _CONEXOES.get(
                usuario_id
            )
        )


# ============================================================
# PEGAR SIDS DO USUÁRIO
# ============================================================

def sids_do_usuario(
    usuario_id
):

    try:

        usuario_id = int(
            usuario_id
        )

    except (
        TypeError,
        ValueError
    ):

        return []


    with _LOCK:

        _limpar_expirados_locked()


        return list(

            _CONEXOES.get(
                usuario_id,
                {}
            ).keys()

        )


# ============================================================
# STATUS DE VÁRIOS USUÁRIOS
# ============================================================

def status_varios(
    ids
):

    resultado = {}


    with _LOCK:

        _limpar_expirados_locked()


        for usuario_id in ids:

            try:

                usuario_id = int(
                    usuario_id
                )

            except (
                TypeError,
                ValueError
            ):

                continue


            resultado[
                str(
                    usuario_id
                )
            ] = bool(

                _CONEXOES.get(
                    usuario_id
                )

            )


    return resultado