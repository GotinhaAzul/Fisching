import random
import time
import estado
from pools import POOLS
from pools.bloqueios import (
    descricao_pool_bloqueada,
    ha_outros_locais_disponiveis,
    pool_desbloqueada,
    pools_desbloqueados,
    tentar_desbloquear_poco_de_desejos,
)
from varas import VARAS
from utils import limpar_console
from falas import (
    aleatoria,
    aleatoria_formatada,
    FALAS_APEX_CAPTURA,
    FALAS_INCENTIVO_VARIAR,
    FALAS_PESCA,
    FALAS_POOLS,
    FALAS_SECRETO_CAPTURA,
    FALAS_VARA_REFORCADA,
    MENSAGENS_TROFEU_LENDARIO,
)
from eventos import sortear_evento, ajustar_pesos_raridade, EVENTO_PADRAO
from dados import MUTACOES, RARIDADE_INTERVALO_PESO, CHANCE_PEIXE_SECRETO, PEIXES_SECRETOS

TECLAS = ["w", "a", "s", "d"]
RARIDADE_VALOR_MULT = {
    "Comum": 1,
    "Incomum": 1,
    "Raro": 2,
    "Lendário": 8,
    "Apex": 12,
    "Secreto": 20,
}
RARIDADE_XP_MULT = {
    "Comum": 1,
    "Incomum": 1,
    "Raro": 2,
    "Lendário": 8,
    "Apex": 12,
    "Secreto": 15,
}
MEDIA_MULT_MUTACAO = sum(MUTACOES.values()) / len(MUTACOES)

def registrar_pescado_por_raridade(raridade):
    atual = estado.peixes_pescados_por_raridade.get(raridade, 0)
    estado.peixes_pescados_por_raridade[raridade] = atual + 1

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
    entrada_raw = input(">>> ").lower().strip()
    reacao = time.time() - inicio

    # Permite digitar com ou sem espaços entre as letras (ex.: "wasd" ou "w a s d")
    entrada_processada = (
        list(entrada_raw) if " " not in entrada_raw else entrada_raw.split()
    )

    return reacao <= tempo and entrada_processada == combo

def escolher_pool():
    while True:
        limpar_console()
        print(aleatoria(FALAS_POOLS) + "\n")
        print("🌊 Escolha onde pescar:")

        opcoes_menu = []

        # Monta lista de pools disponíveis e bloqueadas
        for pool in POOLS.values():
            if pool_desbloqueada(pool):
                opcoes_menu.append({"pool": pool, "nome": pool["nome"]})
            else:
                opcoes_menu.append({"pool": None, "nome": descricao_pool_bloqueada(pool)})

        for i, opcao in enumerate(opcoes_menu, 1):
            print(f"{i}. {opcao['nome']}")
        print("0. Voltar ao menu")

        escolha = input("> ")
        if not escolha.isdigit():
            continue
        escolha = int(escolha)

        if escolha == 0:
            return None

        # Só permite selecionar pools desbloqueadas
        if 1 <= escolha <= len(opcoes_menu):
            selecionada = opcoes_menu[escolha - 1]
            if selecionada["pool"] is not None:
                return selecionada["pool"]


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

        pescou_secreto = random.random() < CHANCE_PEIXE_SECRETO
        if pescou_secreto:
            raridade = "Secreto"
            peixe = random.choice(PEIXES_SECRETOS)
        else:
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

        # Maestria por nível: bônus cumulativo de peso (0.2% por nível, sem limite)
        bonus_mestria = estado.nivel * 0.002
        kg *= (1 + bonus_mestria)

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
        registrar_pescado_por_raridade(raridade)
        if raridade == "Secreto" and not estado.mostrar_secreto:
            estado.mostrar_secreto = True

        # Marca peixe como descoberto no bestiário
        if raridade != "Secreto":
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
            estado.lendarios_pescados += 1
            novo_recorde = registrar_trofeu(peixe, kg, pool.get("nome", "Desconhecido"))
            trofeu_msg = aleatoria_formatada(MENSAGENS_TROFEU_LENDARIO, peixe=peixe, kg=kg)
            if novo_recorde:
                trofeu_msg += " 🏅 Novo recorde!"
            else:
                trofeu_msg += " 🏅 Troféu registrado anteriormente."

        captura_especial = None
        if raridade == "Apex":
            captura_especial = aleatoria_formatada(FALAS_APEX_CAPTURA, peixe=peixe, kg=kg)
        elif raridade == "Secreto":
            captura_especial = aleatoria_formatada(FALAS_SECRETO_CAPTURA, peixe=peixe, kg=kg)

        mensagem_poco = tentar_desbloquear_poco_de_desejos()

        mut_txt = f" ({mutacao})" if mutacao else ""
        print(f"\n🎣 Você pescou: {peixe}{mut_txt} [{raridade}] - {kg:.2f}kg")
        print(f"💰 Valor: ${valor:.2f}")
        if trofeu_msg:
            print(trofeu_msg)
        if captura_especial:
            print(captura_especial)

        if raridade == "Lendário" and not estado.desbloqueou_cacadas:
            estado.desbloqueou_cacadas = True
            print("\n🗝️  Você desbloqueou as Caçadas APEX no menu!")
        if mensagem_poco:
            print(mensagem_poco)

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
    desbloqueados = pools_desbloqueados()
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
        if peso <= 0 or pesos_totais <= 0:
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

    chance_secreto = CHANCE_PEIXE_SECRETO
    valor_esperado *= (1 - chance_secreto)
    xp_esperado *= (1 - chance_secreto)

    intervalo_secreto = RARIDADE_INTERVALO_PESO.get("Secreto")
    if intervalo_secreto and vara["peso_max"] >= intervalo_secreto[0]:
        peso_medio = ((intervalo_secreto[0] + intervalo_secreto[1]) / 2) * bonus_peso
        peso_medio = min(peso_medio, vara["peso_max"])
        valor_secreto = (
            (peso_medio * 0.1)
            * pool["valor_base"]
            * mult_mutacao_esperado
            * bonus_valor
            * RARIDADE_VALOR_MULT["Secreto"]
        )
        xp_secreto = peso_medio * RARIDADE_XP_MULT["Secreto"] * xp_mult
        valor_esperado += chance_secreto * valor_secreto
        xp_esperado += chance_secreto * xp_secreto

    return valor_esperado, xp_esperado, raridades_bloqueadas
