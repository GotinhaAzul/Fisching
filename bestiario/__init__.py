from pools import POOLS
from cacadas import CACADAS
from dados import RARIDADE_INTERVALO_PESO

BESTIARIO = {}

for pool_name, pool in POOLS.items():
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
            }
