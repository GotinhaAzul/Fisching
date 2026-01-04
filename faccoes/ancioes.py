FACCAO = {
    "id": "ancioes",
    "nome": "Os Anciões",
    "descricao": (
        "Guardam o cume escondido por névoas eternas. Só recebem quem já encarou a Punição "
        "e consegue subir levando lembranças das profundezas e dos sonhos partidos."
    ),
    "missoes": [
        {
            "id": "escalar_montanha",
            "titulo": "Escalar da montanha",
            "descricao": (
                "Transpasse a encosta encharcada e alcance o platô onde a névoa abre. "
                "Suba carregando provas de que viu o vazio e atravessou as caçadas APEX."
            ),
            "requisitos": {
                "flags": ["questline_ancioes_desbloqueada"],
                "nivel_min": 70,
                "pagar_dinheiro": 8000,
                "peixes": {
                    "Pesadelos estilhaçados": 10,
                    "Serpente das Profundezas": 1,
                },
            },
            "recompensa": {
                "itens": [
                    {
                        "nome": "Cabo dos Sonhos",
                        "tipo": "item",
                        "raridade": "Artefato",
                        "kg": 0.0,
                        "valor": 0.0,
                        "vendavel": False,
                        "descricao": "Um cabo trançado que pulsa como se respirasse, recolhendo ecos do vazio.",
                    }
                ],
                "set_flag": "cabo_dos_sonhos_obtido",
            },
            "lore": (
                "A entidade Punição foi criada a partir da ganância dos pescadores, da reclusão dos "
                "Santuários e do orgulho dos piratas. Os Anciões aceitam falar porque você carregou "
                "essas memórias até o topo."
            ),
        },
        {
            "id": "exclusividade",
            "titulo": "Exclusividade",
            "descricao": (
                "Sente-se diante do círculo dos Anciões e questione por que escaparam da Punição. "
                "Mostre que já viu o pior das marés e traga criaturas que nasceram de sonhos quebrados."
            ),
            "requisitos": {
                "nivel_min": 78,
                "pagar_dinheiro": 4500,
                "capturou_punicao": True,
                "peixes": {
                    "Fênix Marinha": 1,
                    "Titã da Aurora": 1,
                    "Hidra Putrefata": 1,
                },
            },
            "recompensa": {
                "itens": [
                    {
                        "nome": "Linha dos Pesadelos",
                        "tipo": "item",
                        "raridade": "Artefato",
                        "kg": 0.0,
                        "valor": 0.0,
                        "vendavel": False,
                        "descricao": "Fibra fria que ecoa sussurros proféticos e não pode ser vendida.",
                    }
                ],
                "set_flag": [
                    "linha_dos_pesadelos_obtida",
                    "projeto_vara_punicao_desbloqueado",
                ],
            },
            "lore": (
                "Eles sempre souberam dos acontecimentos futuros da ilha, tinham diversos sonhos proféticos "
                "com isso. Mas, se este era o futuro, suas ações poderiam mesmo mudá-lo? Isso causou a loucura "
                "da Punição."
            ),
        },
    ],
    "buffs_passivos": [],
}
