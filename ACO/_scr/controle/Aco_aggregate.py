from copy import deepcopy
from random import random

from _scr.aco.aco import Aco
from _scr.controle.Ant_aggregate import Ant_aggregate


class Aco_aggregate(Aco):
    def __init__(self, niter, pheromone, M, cvrp):
        self.__niter = niter
        self.__pheromone = pheromone
        self.__M = M
        self.__cvrp = cvrp

    def execute(self):
        cost = self.__cvrp.dist_
        n = len(self.__pheromone)  # n clientes + deposito central

        # heuristica
        quality = [[1.0 / cost(u, v) if cost(u, v) != 0 else float('inf') for v in range(n)] for u in range(n)]

        Ants = [Ant_aggregate(random(), random(), random(), self.__cvrp) for _ in range(self.__M)]

        for x in Ants:
            x.build_solution(self.__pheromone, quality)
            print(x.get_fitness())

        average_solutions = sum(x.get_fitness() for x in Ants) / self.__M

        Ants.sort(key=lambda x: x.get_fitness())
        best = deepcopy(Ants[0])

        for _ in range(self.__niter):
            for ant in Ants:
                ant.build_solution(self.__pheromone, quality)
            Ants.sort(key=lambda x: x.get_fitness())

            new_average_solutions = sum(x.get_fitness() for x in Ants) / self.__M

            self.update_pheromone(Ants)
            self.update_parameters(Ants, average_solutions, new_average_solutions)
            if best.get_fitness() > Ants[0].get_fitness():
                best = deepcopy(Ants[0])

            average_solutions = new_average_solutions
        return best

    def update_pheromone(self, population):
        n = len(self.__pheromone)
        delta = [[0] * n] * n

        average_rho = 0
        for x in population:
            x.update_delta(delta)
            average_rho += x.get_rho()

        average_rho = average_rho/self.__M

        for i in range(n):
            for j in range(n):
                self.__pheromone[i][j] = (1 - average_rho) * self.__pheromone[i][j] + average_rho * delta[i][j]

    def update_parameters(self, population, average_solutions, new_average_solutions):
        # TODO: melhorar esse update.
        delta = 0.0001

        if new_average_solutions > average_solutions:
            delta *= -1

        for x in population:
            x.update(delta)
            delta *= random()
