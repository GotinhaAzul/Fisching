import os
import random
import sys
import threading
import time
import estado
from buffs import consumir_uso, obter_bonus_ativos, resumo_buffs_ativos
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
from eventos import (
    EVENTO_PADRAO,
    ajustar_pesos_raridade,
    media_multiplicador_mutacoes,
    mutacoes_disponiveis,
    peixes_exclusivos_para_pool,
    pesos_mutacoes,
    sortear_evento,
)
from dados import RARIDADE_INTERVALO_PESO, CHANCE_PEIXE_SECRETO, PEIXES_SECRETOS

TECLAS = ["w", "a", "s", "d"]
POOL_VAZIO_NOME = "O Vazio"
PESADELOS_NOME = "Pesadelos estilhaçados"
PUNICAO_NOME = "Punição"
PUNICAO_CHANCE_BASE = 0.01
PUNICAO_PITY_INCREMENTO = 0.005
PUNICAO_PITY_GARANTIA = 120
PEIXES_DESMATERIALIZAM = {PESADELOS_NOME}
PEIXES_SEM_RARIDADE_VISUAL = {PUNICAO_NOME}
PEIXES_IGNORAR_BESTIARIO = {PESADELOS_NOME, PUNICAO_NOME}
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
# Capturas rápidas servem para impedir spam quase instantâneo.
# Limites mais brandos evitam punição para um ritmo normal de pesca.
CAPTURAS_RAPIDAS_LIMITE = 5
INTERVALO_CAPTURA_RAPIDA = 1.5
TEMPO_RECUPERACAO_LINHA = 5
BARRA_TEMPO_TAMANHO = 20


def _ler_tecla_disponivel():
    """Retorna uma tecla pressionada sem exigir ENTER, caso haja."""
    try:
        if os.name == "nt":
            import msvcrt  # type: ignore

            if msvcrt.kbhit():
                return msvcrt.getwch()
        else:
            import select

            pronto, _, _ = select.select([sys.stdin], [], [], 0)
            if pronto:
                return sys.stdin.read(1)
    except Exception:
        return None
    return None


def _ler_combo_sem_enter(tempo_limite: float, quantidade: int):
    """
    Captura `quantidade` de teclas sem exigir ENTER, exibindo barra de tempo.
    Retorna (teclas, tempo_decorrido, expirou) ou (None, tempo_decorrido, expirou).
    """
    teclas = []
    inicio = time.time()
    completou = False
    expirou = False

    fd = None
    configuracao_antiga = None
    if os.name != "nt" and sys.stdin.isatty():
        import termios
        import tty

        fd = sys.stdin.fileno()
        configuracao_antiga = termios.tcgetattr(fd)
        tty.setcbreak(fd)

    try:
        while True:
            decorrido = time.time() - inicio
            if decorrido >= tempo_limite:
                expirou = True
                sys.stdout.write("\r⏳ Tempo esgotou!                \n")
                sys.stdout.flush()
                break

            progresso = min(1.0, decorrido / tempo_limite)
            preenchido = int(BARRA_TEMPO_TAMANHO * progresso)
            barra = "█" * preenchido + "░" * (BARRA_TEMPO_TAMANHO - preenchido)
            restante = max(0.0, tempo_limite - decorrido)
            sys.stdout.write(f"\r⏳ Tempo: [{barra}] {restante:.1f}s")
            sys.stdout.flush()

            tecla = _ler_tecla_disponivel()
            if tecla:
                tecla = tecla.lower()
                if tecla in ("\n", "\r"):
                    continue
                teclas.append(tecla)
                if len(teclas) == quantidade:
                    completou = True
                    break

            time.sleep(0.02)
    finally:
        if configuracao_antiga is not None and fd is not None:
            import termios

            termios.tcsetattr(fd, termios.TCSADRAIN, configuracao_antiga)

    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()

    if completou:
        return teclas, time.time() - inicio, expirou
    return None, time.time() - inicio, expirou

