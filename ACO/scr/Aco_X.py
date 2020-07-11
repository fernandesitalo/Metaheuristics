from copy import deepcopy
from random import random

from scr.Ant import Ant
from scr.aco import Aco


class Aco_X:

    def __init__(self, niter, pheromone, M, cvrp):
        self._alpha_ = random()
        self._beta_ = random()
        self._rho_ = random()
        print("asdasd")
        self.__niter = niter
        self.__pheromone = pheromone
        self.__M = M
        self.__cvrp = cvrp
        self.best = None
        print("ASDC")

    def execute(self):
        cost = self.__cvrp.dist
        n = len(self.__pheromone)  # n clientes + deposito central
        quality = [[1.0 / cost(u, v) if cost(u, v) != 0 else float('inf') for v in range(n)] for u in range(n)]
        Ants = [Ant(self.__cvrp) for _ in range(self.__M)]

        for i in range(self.__M):
            Ants[i].build_solution(self._alpha_, self._beta_, self.__pheromone, quality)

        Ants.sort(key=lambda x: x.get_fitness())
        self.best = deepcopy(Ants[0])

        for _ in range(self.__niter):
            for ant in Ants:
                ant.build_solution(self._alpha_, self._beta_, self.__pheromone, quality)
            Ants.sort(key=lambda x: x.get_fitness())
            self.update_pheromone(Ants)
            self.update_best(Ants[0])

        param = self.update_parameters()
        self.__alfa = param[0]
        self._beta_ = param[1]
        self._rho_ = param[2]
        return self.best

    def update_parameters(self):
        M = 5
        niter = 100
        best_fitness = 123456
        paramters = []
        for a in range(0, 10):
            for b in range(0, 10):
                for r in range(0, 10):
                    alfa = a/10 + 0.1 * random()
                    beta = b/10 + 0.1 * random()
                    rho = r/10 + 0.1 * random()
                    partial = Aco(alfa, beta, rho, niter, self.__pheromone, M, self.__cvrp).execute()
                    if partial.get_fitness() < best_fitness:
                        best_fitness = partial.get_fitness()
                        paramters = [alfa, beta, rho]
                    self.update_best(partial)
        return paramters

    def update_pheromone(self, population):
        n = len(self.__pheromone)
        delta = [[0] * n] * n

        for x in population:
            x.update_delta(delta)

        for i in range(n):
            for j in range(n):
                self.__pheromone[i][j] = (1 - self._rho_) * self.__pheromone[i][j] + self._rho_ * delta[i][j]

    def update_best(self, new_solution):
        if self.best.get_fitness() > new_solution.get_fitness():
            self.best = deepcopy(new_solution)