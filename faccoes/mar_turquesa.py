BUFFS = {
    "instinto_saqueador": {
        "id": "instinto_saqueador",
        "nome": "Instinto Saqueador",
        "efeito": "+2% no valor dos peixes pescados.",
        "efeitos": {"bonus_valor": 1.02},
        "fonte": "Vida de Gato do Mar",
    },
    "licenca_contrabando": {
        "id": "licenca_contrabando",
        "nome": "Licença de Contrabando",
        "efeito": "A vara dos piratas passa a aparecer nas bancadas do mercado.",
        "efeitos": {},
        "fonte": "Orgulho",
    },
}


FACCAO = {
    "id": "piratas_do_pouso",
    "nome": "Piratas do Pouso",
    "descricao": (
        "Visível à beira do Pouso Pirata, mas só falam após você destravar a pool. "
        "Eles defendem o próprio cais com histórias de saques e desafiam iniciantes a provar "
        "que merecem ouvir os segredos do mar.")
    ,
    "missoes": [
        {
            "id": "conhecer_dos_marujos",
            "titulo": "Conhecer dos marujos",
            "descricao": (
                "Pergunte como os piratas surgiram enquanto eles vigiam o cais recém-aberto."
            ),
            "requisitos": {
                "pools_desbloqueadas": ["Pouso Pirata"],
                "nivel_min": 5,
                "missoes_rng_min": 6,
                "pagar_dinheiro": 60,
                "peixes_por_raridade": {"Comum": 4},
            },
            "recompensa": {
                "xp": 100,
            },
            "lore": (
                "Os piratas nasceram dos primeiros pescadores expulsos pelos anciãos. "
                "Viraram mercenários, saqueando barcos que deixavam a ilha e vendendo o butim em mercados negros."
            ),
        },
        {
            "id": "vida_de_gato_do_mar",
            "titulo": "Vida de gato do mar",
            "descricao": (
                "Pergunte onde escondem as riquezas enquanto ajuda a carregar caixotes."
            ),
            "requisitos": {
                "pools_desbloqueadas": ["Pouso Pirata"],
                "nivel_min": 5,
                "missoes_rng_min": 7,
                "pagar_dinheiro": 80,
                "peixes": {"Tilápia do Convés": 2, "Robalo do Capitão": 1},
            },
            "recompensa": {
                "buff_permanente": BUFFS["instinto_saqueador"],
            },
            "lore": (
                "Numa noite silenciosa, os piratas roubaram um artefato dos anciãos e o embutiram "
                "em uma vara feita para atrair riquezas. A tripulação ainda caça pistas do tesouro perdido."
            ),
            "buff_preview": BUFFS["instinto_saqueador"],
        },
        {
            "id": "o_capitao",
            "titulo": "O capitão",
            "descricao": "Pergunte ao capitão sobre as lendas terríveis das águas fundas.",
            "requisitos": {
                "pools_desbloqueadas": ["Pouso Pirata"],
                "nivel_min": 6,
                "missoes_rng_min": 8,
                "pagar_dinheiro": 120,
                "peixes_por_raridade": {"Incomum": 2, "Raro": 1},
            },
            "recompensa": {
                "dinheiro": 500,
            },
            "lore": (
                "O capitão jura ter visto feras alteradas no fundo do oceano. "
                "Não eram peixes comuns: pareciam atiçados por um poder invisível, "
                "presos em um estado de raiva constante."
            ),
        },
        {
            "id": "orgulho_pirata",
            "titulo": "Orgulho",
            "descricao": "Pergunte pelo orgulho ferido do capitão e o que ainda os mantém acordados.",
            "requisitos": {
                "pools_desbloqueadas": ["Pouso Pirata"],
                "nivel_min": 6,
                "missoes_rng_min": 9,
                "pagar_dinheiro": 140,
                "peixes": {"Arraia do Saque": 1},
            },
            "recompensa": {
                "buff_permanente": BUFFS["licenca_contrabando"],
            },
            "lore": (
                "Eles já fisgaram bestas marinas, mas nunca conseguiram puxá-las por causa de um poder invisível. "
                "Ainda assim, o valor prometido por esses monstros os mantém acordados e alimenta o desejo de voltar. "
                "Com a confiança conquistada, a vara dos piratas passa a ser vendida no mercado."
            ),
            "buff_preview": BUFFS["licenca_contrabando"],
        },
    ],
    "buffs_passivos": [
        BUFFS["instinto_saqueador"],
        BUFFS["licenca_contrabando"],
    ],
}