def _ler_input_com_barra(tempo_limite: float):
    """
    Lê o input do usuário mostrando uma barra de tempo que preenche até o limite.
    Retorna a string digitada ou None caso o tempo estoure antes de receber entrada.
    """
    inicio = time.time()
    caracteres = []

    while True:
        decorrido = time.time() - inicio
        if decorrido >= tempo_limite:
            sys.stdout.write("\r⏳ Tempo esgotou!                \n")
            sys.stdout.flush()
            return None

        progresso = min(1.0, decorrido / tempo_limite)
        preenchido = int(BARRA_TEMPO_TAMANHO * progresso)
        barra = "█" * preenchido + "░" * (BARRA_TEMPO_TAMANHO - preenchido)
        restante = max(0.0, tempo_limite - decorrido)
        sys.stdout.write(f"\r⏳ Tempo: [{barra}] {restante:.1f}s")
        sys.stdout.flush()

        if os.name == "nt":
            import msvcrt  # type: ignore

            while msvcrt.kbhit():
                tecla = msvcrt.getwch()
                if tecla in ("\r", "\n"):
                    sys.stdout.write("\r" + " " * 40 + "\r")
                    sys.stdout.flush()
                    return "".join(caracteres).lower().strip()
                caracteres.append(tecla)
        else:
            import select

            pronto, _, _ = select.select([sys.stdin], [], [], 0.05)
            if pronto:
                tecla = sys.stdin.read(1)
                if tecla in ("\n", "\r"):
                    sys.stdout.write("\r" + " " * 40 + "\r")
                    sys.stdout.flush()
                    return "".join(caracteres).lower().strip()
                if tecla == "":
                    return "".join(caracteres).lower().strip()
                caracteres.append(tecla)

        time.sleep(0.02)

def registrar_pescado_por_raridade(raridade):
    atual = estado.peixes_pescados_por_raridade.get(raridade, 0)
    estado.peixes_pescados_por_raridade[raridade] = atual + 1

def minigame_reacao(vara, raridade):
    buffs = obter_bonus_ativos()
    bonus_reacao = vara["bonus_reacao"] + buffs.get("bonus_reacao", 0.0)
    if raridade == "Apex":
        tempo = 1.0 + bonus_reacao
        combo = random.choices(TECLAS, k=5)
    elif raridade == "Raro":
        tempo = 1.2 + bonus_reacao
        combo = random.choices(TECLAS, k=2)
    elif raridade == "Lendário":
        tempo = 1.2 + bonus_reacao
        combo = random.choices(TECLAS, k=3)
    else:
        tempo = 1.2 + bonus_reacao
        combo = random.choices(TECLAS, k=1)

    print("\n🐟 O peixe mordeu!")
    print("⚡ Digite:")
    print(" → ".join(combo).upper())
    print(f"⏳ Você tem {tempo:.1f}s para reagir!")

    entrada_combo, reacao, expirou = _ler_combo_sem_enter(tempo, len(combo))
    entrada_raw = None

    # Fallback para ambientes sem suporte a leitura sem ENTER
    if entrada_combo is None and not expirou:
        inicio = time.time()
        entrada_raw = _ler_input_com_barra(tempo)
        reacao = time.time() - inicio
    elif expirou:
        return False

    if entrada_combo is None and entrada_raw is None:
        return False

    if entrada_combo is None:
        # Permite digitar com ou sem espaços entre as letras (ex.: "wasd" ou "w a s d")
        entrada_processada = (
            list(entrada_raw) if " " not in entrada_raw else entrada_raw.split()
        )
    else:
        entrada_processada = entrada_combo

    return reacao <= tempo and entrada_processada == combo


