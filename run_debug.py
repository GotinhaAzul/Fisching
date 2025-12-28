import traceback

try:
    import main
except Exception as e:
    print("❌ Ocorreu um erro ao executar o jogo:\n")
    traceback.print_exc()
    input("\nPressione ENTER para sair.")
