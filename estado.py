dinheiro = 0
inventario = []
vara_atual = "Basica"
varas_possuidas = ["Basica"]
peixes_descobertos = set()

desbloqueou_cacadas = False
desbloqueou_poco_de_desejos = False
serenidade_desbloqueada = False

nivel = 1        # nível do jogador
xp = 0           # experiência atual
xp_por_nivel = 100  # XP necessário para subir de nível
lendarios_pescados = 0  # total de peixes lendários já pescados

# Contagem de peixes pescados por raridade
peixes_pescados_por_raridade = {
    "Comum": 0,
    "Incomum": 0,
    "Raro": 0,
    "Lendário": 0,
    "Apex": 0,
    "Secreto": 0,
}

# Registro de troféus lendários capturados (melhor peso por peixe)
trofeus = {}

# Sistema de missões
missoes_ativas = []
ultimo_refresh_missoes = 0
missoes_concluidas = 0

mostrar_secreto = False

# Controle de pools desbloqueadas e histórias já tocadas
pools_desbloqueadas = set()
historias_pool_tocadas = set()