def minigame_punicao(vara):
    buffs = obter_bonus_ativos()
    bonus_reacao = vara["bonus_reacao"] + buffs.get("bonus_reacao", 0.0)
    tempo = 2.8 + bonus_reacao
    combo = random.choices(TECLAS, k=10)

    print("\n🐚 O vazio responde.")
    print("⚡ Digite a sequência profana:")
    print(" → ".join(combo).upper())
    print(f"⏳ Você tem {tempo:.1f}s para não ser engolido.")

    entrada_combo, reacao, expirou = _ler_combo_sem_enter(tempo, len(combo))
    entrada_raw = None
    if entrada_combo is None and not expirou:
        inicio = time.time()
        entrada_raw = _ler_input_com_barra(tempo)
        reacao = time.time() - inicio
    elif expirou:
        return False

    if entrada_combo is None and entrada_raw is None:
        return False

    if entrada_combo is None:
        entrada_processada = list(entrada_raw) if " " not in entrada_raw else entrada_raw.split()
    else:
        entrada_processada = entrada_combo

    return reacao <= tempo and entrada_processada == combo


def _chance_punicao_atual():
    if estado.punicao_pity >= PUNICAO_PITY_GARANTIA:
        return 1.0
    chance = PUNICAO_CHANCE_BASE + (estado.punicao_pity * PUNICAO_PITY_INCREMENTO)
    return min(chance, 1.0)


def _sortear_peixe_vazio():
    chance = _chance_punicao_atual()
    if random.random() < chance:
        return PUNICAO_NOME, "Apex", True
    return PESADELOS_NOME, "Comum", False


def _registrar_resultado_vazio(capturou_punicao):
    if capturou_punicao:
        estado.punicao_pity = 0
        estado.punicao_pescada = True
    else:
        estado.punicao_pity += 1


