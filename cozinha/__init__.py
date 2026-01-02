import copy
import importlib
import os

import estado
from buffs import ativar_buff, efeitos_para_texto
from utils import limpar_console, mostrar_lista_paginada

# Estrutura de receitas:
# - ingredientes: dict com chaves opcionais "raridades" e "mutacoes", cada uma mapeando item -> quantidade
# - multiplicador: valor final = (soma dos valores base dos peixes usados) * multiplicador
RECEITAS = []


def _carregar_receitas():
    pasta = os.path.join(os.path.dirname(__file__), "receitas")
    if not os.path.isdir(pasta):
        return

    arquivos = [
        arquivo
        for arquivo in os.listdir(pasta)
        if arquivo.endswith(".py") and arquivo != "__init__.py"
    ]

    for arquivo in sorted(arquivos):
        mod = importlib.import_module(f"{__package__}.receitas.{arquivo[:-3]}")

        novas_receitas = []
        if hasattr(mod, "RECEITAS"):
            novas_receitas.extend(mod.RECEITAS)
        else:
            receita = getattr(mod, "RECEITA", None)
            if receita:
                novas_receitas.append(receita)

        for receita in novas_receitas:
            if receita.get("nome"):
                RECEITAS.append(receita)


_carregar_receitas()


def _descricao_buff(receita):
    buff = receita.get("buff") or {}
    duracao = buff.get("duracao_pescas")
    efeitos = buff.get("efeitos")
    partes = []
    if duracao:
        partes.append(f"Duração: {duracao} pescas")
    if efeitos:
        partes.append(efeitos_para_texto(efeitos))
    return " | ".join(partes) if partes else "Sem buff definido."


def cozinhar():
    while True:
        titulo = (
            "👩‍🍳 Cozinha\n"
            f"🍽️ Peixes disponíveis: {len(estado.inventario)}\n"
            f"💰 Dinheiro: ${estado.dinheiro:.2f}\n\n"
            "Receitas disponíveis:"
        )
        linhas = []
        for i, receita in enumerate(RECEITAS, 1):
            ingredientes = ingredientes_para_texto(receita["ingredientes"])
            linhas.append(
                f"{i}. {receita['nome']} - x{receita['multiplicador']:.2f} | {ingredientes}"
            )
            linhas.append(f"   {receita['descricao']}")
            linhas.append(f"   🎁 Buff: {_descricao_buff(receita)}")
            linhas.append("")
            linhas.append("")

        escolha, _ = mostrar_lista_paginada(linhas, titulo=titulo, itens_por_pagina=10, prompt="> ")
        if escolha == "0":
            break
        if not escolha.isdigit():
            continue

        escolha_int = int(escolha)
        if escolha_int == 0:
            break

        if 1 <= escolha_int <= len(RECEITAS):
            receita = RECEITAS[escolha_int - 1]
            if not estado.inventario:
                print("\nVocê não tem peixes para cozinhar.")
                input("Pressione ENTER para continuar.")
                continue
            tem, faltantes = avaliar_ingredientes(receita["ingredientes"])
            if not tem:
                print("\nIngredientes insuficientes para esta receita.")
                faltantes_txt = faltantes_para_texto(faltantes)
                if faltantes_txt:
                    print(f"Faltam: {faltantes_txt}.")
                input("Pressione ENTER para continuar.")
                continue
            cozinhar_receita(receita)


def normalizar_ingredientes(ingredientes):
    return {
        "raridades": ingredientes.get("raridades", {}),
        "mutacoes": ingredientes.get("mutacoes", {}),
    }


def avaliar_ingredientes(ingredientes_necessarios):
    """Verifica se há peixes suficientes sem reutilizar o mesmo item para dois requisitos."""
    ingredientes_necessarios = normalizar_ingredientes(ingredientes_necessarios)
    faltantes_raridades = ingredientes_necessarios["raridades"].copy()
    faltantes_mutacoes = ingredientes_necessarios["mutacoes"].copy()

    for peixe in estado.inventario:
        mutacao = peixe.get("mutacao")
        if mutacao and faltantes_mutacoes.get(mutacao, 0) > 0:
            faltantes_mutacoes[mutacao] -= 1
            continue

        raridade = peixe["raridade"]
        if faltantes_raridades.get(raridade, 0) > 0:
            faltantes_raridades[raridade] -= 1

    faltantes = {
        "raridades": {r: qtd for r, qtd in faltantes_raridades.items() if qtd > 0},
        "mutacoes": {m: qtd for m, qtd in faltantes_mutacoes.items() if qtd > 0},
    }

    tem_tudo = not faltantes["raridades"] and not faltantes["mutacoes"]
    return tem_tudo, faltantes


def tem_ingredientes(ingredientes_necessarios):
    tem, _ = avaliar_ingredientes(ingredientes_necessarios)
    return tem


