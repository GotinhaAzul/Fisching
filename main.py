import estado
from pesca import pescar
from inventario import mostrar_inventario, vender_peixe_individual, vender_tudo, mercado_varas
from cozinha import cozinhar
from utils import limpar_console
from bestiario import BESTIARIO
from falas import FALAS_MENU, aleatoria
from missoes import menu_missoes


def menu():
    while True:
        limpar_console()
        print("🎣 JOGO DE PESCA")
        print(f"💰 Dinheiro: ${estado.dinheiro:.2f}")
        print(f"🎯 Vara atual: {estado.vara_atual}")
        print(f"⭐ Nível: {estado.nivel} - XP: {estado.xp}/{estado.xp_por_nivel}\n")

        print(f"{aleatoria(FALAS_MENU)}\n")

        print("1. Pescar")
        print("2. Inventário")
        print("3. Mercado")
        print("4. Cozinha")
        print("5. Bestiário")
        print("6. Missões")
        if estado.desbloqueou_cacadas:
            print("7. Caçadas APEX")
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
        elif op == "6":
            menu_missoes()
        elif op == "7" and estado.desbloqueou_cacadas:
            from cacadas import menu_cacadas
            menu_cacadas()
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
            peso_min = info.get("peso_min")
            peso_max = info.get("peso_max")
            faixa_peso = ""
            if peso_min is not None and peso_max is not None:
                faixa_peso = f" - Peso: {peso_min}-{peso_max}kg"
            print(f"- {nome} [{info['raridade']}] (Pool: {info['pool']}){faixa_peso}")
        else:
            print("- ???")  # peixe ainda não descoberto
    input("\nPressione ENTER para voltar")


menu()