def escolher_pool():
    while True:
        limpar_console()
        print(aleatoria(FALAS_POOLS) + "\n")
        print("🌊 Escolha onde pescar:")

        opcoes_menu = []

        pools_ordenadas = sorted(POOLS.values(), key=lambda pool: pool["nome"])
        pools_desbloqueadas = []
        pools_bloqueadas = []

        # Monta lista de pools disponíveis e bloqueadas, mantendo as desbloqueadas no topo
        for pool in pools_ordenadas:
            if pool["nome"] == POOL_VAZIO_NOME and estado.punicao_pescada:
                continue
            if pool_desbloqueada(pool):
                pools_desbloqueadas.append(pool)
            else:
                pools_bloqueadas.append(pool)

        for pool in pools_desbloqueadas:
            opcoes_menu.append({"pool": pool, "nome": pool["nome"]})
        for pool in pools_bloqueadas:
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
    ultima_captura = None
    capturas_rapidas_consecutivas = 0
    linha_quebrada_ate = 0

    while True:
        buffs_ativos = obter_bonus_ativos()
        agora = time.time()
        if agora < linha_quebrada_ate:
            pausa = linha_quebrada_ate - agora
            limpar_console()
            print("\n🪝 Sua linha quebrou de tanto esforço!")
            print(f"⏳ Espere {pausa:.1f}s para voltar a pescar.")
            time.sleep(pausa)
            ultima_captura = None
            capturas_rapidas_consecutivas = 0
            continue

        limpar_console()
        exibir_contexto(pool, evento, buffs_ativos)
        print(aleatoria(FALAS_PESCA) + "\n")
        vara = VARAS[estado.vara_atual]

        vazio_pool = pool["nome"] == POOL_VAZIO_NOME
        punicao_sorteada = False
        pescou_secreto = False

        if vazio_pool:
            peixe, raridade, punicao_sorteada = _sortear_peixe_vazio()
        else:
            pescou_secreto = random.random() < CHANCE_PEIXE_SECRETO
            if pescou_secreto:
                raridade = "Secreto"
                peixe = random.choice(PEIXES_SECRETOS)
            else:
                bonus_raridade_evento = evento.get("bonus_raridade", {}).copy()
                for raridade_buff, mult in (buffs_ativos.get("bonus_raridade") or {}).items():
                    bonus_raridade_evento[raridade_buff] = bonus_raridade_evento.get(raridade_buff, 1.0) * mult
                raridades_ajustadas = ajustar_pesos_raridade(
                    pool["raridades"],
                    bonus_raridade_evento,
                    vara.get("bonus_raridade", 0.0) + buffs_ativos.get("bonus_raridade_vara", 0.0),
                )
                raridade = random.choices(
                    [r[0] for r in raridades_ajustadas],
                    weights=[r[1] for r in raridades_ajustadas]
                )[0]

                peixes_disponiveis = pool["peixes"][raridade] + peixes_exclusivos_para_pool(
                    evento, pool["nome"], raridade
                )
                peixe = random.choice(peixes_disponiveis)

        mutacao = None
        mult_mut = 1.0
        mutacao_chance = 0.0
        mutacoes_evento = mutacoes_disponiveis(evento, vara)
        if not vazio_pool:
            mutacao_chance = (
                0.15
                + vara["bonus_mutacao"]
                + evento.get("bonus_mutacao", 0)
                + buffs_ativos.get("bonus_mutacao", 0.0)
            )
        if mutacao_chance and random.random() < mutacao_chance:
            prioritarias = set(vara.get("mutacoes_exclusivas", {}).keys())
            chaves_mutacoes = list(mutacoes_evento.keys())
            pesos = pesos_mutacoes(chaves_mutacoes, prioritarias)
            mutacao = random.choices(chaves_mutacoes, weights=pesos)[0]
            mult_mut = mutacoes_evento[mutacao]

        peso_min, peso_max = RARIDADE_INTERVALO_PESO.get(raridade, (1, 5))
        if vara["peso_max"] < peso_min:
            print(
                f"\n❌ Sua vara suporta até {vara['peso_max']}kg, mas este peixe pesa no mínimo {peso_min}kg."
            )
            print(aleatoria_formatada(FALAS_VARA_REFORCADA, peso_min=peso_min, peso_max=vara["peso_max"]))
            dica = gerar_dica_alternativas(pool, evento, raridades_bloqueadas=[raridade])
            if dica:
                print(dica)
            if vazio_pool:
                _registrar_resultado_vazio(False)
            input("\nPressione ENTER para continuar")
            continue

        peso_base = random.uniform(peso_min, peso_max)
        kg = peso_base * evento.get("bonus_peso", 1.0) * buffs_ativos.get("bonus_peso", 1.0)

        if peixe == PUNICAO_NOME:
            sucesso = minigame_punicao(vara)
        else:
            sucesso = minigame_reacao(vara, raridade)
        if sucesso:
            kg *= 1.15
        else:
            if peixe == PUNICAO_NOME:
                print("\n💥 A entidade escapou do anzol e mergulhou no vazio.")
                if vazio_pool:
                    _registrar_resultado_vazio(False)
                input("\nPressione ENTER para continuar")
                continue
            if raridade == "Apex":
                print("\n💥 Você errou o combo APEX e o peixe escapou!")
                input("\nPressione ENTER para continuar")
                if vazio_pool:
                    _registrar_resultado_vazio(False)
                continue
            print("\n💨 Você errou o movimento e o peixe escapou!")
            input("\nPressione ENTER para continuar")
            if vazio_pool:
                _registrar_resultado_vazio(False)
            continue

        # Maestria por nível: bônus cumulativo de peso (0.2% por nível, sem limite)
        bonus_mestria = estado.nivel * 0.002
        kg *= (1 + bonus_mestria)

        if kg > vara["peso_max"]:
            kg = vara["peso_max"]

        valor = (
            (kg * 0.1)
            * pool["valor_base"]
            * mult_mut
            * evento.get("bonus_valor", 1.0)
            * buffs_ativos.get("bonus_valor", 1.0)
            * RARIDADE_VALOR_MULT.get(raridade, 1)
        )
        if peixe in PEIXES_DESMATERIALIZAM or peixe == PUNICAO_NOME:
            valor = 0

        item_capturado = {
            "nome": peixe,
            "raridade": raridade,
            "mutacao": mutacao,
            "kg": kg,
            "valor": valor,
            "vendavel": peixe != PUNICAO_NOME,
            "pool": pool.get("nome"),
        }

        if peixe not in PEIXES_DESMATERIALIZAM:
            estado.inventario.append(item_capturado)
        registrar_pescado_por_raridade(raridade)
        if raridade == "Secreto" and not estado.mostrar_secreto:
            estado.mostrar_secreto = True

        # Marca peixe como descoberto no bestiário
        if raridade != "Secreto" and peixe not in PEIXES_IGNORAR_BESTIARIO:
            estado.peixes_descobertos.add(peixe)

        # Concede XP
        xp_base = kg * RARIDADE_XP_MULT.get(raridade, 1)
        pool_xp_mult = pool.get("xp_mult", 1.0)
        bonus_xp_vara = 1 + vara.get("bonus_xp", 0.0)
        xp_ganho = int(
            xp_base
            * evento.get("xp_multiplicador", 1.0)
            * buffs_ativos.get("xp_multiplicador", 1.0)
            * bonus_xp_vara
        )
        xp_ganho = int(xp_ganho * pool_xp_mult)
        xp_ganho = max(1, xp_ganho)
        estado.xp += xp_ganho
        print(f"⭐ Você ganhou {xp_ganho} XP!")

        # Verifica subida de nível
        while estado.xp >= estado.xp_por_nivel:
            estado.xp -= estado.xp_por_nivel
            estado.nivel += 1
            estado.xp_por_nivel = estado.calcular_xp_por_nivel(estado.nivel)
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
        if raridade == "Apex" and peixe != PUNICAO_NOME:
            captura_especial = aleatoria_formatada(FALAS_APEX_CAPTURA, peixe=peixe, kg=kg)
        elif raridade == "Secreto":
            captura_especial = aleatoria_formatada(FALAS_SECRETO_CAPTURA, peixe=peixe, kg=kg)

        mensagem_poco = tentar_desbloquear_poco_de_desejos()

        mut_txt = f" ({mutacao})" if mutacao else ""
        raridade_txt = "" if peixe in PEIXES_SEM_RARIDADE_VISUAL else f" [{raridade}]"
        print(f"\n🎣 Você pescou: {peixe}{mut_txt}{raridade_txt} - {kg:.2f}kg")
        print(f"💰 Valor: ${valor:.2f}")
        if peixe in PEIXES_DESMATERIALIZAM:
            print("🌫️ O peixe se desmaterializa em suas mãos. Nada foi adicionado ao inventário.")
        elif peixe == PUNICAO_NOME:
            print("⚖️ A Punição não pode ser vendida, mas permanece em seu inventário.")
        if trofeu_msg:
            print(trofeu_msg)
        if captura_especial:
            print(captura_especial)

        if raridade == "Lendário" and not estado.desbloqueou_cacadas:
            estado.desbloqueou_cacadas = True
            print("\n🗝️  Você desbloqueou as Caçadas APEX no menu!")
        if mensagem_poco:
            print(mensagem_poco)
        if vazio_pool:
            _registrar_resultado_vazio(peixe == PUNICAO_NOME and sucesso)
        expirados = consumir_uso()
        for buff_expirado in expirados:
            print(f"⏳ O efeito de {buff_expirado.get('nome', 'um buff')} acabou.")

        fim_captura = time.time()
        if ultima_captura is not None and (fim_captura - ultima_captura) < INTERVALO_CAPTURA_RAPIDA:
            capturas_rapidas_consecutivas += 1
        else:
            capturas_rapidas_consecutivas = 0
        ultima_captura = fim_captura

        if capturas_rapidas_consecutivas >= CAPTURAS_RAPIDAS_LIMITE:
            linha_quebrada_ate = fim_captura + TEMPO_RECUPERACAO_LINHA
            capturas_rapidas_consecutivas = 0
            ultima_captura = None
            print("\n🪝 Você puxou rápido demais e a linha quebrou!")
            print(f"🧵 Faça uma pausa de {TEMPO_RECUPERACAO_LINHA:.0f}s para reforçar o equipamento.")
            time.sleep(1.5)

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


