import random
import estado
from utils import limpar_console
from varas import VARAS
from dados import MUTACOES
from pesca import minigame_reacao, RARIDADE_VALOR_MULT, RARIDADE_XP_MULT

CACADAS = [
    {
        "nome": "Caçada do Leviatã",
        "descricao": "Um titã dos mares responde apenas a sacrifícios lendários específicos.",
        "sacrificios": {
            "peixes": {"Kraken": 1, "Nemo": 1},
            "mutacoes": {"Divino": 1},
        },
        "apex_peixes": ["Leviatã Primevo", "Serpente das Profundezas"],
        "peso_min": 80,
        "peso_max": 120,
        "valor_base": 350,
        "tentativas": 5,
    },
    {
        "nome": "Caçada da Fênix Marinha",
        "descricao": "As chamas frias do oceano atraem um pássaro mítico quando ofertas raras são feitas.",
        "sacrificios": {
            "peixes": {"Enguia Fantasma": 1, "Koi Dourada": 1},
            "mutacoes": {"Temporal": 1},
        },
        "apex_peixes": ["Fênix Marinha", "Arpão Celeste"],
        "peso_min": 75,
        "peso_max": 110,
        "valor_base": 300,
        "tentativas": 5,
    },
]

CHANCE_APEX = 0.05


def _contar_recursos():
    peixes = {}
    mutacoes = {}
    for item in estado.inventario:
        nome = item.get("nome")
        mut = item.get("mutacao")
        if nome:
            peixes[nome] = peixes.get(nome, 0) + 1
        if mut:
            mutacoes[mut] = mutacoes.get(mut, 0) + 1
    return peixes, mutacoes


def _consumir_recursos(cacada):
    req_peixes = cacada["sacrificios"]["peixes"]
    req_mutacoes = cacada["sacrificios"]["mutacoes"]
    restantes = []
    consumo_peixes = req_peixes.copy()
    consumo_mut = req_mutacoes.copy()

    for item in estado.inventario:
        nome = item.get("nome")
        mut = item.get("mutacao")

        if nome in consumo_peixes and consumo_peixes[nome] > 0:
            consumo_peixes[nome] -= 1
            continue

        if mut and mut in consumo_mut and consumo_mut[mut] > 0:
            consumo_mut[mut] -= 1
            continue

        restantes.append(item)

    estado.inventario = restantes


def _pescar_em_cacada(cacada):
    vara = VARAS[estado.vara_atual]
    tentativas_restantes = cacada.get("tentativas", 5)
    while tentativas_restantes > 0:
        if vara["peso_max"] < cacada["peso_min"]:
            print(
                f"\n❌ Sua vara atual suporta até {vara['peso_max']}kg, "
                f"mas o alvo APEX pesa no mínimo {cacada['peso_min']}kg."
            )
            print("Equipe uma vara mais forte para iniciar esta caçada.")
            input("\nPressione ENTER para voltar")
            break

        limpar_console()
        print(f"🎯 Caçada: {cacada['nome']}")
        print(cacada["descricao"])
        print(f"Chance de fisgar um peixe APEX: {int(CHANCE_APEX * 100)}%")
        print(f"Tentativas restantes: {tentativas_restantes}")
        print("\n[L] Lançar isca")
        print("[V] Voltar")
        escolha = input("> ").lower()

        if escolha != "l":
            break

        tentativas_restantes -= 1

        if random.random() > CHANCE_APEX:
            print("\n🌌 O alvo APEX não apareceu desta vez.")
            input("\nPressione ENTER para tentar novamente")
            continue

        raridade = "Apex"
        peixe = random.choice(cacada["apex_peixes"])

        mutacao = None
        mult_mut = 1.0
        mutacao_chance = 0.10 + vara["bonus_mutacao"]
        if random.random() < mutacao_chance:
            mutacao = random.choice(list(MUTACOES.keys()))
            mult_mut = MUTACOES[mutacao]

        kg = random.uniform(cacada["peso_min"], cacada["peso_max"])

        if not minigame_reacao(vara, raridade):
            print("\n💥 Você errou o combo APEX e o peixe escapou!")
            input("\nPressione ENTER para continuar")
            continue

        kg *= 1.20
        if kg > vara["peso_max"]:
            kg = vara["peso_max"]

        valor = (kg * 0.1) * cacada["valor_base"] * mult_mut * RARIDADE_VALOR_MULT.get(raridade, 1)

        estado.inventario.append(
            {
                "nome": peixe,
                "raridade": raridade,
                "mutacao": mutacao,
                "kg": kg,
                "valor": valor,
            }
        )
        estado.peixes_descobertos.add(peixe)

        xp_ganho = int(kg * RARIDADE_XP_MULT.get(raridade, 1))
        xp_ganho = max(1, xp_ganho)
        estado.xp += xp_ganho
        print(f"\n🎣 Você pescou: {peixe} [{raridade}] - {kg:.2f}kg")
        print(f"💰 Valor: ${valor:.2f}")
        print(f"⭐ Você ganhou {xp_ganho} XP!")

        while estado.xp >= estado.xp_por_nivel:
            estado.nivel += 1
            estado.xp -= estado.xp_por_nivel
            print(f"🎉 Parabéns! Você subiu para o nível {estado.nivel}!")

        input("\nPressione ENTER para continuar a caçada")

    if tentativas_restantes == 0:
        print("\n⌛ Você esgotou as tentativas desta caçada.")
        input("\nPressione ENTER para voltar")


