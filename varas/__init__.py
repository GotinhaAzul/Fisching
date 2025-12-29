import importlib
import os

VARAS = {}


def _carregar_varas():
    pasta = os.path.dirname(__file__)
    arquivos = [
        arquivo
        for arquivo in os.listdir(pasta)
        if arquivo.endswith(".py") and arquivo != "__init__.py"
    ]

    for arquivo in sorted(arquivos):
        mod = importlib.import_module(f"{__package__}.{arquivo[:-3]}")
        novas_varas = {}

        if hasattr(mod, "VARAS"):
            novas_varas.update(mod.VARAS)
        else:
            nome = getattr(mod, "NOME_VARA", None)
            dados = getattr(mod, "DADOS_VARA", None)
            if nome and dados:
                novas_varas[nome] = dados

        VARAS.update(novas_varas)


_carregar_varas()

