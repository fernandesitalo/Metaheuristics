from collections import Generator
from random import random

from scr.min_queue import MinQueue


def choose_neighbor(values, s=None):
    """
    Select one index from values.
    The probability to choose index k is proportional to values[k], i.e., values[k] / sum(values).
    :param values: List with values corresponding to the probability to choose index k.
    :param s: Sum of values. This may speed up the algorithm.
    :return: An integer in range [0, len(values)), the chosen index.
    """
    if s is None:
        if isinstance(values, Generator):
            values = list(values)
        s = sum(values)
    r = random()
    for i, x in enumerate(v / s for v in values):
        r -= x
        if r < 0:
            return i
    return len(values) - 1


class Ant(object):

    def __init__(self, cvrp):
        self.__tour = [0] * cvrp.get_n()
        self.__cvrp = cvrp
        self.__fitness = 0
        self.truck = []

    def build_solution(self, alpha, beta, pheromone, quality):
        n = len(pheromone) - 1  # TAMANHO DO TOUR A SER CONSTRUIDO.
        u = 0  # COMEÇA NO DEPOISTO CENTRAL
        load = 0  # CARREGADO COM 0
        candidate = [u for u in range(0, n + 1)]  # CLIENTES
        for i in range(0, len(candidate) - 1):  # CONTROI O TOUR
            prob_neighbor = [pheromone[u][v] ** alpha * quality[u][v] ** beta for v in candidate]
            u = candidate[choose_neighbor(x for x in prob_neighbor)]
            if u == 0 or load + self.__cvrp.get_demand(u) > self.__cvrp.get_capacity():
                # AGORA ESTOU EM ZERO E QUERO IR PRA ALGUEM QUE N FOI VISITADO AINDA...
                prob_neighbor = [pheromone[0][v] ** alpha * quality[0][v] ** beta for v in candidate[1:]]
                u = candidate[choose_neighbor(x for x in prob_neighbor) + 1]
                load = 0
            load += self.__cvrp.get_demand(u)  ######################
            candidate.remove(u)
            self.__tour[i] = u
        self._evaluate_fitness()  # splita o tour feito de forma otima!

    #
    # def update_delta(self, delta):
    #     change = 1.0 / self.__fitness
    #
    #     for i, j in self._truck_ranges():
    #         u = 0
    #         for v in self.tour[i: j + 1]:
    #             delta[u][v] += change
    #             u = v
    #         delta[u][0] += change

    def get_fitness(self):
        return self.__fitness

    def get_tour(self):
        return self.__tour

    # jeito pika de fazer os splits dos caminhoes.
    def _evaluate_fitness(self):
        cvrp = self.__cvrp
        tour = self.__tour
        n = cvrp.get_n()

        distances = [cvrp.dist(tour[i], tour[i + 1]) for i in range(n - 1)]
        split = [cvrp.dist(tour[i], 0) + cvrp.dist(0, tour[i + 1]) - distances[i] for i in range(n - 1)]
        path = [None] * n
        used = 0
        best = None
        i = 0
        queue = MinQueue()
        queue.push((0, -1))
        for j in range(n):
            used += cvrp.get_demand(tour[j])
            while used > cvrp.get_capacity():
                used -= cvrp.get_demand(tour[i])
                i += 1
                queue.pop()

            assert i <= j
            best, path[j] = queue.min()
            if j < n - 1:
                queue.push((split[j] + best, j))

        self.__fitness = best + cvrp.dist(0, tour[0]) + sum(distances) + cvrp.dist(tour[-1], 0)
        self.truck = []
        v = n - 1
        while v != -1:
            self.truck.append(v)
            v = path[v]
        self.truck = self.truck[::-1]

        # self.validate()
