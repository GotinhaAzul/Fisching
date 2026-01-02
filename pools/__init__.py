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
            pool_info = {
                "nome": nome_pool,
                "peixes": getattr(mod, "PEIXES"),
                "raridades": getattr(mod, "RARIDADES"),
                "valor_base": getattr(mod, "VALOR_MULT"),
                "nivel_min": getattr(mod, "NIVEL_MIN", 1),
            }

            missoes_min = getattr(mod, "MISSOES_MIN", None)
            if missoes_min is not None:
                pool_info["missoes_min"] = missoes_min

            xp_mult = getattr(mod, "XP_MULT", None)
            if xp_mult is not None:
                pool_info["xp_mult"] = xp_mult

            dica_bloqueio = getattr(mod, "DICA_BLOQUEIO", None)
            if dica_bloqueio:
                pool_info["dica_bloqueio"] = dica_bloqueio

            requer_flag = getattr(mod, "REQUIR_FLAG", None)
            if requer_flag:
                pool_info["requer_flag"] = requer_flag

            POOLS[nome_pool] = pool_info
