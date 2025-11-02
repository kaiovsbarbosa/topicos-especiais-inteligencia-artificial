import random
import time
from statistics import mean, pstdev
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any, Optional


USA13 = [
    [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
]
N_CIDADES = len(USA13)
CIDADES_ROTA = list(range(1, N_CIDADES))
NUM_EXECUCOES = 30 
DEFAULT_MAX_GERACOES = 400
DEFAULT_TAXA_CROSSOVER = 0.9


def calcula_fitness(rota, matriz=USA13, inicio=0):
    rota_completa = [inicio] + rota + [inicio]
    distancia = 0
    for i in range(len(rota_completa) - 1):
        distancia += matriz[rota_completa[i]][rota_completa[i+1]]
    return distancia


class IndividuoTSP:
    def __init__(self, rota_genes):
        self.genes = rota_genes
        self.fitness = calcula_fitness(rota_genes)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def copy(self):
        return IndividuoTSP(self.genes.copy())


def inicializar_populacao_tsp(pop_size):
    populacao = []
    n_cidades_permutadas = len(CIDADES_ROTA)
    for _ in range(pop_size):
        genes = random.sample(CIDADES_ROTA, n_cidades_permutadas)
        populacao.append(IndividuoTSP(genes))
    return populacao


def _gerar_filho_ox(segmento_pai, pai_ordenacao, start, end):
    tamanho = len(segmento_pai)
    filho_genes = [None] * tamanho
    segmento_copiado = segmento_pai[start:end + 1]
    filho_genes[start:end + 1] = segmento_copiado
    cidades_presentes = set(segmento_copiado)
    pai_circular = pai_ordenacao[end + 1:] + pai_ordenacao[:end + 1]
    cidades_para_inserir = [cidade for cidade in pai_circular if cidade not in cidades_presentes]
    indice_insercao = end + 1
    for cidade in cidades_para_inserir:
        if indice_insercao >= tamanho:
            indice_insercao = 0
        filho_genes[indice_insercao] = cidade
        indice_insercao += 1
    return filho_genes


def order_crossover(pai1_genes, pai2_genes, taxa_crossover):
    if random.random() >= taxa_crossover:
        return pai1_genes.copy(), pai2_genes.copy()
    tamanho_rota = len(pai1_genes)
    pontos_de_corte = sorted(random.sample(range(tamanho_rota), 2))
    start, end = pontos_de_corte[0], pontos_de_corte[1]

    filho1_genes = _gerar_filho_ox(
        segmento_pai=pai1_genes, pai_ordenacao=pai2_genes, start=start, end=end
    )
    filho2_genes = _gerar_filho_ox(
        segmento_pai=pai2_genes, pai_ordenacao=pai1_genes, start=start, end=end
    )
    return filho1_genes, filho2_genes


def mutacao_swap(individuo_genes, taxa_mutacao):
    mutante = individuo_genes.copy()
    if random.random() < taxa_mutacao:
        size = len(mutante)
        idx1, idx2 = random.sample(range(size), 2)
        mutante[idx1], mutante[idx2] = mutante[idx2], mutante[idx1]
    return mutante


def torneio(populacao: list, fitness: list, num_selecionados: int, tam_torneio: int) -> list:
    selecionados = []
    
    for _ in range(num_selecionados):
        index_competidores = random.sample(range(len(populacao)), tam_torneio)
        
        melhor_fit = float('inf')
        vencedor = None
        
        for index in index_competidores:
            competidor = populacao[index]
            fitness_competidor = fitness[index]
            
            if fitness_competidor < melhor_fit:
                melhor_fit = fitness_competidor
                vencedor = competidor
        
        selecionados.append(vencedor)

    return selecionados


def ag_tsp_parametrizado(pop_size, max_geracoes, tam_torneio, taxa_crossover, taxa_mutacao, num_elite):
    """Algoritmo Genético para TSP que aceita todos os parâmetros configuráveis."""
    populacao = inicializar_populacao_tsp(pop_size)
    historico_melhor_fitness = []

    for geracao in range(max_geracoes):
        populacao.sort()
        elite_count = min(num_elite, pop_size)
        elite = populacao[:elite_count]

        melhor_fitness_atual = populacao[0].fitness
        historico_melhor_fitness.append(melhor_fitness_atual)

        nova_populacao = elite[:]
        fitness_populacao = [ind.fitness for ind in populacao]

        while len(nova_populacao) < pop_size:
            pais_selecionados = torneio(populacao, fitness_populacao, num_selecionados=2, tam_torneio=tam_torneio)
            pai1, pai2 = pais_selecionados[0], pais_selecionados[1]

            filho1_genes, filho2_genes = order_crossover(pai1.genes, pai2.genes, taxa_crossover)

            filho1_genes_mutado = mutacao_swap(filho1_genes, taxa_mutacao)
            filho2_genes_mutado = mutacao_swap(filho2_genes, taxa_mutacao)

            filho1 = IndividuoTSP(filho1_genes_mutado)
            if len(nova_populacao) < pop_size:
                nova_populacao.append(filho1)

            if len(nova_populacao) < pop_size:
                filho2 = IndividuoTSP(filho2_genes_mutado)
                nova_populacao.append(filho2)

        populacao = nova_populacao

    populacao.sort()
    melhor_individuo = populacao[0]
    fitness_final = melhor_individuo.fitness
    
    diversidade = len(set(tuple(ind.genes) for ind in populacao))

    return fitness_final, historico_melhor_fitness, populacao, diversidade



DEFAULT_PARAMS = {
    "pop_size": 50,
    "max_geracoes": DEFAULT_MAX_GERACOES,
    "tam_torneio": 3,
    "taxa_crossover": DEFAULT_TAXA_CROSSOVER,
    "taxa_mutacao": 0.05,
    "num_elite": 5
}

def executar_experimento(valores_teste: List[Any], nome_param: str, default_params: Dict[str, Any], num_execucoes: int = 30) -> Dict[Any, Dict[str, Any]]:
    """Executa o AG para diferentes valores de um parâmetro e coleta resultados."""
    print(f"Startando experimento {nome_param}")
    resultados = {}
    
    for valor in valores_teste:
        print(f"Testando {nome_param} = {valor}")
        
        params = default_params.copy()

        params[nome_param] = valor

        if nome_param == "num_elite":
            num_elite_calculado = valor
            if isinstance(valor, float):
                num_elite_calculado = int(params['pop_size'] * valor)
                if valor > 0 and num_elite_calculado == 0:
                     num_elite_calculado = 1
            
            params['num_elite'] = int(num_elite_calculado)

        fitness_finais = []
        historico_convergencia = []
        tempos_execucao = []
        diversidades = []
        

        for i in range(num_execucoes):
            start_time = time.time()
            
            fitness, historico, pop_final, diversidade_final = ag_tsp_parametrizado(**params)
            
            end_time = time.time()

            fitness_finais.append(fitness)
            tempos_execucao.append(end_time - start_time)
            diversidades.append(diversidade_final)
            
            if i == 0:
                historico_convergencia = historico

        media_tempo = mean(tempos_execucao)
        media_diversidade = mean(diversidades)

        resultados[valor] = {
            "fitness_finais": fitness_finais,
            "historico_convergencia": historico_convergencia,
            "media": mean(fitness_finais),
            "dp": pstdev(fitness_finais),
            "melhor": min(fitness_finais),
            "tempo_medio": media_tempo,
            "diversidade_media": media_diversidade
        }
        print(f"  Média Fit: {resultados[valor]['media']:.2f}, DP: {resultados[valor]['dp']:.2f}, Tempo Médio: {media_tempo:.4f}s")
        
    return resultados


def gerar_graficos_e_analises(experimento_nome: str, resultados: Dict[Any, Dict[str, Any]], analise_tempo: bool = False, analise_diversidade: bool = False):
    """Gera o gráfico de convergência e o boxplot para o experimento."""
    
    config_labels = [str(k) for k in resultados.keys()]
    
    plt.figure(figsize=(12, 7))
    for valor, res in resultados.items():
        plt.plot(res["historico_convergencia"], label=f'{experimento_nome}={valor}', linestyle='-')
        
    plt.title(f"Gráfico de Convergência - Experimento: {experimento_nome}")
    plt.xlabel("Geração")
    plt.ylabel("Melhor Fitness (Distância Total - milhas)")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"convergencia_{experimento_nome}.png")
    plt.close() 

    dados_boxplot = [res["fitness_finais"] for res in resultados.values()]
    plt.figure(figsize=(10, 6))
    plt.boxplot(dados_boxplot, labels=config_labels, patch_artist=True)
    plt.title(f"Boxplot das Soluções Finais - Experimento: {experimento_nome}")
    plt.ylabel("Fitness (Distância Total - milhas)")
    plt.xlabel(experimento_nome)
    plt.grid(axis='y', linestyle='--')
    plt.savefig(f"boxplot_{experimento_nome}.png")
    plt.close()
    
    print(f"Resultados {experimento_nome}")
    print(f"{'Configuração':<15} {'Média (milhas)':<15} {'DP (milhas)':<15} {'Melhor Absoluto':<18} {'Tempo Médio (s)':<18} {'Div. Média':<15}")
    print("-" * 100)
    
    for i, (valor, res) in enumerate(resultados.items()):
        tempo_str = f"{res['tempo_medio']:.4f}" if analise_tempo else "-"
        diversidade_str = f"{res['diversidade_media']:.2f}" if analise_diversidade else "-"
        
        print(
            f"{str(valor):<15} {res['media']:<15.2f} {res['dp']:<15.2f} {res['melhor']:<18} {tempo_str:<18} {diversidade_str:<15}"
        )



if __name__ == "__main__":
    
    pop_sizes = [20, 50, 100]
    exp1_results = executar_experimento(pop_sizes, "pop_size", DEFAULT_PARAMS)
    gerar_graficos_e_analises("Tamanho da População", exp1_results, analise_tempo=True)

    mutacao_rates = [0.01, 0.05, 0.10, 0.20]
    exp2_results = executar_experimento(mutacao_rates, "taxa_mutacao", DEFAULT_PARAMS)
    gerar_graficos_e_analises("Taxa de Mutação", exp2_results)

    torneio_sizes = [2, 3, 5, 7]
    exp3_results = executar_experimento(torneio_sizes, "tam_torneio", DEFAULT_PARAMS)
    gerar_graficos_e_analises("Tamanho do Torneio", exp3_results, analise_diversidade=True)
    
    elite_percentages = [0, 0.02, 0.10, 0.20]
    exp4_results = executar_experimento(elite_percentages, "num_elite", DEFAULT_PARAMS)
    gerar_graficos_e_analises("Elitismo (% População)", exp4_results)
    
    print("\nExecução de todos os experimentos concluída!")