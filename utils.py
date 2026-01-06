import os

from dados import MUTACOES, MUTACOES_COMUNS, MUTACOES_LENDARIAS, MUTACOES_RARAS

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:
    # Ambiente sem colorama instalado (ex.: execução offline). Usa códigos ANSI básicos.
    class _AnsiFore:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"

    class _AnsiStyle:
        RESET_ALL = "\033[0m"

    Fore = _AnsiFore()
    Style = _AnsiStyle()

    def colorama_init(*args, **kwargs):
        return None
else:
    colorama_init(autoreset=False)

from varas import VARAS
import eventos


def limpar_console():
    os.system("cls" if os.name == "nt" else "clear")


def _cor_por_multiplicador(multiplicador):
    if multiplicador >= 1.65:
        return Fore.YELLOW
    if multiplicador >= 1.35:
        return Fore.BLUE
    return Fore.GREEN


def _catalogar_mutacoes():
    mutacoes = {}
    mutacoes.update(MUTACOES)

    for evento in eventos.EVENTOS:
        mutacoes.update(evento.get("mutacoes_exclusivas", {}))

    for vara in VARAS.values():
        mutacoes.update(vara.get("mutacoes_exclusivas", {}))

    return mutacoes


MUTACOES_CATALOGADAS = _catalogar_mutacoes()


def formatar_mutacao(mutacao):
    if not mutacao:
        return ""

    if mutacao in MUTACOES_COMUNS:
        cor = Fore.GREEN
    elif mutacao in MUTACOES_RARAS:
        cor = Fore.BLUE
    elif mutacao in MUTACOES_LENDARIAS:
        cor = Fore.YELLOW
    else:
        multiplicador = MUTACOES_CATALOGADAS.get(mutacao)
        if multiplicador is None:
            return mutacao
        cor = _cor_por_multiplicador(multiplicador)

    return f"{cor}{mutacao}{Style.RESET_ALL}"


def mostrar_lista_paginada(linhas, titulo=None, itens_por_pagina=12, prompt="> ", pagina_inicial=0):
    pagina = max(0, pagina_inicial)
    total_paginas = max(1, (len(linhas) + itens_por_pagina - 1) // itens_por_pagina)
    pagina = min(pagina, total_paginas - 1)

    while True:
        limpar_console()

        if titulo:
            print(titulo)
            print()

        if linhas:
            inicio = pagina * itens_por_pagina
            fim = inicio + itens_por_pagina
            for linha in linhas[inicio:fim]:
                print(linha)
        else:
            print("Nada para mostrar por enquanto.")

        if total_paginas > 1:
            print(f"\nPágina {pagina + 1}/{total_paginas} - (N) próxima, (P) anterior, (0) voltar")
        else:
            print("\n0. Voltar")

        escolha = input(prompt).strip().lower()

        if escolha == "n" and pagina < total_paginas - 1:
            pagina += 1
            continue
        if escolha == "p" and pagina > 0:
            pagina -= 1
            continue

        return escolha, pagina


def formatar_contagem_por_raridade(contagem, mostrar_apex=True, mostrar_secreto=False):
    raridades = ["Comum", "Incomum", "Raro", "Lendário"]
    if mostrar_apex:
        raridades.append("Apex")
    if mostrar_secreto:
        raridades.append("Secreto")

    partes = []
    for raridade in raridades:
        quantidade = contagem.get(raridade, 0)
        partes.append(f"{raridade}: {quantidade}")

    if not partes:
        return "Nenhum peixe pescado ainda."

    return " | ".join(partes)
