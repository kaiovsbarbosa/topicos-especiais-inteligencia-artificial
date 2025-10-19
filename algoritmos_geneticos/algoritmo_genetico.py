import random
import copy
from knapsack import knapsack
from selecao_de_pais import torneio
from operadores_geneticos import (
    aplicar_crossover_um_ponto, 
    aplicar_crossover_dois_pontos, 
    aplicar_crossover_uniforme, 
    mutacao_bit_flip
)
from statistics import mean, pstdev
import matplotlib.pyplot as plt
import numpy as np


POP_SIZE = 50 
DIM = 20
MAX_GERACOES = 500
TAM_TORNEIO = 3
TAXA_CROSSOVER = 0.8
TAXA_MUTACAO = 0.02
NUM_ELITE = 2 
NUM_EXECUCOES = 30 


class Individuo:
    def __init__(self, genes):
        self.genes = genes
        self.fitness, self.peso, self.valido = knapsack(genes, dim=DIM) 

    def __lt__(self, other):
        return self.fitness < other.fitness
    
    def copy(self):
        return Individuo(self.genes.copy())


def inicializar_populacao(pop_size, dim):
    populacao = []
    for _ in range(pop_size):
        genes = [random.randint(0, 1) for _ in range(dim)]
        populacao.append(Individuo(genes))
    return populacao

def ag_knapsack(crossover_func):
    populacao = inicializar_populacao(POP_SIZE, DIM)
    historico_melhor_fitness = []
    
    for geracao in range(MAX_GERACOES):
        populacao.sort(reverse=True)
        elite = populacao[:NUM_ELITE]
        
        melhor_fitness_atual = elite[0].fitness
        historico_melhor_fitness.append(melhor_fitness_atual)

        nova_populacao = elite


        genes_populacao = [ind.genes for ind in populacao]
        fitness_populacao = [ind.fitness for ind in populacao]

        while len(nova_populacao) < POP_SIZE:
            pais_selecionados = torneio(
                genes_populacao, fitness_populacao, num_selecionados=2, tam_torneio=TAM_TORNEIO
            )
            pai1_genes, pai2_genes = pais_selecionados[0], pais_selecionados[1]

            filho1_genes, filho2_genes = crossover_func(pai1_genes, pai2_genes, TAXA_CROSSOVER)
            
            filho1_genes_mutado = mutacao_bit_flip(filho1_genes, TAXA_MUTACAO)
            filho2_genes_mutado = mutacao_bit_flip(filho2_genes, TAXA_MUTACAO)

            filho1 = Individuo(filho1_genes_mutado)
            
            if len(nova_populacao) < POP_SIZE:
                nova_populacao.append(filho1)

            if len(nova_populacao) < POP_SIZE:
                filho2 = Individuo(filho2_genes_mutado)
                nova_populacao.append(filho2)
            
        populacao = nova_populacao # Renovação da população

    populacao.sort(reverse=True)
    fitness_final = populacao[0].fitness

    return fitness_final, historico_melhor_fitness


if __name__ == "__main__":
    HCT_ATIVIDADE_3 = [1005, 938, 961, 916, 948, 941, 936, 959, 950, 999, 926, 973, 950, 943, 946, 967, 951, 948, 938, 917, 979, 950, 1005, 885, 1005, 961, 973, 999, 912, 979]
    
    HCE_ATIVIDADE_3 = [821, 811, 989, 728, 874, 855, 876, 877, 974, 941, 909, 866, 898, 947, 887, 818, 816, 863, 820, 927, 925, 880, 932, 806, 968, 968, 940, 1003, 884, 1003]

    HCT_FITNESS = np.array(HCT_ATIVIDADE_3) 
    HCE_FITNESS = np.array(HCE_ATIVIDADE_3)

    
    resultados_ag = {
        "Um Ponto": {"func": aplicar_crossover_um_ponto, "fitness_finais": [], "historicos": []},
        "Dois Pontos": {"func": aplicar_crossover_dois_pontos, "fitness_finais": [], "historicos": []},
        "Uniforme": {"func": aplicar_crossover_uniforme, "fitness_finais": [], "historicos": []},
    }

    for nome, config in resultados_ag.items():
        print(f"\nIniciando {NUM_EXECUCOES} execuções do AG com Crossover {nome}...")
        for i in range(NUM_EXECUCOES):
            fitness, historico = ag_knapsack(config["func"])
            config["fitness_finais"].append(fitness)
            if i == 0: 
                config["historicos"] = historico
            print(f"Execução {i+1}: Fitness final = {fitness}")


    dados_boxplot = [HCT_FITNESS, HCE_FITNESS]
    labels_boxplot = ["H.C. Tradicional", "H.C. Estocástico"]

    resultados_estatisticos = {
        "H.C. Tradicional": {"Média": mean(HCT_FITNESS), "Desvio Padrão": pstdev(HCT_FITNESS), "Absoluta": max(HCT_FITNESS)},
        "H.C. Estocástico": {"Média": mean(HCE_FITNESS), "Desvio Padrão": pstdev(HCE_FITNESS), "Absoluta": max(HCE_FITNESS)},
    }


    print("Resultados:")
    for nome, config in resultados_ag.items():
        fitness_finais = config["fitness_finais"]
        media = mean(fitness_finais)
        dp = pstdev(fitness_finais)
        melhor_absoluta = max(fitness_finais)
        
        resultados_estatisticos[f"AG {nome}"] = {"Média": media, "Desvio Padrão": dp, "Absoluta": melhor_absoluta}
        
        dados_boxplot.append(fitness_finais)
        labels_boxplot.append(f"AG {nome}")
        
        print(f"AG Crossover {nome}: Média={media:.2f}, DP={dp:.2f}, Melhor Absoluta={melhor_absoluta}")
        
    print("\n" + "="*40 + "\n")
    
    plt.figure(figsize=(10, 6))
    for nome, config in resultados_ag.items():
        plt.plot(config["historicos"], label=f"AG {nome}", linestyle='-')
        
    plt.title("Gráfico de Convergência")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.legend()
    plt.savefig("convergencia_ags.png")
    plt.show()

    # Gráfico Boxplot 
    plt.figure(figsize=(12, 7))
    plt.boxplot(dados_boxplot, labels=labels_boxplot, patch_artist=True)
    plt.title("Boxplot")
    plt.ylabel("Fitness")
    plt.grid(axis='y', linestyle='--')
    plt.savefig("boxplot_comparativo.png")
    plt.show()