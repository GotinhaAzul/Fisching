import random
import time
import estado
from pools import POOLS
from varas import VARAS
from utils import limpar_console
from falas import aleatoria, FALAS_PESCA, FALAS_POOLS
from eventos import sortear_evento, ajustar_pesos_raridade, EVENTO_PADRAO

MUTACOES = {
    "Congelado": 1.2,
    "Chamuscado": 1.15,
    "Anômalo": 1.3,
    "Celestial": 1.6
}

TECLAS = ["w", "a", "s", "d"]

def minigame_reacao(vara, raridade):
    tempo = 1.2 + vara["bonus_reacao"]
    combo = random.choices(TECLAS, k=3 if raridade == "Lendário" else 1)

    print("\n🐟 O peixe mordeu!")
    print("⚡ Digite:")
    print(" → ".join(combo).upper())

    inicio = time.time()
    entrada = input(">>> ").lower().split()
    reacao = time.time() - inicio

    return reacao <= tempo and entrada == combo

def escolher_pool():
    while True:
        limpar_console()
        print(aleatoria(FALAS_POOLS) + "\n")
        print("🌊 Escolha onde pescar:")

        opcoes_disponiveis = []
        nomes_opcoes = []

        # Monta lista de pools disponíveis e bloqueadas
        for pool_name, pool in POOLS.items():
            if estado.nivel >= pool["nivel_min"]:
                opcoes_disponiveis.append(pool)
                nomes_opcoes.append(pool_name)
            else:
                # Áreas bloqueadas aparecem como "???"
                nomes_opcoes.append(f"??? (nível {pool['nivel_min']})")

        for i, nome in enumerate(nomes_opcoes, 1):
            print(f"{i}. {nome}")
        print("0. Voltar ao menu")

        escolha = input("> ")
        if not escolha.isdigit():
            continue
        escolha = int(escolha)

        if escolha == 0:
            return None

        # Só permite selecionar pools desbloqueadas
        if 1 <= escolha <= len(opcoes_disponiveis):
            return opcoes_disponiveis[escolha - 1]

def pescar():
    pool = escolher_pool()
    if pool is None:
        return

    evento = sortear_evento()
    ultima_troca_pool = time.time()

    while True:
        limpar_console()
        exibir_contexto(pool, evento)
        print(aleatoria(FALAS_PESCA) + "\n")
        vara = VARAS[estado.vara_atual]

        raridades_ajustadas = ajustar_pesos_raridade(pool["raridades"], evento.get("bonus_raridade"))
        raridade = random.choices(
            [r[0] for r in raridades_ajustadas],
            weights=[r[1] for r in raridades_ajustadas]
        )[0]

        peixe = random.choice(pool["peixes"][raridade])

        mutacao = None
        mult_mut = 1.0
        mutacao_chance = 0.15 + vara["bonus_mutacao"] + evento.get("bonus_mutacao", 0)
        if random.random() < mutacao_chance:
            mutacao = random.choice(list(MUTACOES.keys()))
            mult_mut = MUTACOES[mutacao]

        kg = random.uniform(1, 5 if raridade != "Lendário" else 15) * evento.get("bonus_peso", 1.0)

        sucesso = minigame_reacao(vara, raridade)
        if sucesso:
            kg *= 1.15
        else:
            if mutacao:
                mutacao = None
                mult_mut = 1.0
            else:
                kg *= 0.75

        if kg > vara["peso_max"]:
            kg = vara["peso_max"]

        valor = (kg * 0.1) * pool["valor_base"] * mult_mut * evento.get("bonus_valor", 1.0) * (
            5 if raridade == "Lendário" else 2 if raridade == "Raro" else 1
        )

        estado.inventario.append({
            "nome": peixe,
            "raridade": raridade,
            "mutacao": mutacao,
            "kg": kg,
            "valor": valor
        })

        # Marca peixe como descoberto no bestiário
        estado.peixes_descobertos.add(peixe)

        # Concede XP
        xp_base = kg * (5 if raridade == "Lendário" else 2 if raridade == "Raro" else 1)
        xp_ganho = int(xp_base * evento.get("xp_multiplicador", 1.0))
        xp_ganho = max(1, xp_ganho)
        estado.xp += xp_ganho
        print(f"⭐ Você ganhou {xp_ganho} XP!")

        # Verifica subida de nível
        while estado.xp >= estado.xp_por_nivel:
            estado.nivel += 1
            estado.xp -= estado.xp_por_nivel
            print(f"🎉 Parabéns! Você subiu para o nível {estado.nivel}!")

        mut_txt = f" ({mutacao})" if mutacao else ""
        print(f"\n🎣 Você pescou: {peixe}{mut_txt} [{raridade}] - {kg:.2f}kg")
        print(f"💰 Valor: ${valor:.2f}")

        print("\n[P] Pescar novamente na mesma pool")
        print("[M] Mudar de local")
        print("[V] Voltar ao menu")
        escolha = input("> ").lower()
        if escolha == "p":
            continue
        elif escolha == "m":
            pool = escolher_pool()
            if pool is None:
                break
            agora = time.time()
            if agora - ultima_troca_pool < 10:
                evento = EVENTO_PADRAO
            else:
                evento = sortear_evento()
            ultima_troca_pool = agora
        else:
            break


def exibir_contexto(pool, evento):
    print(f"🌊 Local: {pool.get('nome', 'Desconhecido')}")
    print(f"🎯 Vara: {estado.vara_atual}")
    print(f"⚙️  Evento: {evento['nome']}")
    print(f"   {evento['descricao']}\n")
