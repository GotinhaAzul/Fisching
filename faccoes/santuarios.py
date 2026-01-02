FACCAO = {
    "id": "santuarios",
    "nome": "Os Santuários",
    "descricao": (
        "Um grupo remanescente dos habitantes originais, agora reclusos em um túnel"
        " subterrâneo. Eles se aproximam apenas de pescadores que demonstram cuidado"
        " com a ilha e curiosidade pelas lendas."),
    "missoes": [
        {
            "id": "vestes_brancas",
            "titulo": "Vestes",
            "descricao": (
                "Converse com o homem de roupas brancas na rua e pergunte sobre as vestes"
                " que ele guarda desde antes dos pescadores chegarem."),
            "requisitos": {
                "nivel_min": 4,
                "missoes_rng_min": 2,
            },
            "recompensa": {
                "xp": 130,
            },
            "lore": (
                "Os Santuários eram um pequeno grupo dos habitantes originais. Eles tentaram"
                " expulsar os pescadores com armas improvisadas, mas falharam."),
        },
        {
            "id": "nossa_queda",
            "titulo": "Nossa queda",
            "descricao": (
                "Pergunte ao membro do Santuário por que falharam e escute as fraturas"
                " internas do grupo."),
            "requisitos": {
                "nivel_min": 5,
                "missoes_rng_min": 3,
                "xp_min": 200,
            },
            "recompensa": {
                "buff_permanente": {
                    "id": "memorias_santuarios",
                    "nome": "Memórias dos Santuários",
                    "efeito": "+2% XP ganho ao pescar.",
                    "efeitos": {"xp_multiplicador": 1.02},
                },
            },
            "lore": (
                "A ganância dos pescadores era insaciável. Com a ajuda dos piratas, tornou-se"
                " impossível lutar. Eles decidiram buscar um plano alternativo."),
        },
        {
            "id": "santuario_sagrado",
            "titulo": "O santuário sagrado",
            "descricao": (
                "Pergunte ao Santuário sobre o plano ousado que guardaram em segredo"
                " desde a retirada."),
            "requisitos": {
                "nivel_min": 6,
                "missoes_rng_min": 4,
                "peixes_por_raridade": {"Comum": 12},
            },
            "recompensa": {
                "xp": 150,
            },
            "lore": (
                "Eles passaram a pescar de madrugada, longe dos olhares dos pescadores,"
                " e levavam os peixes a um santuário subterrâneo. O lugar atraiu espíritos"
                " e transformou o lago em um refúgio místico."),
        },
        {
            "id": "reclusao",
            "titulo": "Reclusão",
            "descricao": (
                "Ajude o Santuário a relembrar quais peixes protegiam o lago escondido"
                " e onde fica a entrada."),
            "requisitos": {
                "nivel_min": 7,
                "missoes_rng_min": 5,
                "peixes_por_raridade": {"Incomum": 6, "Raro": 2},
                "pagar_dinheiro": 180,
            },
            "recompensa": {
                "xp": 200,
                "set_flag": "desbloqueou_santuario_sagrado",
                "buff_permanente": {
                    "id": "santuario_sagrado_pool",
                    "nome": "Entrada do Santuário",
                    "efeito": "Acesso à pool Santuário Sagrado e +10% XP naquele lago.",
                    "efeitos": {
                        "xp_multiplicador": 1.10,
                    },
                },
            },
            "lore": (
                "As forças sobrenaturais fortaleceram os peixes do lago. Alguns foram"
                " interceptados pelos piratas e lançados ao mar, criando um pequeno"
                " grupo de peixes secretos para quase todos."),
        },
    ],
    "buffs_passivos": [],
}
