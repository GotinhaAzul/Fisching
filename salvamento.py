import json
import os

import estado


ARQUIVO_SAVE = "savegame.json"
VERSAO_SAVE = 1


def estado_para_dict():
    return {
        "versao": VERSAO_SAVE,
        "dinheiro": estado.dinheiro,
        "inventario": estado.inventario,
        "vara_atual": estado.vara_atual,
        "varas_possuidas": estado.varas_possuidas,
        "peixes_descobertos": list(estado.peixes_descobertos),
        "desbloqueou_cacadas": estado.desbloqueou_cacadas,
        "desbloqueou_poco_de_desejos": estado.desbloqueou_poco_de_desejos,
        "nivel": estado.nivel,
        "xp": estado.xp,
        "xp_por_nivel": estado.xp_por_nivel,
        "lendarios_pescados": estado.lendarios_pescados,
        "trofeus": estado.trofeus,
        "missoes_ativas": estado.missoes_ativas,
        "ultimo_refresh_missoes": estado.ultimo_refresh_missoes,
        "missoes_concluidas": estado.missoes_concluidas,
    }


def aplicar_estado(dados):
    estado.dinheiro = dados.get("dinheiro", estado.dinheiro)
    estado.inventario = dados.get("inventario", [])
    estado.vara_atual = dados.get("vara_atual", estado.vara_atual)
    estado.varas_possuidas = dados.get("varas_possuidas", estado.varas_possuidas)
    estado.peixes_descobertos = set(dados.get("peixes_descobertos", []))
    estado.desbloqueou_cacadas = dados.get("desbloqueou_cacadas", False)
    estado.desbloqueou_poco_de_desejos = dados.get("desbloqueou_poco_de_desejos", False)
    estado.nivel = dados.get("nivel", estado.nivel)
    estado.xp = dados.get("xp", estado.xp)
    estado.xp_por_nivel = dados.get("xp_por_nivel", estado.xp_por_nivel)
    estado.lendarios_pescados = dados.get("lendarios_pescados", estado.lendarios_pescados)
    estado.trofeus = dados.get("trofeus", {})
    estado.missoes_ativas = dados.get("missoes_ativas", [])
    estado.ultimo_refresh_missoes = dados.get("ultimo_refresh_missoes", 0)
    estado.missoes_concluidas = dados.get("missoes_concluidas", 0)


def salvar_jogo(caminho=ARQUIVO_SAVE):
    dados = estado_para_dict()
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_jogo(caminho=ARQUIVO_SAVE, quiet=False):
    if not os.path.exists(caminho):
        if not quiet:
            print("⚠️ Nenhum save encontrado.")
        return False
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        aplicar_estado(dados)
        if not quiet:
            print("✅ Jogo carregado com sucesso!")
        return True
    except Exception as e:
        if not quiet:
            print(f"❌ Erro ao carregar save: {e}")
        return False
