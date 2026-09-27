# ============================================================
# FLASHMATTY - CATÁLOGO DE COSMÉTICOS
# ============================================================
#
# O catálogo fica no servidor.
# O navegador nunca decide preço, raridade ou tipo do item.
# ============================================================


TIPOS = (
    "titulo",
    "fundo",
    "moldura",
    "badge",
    "nome",
    "card",
    "efeito",
)


TIPOS_LABEL = {
    "titulo": "Títulos",
    "fundo": "Fundos de perfil",
    "moldura": "Molduras de avatar",
    "badge": "Badges",
    "nome": "Estilos de nome",
    "card": "Cartões de perfil",
    "efeito": "Efeitos de perfil",
}


RARIDADES = (
    "comum",
    "raro",
    "epico",
    "lendario",
    "mitico",
)


def item(
    item_id,
    tipo,
    nome,
    descricao,
    preco,
    raridade,
    icone,
    valor
):
    return {
        "id": item_id,
        "tipo": tipo,
        "nome": nome,
        "descricao": descricao,
        "preco": int(preco),
        "raridade": raridade,
        "icone": icone,
        "valor": valor,
    }


ITENS = [

    # ========================================================
    # TÍTULOS
    # ========================================================

    item(
        "titulo_calculista",
        "titulo",
        "Calculista",
        "Um título simples para quem gosta de resolver tudo.",
        120,
        "comum",
        "🧮",
        {
            "texto": "Calculista",
        },
    ),

    item(
        "titulo_mestre_tabuada",
        "titulo",
        "Mestre da Tabuada",
        "Mostre que multiplicação é com você.",
        260,
        "raro",
        "✖️",
        {
            "texto": "Mestre da Tabuada",
        },
    ),

    item(
        "titulo_cacador_desafios",
        "titulo",
        "Caçador de Desafios",
        "Para jogadores que não fogem de uma partida difícil.",
        420,
        "epico",
        "🎯",
        {
            "texto": "Caçador de Desafios",
        },
    ),

    item(
        "titulo_genio_numeros",
        "titulo",
        "Gênio dos Números",
        "Um título épico para quem domina os números.",
        650,
        "epico",
        "🧠",
        {
            "texto": "Gênio dos Números",
        },
    ),

    item(
        "titulo_lenda_flashmatty",
        "titulo",
        "Lenda do FlashMatty",
        "Um dos títulos mais prestigiados da loja.",
        1500,
        "lendario",
        "👑",
        {
            "texto": "Lenda do FlashMatty",
        },
    ),

    # ========================================================
    # FUNDOS
    # ========================================================

    item(
        "fundo_ceu_noturno",
        "fundo",
        "Céu Noturno",
        "Azul profundo com atmosfera noturna.",
        180,
        "comum",
        "🌙",
        {
            "background":
                "linear-gradient(135deg,#020617 0%,#172554 55%,#312e81 100%)",
        },
    ),

    item(
        "fundo_sunset",
        "fundo",
        "Sunset",
        "Um degradê quente inspirado no pôr do sol.",
        320,
        "raro",
        "🌅",
        {
            "background":
                "linear-gradient(135deg,#431407 0%,#9a3412 35%,#be185d 72%,#312e81 100%)",
        },
    ),

    item(
        "fundo_neon",
        "fundo",
        "Neon",
        "Cores elétricas para um perfil chamativo.",
        480,
        "epico",
        "💜",
        {
            "background":
                "radial-gradient(circle at 18% 20%,rgba(34,211,238,.34),transparent 30%),"
                "radial-gradient(circle at 82% 18%,rgba(236,72,153,.32),transparent 32%),"
                "linear-gradient(135deg,#020617 0%,#312e81 50%,#500724 100%)",
        },
    ),

    item(
        "fundo_galaxia",
        "fundo",
        "Galáxia",
        "Um fundo espacial com profundidade e brilho.",
        750,
        "lendario",
        "🌌",
        {
            "background":
                "radial-gradient(circle at 20% 22%,rgba(129,140,248,.45),transparent 24%),"
                "radial-gradient(circle at 80% 30%,rgba(217,70,239,.35),transparent 28%),"
                "radial-gradient(circle at 55% 88%,rgba(14,165,233,.30),transparent 30%),"
                "linear-gradient(145deg,#020617 0%,#111827 38%,#312e81 72%,#0f172a 100%)",
        },
    ),

    item(
        "fundo_esmeralda",
        "fundo",
        "Esmeralda",
        "Tons verdes profundos e sofisticados.",
        520,
        "epico",
        "💚",
        {
            "background":
                "radial-gradient(circle at 75% 25%,rgba(52,211,153,.32),transparent 28%),"
                "linear-gradient(135deg,#022c22 0%,#064e3b 45%,#0f172a 100%)",
        },
    ),

    # ========================================================
    # MOLDURAS
    # ========================================================

    item(
        "moldura_indigo",
        "moldura",
        "Indigo Glow",
        "Moldura brilhante em tons índigo.",
        150,
        "comum",
        "🔵",
        {
            "style":
                "border:4px solid #818cf8;"
                "box-shadow:0 0 0 4px rgba(99,102,241,.20),0 0 24px rgba(99,102,241,.55);",
        },
    ),

    item(
        "moldura_fogo",
        "moldura",
        "Fogo",
        "Uma moldura intensa para o avatar.",
        380,
        "raro",
        "🔥",
        {
            "style":
                "border:4px solid #fb923c;"
                "box-shadow:0 0 0 4px rgba(249,115,22,.20),0 0 26px rgba(239,68,68,.65);",
        },
    ),

    item(
        "moldura_gelo",
        "moldura",
        "Gelo",
        "Visual frio em azul e ciano.",
        380,
        "raro",
        "❄️",
        {
            "style":
                "border:4px solid #67e8f9;"
                "box-shadow:0 0 0 4px rgba(34,211,238,.18),0 0 26px rgba(14,165,233,.62);",
        },
    ),

    item(
        "moldura_ouro",
        "moldura",
        "Ouro Real",
        "Uma moldura dourada de alto destaque.",
        720,
        "lendario",
        "👑",
        {
            "style":
                "border:4px solid #facc15;"
                "box-shadow:0 0 0 4px rgba(250,204,21,.18),0 0 30px rgba(245,158,11,.72);",
        },
    ),

    item(
        "moldura_arco_iris",
        "moldura",
        "Arco-íris",
        "Uma moldura colorida e rara.",
        900,
        "mitico",
        "🌈",
        {
            "style":
                "border:4px solid #c084fc;"
                "box-shadow:0 0 0 4px rgba(56,189,248,.18),"
                "0 0 18px rgba(236,72,153,.62),0 0 34px rgba(34,211,238,.45);",
        },
    ),

    # ========================================================
    # BADGES
    # ========================================================

    item(
        "badge_estrela",
        "badge",
        "Estrela",
        "Uma estrela exibida junto ao avatar.",
        100,
        "comum",
        "⭐",
        {
            "simbolo": "⭐",
            "titulo": "Estrela",
        },
    ),

    item(
        "badge_raio",
        "badge",
        "Raio",
        "Para jogadores rápidos.",
        220,
        "raro",
        "⚡",
        {
            "simbolo": "⚡",
            "titulo": "Raio",
        },
    ),

    item(
        "badge_cerebro",
        "badge",
        "Cérebro",
        "Badge para quem gosta de desafios mentais.",
        360,
        "epico",
        "🧠",
        {
            "simbolo": "🧠",
            "titulo": "Cérebro",
        },
    ),

    item(
        "badge_trofeu",
        "badge",
        "Troféu",
        "Um símbolo de competição.",
        520,
        "epico",
        "🏆",
        {
            "simbolo": "🏆",
            "titulo": "Troféu",
        },
    ),

    item(
        "badge_coroa",
        "badge",
        "Coroa",
        "Badge lendário para o perfil.",
        1000,
        "lendario",
        "👑",
        {
            "simbolo": "👑",
            "titulo": "Coroa",
        },
    ),

    # ========================================================
    # ESTILOS DE NOME
    # ========================================================

    item(
        "nome_ciano",
        "nome",
        "Nome Ciano",
        "Seu nome ganha um tom ciano brilhante.",
        140,
        "comum",
        "🩵",
        {
            "style":
                "color:#67e8f9;text-shadow:0 0 16px rgba(34,211,238,.35);",
        },
    ),

    item(
        "nome_dourado",
        "nome",
        "Nome Dourado",
        "Destaque dourado para o nome do jogador.",
        300,
        "raro",
        "💛",
        {
            "style":
                "color:#fde047;text-shadow:0 0 18px rgba(250,204,21,.42);",
        },
    ),

    item(
        "nome_gradiente",
        "nome",
        "Gradiente Neon",
        "Nome com gradiente violeta, rosa e ciano.",
        560,
        "epico",
        "✨",
        {
            "style":
                "background:linear-gradient(90deg,#22d3ee,#a78bfa,#f472b6);"
                "-webkit-background-clip:text;background-clip:text;color:transparent;"
                "text-shadow:none;",
        },
    ),

    item(
        "nome_esmeralda",
        "nome",
        "Esmeralda",
        "Nome em verde esmeralda luminoso.",
        360,
        "raro",
        "💚",
        {
            "style":
                "color:#6ee7b7;text-shadow:0 0 18px rgba(16,185,129,.42);",
        },
    ),

    item(
        "nome_lendario",
        "nome",
        "Nome Lendário",
        "Um estilo premium com brilho quente.",
        900,
        "lendario",
        "🌟",
        {
            "style":
                "background:linear-gradient(90deg,#fef08a,#f59e0b,#fb7185,#c084fc);"
                "-webkit-background-clip:text;background-clip:text;color:transparent;"
                "filter:drop-shadow(0 0 10px rgba(245,158,11,.38));",
        },
    ),

    # ========================================================
    # CARTÕES
    # ========================================================

    item(
        "card_vidro",
        "card",
        "Vidro",
        "Cartão principal com efeito de vidro.",
        250,
        "raro",
        "🪟",
        {
            "style":
                "background:rgba(15,23,42,.68);"
                "backdrop-filter:blur(16px);"
                "border-color:rgba(148,163,184,.26);",
        },
    ),

    item(
        "card_neon",
        "card",
        "Neon",
        "Borda violeta e brilho neon.",
        480,
        "epico",
        "🟣",
        {
            "style":
                "background:rgba(15,23,42,.82);"
                "border-color:#a78bfa;"
                "box-shadow:0 0 28px rgba(139,92,246,.28);",
        },
    ),

    item(
        "card_ouro",
        "card",
        "Cartão Dourado",
        "Cartão com borda dourada e brilho quente.",
        700,
        "lendario",
        "🏅",
        {
            "style":
                "background:linear-gradient(145deg,rgba(69,26,3,.78),rgba(15,23,42,.90));"
                "border-color:#facc15;"
                "box-shadow:0 0 30px rgba(245,158,11,.25);",
        },
    ),

    item(
        "card_galactico",
        "card",
        "Cartão Galáctico",
        "Um cartão raro com tons cósmicos.",
        860,
        "lendario",
        "🌌",
        {
            "style":
                "background:linear-gradient(145deg,rgba(30,27,75,.88),rgba(88,28,135,.64),rgba(15,23,42,.90));"
                "border-color:#c084fc;"
                "box-shadow:0 0 34px rgba(168,85,247,.30);",
        },
    ),

    # ========================================================
    # EFEITOS
    # ========================================================

    item(
        "efeito_estrelas",
        "efeito",
        "Estrelas",
        "Pequenos pontos de luz se movem pelo fundo.",
        350,
        "raro",
        "✨",
        {
            "classe": "fm-effect-stars",
        },
    ),

    item(
        "efeito_grade",
        "efeito",
        "Grade Digital",
        "Uma grade futurista discreta.",
        520,
        "epico",
        "🔷",
        {
            "classe": "fm-effect-grid",
        },
    ),

    item(
        "efeito_aurora",
        "efeito",
        "Aurora",
        "Faixas luminosas flutuam suavemente.",
        800,
        "lendario",
        "🌈",
        {
            "classe": "fm-effect-aurora",
        },
    ),

    item(
        "efeito_scan",
        "efeito",
        "Scan",
        "Uma faixa luminosa percorre o perfil.",
        620,
        "epico",
        "📡",
        {
            "classe": "fm-effect-scan",
        },
    ),
]


ITENS_POR_ID = {
    item["id"]: item
    for item in ITENS
}


def obter_item(item_id):
    return ITENS_POR_ID.get(
        str(item_id or "").strip()
    )


def itens_por_tipo():
    agrupados = {
        tipo: []
        for tipo in TIPOS
    }

    for registro in ITENS:
        agrupados[
            registro["tipo"]
        ].append(
            registro
        )

    return agrupados
