import importlib
import os

import estado
from dados import MUTACOES_RARAS
from falas import FALAS_CONSTRUCAO, aleatoria
from utils import limpar_console, mostrar_lista_paginada
from varas import VARAS

PROJETOS = []


def _carregar_projetos():
    pasta = os.path.join(os.path.dirname(__file__), "projetos")
    if not os.path.isdir(pasta):
        return

    arquivos = [
        arquivo
        for arquivo in os.listdir(pasta)
        if arquivo.endswith(".py") and arquivo != "__init__.py"
    ]

    for arquivo in sorted(arquivos):
        mod = importlib.import_module(f"{__package__}.projetos.{arquivo[:-3]}")

        novos = []
        if hasattr(mod, "PROJETOS"):
            novos.extend(mod.PROJETOS)
        else:
            projeto = getattr(mod, "PROJETO", None)
            if projeto:
                novos.append(projeto)

        for projeto in novos:
            if projeto.get("nome") and projeto.get("vara"):
                PROJETOS.append(projeto)


_carregar_projetos()


def _flag_liberada(projeto):
    flag = projeto.get("flag_requerida")
    if not flag:
        return True
    return getattr(estado, flag, False) or projeto["vara"] in estado.varas_possuidas


def _peixes_raros_com_mutacao_rara():
    candidatos = []
    for idx, peixe in enumerate(estado.inventario):
        if peixe.get("raridade") == "Raro" and peixe.get("mutacao") in MUTACOES_RARAS:
            candidatos.append((idx, peixe))
    return candidatos


def _sacrificar_peixe_para_abrir():
    candidatos = _peixes_raros_com_mutacao_rara()
    if not candidatos:
        print("\n❌ Você precisa de ao menos 1 peixe Raro com mutação rara para ativar a bancada.")
        input("Pressione ENTER para voltar.")
        return False

    while True:
        limpar_console()
        print("🪓 A bancada consome um peixe Raro com mutação rara para despertar.")
        print("Escolha qual peixe irá sacrificar:\n")
        for i, (_, peixe) in enumerate(candidatos, start=1):
            mut = peixe.get("mutacao")
            print(f"{i}. {peixe['nome']} [{peixe['raridade']}] ({mut}) - {peixe.get('kg', 0):.2f}kg")
        print("0. Voltar")
        escolha = input("> ")

        if not escolha.isdigit():
            continue
        escolha_int = int(escolha)
        if escolha_int == 0:
            return False
        if 1 <= escolha_int <= len(candidatos):
            idx_original, peixe = candidatos[escolha_int - 1]
            estado.inventario.pop(idx_original)
            print(f"\n🔥 {peixe['nome']} com mutação {peixe['mutacao']} foi sacrificado para ativar a bancada.")
            input("Pressione ENTER para continuar.")
            return True


def _normalizar_requisitos(requisitos):
    return {
        "nivel_minimo": requisitos.get("nivel_minimo", 1),
        "missoes_minimas": requisitos.get("missoes_minimas", 0),
        "pescados_raridade": requisitos.get("pescados_raridade", {}),
        "sacrificios": _normalizar_sacrificios(requisitos.get("sacrificios", {})),
        "dinheiro": requisitos.get("dinheiro", 0),
        "itens": requisitos.get("itens", {}),
        "flags": requisitos.get("flags", []),
    }


def _normalizar_sacrificios(sacrificios):
    return {
        "raridades": sacrificios.get("raridades", {}),
        "mutacoes": sacrificios.get("mutacoes", {}),
    }


def _avaliar_sacrificios(sacrificios):
    sacrificios = _normalizar_sacrificios(sacrificios)
    faltantes_raridades = sacrificios["raridades"].copy()
    faltantes_mutacoes = sacrificios["mutacoes"].copy()
    indices_consumo = []

    for idx, peixe in enumerate(estado.inventario):
        mut = peixe.get("mutacao")
        raridade = peixe.get("raridade")

        if mut and faltantes_mutacoes.get(mut, 0) > 0:
            faltantes_mutacoes[mut] -= 1
            indices_consumo.append(idx)
            continue

        if raridade and faltantes_raridades.get(raridade, 0) > 0:
            faltantes_raridades[raridade] -= 1
            indices_consumo.append(idx)

    faltantes = {
        "raridades": {r: qtd for r, qtd in faltantes_raridades.items() if qtd > 0},
        "mutacoes": {m: qtd for m, qtd in faltantes_mutacoes.items() if qtd > 0},
    }
    tem_tudo = not faltantes["raridades"] and not faltantes["mutacoes"]
    return tem_tudo, faltantes, indices_consumo


