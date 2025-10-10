import random

def roleta(populacao: list, fitness: list, num_selecionados: int) -> list:
    total_fit = 0
    for fit in fitness:
        total_fit += fit
    
    selecionados = []

    for _ in range(num_selecionados):
        ponteiro = random.uniform(0, total_fit)
        soma_acumulada = 0

        for j in range(len(populacao)):
            soma_acumulada += fitness[j]

            if ponteiro <= soma_acumulada:
                selecionados.append(populacao[j])
                break
        
    return selecionados


def torneio(populacao: list, fitness: list, num_selecionados: int, tam_torneio: int) -> list:
    selecionados = []


    for _ in range(num_selecionados):
        melhor_fit = 0
        vencedor = None

        for j in range(tam_torneio):
            index_competidor = random.randint(0, len(populacao) - 1)

            competidor = populacao[index_competidor]
            fitness_competidor = fitness[index_competidor]

            if fitness_competidor > melhor_fit:
                melhor_fit = fitness_competidor
                vencedor = competidor
        
        selecionados.append(vencedor)

    return selecionados

if __name__ == '__main__':
    
    simulacao_populacao = ["A", "B", "C", "D", "E"]
    simulacao_fitness = [10, 50, 20, 90, 40]
    
    print("--- Configuração da População ---")
    print(f"Indivíduos (e Fitness): {list(zip(simulacao_populacao, simulacao_fitness))}")
    print(f"Total de Indivíduos: {len(simulacao_populacao)}\n")

    k = 2
    n = 4
    pais_selecionados = torneio(
        simulacao_populacao, simulacao_fitness, num_selecionados=n, tam_torneio=k
    )
    
    print(f"--- Seleção por Torneio (k={k}) ---")
    print(f"Indivíduos Selecionados ({n} vezes): {pais_selecionados}")

    k = 3
    n = 4
    pais_selecionados_k3 = torneio(
        simulacao_populacao, simulacao_fitness, num_selecionados=n, tam_torneio=k
    )

    print(f"\n--- Seleção por Torneio (k={k}) ---")
    print(f"Indivíduos Selecionados ({n} vezes): {pais_selecionados_k3}")
