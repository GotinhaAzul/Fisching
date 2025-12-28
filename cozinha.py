import estado
from utils import limpar_console

# Estrutura de receitas:
# - ingredientes: dict com chaves opcionais "raridades" e "mutacoes", cada uma mapeando item -> quantidade
# - multiplicador: valor final = (soma dos valores base dos peixes usados) * multiplicador
# Para expandir, adicione novos itens em RECEITAS seguindo o mesmo formato.
RECEITAS = [
    {
        "nome": "Grelhado Simples",
        "ingredientes": {"raridades": {"Comum": 1, "Incomum": 1}},
        "multiplicador": 1.5,
        "descricao": "Sabor caseiro que lembra fogueira à beira do lago.",
    },
    {
        "nome": "Ensopado Especial",
        "ingredientes": {"raridades": {"Incomum": 1, "Raro": 1}},
        "multiplicador": 1.85,
        "descricao": "Caldo generoso servido em um tacho fumegante.",
    },
    {
        "nome": "Caldeirada Vibrante",
        "ingredientes": {"raridades": {"Incomum": 1}, "mutacoes": {"Eletrizado": 1}},
        "multiplicador": 2.1,
        "descricao": "Prato que pulsa energia, perfeito para aventureiros cansados.",
    },
    {
        "nome": "Filet Celestial",
        "ingredientes": {"raridades": {"Raro": 1}, "mutacoes": {"Celestial": 1}},
        "multiplicador": 2.4,
        "descricao": "Corte iluminado com brilho suave, digno de um festival.",
    },
    {
        "nome": "Prato Assinado",
        "ingredientes": {"raridades": {"Raro": 1, "Lendário": 1}},
        "multiplicador": 2.5,
        "descricao": "Receita exclusiva do chef, preparada apenas em ocasiões marcantes.",
    },
    {
        "nome": "Risoto da Maré",
        "ingredientes": {"raridades": {"Comum": 1, "Incomum": 1, "Raro": 1}},
        "multiplicador": 1.95,
        "descricao": "Grãos cremosos que destacam a variedade de peixes frescos.",
    },
    {
        "nome": "Taco Tóxico",
        "ingredientes": {"raridades": {"Comum": 2}, "mutacoes": {"Tóxico": 1}},
        "multiplicador": 1.8,
        "descricao": "Picância controlada que surpreende sem ultrapassar o limite seguro.",
    },
    {
        "nome": "Moqueca Encantada",
        "ingredientes": {"raridades": {"Incomum": 2, "Raro": 1}, "mutacoes": {"Enfeitiçado": 1}},
        "multiplicador": 2.2,
        "descricao": "Caldo perfumado que parece brilhar à luz de velas mágicas.",
    },
    {
        "nome": "Caldo Abissal",
        "ingredientes": {"raridades": {"Raro": 1}, "mutacoes": {"Abissal": 1}},
        "multiplicador": 2.45,
        "descricao": "Sopa profunda com sabor denso, feita de criaturas do fundo do mar.",
    },
    {
        "nome": "Banquete Temporal",
        "ingredientes": {"raridades": {"Lendário": 1}, "mutacoes": {"Temporal": 1}},
        "multiplicador": 2.5,
        "descricao": "Prato raro que parece suspender o tempo para apreciar cada garfada.",
    },
]


def cozinhar():
    while True:
        limpar_console()
        print("👩‍🍳 Cozinha")
        print(f"🍽️ Peixes disponíveis: {len(estado.inventario)}")
        print(f"💰 Dinheiro: ${estado.dinheiro:.2f}\n")

        print("Receitas disponíveis:")
        for i, receita in enumerate(RECEITAS, 1):
            ingredientes = ingredientes_para_texto(receita["ingredientes"])
            print(f"{i}. {receita['nome']} - x{receita['multiplicador']:.2f} | {ingredientes} | {receita['descricao']}")
        print("0. Voltar")

        escolha = input("> ")
        if not escolha.isdigit():
            continue

        escolha = int(escolha)
        if escolha == 0:
            break

        if 1 <= escolha <= len(RECEITAS):
            receita = RECEITAS[escolha - 1]
            if not estado.inventario:
                print("\nVocê não tem peixes para cozinhar.")
                input("Pressione ENTER para continuar.")
                continue
            if not tem_ingredientes(receita["ingredientes"]):
                print("\nIngredientes insuficientes para esta receita.")
                input("Pressione ENTER para continuar.")
                continue
            cozinhar_receita(receita)


def normalizar_ingredientes(ingredientes):
    return {
        "raridades": ingredientes.get("raridades", {}),
        "mutacoes": ingredientes.get("mutacoes", {}),
    }