def cozinhar_receita(receita):
    ingredientes_necessarios = normalizar_ingredientes(receita["ingredientes"])
    selecionados = selecionar_peixes_manualmente(ingredientes_necessarios)
    if not selecionados:
        return

    total_base = sum(p["valor"] for p in selecionados)
    ganho = total_base * receita["multiplicador"]

    for peixe in selecionados:
        estado.inventario.remove(peixe)

    while True:
        print(
            f"\n🍽️ Você preparou '{receita['nome']}' usando: {', '.join(p['nome'] for p in selecionados)}."
        )
        print(f"Valor culinário: ${ganho:.2f}")
        print("1. Guardar como prato (buff)")
        print("2. Consumir agora")
        print("0. Cancelar")
        escolha = input("> ")
        if escolha == "1":
            prato = gerar_prato(receita, ganho, selecionados)
            estado.pratos.append(prato)
            print("\n✅ Prato guardado na despensa.")
            input("Pressione ENTER para continuar.")
            break
        elif escolha == "2":
            prato = gerar_prato(receita, ganho, selecionados)
            buff = prato.get("buff")
            if buff:
                ativar_buff(buff, fonte=prato["nome"])
                print("\n✨ Buff aplicado!")
                print(efeitos_para_texto(buff.get("efeitos")))
            else:
                print("\nVocê saboreou o prato, mas ele não concede buffs.")
            input("Pressione ENTER para continuar.")
            break
        elif escolha == "0":
            print("\nAção cancelada. Os peixes já foram consumidos.")
            input("Pressione ENTER para continuar.")
            break


def gerar_prato(receita, valor_base, ingredientes):
    buff_def = copy.deepcopy(receita.get("buff"))
    return {
        "tipo": "prato",
        "nome": receita["nome"],
        "raridade": "Prato",
        "kg": 0.0,
        "mutacao": None,
        "valor": valor_base,
        "ingredientes": [p["nome"] for p in ingredientes],
        "buff": buff_def,
    }


def selecionar_peixes_manualmente(ingredientes_necessarios):
    selecionados_idx = set()
    requisitos_raridades = ingredientes_necessarios.get("raridades", {}).copy()
    requisitos_mutacoes = ingredientes_necessarios.get("mutacoes", {}).copy()

    def restante_texto():
        partes = []
        partes.extend(f"{qtd}x {rar}" for rar, qtd in requisitos_raridades.items() if qtd > 0)
        partes.extend(f"{qtd}x Mutação {mut}" for mut, qtd in requisitos_mutacoes.items() if qtd > 0)
        return ", ".join(partes) or "Nenhum"

    def requisitos_pendentes():
        return any(qtd > 0 for qtd in requisitos_raridades.values()) or any(
            qtd > 0 for qtd in requisitos_mutacoes.values()
        )

    while requisitos_pendentes():
        limpar_console()
        print("👩‍🍳 Selecione os peixes necessários")
        print(f"Restante: {restante_texto()}\n")
        print("Inventário:")
        for i, peixe in enumerate(estado.inventario, 1):
            marcado = "*" if i in selecionados_idx else " "
            print(f"{marcado} {i}. {peixe['nome']} - {peixe['raridade']} - ${peixe['valor']:.2f}")
        print("0. Cancelar")

        escolha = input("> ")
        if not escolha.isdigit():
            continue
        escolha = int(escolha)
        if escolha == 0:
            return []
        if not (1 <= escolha <= len(estado.inventario)):
            continue
        if escolha in selecionados_idx:
            print("Peixe já selecionado.")
            input("Pressione ENTER para continuar.")
            continue

        peixe = estado.inventario[escolha - 1]
        raridade = peixe["raridade"]
        mutacao = peixe.get("mutacao")

        if mutacao and requisitos_mutacoes.get(mutacao, 0) > 0:
            requisitos_mutacoes[mutacao] -= 1
            selecionados_idx.add(escolha)
        elif requisitos_raridades.get(raridade, 0) > 0:
            requisitos_raridades[raridade] -= 1
            selecionados_idx.add(escolha)
        else:
            print("Esse peixe não atende nenhum requisito pendente.")
            input("Pressione ENTER para continuar.")
            continue

    return [estado.inventario[i - 1] for i in sorted(selecionados_idx)]


def ingredientes_para_texto(ingredientes):
    ingredientes = normalizar_ingredientes(ingredientes)
    partes = [f"{qtd}x {raridade}" for raridade, qtd in ingredientes["raridades"].items()]
    partes.extend(f"{qtd}x Mutação {mut}" for mut, qtd in ingredientes["mutacoes"].items())
    return ", ".join(partes)


def faltantes_para_texto(faltantes):
    partes = [f"{qtd}x {raridade}" for raridade, qtd in faltantes.get("raridades", {}).items()]
    partes.extend(f"{qtd}x Mutação {mut}" for mut, qtd in faltantes.get("mutacoes", {}).items())
    return ", ".join(partes)
