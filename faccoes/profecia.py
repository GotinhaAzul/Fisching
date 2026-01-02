FACCAO = {
    "id": "profecia",
    "nome": "A Profecia",
    "descricao": (
        "As páginas roubadas dos mercadores falam de um vazio absoluto. Só quem conhece"
        " cada criatura da ilha consegue ler o que resta sem enlouquecer."
    ),
    "missoes": [
        {
            "id": "a_profecia",
            "titulo": "A PROFECIA",
            "descricao": "Leia a profecia nos registros do mercador.",
            "requisitos": {
                "faccoes_concluidas": ["mercadores"],
                "flags": ["profecia_desbloqueada"],
                "bestiario_completo": True,
            },
            "recompensa": {
                "set_flag": "acesso_ao_vazio",
            },
            "lore": (
                "A existência de uma entidade chamada de \"Punição\", responsável de"
                " trazer inúmeras pragas a essa ilha há muito tempo atrás. Mas, a sua"
                " materialização caiu na loucura."
            ),
        },
        {
            "id": "queda",
            "titulo": "Queda.",
            "descricao": "Fisgue um pouco de senso para a Punição.",
            "requisitos": {
                "flags": ["acesso_ao_vazio"],
                "capturou_punicao": True,
            },
            "recompensa": {
                "set_flag": "questline_ancioes_desbloqueada",
            },
            "lore": (
                "Sem a entidade de tormento, agora a ilha se via livre. No entanto, algo"
                " doi no fundo de sua cabeça, apenas quem erra merece ser punido."
            ),
        },
    ],
    "buffs_passivos": [],
}
