import estado
from pesca import pescar
from inventario import mostrar_inventario, vender_peixe_individual, vender_tudo, mercado_varas
from cozinha import cozinhar
from utils import formatar_contagem_por_raridade, limpar_console, mostrar_lista_paginada
from bestiario import BESTIARIO
from dados import RARIDADE_INTERVALO_PESO
from falas import FALAS_MENU, aleatoria
from missoes import menu_missoes
from salvamento import salvar_jogo, carregar_jogo
from altar import altar_disponivel, invocar_altar


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
        print(f"⭐ Nível: {estado.nivel} - XP: {estado.xp}/{estado.xp_por_nivel}")
        contagem = formatar_contagem_por_raridade(
            estado.peixes_pescados_por_raridade,
            mostrar_apex=estado.desbloqueou_cacadas,
            mostrar_secreto=estado.mostrar_secreto,
        )
        print(f"📊 Pescados por raridade: {contagem}\n")

        print(f"{aleatoria(FALAS_MENU)}\n")

        print("1. Pescar")
        print("2. Inventário")
        print("3. Mercado")
        print("4. Cozinha")
        print("5. Bestiário")
        print("6. Missões")
        print("7. Salvar jogo")
        proximo_indice = 8
        if estado.desbloqueou_cacadas:
            print(f"{proximo_indice}. Caçadas APEX")
            indice_cacadas = str(proximo_indice)
            proximo_indice += 1
        else:
            indice_cacadas = None
        if altar_disponivel():
            print(f"{proximo_indice}. Altar")
            indice_altar = str(proximo_indice)
            proximo_indice += 1
        else:
            indice_altar = None
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
        elif indice_cacadas and op == indice_cacadas:
            from cacadas import menu_cacadas
            menu_cacadas()
        elif indice_altar and op == indice_altar:
            invocar_altar()
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
        if estado.nivel >= 5:
            print("4. Forja")
            indice_forja = "4"
        else:
            indice_forja = None
        print("0. Voltar ao menu")

        op = input("> ")

        if op == "1":
            vender_peixe_individual()
        elif op == "2":
            vender_tudo()
        elif op == "3":
            mercado_varas()
        elif indice_forja and op == indice_forja:
            from construcao_varas import menu_construcao_varas
            menu_construcao_varas()
        elif op == "0":
            break


def mostrar_bestiario():
    titulo = "📖 Bestiário"
    raridades_descobertas = set()
    for peixe in estado.peixes_descobertos:
        info = BESTIARIO.get(peixe)
        if info:
            raridades_descobertas.add(info["raridade"])

    linhas = []
    for nome, info in BESTIARIO.items():
        if nome in estado.peixes_descobertos:
            linhas.append(f"- {nome} [{info['raridade']}] (Pool: {info['pool']})")
        else:
            linhas.append("- ???")  # peixe ainda não descoberto

    linhas.append("")
    linhas.append("📏 Faixas de peso conhecidas por raridade:")
    for raridade, (peso_min, peso_max) in RARIDADE_INTERVALO_PESO.items():
        faixa_peso = f"{peso_min}-{peso_max}kg" if peso_min is not None and peso_max is not None else "???"
        if raridade in raridades_descobertas:
            linhas.append(f"- {raridade}: {faixa_peso}")
        else:
            linhas.append(f"- {raridade}: ???")

    mostrar_lista_paginada(linhas, titulo=titulo, itens_por_pagina=12)


iniciar_jogo()
menu()
