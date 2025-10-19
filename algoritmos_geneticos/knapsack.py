def _knapsack_constants(dim):
    GANHOS = []
    PESOS = []
    CAPACIDADE_MAXIMA = 0

    if dim == 20:
        GANHOS = [92, 4, 43, 83, 84, 68, 92, 82, 6, 44, 32, 18, 56, 83, 25, 96, 70, 48, 14, 58]
        PESOS = [44, 46, 90, 72, 91, 40, 75, 35, 8, 54, 78, 40, 77, 15, 61, 17, 75, 29, 75, 63]
        CAPACIDADE_MAXIMA = 878

    return GANHOS, PESOS, CAPACIDADE_MAXIMA

def knapsack(solution, dim=20):
    """
    Avalia uma seleção de itens para o problema da mochila com 10 dimensões.
    https://en.wikipedia.org/wiki/Knapsack_problem
    Args:
        solution: lista binária [0,1,0,1,...] indicando quais itens foram selecionados
    Returns:
        tuple: (valor_total, peso_total, é_válido)
    """

    # A instância implementada considera 20 dimensões
    assert len(solution) == dim, "A solução deve ter exatamente 20 dimensões."

    # Valores dos itens (benefícios)
    GANHOS, PESOS, CAPACIDADE_MAXIMA = _knapsack_constants(dim)

    # Calcula valor total e peso total dos itens selecionados
    ganho_total = 0
    peso_total = 0

    for i in range(len(solution)):
        if solution[i] == 1:  # Item foi selecionado
            ganho_total += GANHOS[i]
            peso_total += PESOS[i]

    # Verifica se a solução é válida (não excede a capacidade)
    eh_valido = peso_total <= CAPACIDADE_MAXIMA

    if not eh_valido:
        ganho_total = 0

    return ganho_total, peso_total, eh_valido

def test_knapsack():
    print("=== EXEMPLOS DE USO ===\n")

    # Exemplo 1: Selecionar apenas o item 1 (índice 1)
    selecao1 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
    valor, peso, valido = knapsack(selecao1)
    print(f"Seleção: {selecao1}")
    print(f"Valor: {valor}, Peso: {peso}, Válido: {valido}\n")

    # Exemplo 2: Selecionar itens leves (índices 1, 4, 6)
    selecao2 = [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
    valor, peso, valido = knapsack(selecao2)
    print(f"Seleção: {selecao2}")
    print(f"Valor: {valor}, Peso: {peso}, Válido: {valido}\n")

    # Exemplo 3: Tentar selecionar muitos itens (pode exceder capacidade)
    selecao3 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    valor, peso, valido = knapsack(selecao3)
    print(f"Seleção: {selecao3}")
    print(f"Valor: {valor}, Peso: {peso}, Válido: {valido}\n")

    print("=== INFORMAÇÕES DOS ITENS ===")
    ganhos = [92, 4, 43, 83, 84, 68, 92, 82, 6, 44, 32, 18, 56, 83, 25, 96, 70, 48, 14, 58]
    pesos = [44, 46, 90, 72, 91, 40, 75, 35, 8, 54, 78, 40, 77, 15, 61, 17, 75, 29, 75, 63]

    print("Item | Valor | Peso | Razão Valor/Peso")
    print("-" * 35)
    for i in range(20):
        razao = ganhos[i] / pesos[i]
        print(f"{i:4d} | {ganhos[i]:5d} | {pesos[i]:4d} | {razao:.3f}")

    print("\nCapacidade máxima da mochila: 878")

