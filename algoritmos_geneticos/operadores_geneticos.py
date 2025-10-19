import random

def _aplicar_crossover_com_taxa(pai1, pai2, func_crossover, taxa_crossover=0.8):
    if random.random() < taxa_crossover:
        return func_crossover(pai1, pai2)
    else:
        return pai1.copy(), pai2.copy()

def crossover_um_ponto(pai1: list, pai2: list) -> tuple:
    dim = len(pai1)
    ponto = random.randint(1, dim - 1) 
    
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    
    return filho1, filho2

def crossover_dois_pontos(pai1: list, pai2: list) -> tuple:
    dim = len(pai1)
    
    pontos = sorted(random.sample(range(1, dim), 2))
    ponto1, ponto2 = pontos
    
    filho1 = pai1[:ponto1] + pai2[ponto1:ponto2] + pai1[ponto2:]
    filho2 = pai2[:ponto1] + pai1[ponto1:ponto2] + pai2[ponto2:]
    
    return filho1, filho2

def crossover_uniforme(pai1: list, pai2: list) -> tuple:
    dim = len(pai1)
    filho1 = [0] * dim
    filho2 = [0] * dim
    
    for i in range(dim):
        if random.random() < 0.5: 
            filho1[i] = pai1[i]
            filho2[i] = pai2[i]
        else:
            filho1[i] = pai2[i]
            filho2[i] = pai1[i]
            
    return filho1, filho2

def mutacao_bit_flip(individuo: list, taxa_mutacao: float = 0.02) -> list:
    mutante = individuo.copy()
    for i in range(len(mutante)):
        if random.random() < taxa_mutacao:
            mutante[i] = 1 - mutante[i]
            
    return mutante

def aplicar_crossover_um_ponto(pai1: list, pai2: list, taxa_crossover: float = 0.8) -> tuple:
    return _aplicar_crossover_com_taxa(pai1, pai2, crossover_um_ponto, taxa_crossover)

def aplicar_crossover_dois_pontos(pai1: list, pai2: list, taxa_crossover: float = 0.8) -> tuple:
    return _aplicar_crossover_com_taxa(pai1, pai2, crossover_dois_pontos, taxa_crossover)

def aplicar_crossover_uniforme(pai1: list, pai2: list, taxa_crossover: float = 0.8) -> tuple:
    return _aplicar_crossover_com_taxa(pai1, pai2, crossover_uniforme, taxa_crossover)