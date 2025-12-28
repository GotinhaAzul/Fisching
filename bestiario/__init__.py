from pools import POOLS

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
