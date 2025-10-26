import random


def torneio(populacao: list, fitness: list, num_selecionados: int, tam_torneio: int) -> list:
    selecionados = []

    for _ in range(num_selecionados):

        index_primeiro_competidor = random.randint(0, len(populacao) - 1)
        melhor_fit = fitness[index_primeiro_competidor]
        vencedor = populacao[index_primeiro_competidor]

        for j in range(tam_torneio - 1):
            index_competidor = random.randint(0, len(populacao) - 1)

            competidor = populacao[index_competidor]
            fitness_competidor = fitness[index_competidor]

            if fitness_competidor < melhor_fit:
                melhor_fit = fitness_competidor
                vencedor = competidor

        selecionados.append(vencedor)

    return selecionados