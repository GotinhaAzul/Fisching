FACCAO = {
    "id": "vigilia_do_vazio",
    "nome": "Vigia do Vazio",
    "descricao": (
        "Aliança final entre anciões, piratas arrependidos e santuários. Só aparece após concluir as outras linhas "
        "e confirma a profecia sobre o julgamento da Punição."
    ),
    "missoes": [
        {
            "id": "v1_porta",
            "titulo": "Abertura do Vazio",
            "descricao": "Coordene piratas, santuários e mercadores para estabilizar a pool 'O Vazio'.",
            "requisitos": {
                "entregar_peixes": {"Raro": 4},
                "peixes_mutados": {"Etéreo": 2},
                "missoes_rng_concluidas": 12,
                "progresso_bestiario": 0.85,
                "dinheiro": 0,
            },
            "lore_revelada": (
                "Os anciões sempre souberam do destino da ilha. Sonhos proféticos mostraram as pragas e a Punição, mas "
                "eles temeram quebrar a ordem natural. Agora, com as facções reunidas, a porta para 'O Vazio' pode ser "
                "aberta sem condenar a ilha."
            ),
            "recompensa": {
                "dinheiro": 0,
                "buff": "+1% XP em capturas dentro de 'O Vazio'",
            },
            "buff_preview": {
                "nome": "Vigília Compartilhada",
                "efeito": "+1% XP dentro da pool 'O Vazio'.",
                "fonte": "Unir as facções",
            },
        },
        {
            "id": "v2_julgamento",
            "titulo": "Julgamento da Punição",
            "descricao": "Complete 100% do bestiário, alcance o nível 100 e enfrente o minigame de dez teclas.",
            "requisitos": {
                "entregar_peixes": {"Lendário": 2},
                "peixes_mutados": {"Ruína": 1},
                "nivel_minimo": 100,
                "progresso_bestiario": 1.0,
                "dinheiro": 0,
            },
            "lore_revelada": (
                "Na pool 'O Vazio' só há dois peixes: Pesadelos Estilhaçados, que se desmaterializam, e a Punição com "
                "1% de chance. Ao capturá-la, uma mensagem ecoa — a entidade entende que apenas o player, o cozinheiro "
                "renomado que um dia sonhou com o oceano vivo, podia julgá-la. Ela concede muito XP, pode ser vendida por "
                "10k e, ao perecer, deixa um vestígio de sorte dos anciões: +10% de sorte permanente."
            ),
            "recompensa": {
                "dinheiro": 10000,
                "buff": "+10% sorte permanente",
                "xp": "Grande quantidade de XP pela captura",
                "mensagem": "Mensagem única ao capturar a Punição",
            },
            "buff_preview": {
                "nome": "Sorte dos Anciões",
                "efeito": "+10% sorte permanente após derrotar a Punição.",
                "fonte": "Conclusão da profecia",
            },
        },
    ],
    "buffs_passivos": [
        {
            "nome": "Vigília Compartilhada",
            "efeito": "+1% XP dentro da pool 'O Vazio'.",
            "fonte": "Capítulo 1",
        },
        {
            "nome": "Sorte dos Anciões",
            "efeito": "+10% sorte permanente após derrotar a Punição.",
            "fonte": "Capítulo 2",
        },
    ],
}
