import estado
from pesca import pescar
from inventario import mostrar_inventario, vender_peixe_individual, vender_tudo, mercado_varas
from cozinha import cozinhar
from utils import limpar_console
from bestiario import BESTIARIO
from dados import RARIDADE_INTERVALO_PESO
from falas import FALAS_MENU, aleatoria
from missoes import menu_missoes
from salvamento import salvar_jogo, carregar_jogo


def iniciar_jogo():
    # Tenta carregar save automaticamente para reduzir fricção
    carregado = carregar_jogo(quiet=True)
    if carregado:
        print("💾 Save carregado automaticamente.")
        input("Pressione ENTER para continuar")


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
        print("7. Salvar jogo")
        if estado.desbloqueou_cacadas:
            print("8. Caçadas APEX")
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
        elif op == "7":
            salvar_jogo()
            input("💾 Jogo salvo! Pressione ENTER para continuar")
        elif op == "8" and estado.desbloqueou_cacadas:
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
    raridades_descobertas = set()
    for peixe in estado.peixes_descobertos:
        info = BESTIARIO.get(peixe)
        if info:
            raridades_descobertas.add(info["raridade"])

    for nome, info in BESTIARIO.items():
        if nome in estado.peixes_descobertos:
            print(f"- {nome} [{info['raridade']}] (Pool: {info['pool']})")
        else:
            print("- ???")  # peixe ainda não descoberto

    print("\n📏 Faixas de peso conhecidas por raridade:")
    for raridade, (peso_min, peso_max) in RARIDADE_INTERVALO_PESO.items():
        faixa_peso = f"{peso_min}-{peso_max}kg" if peso_min is not None and peso_max is not None else "???"
        if raridade in raridades_descobertas:
            print(f"- {raridade}: {faixa_peso}")
        else:
            print(f"- {raridade}: ???")
    input("\nPressione ENTER para voltar")


iniciar_jogo()
menu()
