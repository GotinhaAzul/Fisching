import estado
from varas import VARAS
from utils import limpar_console
from falas import aleatoria, FALAS_MERCADO

def mostrar_inventario():
    limpar_console()
    if not estado.inventario:
        print("Inventário vazio.")
    else:
        for i, peixe in enumerate(estado.inventario, 1):
            mut = f" ({peixe['mutacao']})" if peixe["mutacao"] else ""
            print(f"{i}. {peixe['nome']}{mut} - {peixe['raridade']} - {peixe['kg']:.2f}kg")
    input("\nPressione ENTER para voltar.")

def vender_peixe_individual():
    if not estado.inventario:
        print("Inventário vazio.")
        input("Pressione ENTER para voltar.")
        return

    for i, peixe in enumerate(estado.inventario):
        mut = f" {peixe['mutacao']}" if peixe["mutacao"] else ""
        print(f"{i+1}. {peixe['nome']}{mut} ({peixe['raridade']}) - ${peixe['valor']:.2f}")

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
        print(aleatoria(FALAS_MERCADO) + "\n")
        print("🛒 Comprar Varas")
        print(f"💰 Dinheiro: ${estado.dinheiro:.2f}\n")
        for i, (nome, dados) in enumerate(VARAS.items(), 1):
            print(f"{i}. {nome} - ${dados['preco']} - {dados['descricao']}")
        print("0. Voltar")

        escolha = input("> ")
        if not escolha.isdigit():
            continue

        escolha = int(escolha)
        if escolha == 0:
            break

        if 1 <= escolha <= len(VARAS):
            nome_vara = list(VARAS.keys())[escolha - 1]
            preco = VARAS[nome_vara]['preco']
            if estado.dinheiro >= preco:
                estado.dinheiro -= preco
                estado.vara_atual = nome_vara
                print(f"Você comprou a vara {nome_vara} e ela está equipada!")
            else:
                print("💸 Dinheiro insuficiente!")
            input("Pressione ENTER para continuar.")
