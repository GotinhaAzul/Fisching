import random

from dados import RARIDADE_PESO_AJUSTE_GLOBAL

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
