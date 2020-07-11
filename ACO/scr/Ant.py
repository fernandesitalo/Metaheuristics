from collections import Generator
from random import random

from scr.min_queue import MinQueue


def choose_neighbor(values, s=None):
    # SELECIONA UM INDEX DO ARRAY VALUES COM PROBABILIDADE VALUE[K]/SUM(VALUES)
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
        self.__tour = []
        self.__cvrp = cvrp
        self.__fitness = 0
        self.truck = []


    def build_solution(self, alpha, beta, pheromone, quality):
        # a formiga faz o mesmo que o caminhão... se ela escolheu ir para o deposito central (0) ou ela
        # "carregou tota sua capacidade" então ela sorteia um novo vizinho com excessão do deposito (já está lá)
        # simulação bem fiel ao modelo do roteamento de veiculos capacitado

        n = len(pheromone) - 1
        u = 0
        load = 0
        candidate = [u for u in range(0, n + 1)]
        self.__tour = []
        for i in range(0, len(candidate) - 1):
            assert candidate[0] == 0, "Implementation error: changed candidate 0 to {}".format(candidate[0])
            probability = [pheromone[u][v] ** alpha * quality[u][v] ** beta for v in candidate]
            u = candidate[choose_neighbor(x for x in probability)]
            if u == 0 or load + self.__cvrp.get_demand(u) > self.__cvrp.get_capacity():
                probability = [pheromone[0][v] ** alpha * quality[0][v] ** beta for v in candidate[1:]]
                u = candidate[choose_neighbor(x for x in probability) + 1]
                load = 0
            load += self.__cvrp.get_demand(u)
            candidate.remove(u)
            self.__tour.append(u)
        self._evaluate_fitness()

    def update_delta(self, delta):
        change = 1.0 / self.__fitness
        L = self.ranges_truck()
        for i, j in L:
            u = 0
            for v in self.__tour[i: j + 1]:
                delta[u][v] += change
                u = v
            delta[u][0] += change

    def get_fitness(self):
        return self.__fitness

    def get_tour(self):
        return self.__tour

    def _evaluate_fitness(self):
        cvrp = self.__cvrp
        tour = self.__tour
        dist = cvrp.dist
        n = cvrp.get_n()

        distances = [dist(tour[i], tour[i + 1]) for i in range(n - 1)]
        split = [dist(tour[i], 0) + dist(0, tour[i + 1]) - distances[i] for i in range(n - 1)]
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

        self.__fitness = best + dist(0, tour[0]) + sum(distances) + dist(tour[-1], 0)
        self.truck = []
        v = n - 1
        while v != -1:
            self.truck.append(v)
            v = path[v]
        self.truck = self.truck[::-1]

    def ranges_truck(self):
        ranges = [(0, self.truck[0])]
        for i in range(1, len(self.truck)):
            ranges.append((self.truck[i - 1] + 1, self.truck[i]))
        return ranges