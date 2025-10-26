import random


def order_crossover(pai1_genes, pai2_genes, taxa_crossover):
    if random.random() >= taxa_crossover:
        return pai1_genes.copy(), pai2_genes.copy()

    tamanho_rota = len(pai1_genes)

    pontos_de_corte = sorted(random.sample(range(tamanho_rota), 2))
    start, end = pontos_de_corte[0], pontos_de_corte[1]

    filho1_genes = _gerar_filho_ox(
        segmento_pai=pai1_genes,
        pai_ordenacao=pai2_genes,
        start=start,
        end=end
    )

    filho2_genes = _gerar_filho_ox(
        segmento_pai=pai2_genes,
        pai_ordenacao=pai1_genes,
        start=start,
        end=end
    )

    return filho1_genes, filho2_genes


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


def mutacao_swap(individuo_genes, taxa_mutacao):
    mutante = individuo_genes.copy()
    if random.random() < taxa_mutacao:
        size = len(mutante)
        idx1, idx2 = random.sample(range(size), 2)
        mutante[idx1], mutante[idx2] = mutante[idx2], mutante[idx1]
    return mutante