import estado
from varas import VARAS
from utils import formatar_contagem_por_raridade, limpar_console, mostrar_lista_paginada
from falas import aleatoria, FALAS_MERCADO

def mostrar_inventario():
    while True:
        limpar_console()
        print("🎒 Inventário\n")
        print(f"🎯 Vara atual: {estado.vara_atual}")
        print(f"🎣 Peixes: {len(estado.inventario)}")
        contagem = formatar_contagem_por_raridade(
            estado.peixes_pescados_por_raridade, mostrar_apex=estado.desbloqueou_cacadas
        )
        print(f"📊 Pescados por raridade: {contagem}")

        pode_trocar = len(estado.varas_possuidas) > 1

        print("\nOpções:")
        print("1. Ver peixes")
        print("2. Trocar de vara" + ("" if pode_trocar else " (necessário ter outra vara)"))
        print("0. Voltar")
        escolha = input("> ")

        if escolha == "1":
            listar_peixes()
        elif escolha == "2":
            limpar_console()
            if pode_trocar:
                trocar_vara()
            else:
                print("Você ainda não possui outra vara.")
                input("Pressione ENTER para continuar.")
        elif escolha == "0":
            break

def listar_peixes():
    if not estado.inventario:
        limpar_console()
        print("Inventário vazio.")
        input("\nPressione ENTER para voltar.")
        return

    linhas = [formatar_item(i, peixe) for i, peixe in enumerate(estado.inventario, 1)]
    mostrar_lista_paginada(linhas, titulo="🐟 Seus Peixes", itens_por_pagina=12)

def vender_peixe_individual():
    if not estado.inventario:
        print("Inventário vazio.")
        input("Pressione ENTER para voltar.")
        return

    for i, peixe in enumerate(estado.inventario):
        print(f"{i+1}. {formatar_item_sem_indice(peixe)} - ${peixe['valor']:.2f}")

    escolha = input("Digite o número do peixe para vender (0 para cancelar): ")
    if not escolha.isdigit():
        return

    escolha = int(escolha)
    if escolha == 0:
        return

    if 1 <= escolha <= len(estado.inventario):
        peixe = estado.inventario.pop(escolha - 1)
        estado.dinheiro += peixe["valor"]
        print(f"💰 Você vendeu por ${peixe['valor']:.2f}")
        input("Pressione ENTER para continuar.")

def vender_tudo():
    if not estado.inventario:
        print("Você não tem peixes para vender.")
        input("Pressione ENTER para voltar.")
        return

    total = sum(p["valor"] for p in estado.inventario)
    estado.inventario.clear()
    estado.dinheiro += total
    print(f"💰 Você vendeu tudo por ${total:.2f}")
    input("Pressione ENTER para continuar.")

def mercado_varas():
    while True:
        limpar_console()
        titulo = aleatoria(FALAS_MERCADO) + "\n\n🛒 Comprar Varas\n" + f"💰 Dinheiro: ${estado.dinheiro:.2f}\n"
        linhas = [f"{i}. {nome} - ${dados['preco']} - {dados['descricao']}" for i, (nome, dados) in enumerate(VARAS.items(), 1)]
        escolha, pagina = mostrar_lista_paginada(linhas, titulo=titulo, itens_por_pagina=10, prompt="> ")

        if escolha == "0":
            break
        if not escolha.isdigit():
            continue

        escolha_int = int(escolha)
        if escolha_int == 0:
            break

        if 1 <= escolha_int <= len(VARAS):
            nome_vara = list(VARAS.keys())[escolha_int - 1]
            preco = VARAS[nome_vara]['preco']
            if nome_vara in estado.varas_possuidas:
                estado.vara_atual = nome_vara
                print(f"Você já possuía a vara {nome_vara}. Ela foi equipada!")
            elif estado.dinheiro >= preco:
                estado.dinheiro -= preco
                estado.vara_atual = nome_vara
                estado.varas_possuidas.append(nome_vara)
                print(f"Você comprou a vara {nome_vara} e ela está equipada!")
            else:
                print("💸 Dinheiro insuficiente!")
            input("Pressione ENTER para continuar.")

def trocar_vara():
    while True:
        print("🎒 Trocar de Vara\n")
        print(f"Equipada: {estado.vara_atual}\n")
        for i, nome in enumerate(estado.varas_possuidas, 1):
            dados = VARAS[nome]
            equipada = " (Equipada)" if nome == estado.vara_atual else ""
            print(f"{i}. {nome}{equipada} - {dados['descricao']}")
        print("0. Voltar")

        escolha = input("> ")
        if not escolha.isdigit():
            continue

        escolha = int(escolha)
        if escolha == 0:
            break

        if 1 <= escolha <= len(estado.varas_possuidas):
            estado.vara_atual = estado.varas_possuidas[escolha - 1]
            print(f"Você equipou a vara {estado.vara_atual}!")
            input("Pressione ENTER para continuar.")
            break

def formatar_item(indice, item):
    return f"{indice}. {formatar_item_sem_indice(item)}"


def formatar_item_sem_indice(item):
    tipo = item.get("tipo", "peixe")
    if tipo == "prato":
        return f"{item['nome']} [Prato] - ${item['valor']:.2f}"
    mut = f" ({item['mutacao']})" if item.get("mutacao") else ""
    kg = item.get("kg", 0)
    return f"{item['nome']}{mut} - {item.get('raridade','?')} - {kg:.2f}kg"
