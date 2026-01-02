from pools import POOLS
from cacadas import CACADAS
from dados import RARIDADE_INTERVALO_PESO
from eventos import listar_peixes_exclusivos
import estado

BESTIARIO = {}

for pool_name, pool in POOLS.items():
    if pool.get("ignorar_bestiario"):
        continue
    for raridade, peixes in pool["peixes"].items():
        for peixe in peixes:
            if peixe not in BESTIARIO:  # evita duplicatas
                peso_min, peso_max = RARIDADE_INTERVALO_PESO.get(raridade, (None, None))
                BESTIARIO[peixe] = {
                    "nome": peixe,
                    "raridade": raridade,
                    "pool": pool_name,
                    "peso_min": peso_min,
                    "peso_max": peso_max,
                    "contavel": raridade != "Secreto",
                }

for peixe_evento in listar_peixes_exclusivos():
    if peixe_evento["nome"] not in BESTIARIO:
        peso_min, peso_max = RARIDADE_INTERVALO_PESO.get(peixe_evento["raridade"], (None, None))
        BESTIARIO[peixe_evento["nome"]] = {
            "nome": peixe_evento["nome"],
            "raridade": peixe_evento["raridade"],
            "pool": f"{peixe_evento['pool']} (Evento: {peixe_evento['evento']})",
            "peso_min": peso_min,
            "peso_max": peso_max,
            "contavel": peixe_evento["raridade"] != "Secreto",
        }

for cacada in CACADAS:
    for peixe in cacada["apex_peixes"]:
        if peixe not in BESTIARIO:
            BESTIARIO[peixe] = {
                "nome": peixe,
                "raridade": "Apex",
                "pool": f"Caçada: {cacada['nome']}",
                "peso_min": cacada.get("peso_min"),
                "peso_max": cacada.get("peso_max"),
                "contavel": True,
            }


def progresso_bestiario():
    total_contaveis = sum(1 for info in BESTIARIO.values() if info.get("contavel", True))
    descobertos = sum(
        1
        for nome in estado.peixes_descobertos
        if BESTIARIO.get(nome, {}).get("contavel", False)
    )
    return descobertos, total_contaveis


def bestiario_completo():
    descobertos, total = progresso_bestiario()
    if total == 0:
        return False
    return descobertos >= total
