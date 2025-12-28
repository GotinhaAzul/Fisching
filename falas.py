import random

FALAS_MERCADO = [
    "Tem peixes fresquinhos hoje!",
    "Seus peixes valem ouro, sabia?",
    "Não se esqueça de conferir nossas varas especiais!",
    "Estou oferecendo um desconto especial nas varas hoje!",
    "A água do lago está ótima para pesca hoje!"
]

FALAS_POOLS = [
    "O vento sopra forte sobre o lago...",
    "Você sente que hoje os peixes estão ativos!",
    "As águas do oceano profundo brilham estranhamente..."
]

FALAS_PESCA = [
    "Pescando com atenção...",
    "Você sente um puxão na vara!",
    "O peixe parece querer fugir!"
]

def aleatoria(lista):
    return random.choice(lista)
