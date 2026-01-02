FACCAO = {
    "id": "mercadores_errantes",
    "nome": "Mercadores Errantes",
    "descricao": (
        "Chegaram com os pescadores e lucraram vendendo suprimentos. Fugiram quando as pragas começaram, exceto um "
        "mercador que ainda faz negócios com você. Somente após ajudar piratas e santuários eles confiarão em você."
    ),
    "missoes": [
        {
            "id": "m1_contabilidade",
            "titulo": "Contabilidade Sombria",
            "descricao": "Revise cadernos antigos e entenda como espíritos zombavam dos moradores.",
            "requisitos": {
                "entregar_peixes": {"Comum": 3, "Incomum": 3},
                "dinheiro": 150,
                "missoes_rng_concluidas": 4,
            },
            "lore_revelada": (
                "Os mercadores eram bem recebidos porque facilitavam o comércio, mas notaram espíritos adormecendo "
                "pessoas no fundo do oceano. O único que ficou teme nomear a entidade que ria desses naufrágios."
            ),
            "recompensa": {
                "dinheiro": 120,
                "buff": "+1% XP ao vender itens raros",
            },
            "buff_preview": {
                "nome": "Margem de Lucro",
                "efeito": "+1% XP em vendas de itens raros.",
                "fonte": "Primeiro acordo mercador",
            },
        },
        {
            "id": "m2_punicao",
            "titulo": "Nome Riscado",
            "descricao": "Siga as anotações rasuradas até descobrir o nome da entidade que espalhou pragas.",
            "requisitos": {
                "entregar_peixes": {"Raro": 2},
                "peixes_mutados": {"Sombrio": 2},
                "dinheiro": 220,
                "nivel_minimo": 15,
            },
            "lore_revelada": (
                "Nos papéis, um nome riscado: Punição. Ela trouxe pragas, deu raiva às feras expulsando piratas, apagou "
                "memórias dos santuários e julgou pescadores gananciosos. Ao encará-la, o mercador admitiu que sua "
                "materialização enlouqueceu por não saber como julgar os anciões."
            ),
            "recompensa": {
                "dinheiro": 140,
                "buff": "+1% sorte em negociações de alto valor",
            },
            "buff_preview": {
                "nome": "Assinatura do Contrato",
                "efeito": "+1% sorte em rolagens de negociação.",
                "fonte": "Revelar a Punição",
            },
        },
        {
            "id": "m3_profecia",
            "titulo": "Profecia do Vazio",
            "descricao": "Prepare a rota para a pool ""O Vazio"" e confirme a profecia sobre nivel 100 e bestiário.",
            "requisitos": {
                "entregar_peixes": {"Lendário": 1},
                "peixes_mutados": {"Caos": 1},
                "missoes_rng_concluidas": 10,
                "progresso_bestiario": 0.75,
                "dinheiro": 0,
            },
            "lore_revelada": (
                "O mercador admite: a Punição profetizou que apenas você poderia julgá-la. Para abrir 'O Vazio', será "
                "preciso completar 100% do bestiário e atingir o nível 100. Lá, peixes chamados Pesadelos Estilhaçados "
                "se desmaterializam, e só 1% de chance resta para confrontar a própria Punição em um minigame de dez teclas."
            ),
            "recompensa": {
                "dinheiro": 0,
                "buff": "+1% XP ganho ao registrar peixes no bestiário",
                "desbloqueio": "Libera a última questline na pool 'O Vazio'",
            },
            "buff_preview": {
                "nome": "Guia do Vazio",
                "efeito": "+1% XP ao registrar novos peixes e abertura da pool 'O Vazio'.",
                "fonte": "Preparação para a profecia",
            },
        },
    ],
    "buffs_passivos": [
        {
            "nome": "Margem de Lucro",
            "efeito": "+1% XP em vendas de itens raros.",
            "fonte": "Capítulo 1",
        },
        {
            "nome": "Assinatura do Contrato",
            "efeito": "+1% sorte em rolagens de negociação.",
            "fonte": "Capítulo 2",
        },
        {
            "nome": "Guia do Vazio",
            "efeito": "+1% XP ao registrar novos peixes e abertura da pool 'O Vazio'.",
            "fonte": "Capítulo 3",
        },
    ],
}
