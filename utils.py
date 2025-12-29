import os


def limpar_console():
    os.system("cls" if os.name == "nt" else "clear")


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
            print(f"\nPágina {pagina + 1}/{total_paginas} - (n) próxima, (p) anterior, (0) voltar")
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


def formatar_contagem_por_raridade(contagem, mostrar_apex=True):
    raridades = ["Comum", "Incomum", "Raro", "Lendário"]
    if mostrar_apex:
        raridades.append("Apex")

    partes = []
    for raridade in raridades:
        quantidade = contagem.get(raridade, 0)
        partes.append(f"{raridade}: {quantidade}")

    if not partes:
        return "Nenhum peixe pescado ainda."

    return " | ".join(partes)
