from math import exp
from random import uniform, random, randrange, shuffle, randint
from copy import deepcopy

from scr.SplitPermutation import optimal_split


class SimulatedAnnealing(object):
    def __init__(self, initialTemperature, finalTemperature, alfa, nIter, crvp, solucao_inicial=None):
        self.currentTemperature = initialTemperature
        self.initialTemperature = self.currentTemperature
        self.finalTemperature = finalTemperature
        self.alfa = alfa
        self.nIter = nIter
        self.cvrp = crvp

        # gera uma solucao inicial qualquer
        if (solucao_inicial is None) or solucao_inicial == []:
            self.solucao_atual = [i for i in range(1, self.cvrp.number_of_clients + 1, 1)]
            shuffle(self.solucao_atual)
        else:
            self.solucao_atual = solucao_inicial

        self.melhor_solucao = self.solucao_atual
        self.fitness_atual = optimal_split(crvp, self.melhor_solucao)
        self.melhor_fitness = self.fitness_atual

        print("tour inicial: ", self.melhor_fitness)
        print("fitness inicial: ",self.melhor_solucao)

    def local_search(self,tour):
        raffle = lambda : randint(1, self.cvrp.number_of_clients - 1)
        new_tour = tour[::]
        client1 = raffle()
        client2 = raffle()
        while client1 == client2:
            client2 = raffle()
        new_tour[client1],new_tour[client2] = new_tour[client2], new_tour[client1]
        return new_tour

    def neighbor(self,tour):
        i = randrange(0, self.cvrp.number_of_clients - 1)
        j = randrange(i + 2, self.cvrp.number_of_clients + 1)
        return tour[:i] + tour[i: j][::-1] + tour[j:]


    def execute(self):
        while self.initialTemperature > self.finalTemperature:
            for i in range(self.nIter):
                solucao_vizinha = self.neighbor(self.solucao_atual)
                solucao_vizinha = self.local_search(solucao_vizinha)
                fitness_vizinha = optimal_split(self.cvrp, solucao_vizinha)

                if self.fitness_atual > fitness_vizinha:
                    self.solucao_atual = solucao_vizinha
                    self.fitness_atual = fitness_vizinha
                    if self.melhor_fitness > self.fitness_atual:
                        self.melhor_fitness = self.fitness_atual
                        self.melhor_solucao = self.solucao_atual
                else:
                    if exp(-(fitness_vizinha - self.fitness_atual) / self.currentTemperature) > uniform(0, 1):
                        self.solucao_atual = solucao_vizinha
                        self.fitness_atual = fitness_vizinha
            self.initialTemperature *= self.alfa