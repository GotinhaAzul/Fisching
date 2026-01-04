import random

from dados import MUTACOES, RARIDADE_PESO_AJUSTE_GLOBAL

# Cada evento dá um tempero diferente às sessões de pesca:
# - bonus_raridade: multiplica o peso de determinadas raridades ao sorteá-las
# - bonus_mutacao: soma à chance base de obter mutação
# - bonus_valor: multiplica o valor final do peixe
# - bonus_peso: multiplica o peso gerado antes do limite da vara
# - xp_multiplicador: multiplica o XP ganho
EVENTOS = [
    {
        "nome": "Cardume em Migração",
        "descricao": "Peixes comuns e incomuns aparecem em grandes grupos. Fica mais fácil encher o balde, mas ainda dá para achar raros.",
        "bonus_raridade": {"Comum": 1.15, "Incomum": 1.2},
        "bonus_peso": 1.1,
    },
    {
        "nome": "Noite de Lua Cheia",
        "descricao": "A luz da lua atrai criaturas estranhas. Mais mutações e um pouco mais de raridades altas.",
        "bonus_raridade": {"Raro": 1.1, "Lendário": 1.25},
        "bonus_mutacao": 0.08,
        "bonus_valor": 1.1,
    },
    {
        "nome": "Águas Calmas",
        "descricao": "Os peixes ficam preguiçosos e engordam. Ótimo para vender por mais peso.",
        "bonus_peso": 1.25,
        "bonus_valor": 1.05,
    },
    {
        "nome": "Corrente Misteriosa",
        "descricao": "Um fluxo estranho traz energia às águas. Você aprende mais rápido com cada captura.",
        "bonus_raridade": {"Incomum": 1.05, "Raro": 1.15},
        "xp_multiplicador": 1.2,
    },
    {
        "nome": "Maré Fosforescente",
        "descricao": "Algas bioluminescentes cobrem a superfície. Criaturas que brilham no escuro se aproximam da luz.",
        "bonus_raridade": {"Raro": 1.1, "Lendário": 1.15},
        "bonus_mutacao": 0.05,
        "bonus_peso": 1.05,
        "peixes_exclusivos": {
            "Comum": [],
            "Incomum": ["Tubarão Neon Anão", "Paru-Raio", "Truta Bioluminescente"],
            "Raro": ["Enguia Fantasma Azul", "Carpa das Estrelas Submersas"],
            "Lendário": ["Leviatã Fosforescente", "Oráculo Prismático"],
        },
        "mutacoes_exclusivas": {
            "Bioluminescente": 1.45,
            "Coralizado": 1.35,
        },
    },
    {
        "nome": "Chuva de Meteoros",
        "descricao": "Fragmentos celestes atravessam o céu e alteram as marés. Peixes raros e mutações brilhantes surgem das rachaduras.",
        "bonus_raridade": {"Incomum": 1.05, "Raro": 1.1, "Lendário": 1.1},
        "bonus_mutacao": 0.07,
        "bonus_valor": 1.1,
        "peixes_exclusivos": {
            "Incomum": ["Truta Cadente", "Lambari Cadente"],
            "Raro": ["Bagre Meteoro", "Pacu Meteórico", "Salmão de Cauda Cometa"],
            "Lendário": ["Carpa Estelar"],
            "Secreto": ["Serafim Celeste"],
        },
        "mutacoes_exclusivas": {
            "Incandescente": 1.35,
            "Estilhaçado": 1.5,
        },
    },
]

EVENTO_PADRAO = {
    "nome": "Condições Normais",
    "descricao": "Nada fora do comum. É você, a vara e o silêncio do lago.",
}


def sortear_evento(prob_evento=0.35):
    """Sorteia um evento para a sessão atual de pesca."""
    # Chance reduzida para deixar a aparição de eventos mais especial.
    if random.random() < prob_evento:
        return random.choice(EVENTOS)
    return EVENTO_PADRAO


def peixes_exclusivos_para_pool(evento, pool_nome, raridade):
    """Retorna a lista de peixes exclusivos do evento para a raridade informada."""
    peixes_evento = evento.get("peixes_exclusivos", {})
    if not peixes_evento:
        return []
    return peixes_evento.get(raridade, [])


MUTACAO_PESO_PADRAO = 1.0
MUTACAO_PESO_FAVORITA = 2.0


def mutacoes_disponiveis(evento, vara=None):
    """Combina mutações padrão com mutações exclusivas do evento e da vara atual."""
    mutacoes = MUTACOES.copy()
    mutacoes.update(evento.get("mutacoes_exclusivas", {}))
    if vara:
        mutacoes.update(vara.get("mutacoes_exclusivas", {}))
    return mutacoes


def pesos_mutacoes(mutacoes, mutacoes_prioritarias=None):
    """Define pesos para sorteio de mutações, dando preferência às mutações da vara."""
    prioritarias = mutacoes_prioritarias or set()
    return [
        MUTACAO_PESO_FAVORITA if mutacao in prioritarias else MUTACAO_PESO_PADRAO
        for mutacao in mutacoes
    ]


def media_multiplicador_mutacoes(evento, vara=None):
    mutacoes = mutacoes_disponiveis(evento, vara)
    prioritarias = set(vara.get("mutacoes_exclusivas", {}).keys()) if vara else set()
    pesos = pesos_mutacoes(mutacoes, prioritarias)
    if not mutacoes:
        return 1.0
    soma_pesos = sum(pesos)
    if soma_pesos <= 0:
        return 1.0
    return sum(mult * peso for mult, peso in zip(mutacoes.values(), pesos)) / soma_pesos


def listar_peixes_exclusivos():
    """Gera dicionários com peixes exclusivos para alimentar o bestiário e dicas."""
    for evento in EVENTOS:
        for raridade, peixes in evento.get("peixes_exclusivos", {}).items():
            for peixe in peixes:
                yield {
                    "evento": evento["nome"],
                    "pool": "Qualquer local",
                    "raridade": raridade,
                    "nome": peixe,
                }


def ajustar_pesos_raridade(raridades, bonus_raridade=None, bonus_raridade_vara=0.0):
    """Retorna uma lista de (raridade, peso) com bônus de eventos e da vara aplicados."""
    bonus_raridade = bonus_raridade or {}
    raridades_beneficiadas = {"Incomum", "Raro", "Lendário", "Apex", "Secreto"}
    mult_vara = max(0.0, 1 + bonus_raridade_vara)

    ajustados = []
    for raridade, peso in raridades:
        mult = bonus_raridade.get(raridade, 1.0)
        mult *= RARIDADE_PESO_AJUSTE_GLOBAL.get(raridade, 1.0)
        if raridade in raridades_beneficiadas:
            mult *= mult_vara
        ajustados.append((raridade, max(peso * mult, 0)))
    return ajustados
