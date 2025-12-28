import os
import importlib

POOLS = {}

pasta = os.path.dirname(__file__)
for arquivo in os.listdir(pasta):
    if arquivo.endswith(".py") and arquivo != "__init__.py":
        mod_name = f"{__package__}.{arquivo[:-3]}"
        mod = importlib.import_module(mod_name)
        nome_pool = getattr(mod, "NOME_POOL", None)
        if nome_pool:
            POOLS[nome_pool] = {
                "peixes": getattr(mod, "PEIXES"),
                "raridades": getattr(mod, "RARIDADES"),
                "valor_base": getattr(mod, "VALOR_MULT"),
                "nivel_min": getattr(mod, "NIVEL_MIN", 1)  # <- aqui
            }
