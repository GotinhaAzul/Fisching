import random
import time

import estado
from buffs import adicionar_buff_permanente, efeitos_para_texto
from faccoes import FACCOES
from bestiario import BESTIARIO, bestiario_completo, progresso_bestiario
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
    while True:
        limpar_console()
        print("🗺️ Central de Missões\n")
        print(f"⭐ Nível: {estado.nivel}")
        print(f"✅ Missões concluídas: {estado.missoes_concluidas}")
        print(f"💰 Dinheiro: ${estado.dinheiro:.2f}\n")
        print("1. Missões de pesca (RNG)")
        print("2. Missões de Facções (história)")
        print("0. Voltar ao menu")

        escolha = input("> ")
        if escolha == "1":
            menu_missoes_rng()
        elif escolha == "2":
            menu_missoes_faccoes()
        elif escolha == "0":
            break


def menu_missoes_rng():
    garantir_missoes()

    while True:
        limpar_console()
        print("🎣 Missões de Pesca (RNG)\n")
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
        print("0. Voltar")

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
    recompensa = (120 + estado.nivel * 15) * dificuldade * 0.4 * bonus
    recompensa_maxima = 500
    return round(min(recompensa, recompensa_maxima), 2)


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


# --- Facções ---------------------------------------------------------------


def _progresso_faccao(faccao_id):
    return estado.progresso_faccoes.setdefault(faccao_id, {"capitulo_atual": 0})


def _diario_faccao(faccao_id):
    return estado.diario_faccoes.setdefault(faccao_id, [])


def _faccao_desbloqueada(faccao):
    requisitos = faccao.get("requisitos_desbloqueio")
    if not requisitos:
        return True
    faltas = _checar_requisitos_faccao(requisitos)
    return not faltas


def _descricao_buff_preview(buff):
    if not buff:
        return "Buff a definir"

    partes = [buff.get("nome", "Buff misterioso")]
    efeito = buff.get("efeito") or buff.get("descricao")
    if not efeito:
        efeito = efeitos_para_texto(buff.get("efeitos"))
    if efeito:
        partes.append(f"- {efeito}")
    origem = buff.get("fonte")
    if origem:
        partes.append(f"({origem})")
    return " ".join(partes)


def _formatar_requisitos_missao(requisitos):
    if not requisitos:
        return ["Sem requisitos adicionais."]

    linhas = []

    faccoes_concluidas = requisitos.get("faccoes_concluidas") or []
    for faccao_id in faccoes_concluidas:
        faccao_nome = FACCOES.get(faccao_id, {}).get("nome", faccao_id)
        linhas.append(f"- Concluir todas as missões da facção {faccao_nome}.")

    nivel_min = requisitos.get("nivel_min")
    if nivel_min:
        linhas.append(f"- Nível mínimo {nivel_min}.")

    xp_min = requisitos.get("xp_min")
    if xp_min:
        linhas.append(f"- Possuir pelo menos {xp_min} XP acumulado.")

    missoes_rng_min = requisitos.get("missoes_rng_min")
    if missoes_rng_min:
        linhas.append(f"- Ter concluído {missoes_rng_min} missões RNG.")

    pagar_dinheiro = requisitos.get("pagar_dinheiro")
    if pagar_dinheiro:
        linhas.append(f"- Pagar ${pagar_dinheiro:.2f}.")

    peixes_por_raridade = requisitos.get("peixes_por_raridade") or {}
    for raridade, qtd in peixes_por_raridade.items():
        linhas.append(f"- Histórico de {qtd} peixes {raridade}.")

    peixes = requisitos.get("peixes") or {}
    for peixe, qtd in peixes.items():
        linhas.append(f"- Sacrificar {qtd}x {peixe} do inventário.")

    mutacoes = requisitos.get("mutacoes") or {}
    for mut, qtd in mutacoes.items():
        linhas.append(f"- Sacrificar {qtd} peixe(s) com mutação {mut}.")

    pools_requeridas = requisitos.get("pools_desbloqueadas") or []
    for pool in pools_requeridas:
        linhas.append(f"- Desbloquear a pool {pool}.")

    flags = requisitos.get("flags") or []
    for flag in flags:
        linhas.append(f"- Desbloquear: {flag.replace('_', ' ').title()}.")

    if requisitos.get("bestiario_completo"):
        descobertos, total = progresso_bestiario()
        linhas.append(f"- Completar 100% do bestiário ({descobertos}/{total}).")

    if requisitos.get("capturou_punicao"):
        linhas.append("- Pescar a Punição ao menos uma vez.")

    return linhas or ["Sem requisitos adicionais."]


