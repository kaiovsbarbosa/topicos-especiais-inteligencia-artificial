import random
import matplotlib.pyplot as plt
from statistics import mean, pstdev
from travelling_salesman_problem.operadores_geneticos import mutacao_swap, order_crossover
from travelling_salesman_problem.selecao_de_pais import torneio
from travelling_salesman_problem.tsp import USA13, calcula_fitness



N_CIDADES = len(USA13)
CIDADES_ROTA = list(range(1, N_CIDADES))
POP_SIZE = 50
MAX_GERACOES = 400
TAM_TORNEIO = 3
TAXA_CROSSOVER = 0.9
TAXA_MUTACAO = 0.05
NUM_ELITE = 5
NUM_EXECUCOES = 30


class IndividuoTSP:
    def __init__(self, rota_genes):
        self.genes = rota_genes
        self.fitness = calcula_fitness(rota_genes)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def copy(self):
        return IndividuoTSP(self.genes.copy())


def inicializar_populacao_tsp(pop_size, cidades_rota):
    populacao = []
    n_cidades_permutadas = len(cidades_rota)
    for _ in range(pop_size):
        genes = random.sample(cidades_rota, n_cidades_permutadas)
        populacao.append(IndividuoTSP(genes))
    return populacao


def ag_tsp():
    populacao = inicializar_populacao_tsp(POP_SIZE, CIDADES_ROTA)
    historico_melhor_fitness = []

    for geracao in range(MAX_GERACOES):
        populacao.sort()
        elite = populacao[:NUM_ELITE]

        melhor_fitness_atual = elite[0].fitness
        historico_melhor_fitness.append(melhor_fitness_atual)

        nova_populacao = elite[:]
        fitness_populacao = [ind.fitness for ind in populacao]

        while len(nova_populacao) < POP_SIZE:
            pais_selecionados = torneio(populacao, fitness_populacao, num_selecionados=2, tam_torneio=TAM_TORNEIO)
            pai1, pai2 = pais_selecionados[0], pais_selecionados[1]

            filho1_genes, filho2_genes = order_crossover(pai1.genes, pai2.genes, TAXA_CROSSOVER)

            filho1_genes_mutado = mutacao_swap(filho1_genes, TAXA_MUTACAO)
            filho2_genes_mutado = mutacao_swap(filho2_genes, TAXA_MUTACAO)

            filho1 = IndividuoTSP(filho1_genes_mutado)
            if len(nova_populacao) < POP_SIZE:
                nova_populacao.append(filho1)

            if len(nova_populacao) < POP_SIZE:
                filho2 = IndividuoTSP(filho2_genes_mutado)
                nova_populacao.append(filho2)

        populacao = nova_populacao

    populacao.sort()
    melhor_individuo = populacao[0]
    fitness_final = melhor_individuo.fitness
    melhor_rota = [0] + melhor_individuo.genes + [0]

    return fitness_final, historico_melhor_fitness, melhor_rota


if __name__ == "__main__":
    fitness_finais = []
    historico_convergencia = []
    melhor_rota_encontrada = []

    print(f"Iniciando {NUM_EXECUCOES} execuções do AG para TSP...")
    for i in range(NUM_EXECUCOES):
        fitness, historico, rota = ag_tsp()
        fitness_finais.append(fitness)

        # [cite_start]Armazena o histórico da primeira execução para o gráfico de convergência [cite: 13]
        if i == 0:
            historico_convergencia = historico
            melhor_rota_encontrada = rota
        print(f"Execução {i + 1}: Fitness final = {fitness}")

    media = mean(fitness_finais)
    dp = pstdev(fitness_finais)
    melhor_absoluta = min(fitness_finais)

    print("\n--- Resultados Estatísticos ---")
    print(f"Média das soluções finais: {media:.2f}")
    print(f"Desvio Padrão das soluções finais: {dp:.2f}")
    print(f"Melhor fitness absoluto (menor distância): {melhor_absoluta}")
    print(f"Melhor rota (primeira execução) - Distância: {historico_convergencia[-1]}: {melhor_rota_encontrada}")

    plt.figure(figsize=(10, 6))
    plt.plot(historico_convergencia, label="Melhor Fitness (Distância)", color='blue')
    plt.title("Gráfico de Convergência do AG para TSP")
    plt.xlabel("Geração")
    plt.ylabel("Melhor Fitness (Distância Total - milhas)")
    plt.grid(True)
    plt.legend()
    plt.savefig("convergencia_tsp.png") # Opção para salvar
    plt.show()

    # [cite_start]3. Criar boxplot com os resultados finais [cite: 13]
    plt.figure(figsize=(8, 7))
    plt.boxplot(fitness_finais, labels=['Resultados Finais AG'])
    plt.title("Boxplot dos Resultados Finais do AG para TSP")
    plt.ylabel("Fitness (Distância Total - milhas)")
    plt.grid(axis='y', linestyle='--')
    plt.savefig("boxplot_resultados_finais.png") # Opção para salvar
    plt.show()