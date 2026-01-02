FACCAO = {
    "id": "piratas_exilados",
    "nome": "Irmandade dos Piratas Exilados",
    "descricao": (
        "Mercenários que começaram como pescadores, foram expulsos pelos anciões e agora se escondem na baía "
        "proibida. Eles afirmam ter visto peixes enlouquecidos e quase fisgaram um deles com uma vara que roubaram "
        "dos anciões."
    ),
    "missoes": [
        {
            "id": "p1_origem",
            "titulo": "Rasgos na Névoa",
            "descricao": "Acompanhe o batedor Brasa e descubra como os piratas passaram a saquear barcos de pesca.",
            "requisitos": {
                "entregar_peixes": {"Comum": 6},
                "dinheiro": 50,
                "missoes_rng_concluidas": 2,
            },
            "lore_revelada": (
                "Os piratas nasceram de pescadores que cansaram da miséria. Eles seguiram as histórias do avô do player "
                "sobre um oceano vivo, mas preferiram roubar mercadorias e vendê-las em mercados negros em vez de pescar "
                "com respeito."
            ),
            "recompensa": {
                "dinheiro": 90,
                "buff": "+1% XP ao vender peixes comuns em qualquer loja",
            },
            "buff_preview": {
                "nome": "Rota dos Saques",
                "efeito": "+1% XP em vendas de peixes comuns.",
                "fonte": "Capítulo de origem pirata",
            },
        },
        {
            "id": "p2_exilio",
            "titulo": "Baía Interdita",
            "descricao": "Recupere diários queimados para entender por que os anciões expulsaram a frota.",
            "requisitos": {
                "entregar_peixes": {"Incomum": 4},
                "peixes_mutados": {"Corrompido": 1},
                "dinheiro": 120,
                "nivel_minimo": 8,
            },
            "lore_revelada": (
                "Os anciões, prevendo a ganância crescente, expulsaram os piratas da ilha. Sem porto, eles se isolaram "
                "numa baía recortada, onde a névoa engolia barcos inteiros e fazia até veteranos tremerem."
            ),
            "recompensa": {
                "dinheiro": 110,
                "buff": "+0.5% de chance de encontrar peixes maiores ao pescar em mares abertos",
            },
            "buff_preview": {
                "nome": "Eco da Baía",
                "efeito": "+0.5% tamanho máximo de peixes em mares abertos.",
                "fonte": "Exílio forçado",
            },
        },
        {
            "id": "p3_artefato",
            "titulo": "A Vara Imbuída",
            "descricao": "Investigue o artefato roubado e como ele foi acoplado a uma vara atraidora de riquezas.",
            "requisitos": {
                "entregar_peixes": {"Raro": 3},
                "peixes_mutados": {"Abrasado": 2},
                "dinheiro": 200,
                "peixes_capturados_total": 60,
            },
            "lore_revelada": (
                "Por um curto período, a tripulação roubou um artefato dos anciões. Eles o imbuíram em uma vara capaz "
                "de atrair tesouros, mas o preço foi alto: a madeira queimava as mãos e sussurrava um julgamento "
                "invisível. O artefato veio da aliança forjada entre pescadores e anciões, que tentaram criar varas "
                "para fisgar as bestas e vendê-las longe dali — nenhum pescador conseguiu, e a frustração corroeu a ilha."
            ),
            "recompensa": {
                "dinheiro": 130,
                "buff": "+1% XP ao capturar peixes raros alterados",
            },
            "buff_preview": {
                "nome": "Madeira Profanada",
                "efeito": "+1% XP em peixes raros com mutações.",
                "fonte": "Artefato imbuído",
            },
        },
        {
            "id": "p4_grito",
            "titulo": "Grito das Feras",
            "descricao": "Enfrente o medo do capitão e documente as feras do fundo que vivem em raiva constante.",
            "requisitos": {
                "entregar_peixes": {"Lendário": 1},
                "peixes_mutados": {"Fúria": 1},
                "missoes_rng_concluidas": 8,
                "progresso_bestiario": 0.4,
            },
            "lore_revelada": (
                "O capitão descreve bestas alteradas por pragas espirituais. Eles quase as fisgaram, mas algo não "
                "físico — a tal Punição — cortou as linhas. Sem uma captura bem-sucedida, a ilha parecia destinada ao "
                "fim. O acordo: se você concluir a linha deles, poderá comprar a vara lendária que eles guardam."
            ),
            "recompensa": {
                "dinheiro": 0,
                "buff": "+1% sorte ao perseguir criaturas lendárias do oceano",
                "desbloqueio": "Libera a compra da vara lendária dos piratas",
            },
            "buff_preview": {
                "nome": "Intuição do Corsário",
                "efeito": "+1% sorte para encontros lendários e acesso à vara lendária pirata.",
                "fonte": "Concluir o arco dos piratas",
            },
        },
    ],
    "buffs_passivos": [
        {
            "nome": "Rota dos Saques",
            "efeito": "+1% XP em vendas de peixes comuns.",
            "fonte": "Capítulo 1",
        },
        {
            "nome": "Eco da Baía",
            "efeito": "+0.5% tamanho máximo de peixes em mares abertos.",
            "fonte": "Capítulo 2",
        },
        {
            "nome": "Madeira Profanada",
            "efeito": "+1% XP em peixes raros com mutações.",
            "fonte": "Capítulo 3",
        },
        {
            "nome": "Intuição do Corsário",
            "efeito": "+1% sorte para encontros lendários e compra da vara lendária pirata.",
            "fonte": "Capítulo 4",
        },
    ],
}
