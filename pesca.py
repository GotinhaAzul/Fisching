import random
import time
import estado
from pools import POOLS
from varas import VARAS
from utils import limpar_console
from falas import (
    aleatoria,
    aleatoria_formatada,
    FALAS_INCENTIVO_VARIAR,
    FALAS_PESCA,
    FALAS_POOLS,
    FALAS_VARA_REFORCADA,
)
from eventos import sortear_evento, ajustar_pesos_raridade, EVENTO_PADRAO
from dados import MUTACOES, RARIDADE_INTERVALO_PESO

TECLAS = ["w", "a", "s", "d"]
RARIDADE_VALOR_MULT = {
    "Comum": 1,
    "Incomum": 1,
    "Raro": 2,
    "Lendário": 8,
    "Apex": 12,
}
RARIDADE_XP_MULT = {
    "Comum": 1,
    "Incomum": 1,
    "Raro": 2,
    "Lendário": 8,
    "Apex": 12,
}
MEDIA_MULT_MUTACAO = sum(MUTACOES.values()) / len(MUTACOES)

MENSAGENS_TROFEU_LENDARIO = [
    "🏆 Troféu lendário! Você ergue {peixe} ({kg:.2f}kg) e sente a energia do local vibrar.",
    "🌟 Uma lenda nas suas mãos: {peixe} de {kg:.2f}kg! O acampamento inteiro vai comentar.",
    "✨ Você exibe {peixe} ({kg:.2f}kg) como um troféu brilhante. Até os espíritos do rio prestam atenção.",
]

def minigame_reacao(vara, raridade):
    if raridade == "Apex":
        tempo = 1.0 + vara["bonus_reacao"]
        combo = random.choices(TECLAS, k=5)
    elif raridade == "Lendário":
        tempo = 1.2 + vara["bonus_reacao"]
        combo = random.choices(TECLAS, k=3)
    else:
        tempo = 1.2 + vara["bonus_reacao"]
        combo = random.choices(TECLAS, k=1)

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


def registrar_trofeu(peixe, kg, pool_nome):
    """
    Registra o melhor troféu lendário por peixe.
    Retorna True se for um novo recorde ou primeira captura lendária do peixe.
    """
    trofeu_atual = estado.trofeus.get(peixe)
    novo_recorde = trofeu_atual is None or kg > trofeu_atual["kg"]
    if novo_recorde:
        estado.trofeus[peixe] = {
            "nome": peixe,
            "kg": kg,
            "pool": pool_nome,
            "raridade": "Lendário",
        }
    return novo_recorde


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

        peso_min, peso_max = RARIDADE_INTERVALO_PESO.get(raridade, (1, 5))
        if vara["peso_max"] < peso_min:
            print(
                f"\n❌ Sua vara suporta até {vara['peso_max']}kg, mas este peixe pesa no mínimo {peso_min}kg."
            )
            print(aleatoria_formatada(FALAS_VARA_REFORCADA, peso_min=peso_min, peso_max=vara["peso_max"]))
            dica = gerar_dica_alternativas(pool, evento, raridades_bloqueadas=[raridade])
            if dica:
                print(dica)
            input("\nPressione ENTER para continuar")
            continue

        peso_base = random.uniform(peso_min, peso_max)
        kg = peso_base * evento.get("bonus_peso", 1.0)

        sucesso = minigame_reacao(vara, raridade)
        if sucesso:
            kg *= 1.15
        else:
            if raridade == "Apex":
                print("\n💥 Você errou o combo APEX e o peixe escapou!")
                input("\nPressione ENTER para continuar")
                continue
            if mutacao:
                mutacao = None
                mult_mut = 1.0
            else:
                kg *= 0.75

        if kg > vara["peso_max"]:
            kg = vara["peso_max"]

        valor = (kg * 0.1) * pool["valor_base"] * mult_mut * evento.get("bonus_valor", 1.0) * RARIDADE_VALOR_MULT.get(raridade, 1)

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
        xp_base = kg * RARIDADE_XP_MULT.get(raridade, 1)
        xp_ganho = int(xp_base * evento.get("xp_multiplicador", 1.0))
        xp_ganho = max(1, xp_ganho)
        estado.xp += xp_ganho
        print(f"⭐ Você ganhou {xp_ganho} XP!")

        # Verifica subida de nível
        while estado.xp >= estado.xp_por_nivel:
            estado.nivel += 1
            estado.xp -= estado.xp_por_nivel
            print(f"🎉 Parabéns! Você subiu para o nível {estado.nivel}!")

        trofeu_msg = None
        if raridade == "Lendário":
            novo_recorde = registrar_trofeu(peixe, kg, pool.get("nome", "Desconhecido"))
            trofeu_msg = aleatoria_formatada(MENSAGENS_TROFEU_LENDARIO, peixe=peixe, kg=kg)
            if novo_recorde:
                trofeu_msg += " 🏅 Novo recorde!"
            else:
                trofeu_msg += " 🏅 Troféu registrado anteriormente."

        mut_txt = f" ({mutacao})" if mutacao else ""
        print(f"\n🎣 Você pescou: {peixe}{mut_txt} [{raridade}] - {kg:.2f}kg")
        print(f"💰 Valor: ${valor:.2f}")
        if trofeu_msg:
            print(trofeu_msg)

        if raridade == "Lendário" and not estado.desbloqueou_cacadas:
            estado.desbloqueou_cacadas = True
            print("\n🗝️  Você desbloqueou as Caçadas APEX no menu!")

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
    print(f"   {evento['descricao']}")

    vara = VARAS[estado.vara_atual]
    valor_esperado, xp_esperado, raridades_bloqueadas = calcular_expectativas(pool, evento, vara)

    if valor_esperado or xp_esperado:
        print(f"📈 Expectativa: ~{xp_esperado:.1f} XP | ${valor_esperado:.2f} por lançamento")
    if raridades_bloqueadas:
        bloqueadas = ", ".join(raridades_bloqueadas)
        print(f"⚠️  Raridades pesadas demais para esta vara: {bloqueadas}")
    dica = gerar_dica_alternativas(pool, evento, raridades_bloqueadas)
    if dica:
        print(dica)
    print()


