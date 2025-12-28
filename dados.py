# Mutações e valores base
MUTACOES_COMUNS = ["Congelado", "Chamuscado", "Anômalo", "Escuro", "Venenoso", "Eletrizado", "Tóxico"]
MUTACOES_RARAS = ["Estrelado", "Vazio", "Celestial", "Abissal", "Enfeitiçado"]
MUTACOES_LENDARIAS = ["Divino", "Temporal", "Eterno"]

MUTACOES = {
    # Comuns
    "Congelado": 1.2,
    "Chamuscado": 1.15,
    "Anômalo": 1.3,
    "Escuro": 1.12,
    "Venenoso": 1.18,
    "Eletrizado": 1.25,
    "Tóxico": 1.2,
    # Raras
    "Estrelado": 1.35,
    "Vazio": 1.4,
    "Celestial": 1.6,
    "Abissal": 1.5,
    "Enfeitiçado": 1.4,
    # Lendárias
    "Divino": 1.75,
    "Temporal": 1.8,
    "Eterno": 2.0,
}

CHANCE_MUTACAO = 0.30
CHANCE_MUTACAO_RARA = 0.15
CHANCE_MUTACAO_LENDARIA = 0.05

VALOR_BASE = {
    "Comum": 10,
    "Incomum": 25,
    "Raro": 50,
    "Lendário": 150
}

MULT_MUTACAO = {
    "Comum": 1.5,
    "Rara": 3,
    "Lendária": 6
}