def _avaliar_itens_requeridos(itens_requeridos, ignorar_indices=None):
    ignorar_indices = set(ignorar_indices or [])
    faltantes = itens_requeridos.copy()
    indices_consumo = []

    for idx, item in enumerate(estado.inventario):
        if idx in ignorar_indices:
            continue
        nome = item.get("nome")
        if nome in faltantes and faltantes[nome] > 0:
            faltantes[nome] -= 1
            indices_consumo.append(idx)

    faltantes_limpos = {nome: qtd for nome, qtd in faltantes.items() if qtd > 0}
    tem_tudo = not faltantes_limpos
    return tem_tudo, faltantes_limpos, indices_consumo


def _avaliar_projeto(projeto):
    req = _normalizar_requisitos(projeto["requisitos"])
    faltantes = {
        "nivel": max(0, req["nivel_minimo"] - estado.nivel),
        "missoes": max(0, req["missoes_minimas"] - estado.missoes_concluidas),
        "pescados": {},
        "sacrificios": {},
        "dinheiro": 0,
        "itens": {},
        "flags": [],
    }

    for raridade, qtd in req["pescados_raridade"].items():
        atual = estado.peixes_pescados_por_raridade.get(raridade, 0)
        if atual < qtd:
            faltantes["pescados"][raridade] = qtd - atual

    tem_sacrificios, faltantes_sac, _ = _avaliar_sacrificios(req["sacrificios"])
    if not tem_sacrificios:
        faltantes["sacrificios"] = faltantes_sac

    tem_itens, faltantes_itens, _ = _avaliar_itens_requeridos(req["itens"])
    if not tem_itens:
        faltantes["itens"] = faltantes_itens

    for flag in req["flags"]:
        if not getattr(estado, flag, False):
            faltantes["flags"].append(flag)

    if estado.dinheiro < req["dinheiro"]:
        faltantes["dinheiro"] = round(req["dinheiro"] - estado.dinheiro, 2)

    pronto = (
        faltantes["nivel"] == 0
        and faltantes["missoes"] == 0
        and not faltantes["pescados"]
        and not faltantes["sacrificios"]
        and not faltantes["itens"]
        and not faltantes["flags"]
        and faltantes["dinheiro"] == 0
    )
    return pronto, faltantes, req


def _consumir_indices(indices):
    for idx in sorted(indices, reverse=True):
        estado.inventario.pop(idx)


def _formatar_requisitos(req):
    partes = []
    partes.append(f"Nível {req['nivel_minimo']}")
    partes.append(f"Missões {req['missoes_minimas']}")
    if req["pescados_raridade"]:
        pescados = ", ".join(f"{qtd}x {rar}" for rar, qtd in req["pescados_raridade"].items())
        partes.append(f"Pescados: {pescados}")
    if req["sacrificios"]["raridades"] or req["sacrificios"]["mutacoes"]:
        sac_partes = []
        if req["sacrificios"]["raridades"]:
            sac_partes.append(", ".join(f"{qtd}x {rar}" for rar, qtd in req["sacrificios"]["raridades"].items()))
        if req["sacrificios"]["mutacoes"]:
            sac_partes.append(", ".join(f"{qtd}x mutação {mut}" for mut, qtd in req["sacrificios"]["mutacoes"].items()))
        partes.append(f"Sacrifícios: {', '.join(sac_partes)}")
    if req["itens"]:
        partes.append("Itens: " + ", ".join(f"{qtd}x {nome}" for nome, qtd in req["itens"].items()))
    if req["flags"]:
        partes.append("Ativos: " + ", ".join(req["flags"]))
    if req["dinheiro"] > 0:
        partes.append(f"Custo: ${req['dinheiro']:.2f}")
    return " | ".join(partes)


def _formatar_faltantes(faltantes):
    partes = []
    if faltantes["nivel"] > 0:
        partes.append(f"- Falta subir {faltantes['nivel']} nível(is).")
    if faltantes["missoes"] > 0:
        partes.append(f"- Complete {faltantes['missoes']} missão(ões) a mais.")
    if faltantes["pescados"]:
        pescados = ", ".join(f"{qtd}x {rar}" for rar, qtd in faltantes["pescados"].items())
        partes.append(f"- Pesque mais: {pescados}.")
    if faltantes.get("sacrificios"):
        sac = faltantes["sacrificios"]
        if sac.get("raridades"):
            partes.append(
                "- Sacrifícios por raridade: "
                + ", ".join(f"{qtd}x {rar}" for rar, qtd in sac["raridades"].items())
            )
        if sac.get("mutacoes"):
            partes.append(
                "- Sacrifícios por mutação: "
                + ", ".join(f"{qtd}x {mut}" for mut, qtd in sac["mutacoes"].items())
            )
    if faltantes.get("itens"):
        partes.append(
            "- Itens faltantes: "
            + ", ".join(f"{qtd}x {nome}" for nome, qtd in faltantes["itens"].items())
        )
    if faltantes.get("flags"):
        partes.append("- Ative: " + ", ".join(faltantes["flags"]))
    if faltantes["dinheiro"] > 0:
        partes.append(f"- Dinheiro faltante: ${faltantes['dinheiro']:.2f}.")
    return "\n".join(partes) if partes else "Tudo pronto!"


