import estado
from pesca import pescar
from inventario import mostrar_inventario, vender_peixe_individual, vender_tudo, mercado_varas
from cozinha import cozinhar
from utils import limpar_console
from bestiario import BESTIARIO

def menu():
    while True:
        limpar_console()
        print("🎣 JOGO DE PESCA")
        print(f"💰 Dinheiro: ${estado.dinheiro:.2f}")
        print(f"🎯 Vara atual: {estado.vara_atual}")
        print(f"⭐ Nível: {estado.nivel} - XP: {estado.xp}/{estado.xp_por_nivel}\n")

        print("1. Pescar")
        print("2. Inventário")
        print("3. Mercado")
        print("4. Cozinha")
        print("5. Bestiário")
        print("0. Sair")

        op = input("> ")

        if op == "1":
            pescar()
        elif op == "2":
            mostrar_inventario()
        elif op == "3":
            mercado()
        elif op == "4":
            cozinhar()
        elif op == "5":
            mostrar_bestiario()
        elif op == "0":
            break

def mercado():
    from falas import aleatoria, FALAS_MERCADO
    while True:
        limpar_console()
        print(aleatoria(FALAS_MERCADO) + "\n")
        print("🛒 Mercado")
        print(f"💰 Dinheiro: ${estado.dinheiro:.2f}\n")
        print("1. Vender um peixe")
        print("2. Vender tudo")
        print("3. Comprar varas")
        print("0. Voltar ao menu")

        op = input("> ")

        if op == "1":
            vender_peixe_individual()
        elif op == "2":
            vender_tudo()
        elif op == "3":
            mercado_varas()
        elif op == "0":
            break

def mostrar_bestiario():
    from utils import limpar_console
    limpar_console()
    print("📖 Bestiário\n")
    for nome, info in BESTIARIO.items():
        if nome in estado.peixes_descobertos:
            print(f"- {nome} [{info['raridade']}] (Pool: {info['pool']})")
        else:
            print("- ???")  # peixe ainda não descoberto
    input("\nPressione ENTER para voltar")

menu()
