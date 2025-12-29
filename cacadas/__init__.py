import importlib
import os
import random

import estado
from dados import MUTACOES
from pesca import RARIDADE_VALOR_MULT, RARIDADE_XP_MULT, minigame_reacao, registrar_pescado_por_raridade
from utils import limpar_console, mostrar_lista_paginada
from varas import VARAS

CACADAS = []


def _carregar_cacadas():
    pasta = os.path.dirname(__file__)
    arquivos = [
        arquivo
        for arquivo in os.listdir(pasta)
        if arquivo.endswith(".py") and arquivo != "__init__.py"
    ]

    for arquivo in sorted(arquivos):
        mod = importlib.import_module(f"{__package__}.{arquivo[:-3]}")

        novas_cacadas = []
        if hasattr(mod, "CACADAS"):
            novas_cacadas.extend(mod.CACADAS)
        else:
            cacada = getattr(mod, "CACADA", None)
            if cacada:
                novas_cacadas.append(cacada)

        for cacada in novas_cacadas:
            if cacada.get("nome"):
                CACADAS.append(cacada)


_carregar_cacadas()

CHANCE_APEX_BASE = 0.05
CHANCE_APEX_INCREMENTO = 0.05
CHANCE_APEX_TETO = 0.50


def _contar_recursos():
    peixes = {}
    mutacoes = {}
    for item in estado.inventario:
        nome = item.get("nome")
        mut = item.get("mutacao")
        if nome:
            peixes[nome] = peixes.get(nome, 0) + 1
        if mut:
            mutacoes[mut] = mutacoes.get(mut, 0) + 1
    return peixes, mutacoes


def _consumir_recursos(cacada):
    req_peixes = cacada["sacrificios"]["peixes"]
    req_mutacoes = cacada["sacrificios"]["mutacoes"]
    restantes = []
    consumo_peixes = req_peixes.copy()
    consumo_mut = req_mutacoes.copy()

    for item in estado.inventario:
        nome = item.get("nome")
        mut = item.get("mutacao")

        if nome in consumo_peixes and consumo_peixes[nome] > 0:
            consumo_peixes[nome] -= 1
            continue

        if mut and mut in consumo_mut and consumo_mut[mut] > 0:
            consumo_mut[mut] -= 1
            continue

        restantes.append(item)

    estado.inventario = restantes


def _pescar_em_cacada(cacada):
    vara = VARAS[estado.vara_atual]
    tentativas_restantes = cacada.get("tentativas", 5)
    chance_atual = CHANCE_APEX_BASE
    while tentativas_restantes > 0:
        if vara["peso_max"] < cacada["peso_min"]:
            print(
                f"\n❌ Sua vara atual suporta até {vara['peso_max']}kg, "
                f"mas o alvo APEX pesa no mínimo {cacada['peso_min']}kg."
            )
            print("Equipe uma vara mais forte para iniciar esta caçada.")
            input("\nPressione ENTER para voltar")
            break

        limpar_console()
        print(f"🎯 Caçada: {cacada['nome']}")
        print(cacada["descricao"])
        chance_percentual = int(chance_atual * 100)
        progresso = int((chance_atual / CHANCE_APEX_TETO) * 20)
        barra = "█" * progresso + "·" * (20 - progresso)
        aviso_teto = " (teto atingido)" if chance_atual >= CHANCE_APEX_TETO else ""
        print(f"Chance de fisgar um peixe APEX: {chance_percentual}% {barra}{aviso_teto}")
        print(f"Tentativas restantes: {tentativas_restantes}")
        print("\n[L] Lançar isca")
        print("[V] Voltar")
        escolha = input("> ").lower()

        if escolha != "l":
            break

        tentativas_restantes -= 1

        if random.random() > chance_atual:
            print("\n🌌 O alvo APEX não apareceu desta vez.")
            if chance_atual < CHANCE_APEX_TETO:
                chance_atual = min(CHANCE_APEX_TETO, chance_atual + CHANCE_APEX_INCREMENTO)
                print(f"🔼 Chance aumentada para {int(chance_atual * 100)}%.")
            else:
                print("⚠️ Você já está no teto de chance para esta caçada.")
            input("\nPressione ENTER para tentar novamente")
            continue

        raridade = "Apex"
        peixe = random.choice(cacada["apex_peixes"])

        mutacao = None
        mult_mut = 1.0
        mutacao_chance = 0.10 + vara["bonus_mutacao"]
        if random.random() < mutacao_chance:
            mutacao = random.choice(list(MUTACOES.keys()))
            mult_mut = MUTACOES[mutacao]

        kg = random.uniform(cacada["peso_min"], cacada["peso_max"])

        if not minigame_reacao(vara, raridade):
            print("\n💥 Você errou o combo APEX e o peixe escapou!")
            input("\nPressione ENTER para continuar")
            continue

        kg *= 1.20
        if kg > vara["peso_max"]:
            kg = vara["peso_max"]

        valor = (
            (kg * 0.1)
            * cacada["valor_base"]
            * cacada.get("valor_mult", 1)
            * mult_mut
            * RARIDADE_VALOR_MULT.get(raridade, 1)
        )

        estado.inventario.append(
            {
                "nome": peixe,
                "raridade": raridade,
                "mutacao": mutacao,
                "kg": kg,
                "valor": valor,
            }
        )
        registrar_pescado_por_raridade(raridade)
        estado.peixes_descobertos.add(peixe)

        xp_ganho = int(kg * RARIDADE_XP_MULT.get(raridade, 1) * cacada.get("xp_mult", 1))
        xp_ganho = max(1, xp_ganho)
        estado.xp += xp_ganho
        print(f"\n🎣 Você pescou: {peixe} [{raridade}] - {kg:.2f}kg")
        print(f"💰 Valor: ${valor:.2f}")
        print(f"⭐ Você ganhou {xp_ganho} XP!")

        chance_atual = CHANCE_APEX_BASE

        while estado.xp >= estado.xp_por_nivel:
            estado.xp -= estado.xp_por_nivel
            estado.nivel += 1
            estado.xp_por_nivel = estado.calcular_xp_por_nivel(estado.nivel)
            print(f"🎉 Parabéns! Você subiu para o nível {estado.nivel}!")

        input("\nPressione ENTER para continuar a caçada")

    if tentativas_restantes == 0:
        print("\n⌛ Você esgotou as tentativas desta caçada.")
        input("\nPressione ENTER para voltar")


