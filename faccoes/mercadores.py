FACCAO = {
    "id": "mercadores",
    "nome": "Os Mercadores",
    "descricao": (
        "Recém-tornados senhores das bancas, os mercadores só revelam seus segredos "
        "após você costurar alianças com piratas e santuários. Eles contam histórias "
        "entre moedas contadas e pragas antigas que ainda os assombram."
    ),
    "missoes": [
        {
            "id": "moedas_de_ouro",
            "titulo": "Moedas de ouro",
            "descricao": (
                "Acompanhe o mercador enquanto ele troca moedas manchadas de sal e "
                "pergunte como o mercado nasceu ao lado dos pescadores."
            ),
            "requisitos": {
                "faccoes_concluidas": ["piratas_do_pouso", "santuarios"],
                "nivel_min": 14,
                "pagar_dinheiro": 250,
                "peixes": {"Pargo do Tesouro": 2, "Truta Encoberta": 2},
            },
            "recompensa": {
                "xp": 100,
            },
            "lore": (
                "Os mercadores chegaram junto dos pescadores nessa ilha. Mas, ao invés de pescar, "
                "construíram lojas para ganharem o dinheiro dos pescadores."
            ),
        },
        {
            "id": "e_os_outros",
            "titulo": "E os outros?",
            "descricao": (
                "Puxe conversa ao fim do expediente, quando o mercado esvazia, e questione "
                "quem mais já tentou abrir bancas além dele."
            ),
            "requisitos": {
                "nivel_min": 15,
                "peixes": {
                    "Leviatã do Bucanero": 1,
                    "Peixe-Dragão": 2,
                    "Arraia do Subsolo": 2,
                },
            },
            "recompensa": {
                "dinheiro": 1000,
            },
            "lore": (
                "Com o chegar das pragas, o espírito fraco dos comerciantes os fez fugirem da ilha. "
                "A entidade mexia com as pessoas naquela ilha, zombando delas e as fazendo adormecer "
                "no fundo do oceano."
            ),
        },
        {
            "id": "entidade",
            "titulo": "Entidade?",
            "descricao": (
                "Insista sobre a entidade enquanto observa o mercador fechar caixas, percebendo "
                "o desconforto em cada silêncio."
            ),
            "requisitos": {
                "nivel_min": 16,
                "pagar_dinheiro": 400,
                "peixes": {"Peixe da Névoa Antiga": 1},
                "mutacoes": {"Abissal": 1},
            },
            "recompensa": {
                "xp": 100,
            },
            "lore": (
                "Ele se recusa a falar, mas sem intenção, revela a existência de registros."
            ),
        },
        {
            "id": "um_pouco_de_pirataria",
            "titulo": "Um pouco de pirataria.",
            "descricao": (
                "Invada o depósito à noite e roube os registros do mercador antes que ele "
                "perceba que você não é apenas um comprador fiel."
            ),
            "requisitos": {
                "nivel_min": 18,
                "pagar_dinheiro": 1200,
                "peixes": {
                    "Kraken": 1,
                    "Guardião Espectral": 1,
                    "Serafim Boreal": 1,
                },
                "mutacoes": {"Abissal": 2, "Temporal": 1},
            },
            "recompensa": {
                "set_flag": ["profecia_desbloqueada", "projeto_maelstrom_desbloqueado"],
            },
            "lore": (
                "A existência de uma entidade chamada de \"Punição\", responsável de trazer inúmeras "
                "pragas a essa ilha há muito tempo atrás. Mas, a sua materialização caiu na loucura."
            ),
        },
    ],
    "buffs_passivos": [],
}
