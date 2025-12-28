from pools import POOLS
from cacadas import CACADAS

BESTIARIO = {}

for pool_name, pool in POOLS.items():
    for raridade, peixes in pool["peixes"].items():
        for peixe in peixes:
            if peixe not in BESTIARIO:  # evita duplicatas
                BESTIARIO[peixe] = {
                    "nome": peixe,
                    "raridade": raridade,
                    "pool": pool_name
                }

for cacada in CACADAS:
    for peixe in cacada["apex_peixes"]:
        if peixe not in BESTIARIO:
            BESTIARIO[peixe] = {
                "nome": peixe,
                "raridade": "Apex",
                "pool": f"Caçada: {cacada['nome']}"
            }
