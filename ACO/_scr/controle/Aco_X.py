from copy import deepcopy
from random import random

from _scr.aco.Ant import Ant
from _scr.aco.aco import Aco
from _scr.criterioDeParada.MaxIterations import MaxIterations


class Aco_X:
    def __init__(self, condicao_de_parada, pheromone, M, cvrp):
        self._alpha_ = random()
        self._beta_ = random()
        self._rho_ = random()
        self.__stopping_condition = condicao_de_parada
        self.__pheromone = pheromone
        self.__M = M
        self.__cvrp = cvrp
        self.best = None

        self.L = 5
        self.A = (1, self.L - 1)
        self.B = (1, self.L - 1)
        self.R = (1, self.L - 1)

    def execute(self):
        ans = []
        cost = self.__cvrp.dist_
        n = len(self.__pheromone)  # n clientes + deposito central
        quality = [[1.0 / cost(u, v) if cost(u, v) != 0 else float('inf') for v in range(n)] for u in range(n)]
        Ants = [Ant(self.__cvrp) for _ in range(self.__M)]

        current_average = 0
        for ant in Ants:
            ant.build_solution(self._alpha_, self._beta_, self.__pheromone, quality)
            current_average += ant.get_fitness()
            ant.local_search()

        Ants.sort(key=lambda x: x.get_fitness())
        self.best = deepcopy(Ants[0])
        self.__stopping_condition.start()
        while not self.__stopping_condition:
            last_average = current_average
            current_average = 0
            ans.append([self._alpha_, self._beta_, self._rho_, self.best.get_fitness()])
            for ant in Ants:
                ant.build_solution(self._alpha_, self._beta_, self.__pheromone, quality)
                ant.local_search()
                current_average += ant.get_fitness()

            Ants.sort(key=lambda x: x.get_fitness())
            self.update_pheromone(Ants)
            self.update_best(Ants[0])

            if current_average > last_average and random() > 0.8:
                param = self.update_parameters()
                self._alpha_ = param[0]
                self._beta_ = param[1]
                self._rho_ = param[2]
                self.L -= (self.L-1 != 0)
                self.__stopping_condition.update(True)
            else:
                self.__stopping_condition.update(False)
        ans.append([self._alpha_, self._beta_, self._rho_, self.best.get_fitness()])
        return self.best.get_fitness(), ans

    def update_parameters(self):
        M = 1
        best_fitness = float('inf')
        paramters = []

        v = []

        frac = 1.0 / self.L

        phe = deepcopy(self.__pheromone)

        for a in range(self.A[0], self.A[1] + 1):
            for b in range(self.B[0], self.B[1] + 1):
                for r in range(self.R[0], self.R[1] + 1):
                    alfa = a / self.L + frac * random()
                    beta = b / self.L + frac * random()
                    rho = r / self.L + frac * random()

                    partial = Aco(alfa, beta, rho, MaxIterations(10), phe, M, self.__cvrp).execute()
                    v.append((partial.get_fitness(), [a, b, r]))
                    if partial.get_fitness() < best_fitness:
                        best_fitness = partial.get_fitness()
                        paramters = [alfa, beta, rho]
                        self.update_best(partial)

        v.sort(key=lambda x: x[0])

        A = [self.L - 1, 0]
        B = [self.L - 1, 0]
        R = [self.L - 1, 0]

        for i in range(min(len(v), 2)):
            param = v[i][1]
            A[0] = min(A[0], param[0])
            A[1] = max(A[0], param[0])

            B[0] = min(B[0], param[1])
            B[1] = max(B[1], param[1])

            R[0] = min(R[0], param[2])
            R[1] = max(R[1], param[2])

        self.A = (A[0], A[1])
        self.B = (B[0], B[1])
        self.R = (R[0], R[1])

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