def exibir_contexto(pool, evento, buffs=None):
    buffs = buffs or {}
    print(f"🌊 Local: {pool.get('nome', 'Desconhecido')}")
    print(f"🎯 Vara: {estado.vara_atual}")
    print(f"⚙️  Evento: {evento['nome']}")
    print(f"   {evento['descricao']}")

    vara = VARAS[estado.vara_atual]
    valor_esperado, xp_esperado, raridades_bloqueadas = calcular_expectativas(pool, evento, vara, buffs)

    if valor_esperado or xp_esperado:
        print(f"📈 Expectativa: ~{xp_esperado:.1f} XP | ${valor_esperado:.2f} por lançamento")
    if raridades_bloqueadas:
        bloqueadas = ", ".join(raridades_bloqueadas)
        print(f"⚠️  Raridades pesadas demais para esta vara: {bloqueadas}")
    ativos = resumo_buffs_ativos()
    if ativos:
        print("✨ Buffs ativos:")
        for linha in ativos:
            print(f"   • {linha}")
    dica = gerar_dica_alternativas(pool, evento, raridades_bloqueadas)
    if dica:
        print(dica)
    print()


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


def calcular_expectativas(pool, evento, vara, buffs=None):
    buffs = buffs or {}
    bonus_raridade_evento = evento.get("bonus_raridade", {})
    bonus_raridade_buff = buffs.get("bonus_raridade") or {}
    bonus_raridade = bonus_raridade_evento.copy() if bonus_raridade_evento else {}
    for raridade, mult in bonus_raridade_buff.items():
        bonus_raridade[raridade] = bonus_raridade.get(raridade, 1.0) * mult

    raridades_ajustadas = ajustar_pesos_raridade(
        pool["raridades"],
        bonus_raridade,
        vara.get("bonus_raridade", 0.0) + buffs.get("bonus_raridade_vara", 0.0),
    )

    raridades_validas = []
    raridades_bloqueadas = set()

    bonus_peso = evento.get("bonus_peso", 1.0) * buffs.get("bonus_peso", 1.0)
    bonus_valor = evento.get("bonus_valor", 1.0) * buffs.get("bonus_valor", 1.0)
    bonus_mestria = 1 + estado.nivel * 0.002
    xp_mult = (
        evento.get("xp_multiplicador", 1.0)
        * buffs.get("xp_multiplicador", 1.0)
        * (1 + vara.get("bonus_xp", 0.0))
        * pool.get("xp_mult", 1.0)
    )
    chance_mutacao_base = (
        0.15
        + vara["bonus_mutacao"]
        + evento.get("bonus_mutacao", 0)
        + buffs.get("bonus_mutacao", 0.0)
    )
    chance_mutacao = 0.0
    if pool.get("permite_mutacao", True):
        chance_mutacao = max(0.0, min(1.0, chance_mutacao_base))
    mult_mutacao_base = media_multiplicador_mutacoes(evento, vara)
    mult_mutacao_esperado = 1 + chance_mutacao * (mult_mutacao_base - 1)

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
            raridades_bloqueadas.add(raridade)
            continue

        raridades_validas.append((raridade, peso, peso_min, peso_max))

    pesos_totais = sum(peso for _, peso, _, _ in raridades_validas)

    for raridade, peso, peso_min, peso_max in raridades_validas:
        if pesos_totais <= 0:
            break

        peso_medio = ((peso_min + peso_max) / 2) * bonus_peso * bonus_mestria
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
        peso_medio = ((intervalo_secreto[0] + intervalo_secreto[1]) / 2) * bonus_peso * bonus_mestria
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

    return valor_esperado, xp_esperado, sorted(raridades_bloqueadas)
