dinheiro = 0
inventario = []
vara_atual = "Basica"
varas_possuidas = ["Basica"]
peixes_descobertos = set()

desbloqueou_cacadas = False
desbloqueou_poco_de_desejos = False

nivel = 1        # nível do jogador
xp = 0           # experiência atual
xp_por_nivel = 100  # XP necessário para subir de nível
lendarios_pescados = 0  # total de peixes lendários já pescados

# Registro de troféus lendários capturados (melhor peso por peixe)
trofeus = {}

# Sistema de missões
missoes_ativas = []
ultimo_refresh_missoes = 0
missoes_concluidas = 0