def _checar_requisitos_faccao(requisitos):
    faltas = []
    if not requisitos:
        return faltas

    faccoes_concluidas = requisitos.get("faccoes_concluidas") or []
    for faccao_id in faccoes_concluidas:
        progresso = _progresso_faccao(faccao_id)
        total_capitulos = len(FACCOES.get(faccao_id, {}).get("missoes", []))
        if progresso.get("capitulo_atual", 0) < total_capitulos:
            nome = FACCOES.get(faccao_id, {}).get("nome", faccao_id)
            faltas.append(f"Concluir a linha de missões da facção {nome}.")

    nivel_min = requisitos.get("nivel_min")
    if nivel_min and estado.nivel < nivel_min:
        faltas.append(f"Nível mínimo {nivel_min}.")

    xp_min = requisitos.get("xp_min")
    if xp_min and estado.xp < xp_min:
        faltas.append(f"XP mínimo {xp_min}.")

    missoes_rng_min = requisitos.get("missoes_rng_min")
    if missoes_rng_min and estado.missoes_concluidas < missoes_rng_min:
        faltas.append(f"Concluir {missoes_rng_min} missões RNG.")

    pagar_dinheiro = requisitos.get("pagar_dinheiro", 0)
    if pagar_dinheiro and estado.dinheiro < pagar_dinheiro:
        faltas.append(f"Dinheiro insuficiente (${pagar_dinheiro:.2f}).")

    peixes_por_raridade = requisitos.get("peixes_por_raridade") or {}
    for raridade, qtd in peixes_por_raridade.items():
        obtidos = estado.peixes_pescados_por_raridade.get(raridade, 0)
        if obtidos < qtd:
            faltas.append(f"Capturar {qtd} peixes {raridade} (histórico atual: {obtidos}).")

    peixes = requisitos.get("peixes") or {}
    for peixe, qtd in peixes.items():
        encontrados = sum(1 for item in estado.inventario if item.get("nome") == peixe)
        if encontrados < qtd:
            faltas.append(f"Sacrificar {qtd}x {peixe} (inventário: {encontrados}).")

    mutacoes = requisitos.get("mutacoes") or {}
    for mut, qtd in mutacoes.items():
        encontrados = sum(1 for item in estado.inventario if item.get("mutacao") == mut)
        if encontrados < qtd:
            faltas.append(f"Sacrificar {qtd} peixe(s) com mutação {mut} (inventário: {encontrados}).")

    pools_requeridas = requisitos.get("pools_desbloqueadas") or []
    for pool in pools_requeridas:
        if pool not in estado.pools_desbloqueadas:
            faltas.append(f"Desbloquear a pool {pool}.")

    flags = requisitos.get("flags") or []
    for flag in flags:
        if not getattr(estado, flag, False):
            faltas.append(f"Ativar o acesso '{flag.replace('_', ' ').title()}'.")

    if requisitos.get("bestiario_completo") and not bestiario_completo():
        descobertos, total = progresso_bestiario()
        faltas.append(f"Completar o bestiário ({descobertos}/{total}).")

    if requisitos.get("capturou_punicao") and not estado.punicao_pescada:
        faltas.append("Pescar a Punição com sucesso.")

    return faltas


def _remover_itens_por_chave(requisitos, chave):
    if not requisitos:
        return

    faltantes = requisitos.copy()
    novo_inventario = []
    for item in estado.inventario:
        alvo = item.get(chave)
        if alvo in faltantes and faltantes[alvo] > 0:
            faltantes[alvo] -= 1
            continue
        novo_inventario.append(item)

    estado.inventario = novo_inventario


def _consumir_recursos_missao(requisitos):
    if not requisitos:
        return

    pagar_dinheiro = requisitos.get("pagar_dinheiro", 0)
    if pagar_dinheiro:
        estado.dinheiro -= pagar_dinheiro

    _remover_itens_por_chave(requisitos.get("peixes"), "nome")
    _remover_itens_por_chave(requisitos.get("mutacoes"), "mutacao")


