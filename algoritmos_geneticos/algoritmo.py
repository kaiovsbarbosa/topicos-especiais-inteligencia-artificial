import random
from knapsack import knapsack


class Individuo:
    def __init__(self, genes):
        self.genes = genes
        self.fitness, self.peso, self.valido = knapsack(genes)


    def __repr__(self):
        return f"{self.genes} | fit={self.fitness}"


class AG:
    def __init__(self, pop_size, dim):
        self.pop_size = pop_size
        self.dim = dim
        self.pop = []
        for pos in range(self.pop_size):
            genes = [random.randint(0, 1) for _ in range(self.dim)]
            ind = Individuo(genes)
            # print(ind)
            self.pop.append(ind)

    def __repr__(self):
        output = "Imprimindo AG\n"
        for ind in self.pop:
            output += str(ind) + "\n"
        return output

    def return_individuos(self):
        return self.pop


if __name__ == "__main__":
    dim = 10
    pop_size = 20
    ag = AG(pop_size, dim)
    # print(ag)
    lista_individuos = ag.return_individuos()
    print(lista_individuos)
    # pop = []
    # for pos in range(pop_size):
    #     print(f"Gerando ind #{pos}")
    #     ind = [random.randint(0, 1) for _ in range(dim)]
    #     print(ind)
    #     pop.append(ind)

    # print("População completa")
    # print(pop)
