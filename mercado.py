import estado
from estado import inventario

def vender_peixe_individual():
    if not inventario:
        print("Inventário vazio.")
        return

    for i, peixe in enumerate(inventario):
        if peixe["mutacao"]:
            print(f"{i+1}. {peixe['nome']} {peixe['mutacao']} ({peixe['raridade']}) - ${peixe['valor']}")
        else:
            print(f"{i+1}. {peixe['nome']} ({peixe['raridade']}) - ${peixe['valor']}")

    escolha = input("Digite o número do peixe para vender (0 para cancelar): ")

    if not escolha.isdigit():
        return

    escolha = int(escolha)
    if escolha == 0:
        return

    if 1 <= escolha <= len(inventario):
        peixe = inventario.pop(escolha - 1)
        estado.dinheiro += peixe["valor"]
        print(f"💰 Você vendeu por ${peixe['valor']}.")

def vender_tudo():
    if not inventario:
        print("Você não tem peixes para vender.")
        return

    total = sum(p["valor"] for p in inventario)
    inventario.clear()
    estado.dinheiro += total
    print(f"💰 Você vendeu tudo por ${total}.")