def _resumo_recompensa(recompensa):
    if not recompensa:
        return ["Sem recompensas registradas."]

    linhas = []
    itens = recompensa.get("itens") or []
    if itens:
        linhas.append("Itens: " + ", ".join(item.get("nome", "Item misterioso") for item in itens))
    if recompensa.get("dinheiro"):
        linhas.append(f"+${recompensa['dinheiro']:.2f}")
    if recompensa.get("xp"):
        linhas.append(f"+{recompensa['xp']} XP")

    buff = recompensa.get("buff_permanente")
    if buff:
        efeito_txt = buff.get("efeito") or efeitos_para_texto(buff.get("efeitos"))
        linhas.append(f"Buff permanente: {buff.get('nome', 'Buff')} ({efeito_txt})")

    set_flag = recompensa.get("set_flag")
    if set_flag:
        flags = set_flag if isinstance(set_flag, (list, tuple, set)) else [set_flag]
        for flag in flags:
            linhas.append(f"Desbloqueia: {flag.replace('_', ' ').title()}")
    return linhas or ["Sem recompensas registradas."]


def _aplicar_recompensas_faccao(faccao, missao):
    recompensa = missao.get("recompensa") or {}
    dinheiro = recompensa.get("dinheiro", 0)
    xp = recompensa.get("xp", 0)
    buff = recompensa.get("buff_permanente")
    set_flag = recompensa.get("set_flag")
    itens = recompensa.get("itens") or []

    if dinheiro:
        estado.dinheiro += dinheiro
        print(f"💰 Você recebeu ${dinheiro:.2f}.")

    if xp:
        nivel_antes = estado.nivel
        estado.ganhar_xp(xp)
        print(f"⭐ Você ganhou {xp} XP.")
        if estado.nivel > nivel_antes:
            print(f"🎉 Parabéns! Você subiu para o nível {estado.nivel}!")

    if buff:
        buff_instancia = adicionar_buff_permanente(
            buff, fonte=f"{faccao.get('nome')} - {missao.get('titulo')}"
        )
        if buff_instancia:
            efeito_txt = buff_instancia.get("efeito") or efeitos_para_texto(
                buff_instancia.get("efeitos")
            )
            print(f"✨ Buff permanente obtido: {buff_instancia.get('nome')} ({efeito_txt})")

    for item in itens:
        estado.inventario.append(item)
        print(f"🎁 Item obtido: {item.get('nome', 'Item especial')} foi guardado no inventário.")

    flags = []
    if set_flag:
        if isinstance(set_flag, (list, tuple, set)):
            flags = list(set_flag)
        else:
            flags = [set_flag]

    for flag in flags:
        setattr(estado, flag, True)
        print(f"🔓 Novo acesso liberado: {flag.replace('_', ' ').title()}.")


def _registrar_lore(faccao, missao):
    lore = missao.get("lore")
    if not lore:
        return

    diario = _diario_faccao(faccao["id"])
    entrada_id = missao.get("id") or missao.get("titulo")

    if any(ent.get("id") == entrada_id for ent in diario):
        return

    diario.append(
        {
            "id": entrada_id,
            "titulo": missao.get("titulo"),
            "texto": lore,
        }
    )


def mostrar_diario_faccoes(faccoes_lista=None):
    faccoes_lista = faccoes_lista or list(FACCOES.values())
    limpar_console()
    print("📓 Diário das Facções\n")

    total = 0
    for faccao in faccoes_lista:
        entradas = _diario_faccao(faccao["id"])
        if not entradas:
            continue
        total += len(entradas)
        print(f"🏳️ {faccao.get('nome')}")
        for entrada in entradas:
            print(f"• {entrada.get('titulo')}: {entrada.get('texto')}")
        print()

    if total == 0:
        print("Nenhuma anotação ainda. Conclua missões de facção para registrar o lore.")

    input("\nPressione ENTER para voltar.")


