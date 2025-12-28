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

FALAS_MENU = [
    "O cheiro de maresia invade o ar.",
    "Uma gaivota passa gritando por cima.",
    "A brisa fria sopra das montanhas.",
    "Você escuta histórias de um peixe colossal nas profundezas.",
    "Um pescador ao lado limpa seu equipamento com calma.",
    "O som das ondas acalma sua mente.",
    "Rumores dizem que peixes mutantes surgiram recentemente.",
    "Um gato aparece por perto, de olho no seu balde vazio.",
    "O céu está limpo, perfeito para um dia de pesca.",
    "Algumas pessoas apostam em quem pega o raro primeiro."
]

def aleatoria(lista):
    return random.choice(lista)
