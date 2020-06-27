from copy import deepcopy

from scr.Ant import Ant


def default_pheromone(dimension):
    return [[1] * dimension] * dimension


class ACO(object):
    def __init__(self, alpha, beta, rho, niter, pheromone, M, cvrp):
        self.__alpha = alpha
        self.__beta = beta
        self.__rho = rho
        self.__niter = niter
        self.__pheromone = pheromone
        self.__M = M
        self.__cvrp = cvrp

    def execute(self):
        Ants = [Ant(self.__cvrp) for _ in range(self.__M)]
        Ants.sort(key=lambda x: x.get_fitness())
        best = deepcopy(Ants[0])
        cost = self.__cvrp.dist
        n = len(self.__pheromone)  # n clientes + deposito central
        # eh sempre constante... pode calcular so uma vez e fodac
        quality = [[1.0 / cost(u, v) if cost(u, v) != 0 else float('inf') for v in range(n)] for u in range(n)]
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
        
        for i in range(n):
            for j in range(n):
                self.__pheromone[i][j] = (1 - self.__rho) * self.__pheromone[i][j] + self.__rho * delta[i][j]
