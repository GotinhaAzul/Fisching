import estado
from buffs import ativar_buff, efeitos_para_texto, resumo_buffs_ativos
from varas import VARAS
from utils import formatar_contagem_por_raridade, limpar_console, mostrar_lista_paginada
from falas import aleatoria, FALAS_MERCADO

def mostrar_inventario():
    while True:
        limpar_console()
        print("🎒 Inventário\n")
        print(f"🎯 Vara atual: {estado.vara_atual}")
        print(f"🎣 Peixes: {len(estado.inventario)}")
        print(f"🍲 Pratos: {len(estado.pratos)}")
        contagem = formatar_contagem_por_raridade(
            estado.peixes_pescados_por_raridade,
            mostrar_apex=estado.desbloqueou_cacadas,
            mostrar_secreto=estado.mostrar_secreto,
        )
        print(f"📊 Pescados por raridade: {contagem}")
        print("\n✨ Buffs ativos:")
        for linha in resumo_buffs_ativos():
            print(f"- {linha}")

        pode_trocar = len(estado.varas_possuidas) > 1

        print("\nOpções:")
        print("1. Ver peixes")
        print("2. Ver pratos (consumir)")
        print("3. Trocar de vara" + ("" if pode_trocar else " (necessário ter outra vara)"))
        print("0. Voltar")
        escolha = input("> ")

        if escolha == "1":
            listar_peixes()
        elif escolha == "2":
            listar_pratos()
        elif escolha == "3":
            limpar_console()
            if pode_trocar:
                trocar_vara()
            else:
                print("Você ainda não possui outra vara.")
                input("Pressione ENTER para continuar.")
        elif escolha == "0":
            break

def listar_peixes():
    if not estado.inventario:
        limpar_console()
        print("Inventário vazio.")
        input("\nPressione ENTER para voltar.")
        return

    linhas = [formatar_item(i, peixe) for i, peixe in enumerate(estado.inventario, 1)]
    mostrar_lista_paginada(linhas, titulo="🐟 Seus Peixes", itens_por_pagina=12)


def listar_pratos():
    if not estado.pratos:
        limpar_console()
        print("Nenhum prato disponível.")
        input("\nPressione ENTER para voltar.")
        return

    while True:
        limpar_console()
        print("🍲 Pratos preparados\n")
        for i, prato in enumerate(estado.pratos, 1):
            buff = prato.get("buff") or {}
            duracao = buff.get("duracao_pescas")
            duracao_txt = f"{duracao} pescas" if duracao is not None else "Duração desconhecida"
            efeitos_txt = efeitos_para_texto(buff.get("efeitos"))
            print(f"{i}. {prato['nome']} — {duracao_txt}")
            print(f"   {efeitos_txt}")
        print("0. Voltar")

        escolha = input("\nEscolha um prato para consumir: ")
        if not escolha.isdigit():
            continue
        escolha = int(escolha)
        if escolha == 0:
            break
        if 1 <= escolha <= len(estado.pratos):
            prato = estado.pratos.pop(escolha - 1)
            buff = prato.get("buff")
            if buff:
                ativar_buff(buff, fonte=prato["nome"])
                print(f"\n✨ Você consumiu {prato['nome']} e ganhou um buff!")
                print(efeitos_para_texto(buff.get("efeitos")))
            else:
                print(f"\nVocê consumiu {prato['nome']}, mas ele não concede buff.")
            input("\nPressione ENTER para continuar.")
            break

def vender_peixe_individual():
    if not estado.inventario:
        print("Inventário vazio.")
        input("Pressione ENTER para voltar.")
        return

    peixes_vendaveis = [(idx, peixe) for idx, peixe in enumerate(estado.inventario) if peixe.get("vendavel", True)]
    if not peixes_vendaveis:
        print("Nenhum peixe pode ser vendido.")
        input("Pressione ENTER para continuar.")
        return

    for i, (_, peixe) in enumerate(peixes_vendaveis):
        print(f"{i+1}. {formatar_item_sem_indice(peixe)} - ${peixe['valor']:.2f}")

    escolha = input("Digite o número do peixe para vender (0 para cancelar): ")
    if not escolha.isdigit():
        return

    escolha = int(escolha)
    if escolha == 0:
        return

    if 1 <= escolha <= len(peixes_vendaveis):
        indice_real, peixe = peixes_vendaveis[escolha - 1]
        peixe = estado.inventario.pop(indice_real)
        estado.dinheiro += peixe["valor"]
        print(f"💰 Você vendeu por ${peixe['valor']:.2f}")
        input("Pressione ENTER para continuar.")

def vender_tudo():
    peixes_vendaveis = [p for p in estado.inventario if p.get("vendavel", True)]
    if not peixes_vendaveis:
        print("Você não tem peixes vendáveis no momento.")
        input("Pressione ENTER para voltar.")
        return

    total = sum(p["valor"] for p in peixes_vendaveis)
    estado.inventario = [p for p in estado.inventario if not p.get("vendavel", True)]
    estado.dinheiro += total
    print(f"💰 Você vendeu tudo por ${total:.2f}")
    if estado.inventario:
        print("⚖️ Alguns itens especiais permaneceram no inventário.")
    input("Pressione ENTER para continuar.")