def menu_missoes_faccoes():
    while True:
        limpar_console()
        print("🏳️ Missões de Facções\n")
        print("Tarefas lineares que contam a história do mundo e concedem buffs passivos.\n")
        print("-" * 50)

        if not FACCOES:
            print("Nenhuma facção cadastrada. Adicione arquivos em 'faccoes/'.")
            input("\nPressione ENTER para continuar.")
            break

        faccoes_lista = [f for f in FACCOES.values() if _faccao_desbloqueada(f)]
        if not faccoes_lista:
            print("Nenhuma facção disponível no momento. Avance em outras linhas para desbloquear.")
            input("\nPressione ENTER para continuar.")
            break
        print("D. 📓 Abrir diário das facções\n")
        for idx, faccao in enumerate(faccoes_lista, 1):
            progresso = _progresso_faccao(faccao["id"])
            total_capitulos = len(faccao.get("missoes", []))
            capitulo_atual = progresso.get("capitulo_atual", 0)
            print(f"{idx}. {faccao['nome']} ({capitulo_atual}/{total_capitulos} capítulos)")
            print(f"   {faccao.get('descricao', 'Missões em desenvolvimento.')}")
            buff_preview = faccao.get("buffs_passivos", [])
            if buff_preview:
                proximo_buff = buff_preview[capitulo_atual % len(buff_preview)]
                print(f"   Buff previsto: {_descricao_buff_preview(proximo_buff)}")
            print("   " + "-" * 44)
            print()

        print("0. Voltar")
        escolha = input("> ").strip().lower()
        if escolha == "0":
            break
        if escolha == "d":
            mostrar_diario_faccoes(faccoes_lista)
            continue
        if escolha.isdigit():
            escolha_int = int(escolha)
            if 1 <= escolha_int <= len(faccoes_lista):
                mostrar_faccao(faccoes_lista[escolha_int - 1])


def _imprimir_linha_do_tempo(missoes_planejadas, capitulo_atual):
    if not missoes_planejadas:
        print("📜 As missões desta facção ainda estão sendo escritas.\n")
        return

    print("📚 Linha do tempo:")
    for idx, capitulo in enumerate(missoes_planejadas, 1):
        if idx <= capitulo_atual:
            status = "✅ Concluído"
        elif idx == capitulo_atual + 1:
            status = "🧭 Próximo passo"
        else:
            status = "🔒 Bloqueado"
        print(f"- Capítulo {idx}: {capitulo['titulo']} ({status})")
    print()


def _proxima_missao(missoes_planejadas, capitulo_atual):
    if capitulo_atual >= len(missoes_planejadas):
        return None
    return missoes_planejadas[capitulo_atual]


def _mostrar_resumo_missao(missao):
    print("📘 Próximo capítulo")
    print(f"📌 {missao.get('titulo')}")
    print(missao.get("descricao", ""))
    print("\nRequisitos:")
    for linha in _formatar_requisitos_missao(missao.get("requisitos")):
        print(linha)

    print("\nRecompensas:")
    for linha in _resumo_recompensa(missao.get("recompensa")):
        print(f"- {linha}")

    if missao.get("lore"):
        print("\nLore:")
        print("- 🕵️ Revelada somente ao concluir. Confira o diário após completar a missão.")


def _tentar_concluir_missao_faccao(faccao, missao):
    faltas = _checar_requisitos_faccao(missao.get("requisitos"))
    if faltas:
        print("\n⏳ Você ainda não cumpre os requisitos:")
        for falta in faltas:
            print(f"- {falta}")
        input("\nPressione ENTER para continuar.")
        return False

    _consumir_recursos_missao(missao.get("requisitos"))
    _aplicar_recompensas_faccao(faccao, missao)
    _registrar_lore(faccao, missao)
    progresso = _progresso_faccao(faccao["id"])
    progresso["capitulo_atual"] = progresso.get("capitulo_atual", 0) + 1

    input("\nPressione ENTER para continuar.")
    return True


def mostrar_faccao(faccao):
    while True:
        limpar_console()
        progresso = _progresso_faccao(faccao["id"])
        capitulo_atual = progresso.get("capitulo_atual", 0)
        missoes_planejadas = faccao.get("missoes", [])

        print(f"🏳️ {faccao['nome']}\n")
        print(f"{faccao.get('descricao', '')}\n")
        print("-" * 50 + "\n")

        _imprimir_linha_do_tempo(missoes_planejadas, capitulo_atual)

        proxima = _proxima_missao(missoes_planejadas, capitulo_atual)
        if proxima:
            _mostrar_resumo_missao(proxima)
            print("\nOpções:")
            print("1. Tentar concluir a missão")
            print("2. Abrir diário desta facção")
        else:
            print("🎉 Todas as missões desta facção foram concluídas!")
            print("\nOpções:")
            print("1. Abrir diário desta facção")

        print("0. Voltar")
        escolha = input("> ").strip()
        if escolha == "0":
            break
        if escolha == "1":
            if proxima:
                _tentar_concluir_missao_faccao(faccao, proxima)
            else:
                mostrar_diario_faccoes([faccao])
        elif escolha == "2" and proxima:
            mostrar_diario_faccoes([faccao])
