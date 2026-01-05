import estado

from utils import formatar_mutacao


def vender_peixe_individual():
    inventario = estado.inventario
    if not inventario:
        print("Inventário vazio.")
        return

    for i, peixe in enumerate(inventario):
        mutacao = formatar_mutacao(peixe.get("mutacao"))
        mutacao_txt = f" {mutacao}" if mutacao else ""
        print(
            f"{i+1}. {peixe.get('nome', '?')}{mutacao_txt} ({peixe.get('raridade', '?')}) - ${peixe.get('valor', 0):.2f}"
        )

    escolha = input("Digite o número do peixe para vender (0 para cancelar): ")

    if not escolha.isdigit():
        return

    escolha = int(escolha)
    if escolha == 0:
        return

    if 1 <= escolha <= len(estado.inventario):
        peixe = estado.inventario.pop(escolha - 1)
        ganho = float(peixe.get("valor", 0))
        estado.dinheiro += ganho
        print(f"💰 Você vendeu por ${ganho:.2f}.")


def vender_tudo():
    if not estado.inventario:
        print("Você não tem peixes para vender.")
        return

    total = sum(float(p.get("valor", 0)) for p in estado.inventario)
    estado.inventario.clear()
    estado.dinheiro += total
    print(f"💰 Você vendeu tudo por ${total:.2f}.")