def mercado_varas():
    while True:
        limpar_console()
        titulo = aleatoria(FALAS_MERCADO) + "\n\n🛒 Comprar Varas\n" + f"💰 Dinheiro: ${estado.dinheiro:.2f}\n"

        varas_disponiveis = sorted(
            [
                (nome, dados)
                for nome, dados in VARAS.items()
                if _pode_exibir_vara(nome, dados)
            ],
            key=lambda item: item[1]["preco"],
        )

        linhas = []
        for i, (nome, dados) in enumerate(varas_disponiveis, 1):
            preco = dados["preco"]
            stats = _descrever_vara(dados)
            linhas.append(f"{i}. {nome} - ${preco} | {dados['descricao']}")
            linhas.append(f"   {stats}")

        escolha, pagina = mostrar_lista_paginada(linhas, titulo=titulo, itens_por_pagina=10, prompt="> ")

        if escolha == "0":
            break
        if not escolha.isdigit():
            continue

        escolha_int = int(escolha)
        if escolha_int == 0:
            break

        if 1 <= escolha_int <= len(varas_disponiveis):
            nome_vara = varas_disponiveis[escolha_int - 1][0]
            preco = VARAS[nome_vara]['preco']
            if nome_vara in estado.varas_possuidas:
                estado.vara_atual = nome_vara
                print(f"Você já possuía a vara {nome_vara}. Ela foi equipada!")
            elif estado.dinheiro >= preco:
                estado.dinheiro -= preco
                estado.vara_atual = nome_vara
                estado.varas_possuidas.append(nome_vara)
                print(f"Você comprou a vara {nome_vara} e ela está equipada!")
            else:
                print("💸 Dinheiro insuficiente!")
            input("Pressione ENTER para continuar.")


def _pode_exibir_vara(nome, dados):
    if dados.get("somente_construcao") and nome not in estado.varas_possuidas:
        return False
    if nome == "Serenidade" and not estado.serenidade_desbloqueada and nome not in estado.varas_possuidas:
        return False
    if dados.get("requer_pool") and dados.get("requer_pool") not in estado.pools_desbloqueadas:
        return False
    requer_buff = dados.get("requer_buff_permanente")
    if requer_buff and not any(buff.get("id") == requer_buff for buff in estado.buffs_permanentes):
        return False
    return nome in estado.varas_possuidas or estado.missoes_concluidas >= dados.get("missoes_minimas", 0)

def _descrever_vara(dados):
    bonus = []
    bonus_raridade = dados.get("bonus_raridade", 0)
    if bonus_raridade:
        bonus.append(f"{bonus_raridade*100:+.0f}% raridade")
    bonus_mutacao = dados.get("bonus_mutacao", 0)
    if bonus_mutacao:
        bonus.append(f"{bonus_mutacao*100:+.0f}% mutação")
    bonus_reacao = dados.get("bonus_reacao", 0)
    if bonus_reacao:
        bonus.append(f"{bonus_reacao*100:+.0f}% reação")
    bonus_xp = dados.get("bonus_xp", 0)
    if bonus_xp:
        bonus.append(f"{bonus_xp*100:+.0f}% XP")
    bonus_txt = " | ".join(bonus) if bonus else "Sem bônus"
    return f"Peso máx: {dados['peso_max']}kg · {bonus_txt}"

def trocar_vara():
    while True:
        print("🎒 Trocar de Vara\n")
        print(f"Equipada: {estado.vara_atual}\n")
        for i, nome in enumerate(estado.varas_possuidas, 1):
            dados = VARAS[nome]
            equipada = " (Equipada)" if nome == estado.vara_atual else ""
            print(f"{i}. {nome}{equipada} - {dados['descricao']} ({_descrever_vara(dados)})")
        print("0. Voltar")

        escolha = input("> ")
        if not escolha.isdigit():
            continue

        escolha = int(escolha)
        if escolha == 0:
            break

        if 1 <= escolha <= len(estado.varas_possuidas):
            estado.vara_atual = estado.varas_possuidas[escolha - 1]
            print(f"Você equipou a vara {estado.vara_atual}!")
            input("Pressione ENTER para continuar.")
            break

def formatar_item(indice, item):
    return f"{indice}. {formatar_item_sem_indice(item)}"


def formatar_item_sem_indice(item):
    tipo = item.get("tipo", "peixe")
    if tipo == "prato":
        return f"{item['nome']} [Prato] - ${item['valor']:.2f}"
    mut = f" ({item['mutacao']})" if item.get("mutacao") else ""
    kg = item.get("kg", 0)
    return f"{item['nome']}{mut} - {item.get('raridade','?')} - {kg:.2f}kg"