def menu_cacadas():
    while True:
        peixes_disp, mutacoes_disp = _contar_recursos()
        titulo = (
            "🔥 Caçadas APEX\n\n"
            "Sacrifique peixes lendários específicos e mutações para acessar um alvo APEX temporariamente.\n"
            f"Recursos disponíveis (peixes): {', '.join(f'{qtd}x {nome}' for nome, qtd in peixes_disp.items()) or 'nenhum'}\n"
            f"Recursos disponíveis (mutações): {', '.join(f'{qtd}x {mut}' for mut, qtd in mutacoes_disp.items()) or 'nenhuma'}"
        )

        linhas = []
        for i, cacada in enumerate(CACADAS, start=1):
            linhas.append(
                f"{i}. {cacada['nome']} - custo: "
                f"{', '.join(f'{qtd}x {nome}' for nome, qtd in cacada['sacrificios']['peixes'].items())}; "
                f"mutações: {', '.join(f'{qtd}x {mut}' for mut, qtd in cacada['sacrificios']['mutacoes'].items()) or 'nenhuma'}"
            )
            linhas.append(f"   Alvos: {', '.join(cacada['apex_peixes'])}")
            linhas.append(f"   {cacada['descricao']}")
            linhas.append("")

        if not linhas:
            linhas.append("Nenhuma caçada disponível no momento.")

        escolha, _ = mostrar_lista_paginada(linhas, titulo=titulo, itens_por_pagina=9, prompt="> ")
        if escolha == "0":
            break
        if not escolha.isdigit():
            continue

        indice = int(escolha) - 1
        if indice < 0 or indice >= len(CACADAS):
            continue

        cacada = CACADAS[indice]
        peixes_disp, mutacoes_disp = _contar_recursos()

        def possui_recursos():
            for nome, qtd in cacada["sacrificios"]["peixes"].items():
                if peixes_disp.get(nome, 0) < qtd:
                    return False
            for mut, qtd in cacada["sacrificios"]["mutacoes"].items():
                if mutacoes_disp.get(mut, 0) < qtd:
                    return False
            return True

        if not possui_recursos():
            print("\n❌ Recursos insuficientes para iniciar esta caçada.")
            input("\nPressione ENTER para voltar")
            continue

        vara_atual = VARAS[estado.vara_atual]
        if vara_atual["peso_max"] < cacada["peso_min"]:
            print(
                f"\n❌ Sua vara atual suporta até {vara_atual['peso_max']}kg, "
                f"mas esta caçada exige no mínimo {cacada['peso_min']}kg."
            )
            print("Equipe uma vara mais forte antes de sacrificar seus recursos.")
            input("\nPressione ENTER para voltar")
            continue

        confirmar = input(
            "\nConfirmar sacrifício de "
            + ", ".join(f"{qtd}x {nome}" for nome, qtd in cacada["sacrificios"]["peixes"].items())
            + " e "
            + (
                ", ".join(f"{qtd}x {mut}" for mut, qtd in cacada["sacrificios"]["mutacoes"].items())
                or "nenhuma mutação"
            )
            + "? (s/n) "
        ).lower()
        if confirmar != "s":
            continue

        _consumir_recursos(cacada)
        _pescar_em_cacada(cacada)
