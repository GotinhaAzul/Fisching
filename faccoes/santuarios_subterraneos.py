FACCAO = {
    "id": "santuarios_subterraneos",
    "nome": "Círculo dos Santuários",
    "descricao": (
        "Restos da resistência original da ilha. Eles pescavam de madrugada e escondiam peixes em um santuário "
        "subterrâneo que ganhou vida própria. Precisam de ajuda para recuperar memórias apagadas."
    ),
    "missoes": [
        {
            "id": "s1_resistencia",
            "titulo": "Memórias do Mármore",
            "descricao": "Fale com o sobrevivente sem memória e reconstrua como a resistência surgiu.",
            "requisitos": {
                "entregar_peixes": {"Comum": 4, "Incomum": 2},
                "dinheiro": 60,
                "missoes_rng_concluidas": 1,
            },
            "lore_revelada": (
                "Os santuários nasceram quando habitantes expulsaram pescadores armados. Em segredo, eles pescaram à noite "
                "e juraram proteger a ilha que o avô do player descrevia como viva."
            ),
            "recompensa": {
                "dinheiro": 80,
                "buff": "+1% XP em pescas noturnas",
            },
            "buff_preview": {
                "nome": "Luz de Vigia",
                "efeito": "+1% XP em pescas noturnas.",
                "fonte": "Primeiro passo da resistência",
            },
        },
        {
            "id": "s2_passagens",
            "titulo": "Passagens de Musgo",
            "descricao": "Reforce túneis do santuário onde o musgo solidificou rachaduras.",
            "requisitos": {
                "entregar_peixes": {"Incomum": 4, "Raro": 2},
                "peixes_mutados": {"Luminoso": 1},
                "dinheiro": 110,
                "nivel_minimo": 10,
            },
            "lore_revelada": (
                "O santuário subterrâneo criou vida: musgo fechou rachaduras e espíritos limpam o chão. Alguns peixes "
                "foram interceptados pelos piratas e devolvidos ao mar, criando um grupo secreto e raivoso."
            ),
            "recompensa": {
                "dinheiro": 95,
                "buff": "+1% raridade em pools ligadas ao santuário",
            },
            "buff_preview": {
                "nome": "Sopro do Subsolo",
                "efeito": "+1% chance de raridade alta em pools do santuário.",
                "fonte": "Restauro das passagens",
            },
        },
        {
            "id": "s3_esquecimento",
            "titulo": "Aquele que Esqueceu",
            "descricao": "Recupere fragmentos de memória apagados por uma força misteriosa.",
            "requisitos": {
                "entregar_peixes": {"Raro": 3},
                "peixes_mutados": {"Espectral": 2},
                "missoes_rng_concluidas": 6,
                "progresso_bestiario": 0.45,
                "dinheiro": 0,
            },
            "lore_revelada": (
                "A força chamada Punição apagou memórias por covardia dos santuários ao fugir com peixes. Ainda assim, "
                "eles guardam as criaturas resgatadas e abrirão o santuário quando você completar a linha."
            ),
            "recompensa": {
                "dinheiro": 0,
                "buff": "+1% duração de buffs de prato quando em cavernas",
                "desbloqueio": "Desbloqueia o acesso ao santuário subterrâneo",
            },
            "buff_preview": {
                "nome": "Guardiões da Madrugada",
                "efeito": "+1% duração de buffs de prato em áreas cavernosas e abertura do santuário.",
                "fonte": "Conclusão do arco dos santuários",
            },
        },
    ],
    "buffs_passivos": [
        {
            "nome": "Luz de Vigia",
            "efeito": "+1% XP em pescas noturnas.",
            "fonte": "Capítulo 1",
        },
        {
            "nome": "Sopro do Subsolo",
            "efeito": "+1% chance de raridade alta em pools do santuário.",
            "fonte": "Capítulo 2",
        },
        {
            "nome": "Guardiões da Madrugada",
            "efeito": "+1% duração de buffs de prato em áreas cavernosas; abre o santuário.",
            "fonte": "Capítulo 3",
        },
    ],
}