def _construir_projeto(projeto):
    if not _flag_liberada(projeto):
        print("\n❌ Projeto indisponível. Desbloqueie o blueprint correspondente para prosseguir.")
        input("Pressione ENTER para continuar.")
        return

    pronto, faltantes, req = _avaliar_projeto(projeto)
    if projeto["vara"] not in VARAS:
        print("\n❌ Vara não encontrada no catálogo. Verifique a definição em 'varas'.")
        input("Pressione ENTER para voltar.")
        return

    if projeto["vara"] in estado.varas_possuidas:
        print("\n✅ Você já possui essa vara. Equipe-a no inventário.")
        input("Pressione ENTER para continuar.")
        return

    if not pronto:
        print("\nAinda há pendências para construir esta vara:\n")
        print(_formatar_faltantes(faltantes))
        input("\nPressione ENTER para continuar.")
        return

    tem_sacrificios, _, indices_consumo = _avaliar_sacrificios(req["sacrificios"])
    tem_itens, _, indices_itens = _avaliar_itens_requeridos(req["itens"], ignorar_indices=indices_consumo)
    if not tem_sacrificios or not tem_itens:
        print("\nAlguns recursos sumiram antes da construção:\n")
        pronto_atual, faltantes_atual, _ = _avaliar_projeto(projeto)
        print(_formatar_faltantes(faltantes_atual))
        input("\nPressione ENTER para continuar.")
        return

    _consumir_indices(indices_consumo + [i for i in indices_itens if i not in indices_consumo])
    estado.dinheiro -= req["dinheiro"]

    estado.varas_possuidas.append(projeto["vara"])
    estado.vara_atual = projeto["vara"]
    print(f"\n🛠️ Você construiu a vara {projeto['vara']}! Ela foi equipada automaticamente.")
    input("Pressione ENTER para continuar.")


def menu_construcao_varas():
    if estado.nivel < 5:
        print("\nA forja é desbloqueada no nível 5.")
        input("Pressione ENTER para continuar.")
        return

    if not _sacrificar_peixe_para_abrir():
        return

    while True:
        titulo = (
            f"{aleatoria(FALAS_CONSTRUCAO)}\n\n"
            "⚒️ Forja de Varas\n"
            f"💰 Dinheiro: ${estado.dinheiro:.2f}\n"
            f"⭐ Nível: {estado.nivel} | Missões concluídas: {estado.missoes_concluidas}\n"
        )

        linhas = []
        opcoes_projetos = []
        for projeto in PROJETOS:
            if not _flag_liberada(projeto):
                continue

            i = len(opcoes_projetos) + 1
            pronto, _, req = _avaliar_projeto(projeto)
            bloqueado_por_nivel = estado.nivel < req["nivel_minimo"]
            status = "Pronto" if pronto else "Pendências"
            if projeto["vara"] in estado.varas_possuidas:
                status = "Já construída"
            if bloqueado_por_nivel:
                linhas.append(f"{i}. ??? (Desbloqueia no nível {req['nivel_minimo']})")
                linhas.append("   Resultado: ???")
                linhas.append("   ???")
            else:
                linhas.append(f"{i}. {projeto['nome']} ({status})")
                linhas.append(f"   Resultado: {projeto['vara']} - {projeto['descricao']}")
                linhas.append(f"   { _formatar_requisitos(req) }")
            linhas.append("")
            opcoes_projetos.append((projeto, bloqueado_por_nivel, req["nivel_minimo"]))

        escolha, _ = mostrar_lista_paginada(linhas, titulo=titulo, itens_por_pagina=10, prompt="> ")
        if escolha == "0":
            break
        if not escolha.isdigit():
            continue

        escolha_int = int(escolha)
        if 1 <= escolha_int <= len(opcoes_projetos):
            projeto, bloqueado_por_nivel, nivel_minimo = opcoes_projetos[escolha_int - 1]
            if bloqueado_por_nivel:
                print(f"\n❌ ??? - atinja o nível {nivel_minimo} para revelar este projeto.")
                input("Pressione ENTER para continuar.")
                continue
            _construir_projeto(projeto)