def ha_outros_locais_disponiveis(pool_atual_nome):
    desbloqueados = [
        pool_info for pool_info in POOLS.values() if estado.nivel >= pool_info["nivel_min"]
    ]
    return any(pool_info["nome"] != pool_atual_nome for pool_info in desbloqueados)


def gerar_dica_alternativas(pool, evento, raridades_bloqueadas=None):
    raridades_bloqueadas = raridades_bloqueadas or []
    evento_padrao = evento is EVENTO_PADRAO
    pode_trocar_local = ha_outros_locais_disponiveis(pool.get("nome", ""))
    if not (evento_padrao or pode_trocar_local or raridades_bloqueadas):
        return None
    return aleatoria_formatada(
        FALAS_INCENTIVO_VARIAR,
        pool=pool.get("nome", "outro poço"),
        evento=evento.get("nome", "um evento"),
    )


def calcular_expectativas(pool, evento, vara):
    raridades_ajustadas = ajustar_pesos_raridade(pool["raridades"], evento.get("bonus_raridade"))
    pesos_totais = sum(max(item[1], 0) for item in raridades_ajustadas)
    raridades_bloqueadas = []

    if pesos_totais <= 0:
        return 0.0, 0.0, raridades_bloqueadas

    bonus_peso = evento.get("bonus_peso", 1.0)
    bonus_valor = evento.get("bonus_valor", 1.0)
    xp_mult = evento.get("xp_multiplicador", 1.0)
    chance_mutacao = max(
        0.0, min(1.0, 0.15 + vara["bonus_mutacao"] + evento.get("bonus_mutacao", 0))
    )
    mult_mutacao_esperado = 1 + chance_mutacao * (MEDIA_MULT_MUTACAO - 1)

    valor_esperado = 0.0
    xp_esperado = 0.0

    for raridade, peso in raridades_ajustadas:
        if peso <= 0:
            continue
        intervalo = RARIDADE_INTERVALO_PESO.get(raridade)
        if not intervalo:
            continue
        peso_min, peso_max = intervalo
        if vara["peso_max"] < peso_min:
            raridades_bloqueadas.append(raridade)
            continue

        peso_medio = ((peso_min + peso_max) / 2) * bonus_peso
        peso_medio = min(peso_medio, vara["peso_max"])
        prob = peso / pesos_totais

        valor = (
            (peso_medio * 0.1)
            * pool["valor_base"]
            * mult_mutacao_esperado
            * bonus_valor
            * RARIDADE_VALOR_MULT.get(raridade, 1)
        )
        xp = peso_medio * RARIDADE_XP_MULT.get(raridade, 1) * xp_mult

        valor_esperado += prob * valor
        xp_esperado += prob * xp

    return valor_esperado, xp_esperado, raridades_bloqueadas
