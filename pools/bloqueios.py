import estado
from pools import POOLS

POCO_DE_DESEJOS_NOME = "Poço de desejos"
LENDARIOS_PARA_POCO_DE_DESEJOS = 10


def requisitos_poco_de_desejos():
    pool_info = POOLS.get(POCO_DE_DESEJOS_NOME)
    if not pool_info:
        return True, []

    faltantes = []
    if estado.nivel < pool_info["nivel_min"]:
        faltantes.append(f"nível {pool_info['nivel_min']}")
    if estado.lendarios_pescados < LENDARIOS_PARA_POCO_DE_DESEJOS:
        faltantes.append(f"pescar {LENDARIOS_PARA_POCO_DE_DESEJOS} peixes Lendários")

    return len(faltantes) == 0, faltantes


def pool_desbloqueada(pool):
    if pool["nome"] == POCO_DE_DESEJOS_NOME:
        return estado.desbloqueou_poco_de_desejos

    requer_flag = pool.get("requer_flag")
    if requer_flag and not getattr(estado, requer_flag, False):
        return False

    if estado.nivel < pool.get("nivel_min", 1):
        return False

    missoes_min = pool.get("missoes_min")
    if missoes_min is not None and estado.missoes_concluidas < missoes_min:
        return False

    return True


def descricao_pool_bloqueada(pool):
    if pool["nome"] == POCO_DE_DESEJOS_NOME:
        return "??? (As lendas aguardam seu desejo.)"

    requer_flag = pool.get("requer_flag")
    if requer_flag:
        return "??? (Segredos ainda dormem sob a ilha.)"

    if pool["nome"] == "Pouso Pirata":
        dica = pool.get("dica_bloqueio")
        if dica:
            return f"??? ({dica})"
        return "???"

    requisitos = [f"nível {pool['nivel_min']}"]
    if "missoes_min" in pool:
        requisitos.append(f"{pool['missoes_min']} missões")

    dica = pool.get("dica_bloqueio")
    requisitos_txt = ", ".join(requisitos)

    if dica:
        return f"??? ({requisitos_txt}) - dica: {dica}"

    return f"??? ({requisitos_txt})"


def pools_desbloqueados():
    desbloqueados = []
    for pool_info in POOLS.values():
        if pool_desbloqueada(pool_info):
            nome = pool_info["nome"]
            if nome not in estado.pools_desbloqueadas:
                estado.pools_desbloqueadas.add(nome)
                narrativa = narrativa_pool_desbloqueada(pool_info)
                if narrativa:
                    print(narrativa)
            desbloqueados.append(pool_info)
    return desbloqueados


def narrativa_pool_desbloqueada(pool_info):
    nome = pool_info.get("nome")
    if not nome or nome in estado.historias_pool_tocadas:
        return None

    if nome == POCO_DE_DESEJOS_NOME:
        estado.historias_pool_tocadas.add(nome)
        return (
            "\n🌌  Na floresta abandonada, o Poço de Desejos ganha vida à noite:"
            " espíritos silenciosos guiam pescadores às suas águas cintilantes."
        )

    if nome == "Pouso Pirata":
        estado.historias_pool_tocadas.add(nome)
        return (
            "\n🏴‍☠️  Boatos se espalham: os anciãos expulsaram os piratas da ilha, "
            "mas os tesouros e criaturas que eles atraíram ainda rondam o Pouso Pirata."
        )
    if nome == "O Vazio":
        estado.historias_pool_tocadas.add(nome)
        return (
            "\n🌑  As páginas rasgadas sussurram sobre um lago que não reflete nada, "
            "onde o som é engolido e apenas pesadelos sobram."
        )

    return None


def tentar_desbloquear_poco_de_desejos():
    if estado.desbloqueou_poco_de_desejos:
        return None

    liberado, _ = requisitos_poco_de_desejos()
    if liberado:
        estado.desbloqueou_poco_de_desejos = True
        narrativa = (
            "\n🌌  Na floresta abandonada, espíritos guiam pescadores até as águas do Poço."
        )
        return (
            "\n🌠 Seus desejos se realizam: um Poço de Desejos agora está acessível!"
            f"{narrativa}"
        )
    return None


def ha_outros_locais_disponiveis(pool_atual_nome):
    desbloqueados = pools_desbloqueados()
    return any(pool_info["nome"] != pool_atual_nome for pool_info in desbloqueados)
