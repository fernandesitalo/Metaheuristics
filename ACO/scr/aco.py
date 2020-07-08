from collections import Generator
from copy import deepcopy
from typing import Tuple

from scr.Ant import Ant


def default_pheromone(dimension):
    return [[0.5] * dimension] * dimension


class Aco(object):
    def __init__(self, alpha, beta, rho, niter, pheromone, M, cvrp):
        self.__alpha = alpha
        self.__beta = beta
        self.__rho = rho
        self.__niter = niter
        self.__pheromone = pheromone
        self.__M = M
        self.__cvrp = cvrp

    def execute(self):

        cost = self.__cvrp.dist
        n = len(self.__pheromone)  # n clientes + deposito central
        quality = [[1.0 / cost(u, v) if cost(u, v) != 0 else float('inf') for v in range(n)] for u in range(n)]
        Ants = [Ant(self.__cvrp) for _ in range(self.__M)]

        for i in range(self.__M):
            Ants[i].build_solution(self.__alpha, self.__beta, self.__pheromone, quality)

        Ants.sort(key=lambda x: x.get_fitness())
        best = deepcopy(Ants[0])

        for _ in range(self.__niter):
            for ant in Ants:
                ant.build_solution(self.__alpha, self.__beta, self.__pheromone, quality)
            Ants.sort(key=lambda x: x.get_fitness())
            self.update_pheromone(Ants)
            if best.get_fitness() > Ants[0].get_fitness():
                best = deepcopy(Ants[0])
        return best

    def update_pheromone(self, population):
        n = len(self.__pheromone)
        delta = [[0] * n] * n

        for x in population:
            x.update_delta(delta)

        for i in range(n):
            for j in range(n):
                self.__pheromone[i][j] = (1 - self.__rho) * self.__pheromone[i][j] + self.__rho * delta[i][j]