def menu_cacadas():
    while True:
        limpar_console()
        peixes_disp, mutacoes_disp = _contar_recursos()
        print("🔥 Caçadas APEX\n")
        print("Sacrifique peixes lendários específicos e mutações para acessar um alvo APEX temporariamente.")
        print("Recursos disponíveis (peixes):")
        print(", ".join(f"{qtd}x {nome}" for nome, qtd in peixes_disp.items()) or "nenhum")
        print("Recursos disponíveis (mutações):")
        print(", ".join(f"{qtd}x {mut}" for mut, qtd in mutacoes_disp.items()) or "nenhum")
        print()

        for i, cacada in enumerate(CACADAS, start=1):
            print(
                f"{i}. {cacada['nome']} - custo: "
                f"{', '.join(f'{qtd}x {nome}' for nome, qtd in cacada['sacrificios']['peixes'].items())}; "
                f"mutações: {', '.join(f'{qtd}x {mut}' for mut, qtd in cacada['sacrificios']['mutacoes'].items()) or 'nenhuma'}"
            )
            print(f"   Alvos: {', '.join(cacada['apex_peixes'])}")
            print(f"   {cacada['descricao']}\n")
        print("0. Voltar")

        escolha = input("> ")
        if escolha == "0":
            break
        if not escolha.isdigit():
            continue

        indice = int(escolha) - 1
        if indice < 0 or indice >= len(CACADAS):
            continue

        cacada = CACADAS[indice]
        peixes_disp, mutacoes_disp = _contar_recursos()

        def possui_recursos():
            for nome, qtd in cacada["sacrificios"]["peixes"].items():
                if peixes_disp.get(nome, 0) < qtd:
                    return False
            for mut, qtd in cacada["sacrificios"]["mutacoes"].items():
                if mutacoes_disp.get(mut, 0) < qtd:
                    return False
            return True

        if not possui_recursos():
            print("\n❌ Recursos insuficientes para iniciar esta caçada.")
            input("\nPressione ENTER para voltar")
            continue

        confirmar = input(
            "\nConfirmar sacrifício de "
            + ", ".join(f"{qtd}x {nome}" for nome, qtd in cacada["sacrificios"]["peixes"].items())
            + " e "
            + (", ".join(f"{qtd}x {mut}" for mut, qtd in cacada["sacrificios"]["mutacoes"].items()) or "nenhuma mutação")
            + "? (s/n) "
        ).lower()
        if confirmar != "s":
            continue

        _consumir_recursos(cacada)
        _pescar_em_cacada(cacada)
