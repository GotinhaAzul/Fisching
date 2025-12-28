import random
import time

import estado
from bestiario import BESTIARIO
from dados import MUTACOES
from utils import limpar_console
from pesca import pools_desbloqueados

TEMPO_REFRESH_SEGUNDOS = 3600
TAXA_REFRESH_BASE = 750

RARIDADE_PESO_DIFICULDADE = {
    "Comum": 1.0,
    "Incomum": 1.2,
    "Raro": 1.6,
    "Lendário": 2.2,
    "Apex": 3.0,
}


def menu_missoes():
    garantir_missoes()

    while True:
        limpar_console()
        print("🗺️  Missões de Pesca\n")
        print(f"⭐ Nível: {estado.nivel}")
        print(f"✅ Missões concluídas: {estado.missoes_concluidas}")
        print(f"💰 Dinheiro: ${estado.dinheiro:.2f}\n")

        if not estado.missoes_ativas:
            print("Sem missões disponíveis. Volte mais tarde!")
        else:
            for i, missao in enumerate(estado.missoes_ativas, 1):
                status = "Pronta para entregar" if missao_concluivel(missao) else "Em progresso"
                print(f"{i}. {missao['titulo']} ({status})")
                print(f"   Requisitos: {missao['descricao']}")
                print(f"   Recompensa: ${missao['recompensa']:.2f} | Dificuldade: {missao['dificuldade']:.1f}")
                print()

        pode_refresh_gratis = pode_refresh_sem_custo()
        custo_refresh = custo_troca()
        print("Opções:")
        print("1-3. Entregar missão correspondente")
        print(f"9. Trocar missões ({'Grátis' if pode_refresh_gratis else f'${custo_refresh:.2f}'})")
        print("0. Voltar ao menu")

        escolha = input("> ")
        if escolha == "0":
            break
        if escolha == "9":
            trocar_missoes()
        elif escolha in {"1", "2", "3"}:
            indice = int(escolha) - 1
            if 0 <= indice < len(estado.missoes_ativas):
                entregar_missao(indice)
        else:
            continue


def garantir_missoes():
    if len(estado.missoes_ativas) >= 3:
        return

    gerar_missoes()


def pode_refresh_sem_custo():
    if estado.ultimo_refresh_missoes == 0:
        return True
    return time.time() - estado.ultimo_refresh_missoes >= TEMPO_REFRESH_SEGUNDOS


def custo_troca():
    return TAXA_REFRESH_BASE + estado.nivel * 150


def trocar_missoes():
    if not pode_refresh_sem_custo():
        custo = custo_troca()
        if estado.dinheiro < custo:
            print("\n💸 Dinheiro insuficiente para trocar as missões agora.")
            input("\nPressione ENTER para continuar.")
            return
        estado.dinheiro -= custo
        print(f"\nVocê pagou ${custo:.2f} para novas missões.")

    estado.missoes_ativas.clear()
    estado.ultimo_refresh_missoes = time.time()
    gerar_missoes()
    print("📜 Novas missões foram geradas!")
    input("\nPressione ENTER para continuar.")


def gerar_missoes():
    pools = pools_desbloqueados()
    if not pools:
        return

    while len(estado.missoes_ativas) < 3:
        if random.random() < 0.6:
            missao = gerar_missao_peixes(pools)
        else:
            missao = gerar_missao_mutacoes()

        if missao:
            estado.missoes_ativas.append(missao)


def gerar_missao_peixes(pools):
    quantidade = random.randint(1, 5)
    requeridos = []

    for _ in range(quantidade):
        pool = random.choice(pools)
        raridades = pool["raridades"]
        raridade = random.choices([r[0] for r in raridades], weights=[r[1] for r in raridades])[0]
        peixe = random.choice(pool["peixes"][raridade])
        requeridos.append(peixe)

    contagem = {}
    for peixe in requeridos:
        contagem[peixe] = contagem.get(peixe, 0) + 1

    requisitos_txt = [f"{qtd}x {nome}" for nome, qtd in contagem.items()]
    dificuldade = calcular_dificuldade_peixes(contagem)
    recompensa = calcular_recompensa(dificuldade)

    return {
        "tipo": "peixes",
        "titulo": "Entrega de peixes",
        "descricao": ", ".join(requisitos_txt),
        "recompensa": recompensa,
        "dificuldade": dificuldade,
        "requisitos": contagem,
    }


def gerar_missao_mutacoes():
    quantidade = random.randint(1, 3)
    mutacoes_escolhidas = random.sample(list(MUTACOES.keys()), quantidade)
    contagem = {mut: 1 for mut in mutacoes_escolhidas}

    requisitos_txt = [f"{qtd}x peixe com mutação {mut}" for mut, qtd in contagem.items()]
    dificuldade = calcular_dificuldade_mutacoes(mutacoes_escolhidas)
    recompensa = calcular_recompensa(dificuldade, bonus=1.35)

    return {
        "tipo": "mutacao",
        "titulo": "Caça de mutações",
        "descricao": ", ".join(requisitos_txt),
        "recompensa": recompensa,
        "dificuldade": dificuldade,
        "requisitos": contagem,
    }


def calcular_dificuldade_peixes(contagem):
    dificuldade_base = 1 + (estado.nivel * 0.12)
    dificuldade = dificuldade_base
    for nome, qtd in contagem.items():
        info = BESTIARIO.get(nome)
        peso = RARIDADE_PESO_DIFICULDADE.get(info["raridade"], 1.0) if info else 1.0
        dificuldade += peso * qtd * 0.9
    return round(dificuldade, 1)


def calcular_dificuldade_mutacoes(mutacoes):
    dificuldade_base = 1.5 + (estado.nivel * 0.1)
    dificuldade = dificuldade_base
    for mut in mutacoes:
        dificuldade += MUTACOES.get(mut, 1.0) * 0.7
    return round(dificuldade, 1)


def calcular_recompensa(dificuldade, bonus=1.0):
    return round((120 + estado.nivel * 15) * dificuldade * 0.4 * bonus, 2)


def missao_concluivel(missao):
    if missao["tipo"] == "peixes":
        return requisitos_presentes(missao["requisitos"], chave="nome")
    if missao["tipo"] == "mutacao":
        return requisitos_presentes(missao["requisitos"], chave="mutacao")
    return False


def requisitos_presentes(requisitos, chave):
    inventario = estado.inventario
    for req, qtd in requisitos.items():
        encontrados = sum(1 for item in inventario if item.get(chave) == req)
        if encontrados < qtd:
            return False
    return True


def entregar_missao(indice):
    missao = estado.missoes_ativas[indice]
    if not missao_concluivel(missao):
        print("\n⏳ Você ainda não possui todos os requisitos desta missão.")
        input("\nPressione ENTER para continuar.")
        return

    remover_itens_para_missao(missao)
    estado.dinheiro += missao["recompensa"]
    estado.missoes_concluidas += 1
    estado.missoes_ativas.pop(indice)
    garantir_missoes()

    print("\n🎉 Missão concluída!")
    print(f"Recompensa: ${missao['recompensa']:.2f}")
    input("\nPressione ENTER para continuar.")


def remover_itens_para_missao(missao):
    requisitos = missao["requisitos"].copy()
    chave = "nome" if missao["tipo"] == "peixes" else "mutacao"

    novo_inventario = []
    for item in estado.inventario:
        alvo = item.get(chave)
        if alvo in requisitos and requisitos[alvo] > 0:
            requisitos[alvo] -= 1
            continue
        novo_inventario.append(item)

    estado.inventario = novo_inventario
