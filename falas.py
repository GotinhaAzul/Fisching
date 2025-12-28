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

FALAS_VARA_REFORCADA = [
    "Talvez seja hora de investir em uma vara que aguente mais de {peso_min}kg.",
    "Sua vara range... procure algo que passe dos {peso_min}kg ou você só vai assistir os gigantes irem embora.",
    "Peixes desse porte exigem cabos reforçados. Uma vara acima de {peso_min}kg resolveria.",
    "Trocar para uma vara mais robusta vai evitar perder peixes de {peso_min}kg+.",
]

FALAS_INCENTIVO_VARIAR = [
    "Experimentar outro poço pode destravar peixes diferentes e bônus melhores.",
    "Talvez valha rodar um evento novo ou tentar outro poço para mudar a maré.",
    "Procure um poço alternativo ou espere um evento: os bônus podem facilitar.",
    "Outro poço ou evento pode trazer peixes que combinem melhor com sua vara.",
]

def aleatoria(lista):
    return random.choice(lista)


def aleatoria_formatada(lista, **kwargs):
    return random.choice(lista).format(**kwargs)
