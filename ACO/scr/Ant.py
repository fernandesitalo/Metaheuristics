from collections import Generator
from random import random


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
        self.__tour = []
        self.__cvrp = cvrp
        self.__fitness = 0

    def build_solution(self, alpha, beta, pheromone, quality):
        self.__tour = [0]
        self.__fitness = 0
        n = len(pheromone) - 1  # TAMANHO DO TOUR A SER CONSTRUIDO.
        u = 0  # COMEÇA NO DEPOISTO CENTRAL
        load = 0  # CARREGADO COM 0
        candidate = [u for u in range(0, n + 1)]  # CLIENTES

        for i in range(0, len(candidate) - 1):  # CONTROI O TOUR
            prob_neighbor = [pheromone[u][v] ** alpha * quality[u][v] ** beta for v in candidate]
            u = candidate[choose_neighbor(x for x in prob_neighbor)]
            if u == 0 or load + self.__cvrp.get_demand(u) > self.__cvrp.get_capacity():
                # AGORA ESTOU EM ZERO E QUERO IR PRA ALGUEM QUE N FOI VISITADO AINDA...
                self.__fitness += self.__cvrp.dist(self.__tour[-1], 0)
                self.__tour.append(0)
                prob_neighbor = [pheromone[0][v] ** alpha * quality[0][v] ** beta for v in candidate[1:]]
                u = candidate[choose_neighbor(x for x in prob_neighbor) + 1]
                load = 0
            load += self.__cvrp.get_demand(u)  ######################
            candidate.remove(u)
            self.__fitness += self.__cvrp.dist(self.__tour[-1], u)
            self.__tour.append(u)

        if self.__tour[-1] != 0:
            self.__fitness += self.__cvrp.dist(self.__tour[-1], 0)
            self.__tour.append(0)

        # self._evaluate_fitness()  # splita o tour feito de forma otima!

    def update_delta(self, delta):  # ACRESCIMO -> DEPOSITO DO FEROMONIO
        delta_tal_x_y = 1.0 / self.__fitness  # Q/(distancia total percorrida pela formiga).
        for i in range(1, len(self.__tour)):
            delta[self.__tour[i - 1]][self.__tour[i]] += delta_tal_x_y

    def get_fitness(self):
        return self.__fitness

    def get_tour(self):
        return self.__tour
