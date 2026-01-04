import math


XP_BASE = 100
XP_FATOR_CRESCIMENTO = 1.15


def calcular_xp_por_nivel(nivel: int) -> int:
    return math.ceil(XP_BASE * (XP_FATOR_CRESCIMENTO ** (nivel - 1)))


dinheiro = 0
inventario = []
pratos = []
buffs_ativos = []
buffs_permanentes = []
diario_faccoes = {}
vara_atual = "Basica"
varas_possuidas = ["Basica"]
peixes_descobertos = set()

desbloqueou_cacadas = False
desbloqueou_poco_de_desejos = False
serenidade_desbloqueada = False
desbloqueou_santuario_sagrado = False
profecia_desbloqueada = False
projeto_maelstrom_desbloqueado = False
projeto_vara_punicao_desbloqueado = False
cabo_dos_sonhos_obtido = False
linha_dos_pesadelos_obtida = False
acesso_ao_vazio = False
punicao_pescada = False
questline_ancioes_desbloqueada = False
punicao_pity = 0
introducao_mostrada = False

nivel = 1  # nível do jogador
xp = 0  # experiência atual
xp_por_nivel = calcular_xp_por_nivel(nivel)  # XP necessário para subir de nível
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
progresso_faccoes = {}

mostrar_secreto = False

# Controle de pools desbloqueadas e histórias já tocadas
pools_desbloqueadas = set()
historias_pool_tocadas = set()


def ganhar_xp(quantidade: int):
    global xp, nivel, xp_por_nivel

    if quantidade <= 0:
        return

    xp += quantidade
    while xp >= xp_por_nivel:
        xp -= xp_por_nivel
        nivel += 1
        xp_por_nivel = calcular_xp_por_nivel(nivel)
