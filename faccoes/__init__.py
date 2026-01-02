import importlib
import os


FACCOES = {}


def _carregar_faccoes():
    pasta = os.path.dirname(__file__)
    for arquivo in sorted(os.listdir(pasta)):
        if not arquivo.endswith(".py") or arquivo == "__init__.py":
            continue

        mod = importlib.import_module(f"{__package__}.{arquivo[:-3]}")
        faccao = getattr(mod, "FACCAO", None)
        if not faccao:
            continue

        faccao_id = faccao.get("id")
        if not faccao_id:
            continue

        faccao.setdefault("missoes", [])
        faccao.setdefault("buffs_passivos", [])
        FACCOES[faccao_id] = faccao


_carregar_faccoes()
