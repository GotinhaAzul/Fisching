import random

FALAS_MERCADO = [
    "Tem peixes fresquinhos hoje!",
    "Seus peixes valem ouro, sabia?",
    "Não se esqueça de conferir nossas varas especiais!",
    "Estou oferecendo um desconto especial nas varas hoje!",
    "A água do lago está ótima para pesca hoje!",
    "As melhores iscas chegam cedo, aproveite!",
    "Ouvi dizer que um pescador ficou rico vendendo um Apex ontem...",
]

FALAS_POOLS = [
    "O vento sopra forte sobre o lago...",
    "Você sente que hoje os peixes estão ativos!",
    "As águas do oceano profundo brilham estranhamente...",
    "Ondas leves revelam sombras gigantes logo abaixo...",
    "Bolinhas na superfície denunciam cardumes famintos.",
]


FALAS_PESCA = [
    "Pescando com atenção...",
    "Você sente um puxão na vara!",
    "O peixe parece querer fugir!",
    "O anzol vibra, algo grande está mordendo...",
    "A linha canta, sinal de briga boa!",
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
    "Algumas pessoas apostam em quem pega o raro primeiro.",
    "Não conhece o peixe? Pesque um pouco mais!",
    "O rádio toca histórias sobre um peixe que brilha no escuro.",
    "O velhinho do cais diz ter visto um Apex ontem à noite.",
    "A maré trouxe conchas estranhas para a praia hoje.",
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

FALAS_APEX_CAPTURA = [
    "🔥 A vara arqueia com força! Seu {peixe} APEX de {kg:.2f}kg impõe respeito.",
    "🌊 A água explode quando você ergue o APEX {peixe}! {kg:.2f}kg de pura lenda.",
    "⚡ Você mal acredita: {peixe} APEX fisgado! {kg:.2f}kg de adrenalina pura.",
    "🏔️ Os ecos do cais celebram seu {peixe} APEX de {kg:.2f}kg. Que captura!",
]

FALAS_SECRETO_CAPTURA = [
    "🌙 O silêncio toma conta... um {peixe} Secreto de {kg:.2f}kg surge das profundezas.",
    "🕯️ Luzes estranhas piscam ao erguer o {peixe} Secreto ({kg:.2f}kg). Algo despertou.",
    "🔮 A linha vibra diferente: {peixe} Secreto fisgado! {kg:.2f}kg de mistério.",
    "👁️ Você sente que alguém observa enquanto levanta o {peixe} Secreto de {kg:.2f}kg.",
]

MENSAGENS_TROFEU_LENDARIO = [
    "🏆 Troféu lendário! Você ergue {peixe} ({kg:.2f}kg) e sente a energia do local vibrar.",
    "🌟 Uma lenda nas suas mãos: {peixe} de {kg:.2f}kg! O acampamento inteiro vai comentar.",
    "✨ Você exibe {peixe} ({kg:.2f}kg) como um troféu brilhante. Até os espíritos do rio prestam atenção.",
]

def aleatoria(lista):
    return random.choice(lista)


def aleatoria_formatada(lista, **kwargs):
    return random.choice(lista).format(**kwargs)
