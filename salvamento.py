import json
import os
import shutil

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
    temp_path = f"{caminho}.tmp"
    backup_path = f"{caminho}.bak"

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    # Mantém um backup do save anterior para recuperação em caso de corrupção.
    if os.path.exists(caminho):
        shutil.copyfile(caminho, backup_path)
    else:
        shutil.copyfile(temp_path, backup_path)

    os.replace(temp_path, caminho)


def carregar_jogo(caminho=ARQUIVO_SAVE, quiet=False):
    if not os.path.exists(caminho):
        if not quiet:
            print("⚠️ Nenhum save encontrado.")
        return False

    def _ler_caminho(alvo):
        with open(alvo, "r", encoding="utf-8") as f:
            return json.load(f)

    try:
        dados = _ler_caminho(caminho)
    except Exception as erro_principal:
        backup_path = f"{caminho}.bak"
        if os.path.exists(backup_path):
            try:
                dados = _ler_caminho(backup_path)
                if not quiet:
                    print("♻️ Save principal corrompido. Backup restaurado.")
            except Exception as erro_backup:
                if not quiet:
                    print(f"❌ Erro ao carregar save: {erro_principal}")
                    print(f"❌ Erro ao carregar backup: {erro_backup}")
                return False
        else:
            if not quiet:
                print(f"❌ Erro ao carregar save: {erro_principal}")
            return False

    aplicar_estado(dados)
    if not quiet:
        print("✅ Jogo carregado com sucesso!")
    return True
