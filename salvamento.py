import json
import os
import shutil
from pathlib import Path

import estado


ARQUIVO_SAVE = "savegame.json"
VERSAO_SAVE = 1


def _pasta_save_padrao():
    """Retorna um diretório de save com maior chance de ter permissão de escrita."""
    candidatos = [
        os.getenv("LOCALAPPDATA"),
        os.getenv("APPDATA"),
        os.getenv("XDG_DATA_HOME"),
        Path.home() / ".local" / "share",
        Path.home(),
    ]

    for base in candidatos:
        if not base:
            continue

        caminho_base = Path(base)
        destino = caminho_base / "Fisching"
        try:
            destino.mkdir(parents=True, exist_ok=True)
            return destino
        except OSError:
            # Se não conseguir criar, tenta o próximo candidato.
            continue

    # Último recurso: usa o diretório atual.
    return Path.cwd()


def _caminho_padrao_save():
    return _pasta_save_padrao() / ARQUIVO_SAVE


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
        "peixes_pescados_por_raridade": estado.peixes_pescados_por_raridade,
        "trofeus": estado.trofeus,
        "missoes_ativas": estado.missoes_ativas,
        "ultimo_refresh_missoes": estado.ultimo_refresh_missoes,
        "missoes_concluidas": estado.missoes_concluidas,
        "mostrar_secreto": estado.mostrar_secreto,
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
    contagem_padrao = {
        "Comum": 0,
        "Incomum": 0,
        "Raro": 0,
        "Lendário": 0,
        "Apex": 0,
        "Secreto": 0,
    }
    contagem_padrao.update(dados.get("peixes_pescados_por_raridade", {}))
    estado.peixes_pescados_por_raridade = contagem_padrao
    estado.trofeus = dados.get("trofeus", {})
    estado.missoes_ativas = dados.get("missoes_ativas", [])
    estado.ultimo_refresh_missoes = dados.get("ultimo_refresh_missoes", 0)
    estado.missoes_concluidas = dados.get("missoes_concluidas", 0)
    estado.mostrar_secreto = dados.get(
        "mostrar_secreto", estado.peixes_pescados_por_raridade.get("Secreto", 0) > 0
    )


def _resolver_caminho(caminho):
    if caminho is None:
        return _caminho_padrao_save()
    return Path(caminho)


def salvar_jogo(caminho=None):
    destino = _resolver_caminho(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)

    dados = estado_para_dict()
    temp_path = destino.with_suffix(destino.suffix + ".tmp")
    backup_path = destino.with_suffix(destino.suffix + ".bak")

    with temp_path.open("w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    # Mantém um backup do save anterior para recuperação em caso de corrupção.
    if destino.exists():
        shutil.copyfile(destino, backup_path)
    else:
        shutil.copyfile(temp_path, backup_path)

    os.replace(temp_path, destino)


def carregar_jogo(caminho=None, quiet=False):
    caminho_destino = _resolver_caminho(caminho)

    # Se estivermos usando o caminho padrão e ele não existir, tentamos um save na pasta atual
    # para compatibilidade retroativa.
    if caminho is None and not caminho_destino.exists():
        caminho_legado = Path.cwd() / ARQUIVO_SAVE
        if caminho_legado.exists():
            caminho_destino = caminho_legado

    if not caminho_destino.exists():
        if not quiet:
            print("⚠️ Nenhum save encontrado.")
        return False

    def _ler_caminho(alvo: Path):
        with alvo.open("r", encoding="utf-8") as f:
            return json.load(f)

    try:
        dados = _ler_caminho(caminho_destino)
    except Exception as erro_principal:
        backup_path = caminho_destino.with_suffix(caminho_destino.suffix + ".bak")
        if backup_path.exists():
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
