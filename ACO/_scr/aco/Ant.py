from collections import Generator, Callable
from itertools import accumulate, chain
from random import random
from typing import List

from _scr.others.min_queue import MinQueue


def choose_neighbor(values, s=None):
    # SELECIONA UM INDEX DO ARRAY VALUES COM PROBABILIDADE VALUE[K]/SUM(VALUES)
    if s is None:
        if isinstance(values, Generator):
            values = list(values)
        s = sum(values)

    r = float(random())
    # print('{}  {}'.format(s, values))

    for i, x in enumerate(v / s for v in values):
        r -= x
        if float(r) < 0:
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
        dist = cvrp.dist_
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

    # def local_search(self):
    #     a = randint(0,len(self.__tour) - 1)
    #     b = randint(0,len(self.__tour) - 1)
    #
    #     if b > a:
    #         a,b = b,a
    #     self.__tour = self.__tour[0:a:] + self.__tour[a:b:][::-1] + self.__tour[b:len(self.__tour):]
    #     self._evaluate_fitness()

    def local_search(self):
        self._two_opt()

    def _two_opt(self):
        ranges = self.ranges_truck()
        tour = [self.__tour[i: j + 1] + [0] for i, j in ranges]

        improve = two_opt_AAA(tour, self.__cvrp.get_all_demands(), self.__cvrp.get_capacity(), self.__cvrp.dist_)

        self.truck = [x - 1 for x in accumulate(len(t) - 1 for t in tour if len(t) > 1)]
        self.__tour = list(chain.from_iterable(x[: -1] for x in tour if len(x) > 1))
        self.__fitness -= improve


def two_opt_AAA(tour: list, demand: list, capacity: int, cost: Callable):
    """
    Run 2-opt on CVRP solution.
    :param tour: List with routes of CVRP, each one ending with '0'.
    :param demand: Demand of each client.
    :param capacity: Capacity of truck.
    :param cost: Function of two values u and v that calculates the cost for going from u to v.
    :return: Total improvement and new tour.
    """
    # optimize each route
    improve = sum(two_opt(sub_tour, cost) for sub_tour in tour)

    # exchange routes to be 2-opt
    while True:
        # FIXME: try to simplify this code
        load = [sum(demand[u] for u in sub) for sub in tour]
        ntour = len(tour)
        best = 0
        t1 = t2 = p1 = p2 = op_type = None

        # search for best point
        for p in range(ntour - 1):
            used_p = 0
            for i in range(len(tour[p])):
                a = tour[p][i - 1]
                b = tour[p][i]

                for q in range(p + 1, ntour):
                    # combine first half with first half
                    used_q = 0
                    j = 0
                    while j < len(tour[q]) and (load[p] - used_p) + (load[q] - used_q) > capacity:
                        used_q += demand[tour[q][j]]
                        j += 1
                    while j < len(tour[q]) and used_p + used_q <= capacity:
                        c = tour[q][j - 1]
                        d = tour[q][j]
                        reduce = cost(a, b) + cost(c, d) - cost(a, c) - cost(d, b)
                        if reduce > best:
                            best = reduce
                            t1, t2 = p, q
                            p1, p2 = i, j
                            op_type = 1
                        used_q += demand[tour[q][j]]
                        j += 1

                    # combine first half with second half
                    used_q = 0
                    j = 0
                    while j < len(tour[q]) and used_p + (load[q] - used_q) > capacity:
                        used_q += demand[tour[q][j]]
                        j += 1
                    while j < len(tour[q]) and (load[p] - used_p) + used_q <= capacity:
                        c = tour[q][j - 1]
                        d = tour[q][j]
                        reduce = cost(a, b) + cost(c, d) - cost(a, d) - cost(c, b)
                        if reduce > best:
                            best = reduce
                            t1, t2 = p, q
                            p1, p2 = i, j
                            op_type = 2
                        used_q += demand[tour[q][j]]
                        j += 1

                used_p += demand[b]

        if best == 0:
            break
        improve += best
        r1 = tour[t1]
        r2 = tour[t2]
        if op_type == 1:
            tour[t1], tour[t2] = r1[: p1] + r2[: p2][::-1] + [0], r1[p1: -1][::-1] + r2[p2:]
        else:
            tour[t1], tour[t2] = r1[: p1] + r2[p2:], r2[: p2] + r1[p1:]
        assert tour[t1][-1] == 0
        assert tour[t2][-1] == 0
        assert sorted(r1 + r2) == sorted(tour[t1] + tour[t2])

        improve += two_opt(tour[t1], cost)
        improve += two_opt(tour[t2], cost)

    return improve


def two_opt(tour: List[int], distance: Callable):
    """
    Inplace 2-opt implementation for routing problems.
    If tour is None or len(tour) < 2, the function will simply return 0 without any errors.
    :param tour: A list-like that represents a tour, which will be modified
    :param distance: A function which take as argument two nodes and returns a number representing distance
    :return: The total improvement or 0 if tour is None or len(tour) < 2
    """
    if tour is None or len(tour) < 2:
        return 0
    assert len(set(tour)) == len(tour), "Duplicates found in tour: {}".format(tour)
    assert tour[-1] == 0, "Expected depot at end of tour, found {}".format(tour[-1])

    improve = 0
    n = len(tour)
    while True:
        best = 0
        left = None
        right = None
        dis = [distance(tour[i - 1], tour[i]) for i in range(n)]
        for i in range(-1, n - 3):
            a = tour[i]
            b = tour[i + 1]
            for j in range(i + 2, n - 1):
                c = tour[j]
                d = tour[j + 1]
                reduce = dis[i + 1] + dis[j + 1] - distance(a, c) - distance(b, d)
                if reduce > best:
                    best = reduce
                    left = i + 1
                    right = j

        if best == 0:
            # handle implementation problems
            assert len(set(tour)) == len(tour) and tour[-1] == 0, "Invalid state after execution"
            return improve

        assert left < right
        improve += best
        tour[left: right + 1] = tour[left: right + 1][::-1]
        assert tour[-1] == 0
        assert len(set(tour)) == n