def tem_ingredientes(ingredientes_necessarios):
    ingredientes_necessarios = normalizar_ingredientes(ingredientes_necessarios)
    contagem_raridades = {}
    contagem_mutacoes = {}
    for peixe in estado.inventario:
        contagem_raridades[peixe["raridade"]] = contagem_raridades.get(peixe["raridade"], 0) + 1
        if peixe.get("mutacao"):
            contagem_mutacoes[peixe["mutacao"]] = contagem_mutacoes.get(peixe["mutacao"], 0) + 1

    for raridade, qtd in ingredientes_necessarios["raridades"].items():
        if contagem_raridades.get(raridade, 0) < qtd:
            return False
    for mutacao, qtd in ingredientes_necessarios["mutacoes"].items():
        if contagem_mutacoes.get(mutacao, 0) < qtd:
            return False
    return True


def cozinhar_receita(receita):
    ingredientes_necessarios = normalizar_ingredientes(receita["ingredientes"])
    selecionados = selecionar_peixes_manualmente(ingredientes_necessarios)
    if not selecionados:
        return

    total_base = sum(p["valor"] for p in selecionados)
    ganho = total_base * receita["multiplicador"]

    for peixe in selecionados:
        estado.inventario.remove(peixe)

    while True:
        print(f"\n🍽️ Você preparou '{receita['nome']}' usando: {', '.join(p['nome'] for p in selecionados)}.")
        print(f"Valor do prato: ${ganho:.2f}")
        print("1. Vender agora")
        print("2. Guardar no inventário")
        print("0. Cancelar")
        escolha = input("> ")
        if escolha == "1":
            estado.dinheiro += ganho
            print(f"\n💰 Venda concluída por ${ganho:.2f}!")
            input("Pressione ENTER para continuar.")
            break
        elif escolha == "2":
            prato = {
                "tipo": "prato",
                "nome": receita["nome"],
                "raridade": "Prato",
                "kg": 0.0,
                "mutacao": None,
                "valor": ganho,
                "ingredientes": [p["nome"] for p in selecionados],
            }
            estado.inventario.append(prato)
            print("\n✅ Prato guardado no inventário.")
            input("Pressione ENTER para continuar.")
            break
        elif escolha == "0":
            print("\nAção cancelada. Os peixes já foram consumidos.")
            input("Pressione ENTER para continuar.")
            break


def selecionar_peixes_manualmente(ingredientes_necessarios):
    selecionados_idx = set()
    requisitos_raridades = ingredientes_necessarios.get("raridades", {}).copy()
    requisitos_mutacoes = ingredientes_necessarios.get("mutacoes", {}).copy()

    def restante_texto():
        partes = []
        partes.extend(f"{qtd}x {rar}" for rar, qtd in requisitos_raridades.items() if qtd > 0)
        partes.extend(f"{qtd}x Mutação {mut}" for mut, qtd in requisitos_mutacoes.items() if qtd > 0)
        return ", ".join(partes) or "Nenhum"

    def requisitos_pendentes():
        return any(qtd > 0 for qtd in requisitos_raridades.values()) or any(
            qtd > 0 for qtd in requisitos_mutacoes.values()
        )

    while requisitos_pendentes():
        limpar_console()
        print("👩‍🍳 Selecione os peixes necessários")
        print(f"Restante: {restante_texto()}\n")
        print("Inventário:")
        for i, peixe in enumerate(estado.inventario, 1):
            marcado = "*" if i in selecionados_idx else " "
            print(f"{marcado} {i}. {peixe['nome']} - {peixe['raridade']} - ${peixe['valor']:.2f}")
        print("0. Cancelar")

        escolha = input("> ")
        if not escolha.isdigit():
            continue
        escolha = int(escolha)
        if escolha == 0:
            return []
        if not (1 <= escolha <= len(estado.inventario)):
            continue
        if escolha in selecionados_idx:
            print("Peixe já selecionado.")
            input("Pressione ENTER para continuar.")
            continue

        peixe = estado.inventario[escolha - 1]
        raridade = peixe["raridade"]
        mutacao = peixe.get("mutacao")

        if mutacao and requisitos_mutacoes.get(mutacao, 0) > 0:
            requisitos_mutacoes[mutacao] -= 1
            selecionados_idx.add(escolha)
        elif requisitos_raridades.get(raridade, 0) > 0:
            requisitos_raridades[raridade] -= 1
            selecionados_idx.add(escolha)
        else:
            print("Esse peixe não atende nenhum requisito pendente.")
            input("Pressione ENTER para continuar.")
            continue

    return [estado.inventario[i - 1] for i in sorted(selecionados_idx)]


def ingredientes_para_texto(ingredientes):
    ingredientes = normalizar_ingredientes(ingredientes)
    partes = [f"{qtd}x {raridade}" for raridade, qtd in ingredientes["raridades"].items()]
    partes.extend(f"{qtd}x Mutação {mut}" for mut, qtd in ingredientes["mutacoes"].items())
    return ", ".join(partes)
