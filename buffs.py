import copy
import estado


def _efeitos_base():
    return {
        "bonus_raridade": {},
        "bonus_raridade_vara": 0.0,
        "bonus_mutacao": 0.0,
        "bonus_peso": 1.0,
        "bonus_valor": 1.0,
        "xp_multiplicador": 1.0,
        "bonus_reacao": 0.0,
    }


def _combinar_bonus_raridade(destino, novos):
    if not novos:
        return
    for raridade, mult in novos.items():
        destino[raridade] = destino.get(raridade, 1.0) * mult


def _normalizar_buff(buff_def, fonte=None, permanente=False):
    if not buff_def:
        return None

    instancia = copy.deepcopy(buff_def)
    instancia.setdefault("id", instancia.get("nome", "buff"))
    instancia.setdefault("nome", instancia.get("id", "buff"))
    instancia.setdefault("efeitos", {})
    instancia["fonte"] = fonte or instancia.get("fonte") or instancia["nome"]

    if permanente:
        instancia.pop("duracao_pescas", None)
        instancia["usos_restantes"] = None
    else:
        usos = instancia.get("duracao_pescas", 0)
        instancia["usos_restantes"] = instancia.get("usos_restantes", usos)

    return instancia


def ativar_buff(buff_def, fonte=None):
    """Ativa um buff baseado em um dicionário de definição e o salva no estado."""
    instancia = _normalizar_buff(buff_def, fonte=fonte)
    if not instancia:
        return None

    estado.buffs_ativos.append(instancia)
    return instancia


def normalizar_buffs_salvos(buffs_salvos, permanente=False):
    normalizados = []
    for buff in buffs_salvos:
        copia = _normalizar_buff(buff, fonte=buff.get("fonte"), permanente=permanente)
        if copia:
            normalizados.append(copia)
    return normalizados


def adicionar_buff_permanente(buff_def, fonte=None):
    """Adiciona um buff permanente e idempotente à lista do estado."""

    buff = _normalizar_buff(buff_def, fonte=fonte, permanente=True)
    if not buff:
        return None

    for existente in estado.buffs_permanentes:
        if existente.get("id") == buff.get("id"):
            return existente

    estado.buffs_permanentes.append(buff)
    return buff


def _combinar_efeitos_ativos(bonus, buff):
    efeitos = buff.get("efeitos", {})
    _combinar_bonus_raridade(bonus["bonus_raridade"], efeitos.get("bonus_raridade"))
    bonus["bonus_raridade_vara"] += efeitos.get("bonus_raridade_vara", 0.0)
    bonus["bonus_mutacao"] += efeitos.get("bonus_mutacao", 0.0)
    bonus["bonus_peso"] *= efeitos.get("bonus_peso", 1.0)
    bonus["bonus_valor"] *= efeitos.get("bonus_valor", 1.0)
    bonus["xp_multiplicador"] *= efeitos.get("xp_multiplicador", 1.0)
    bonus["bonus_reacao"] += efeitos.get("bonus_reacao", 0.0)


def obter_bonus_ativos():
    bonus = _efeitos_base()
    for buff in estado.buffs_permanentes + estado.buffs_ativos:
        _combinar_efeitos_ativos(bonus, buff)
    return bonus


def consumir_uso(tipo="pesca"):
    """Consome um uso dos buffs ativos. Por padrão, cada pesca reduz 1 uso."""
    expirados = []
    if tipo != "pesca":
        return expirados

    for buff in list(estado.buffs_ativos):
        restante = buff.get("usos_restantes")
        if restante is None:
            continue
        buff["usos_restantes"] = max(0, restante - 1)
        if buff["usos_restantes"] <= 0:
            expirados.append(buff)
            estado.buffs_ativos.remove(buff)
    return expirados


def efeitos_para_texto(efeitos):
    if not efeitos:
        return "Sem efeitos registrados."

    partes = []
    bonus_raridade = efeitos.get("bonus_raridade") or {}
    if bonus_raridade:
        detalhado = ", ".join(
            f"{rar}: {mult*100:.0f}%" for rar, mult in bonus_raridade.items()
        )
        partes.append(f"Chances por raridade: {detalhado}")

    bonus_raridade_vara = efeitos.get("bonus_raridade_vara", 0.0)
    if bonus_raridade_vara:
        partes.append(f"+{bonus_raridade_vara*100:.0f}% chance geral de raridades altas")

    bonus_mutacao = efeitos.get("bonus_mutacao", 0.0)
    if bonus_mutacao:
        partes.append(f"+{bonus_mutacao*100:.0f}% chance de mutação")

    bonus_peso = efeitos.get("bonus_peso", 1.0)
    if bonus_peso != 1.0:
        partes.append(f"{(bonus_peso-1)*100:+.0f}% peso do peixe")

    bonus_valor = efeitos.get("bonus_valor", 1.0)
    if bonus_valor != 1.0:
        partes.append(f"{(bonus_valor-1)*100:+.0f}% valor do peixe")

    xp_mult = efeitos.get("xp_multiplicador", 1.0)
    if xp_mult != 1.0:
        partes.append(f"{(xp_mult-1)*100:+.0f}% XP ganho")

    bonus_reacao = efeitos.get("bonus_reacao", 0.0)
    if bonus_reacao:
        partes.append(f"+{bonus_reacao:.1f}s para reagir")

    return " | ".join(partes) if partes else "Sem efeitos registrados."


def resumo_buffs_ativos():
    if not estado.buffs_ativos:
        return ["Nenhum buff ativo."]

    linhas = []
    for buff in estado.buffs_ativos:
        efeitos_txt = efeitos_para_texto(buff.get("efeitos"))
        duracao_txt = buff.get("usos_restantes")
        restante_txt = (
            f"{duracao_txt} pescas restantes" if duracao_txt is not None else "Duração indeterminada"
        )
        linhas.append(f"{buff.get('nome', 'Buff')} ({restante_txt}) — {efeitos_txt}")
    return linhas
