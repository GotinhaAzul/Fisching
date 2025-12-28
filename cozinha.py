import estado
from utils import limpar_console

# Estrutura de receitas simples e expansível:
# - ingredientes: dict raridade -> quantidade exigida
# - multiplicador: valor final = (soma dos valores base dos peixes usados) * multiplicador
# Para expandir, basta adicionar novos itens em RECEITAS seguindo o mesmo formato.
RECEITAS = [
    {
        "nome": "Grelhado Simples",
        "ingredientes": {"Comum": 1, "Incomum": 1},
        "multiplicador": 1.5,
        "descricao": "Comum + Incomum, valor final x1.5.",
    },
    {
        "nome": "Ensopado Especial",
        "ingredientes": {"Incomum": 1, "Raro": 1},
        "multiplicador": 1.9,
        "descricao": "Incomum + Raro, quase dobra o valor.",
    },
    {
        "nome": "Prato Assinado",
        "ingredientes": {"Raro": 1, "Épico": 1},
        "multiplicador": 2.5,
        "descricao": "Raro + Épico, obra-prima valorizada.",
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


def tem_ingredientes(ingredientes_necessarios):
    contagem = {}
    for peixe in estado.inventario:
        contagem[peixe["raridade"]] = contagem.get(peixe["raridade"], 0) + 1
    for raridade, qtd in ingredientes_necessarios.items():
        if contagem.get(raridade, 0) < qtd:
            return False
    return True


def cozinhar_receita(receita):
    ingredientes_necessarios = receita["ingredientes"]
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
    requisitos = ingredientes_necessarios.copy()

    def restante_texto():
        return ", ".join(f"{qtd}x {rar}" for rar, qtd in requisitos.items() if qtd > 0) or "Nenhum"

    while any(qtd > 0 for qtd in requisitos.values()):
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
        if requisitos.get(raridade, 0) <= 0:
            print("Essa raridade não é necessária ou já foi preenchida.")
            input("Pressione ENTER para continuar.")
            continue

        requisitos[raridade] -= 1
        selecionados_idx.add(escolha)

    return [estado.inventario[i - 1] for i in sorted(selecionados_idx)]


def ingredientes_para_texto(ingredientes):
    partes = [f"{qtd}x {raridade}" for raridade, qtd in ingredientes.items()]
    return ", ".join(partes)
