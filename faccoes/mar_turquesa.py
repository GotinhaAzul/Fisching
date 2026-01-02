BUFFS = {
    "olhar_cartografico": {
        "id": "olhar_cartografico",
        "nome": "Olhar Cartográfico",
        "efeito": "+2% XP ao pescar em novas pools.",
        "efeitos": {"xp_multiplicador": 1.02},
        "fonte": "Prólogo dos Vigias",
    },
    "vigilia_farol": {
        "id": "vigilia_farol",
        "nome": "Vigília do Farol",
        "efeito": "+1% chance geral de raridades altas.",
        "efeitos": {"bonus_raridade_vara": 0.01},
        "fonte": "Correntes Invisíveis",
    },
    "guia_mares": {
        "id": "guia_mares",
        "nome": "Guia das Marés",
        "efeito": "+0.5s de reação e +1% chance de mutação.",
        "efeitos": {"bonus_reacao": 0.5, "bonus_mutacao": 0.01},
        "fonte": "Juramento do Farol",
    },
}


FACCAO = {
    "id": "vigias_do_mar_turquesa",
    "nome": "Vigias do Mar Turquesa",
    "descricao": (
        "Uma facção de batedores costeiros que mapeia tempestades, registra criaturas raras "
        "e compartilha lendas de pescadores desaparecidos. Suas missões contam a história "
        "do primeiro farol submerso."
    ),
    "missoes": [
        {
            "id": "capitulo_1",
            "titulo": "Chamado das Marolas",
            "descricao": (
                "Conheça a vigia Luma, leve peixes simples para os mapas dela "
                "e descubra por que o farol sumiu."
            ),
            "requisitos": {
                "missoes_rng_min": 1,
                "pagar_dinheiro": 50,
                "peixes_por_raridade": {"Comum": 5},
            },
            "recompensa": {
                "dinheiro": 80,
                "xp": 120,
                "buff_permanente": BUFFS["olhar_cartografico"],
            },
            "lore": (
                "Luma revela que os mapas do farol estão espalhados. O sinal de bruma que ocultou "
                "a torre veio de um cristal de maré quebrado."
            ),
            "buff_preview": BUFFS["olhar_cartografico"],
        },
        {
            "id": "capitulo_2",
            "titulo": "Correntes Invisíveis",
            "descricao": "Siga as correntes que desviam barcos e recolha amostras alteradas.",
            "requisitos": {
                "nivel_min": 2,
                "missoes_rng_min": 3,
                "pagar_dinheiro": 90,
                "peixes_por_raridade": {"Incomum": 3, "Raro": 1},
                "peixes": {"Truta Arco-Íris": 2},
                "mutacoes": {"Congelado": 1},
            },
            "recompensa": {
                "dinheiro": 110,
                "xp": 160,
                "buff_permanente": BUFFS["vigilia_farol"],
            },
            "lore": (
                "As correntes são mantidas por antenas submersas. Uma mensagem gravada indica que "
                "os Vigias evacuaram o farol antes de um vendaval mágico."
            ),
            "buff_preview": BUFFS["vigilia_farol"],
        },
        {
            "id": "capitulo_3",
            "titulo": "Juramento do Farol",
            "descricao": (
                "Restituir o cristal de maré exige tributos raros. Reúna-os e restaure o sinal."
            ),
            "requisitos": {
                "nivel_min": 4,
                "missoes_rng_min": 6,
                "pagar_dinheiro": 150,
                "peixes_por_raridade": {"Raro": 2, "Lendário": 1},
                "mutacoes": {"Abissal": 1},
            },
            "recompensa": {
                "dinheiro": 150,
                "xp": 220,
                "buff_permanente": BUFFS["guia_mares"],
            },
            "lore": (
                "O farol emerge: um brilho turquesa acompanha o juramento dos Vigias. "
                "A facção promete guiar pescadores para evitar novas perdas no nevoeiro."
            ),
            "buff_preview": BUFFS["guia_mares"],
        },
    ],
    "buffs_passivos": [
        BUFFS["olhar_cartografico"],
        BUFFS["vigilia_farol"],
        BUFFS["guia_mares"],
    ],
}
