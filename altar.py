import estado
from utils import limpar_console


REQUISITOS_ALTAR = {
    "Apex": 2,
    "Secreto": 1,
}


def altar_disponivel():
    if estado.serenidade_desbloqueada:
        return False
    return _possui_requisitos()


def _possui_requisitos():
    contagem = {}
    for peixe in estado.inventario:
        raridade = peixe.get("raridade")
        contagem[raridade] = contagem.get(raridade, 0) + 1
    for raridade, qtd in REQUISITOS_ALTAR.items():
        if contagem.get(raridade, 0) < qtd:
            return False
    return True


def _consumir_peixes():
    for raridade, qtd in REQUISITOS_ALTAR.items():
        removidos = 0
        novos = []
        for peixe in estado.inventario:
            if removidos < qtd and peixe.get("raridade") == raridade:
                removidos += 1
                continue
            novos.append(peixe)
        estado.inventario = novos


def invocar_altar():
    if not altar_disponivel():
        return

    limpar_console()
    print("⛩️  Altar dos Anciões\n")
    print(
        "Você encontra um altar escondido entre rochas antigas. As runas contam a história "
        "dos anciões da ilha, que enfrentaram uma besta marinha mítica. Unidos, eles "
        "domaram a criatura usando uma vara forjada para equilíbrio absoluto."
    )
    input("\nPressione ENTER para se aproximar do altar.")

    print(
        "\nAs marcas brilham ao notar seus peixes raros. Uma voz ecoa na sua mente, "
        "pedindo a oferta de 2 APEX e 1 Secreto para reavivar o pacto."
    )
    confirmar = input("Deseja sacrificar esses peixes? (s/n) ").strip().lower()
    if confirmar != "s":
        return

    if not _possui_requisitos():
        print("\n⚠️  Você não possui mais os peixes necessários.")
        input("\nPressione ENTER para continuar.")
        return

    _consumir_peixes()
    estado.serenidade_desbloqueada = True

    print(
        "\nAs águas ao redor do altar ficam imóveis. A lenda revive e a vara Serenidade "
        "aparece listada no mercado por 3000 de ouro."
    )
    input("\nPressione ENTER para continuar.")
