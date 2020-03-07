import math
import random
from copy import deepcopy


class SimulatedAnnealing(object):
    def __init__(self, initialTemperature, finalTemperature, alfa, nIter, nCities, calcCost, dep, demand, capacity,
                 travelCost, solucao_inicial = None):
        self.currentTemperature = initialTemperature  # inicializacao
        self.initialTemperature = self.currentTemperature
        self.finalTemperature = finalTemperature  # inicializacao
        self.alfa = alfa  # inicializacao
        self.nIter = nIter  # inicializacao
        self.calcCost = calcCost
        self.dep = dep
        self.demand = demand
        self.capacity = capacity
        self.nIter = nIter
        self.travelCost = travelCost
        self.nCities = nCities

        if (solucao_inicial is None) or solucao_inicial == []:  # gera uma solucao inicial qualquer
            aux = []
            for i in range(self.nCities):
                if i != self.dep:
                    aux.append(i)
            random.shuffle(aux)
            self.solucao_atual = aux
        else:
            self.solucao_atual = solucao_inicial

        self.melhor_solucao = self.solucao_atual
        self.custo_atual = self.calcCost(self.nCities, self.solucao_atual, self.capacity, self.travelCost, self.demand,
                                         self.dep)
        self.melhor_custo = self.custo_atual

        print("CUSTO SOLUCAO INICIAL:", self.melhor_custo)
        print(self.melhor_solucao)

    def execute(self):
        while self.initialTemperature> self.finalTemperature:
            for i in range(self.nIter):
                solucao_vizinha = self.move()  # move a solucao atual para uma solucao vizinha
                custo_vizinha = self.calcCost(self.nCities, self.solucao_atual, self.capacity, self.travelCost,
                                              self.demand, self.dep)

                if self.custo_atual >= custo_vizinha:  # atualiza a solucao atual
                    self.solucao_atual = solucao_vizinha
                    self.custo_atual = custo_vizinha
                    if (self.melhor_custo > self.custo_atual):  # atualiza melhor solucao
                        self.melhor_custo = self.custo_atual
                        self.melhor_solucao = self.solucao_atual
                else:
                    prob_aceitacao = math.exp(-(
                            custo_vizinha - self.custo_atual) / self.currentTemperature)  # calculo da probabilidade de aceitacao
                    if prob_aceitacao > random.random():  # aleatoriamente pode pegar esse estado ou nao (que pode ou nao levar para uma solucao melhor)
                        self.solucao_atual = solucao_vizinha
                        self.custo_atual = custo_vizinha
            self.initialTemperature*= self.alfa  # calcula nova temperatura

    def move(self):
        L = deepcopy(self.solucao_atual)
        cidade1 = random.randint(0, self.nCities - 2)
        cidade2 = random.randint(0, self.nCities - 2)
        while cidade1 == self.dep:
            cidade1 = random.randint(0, self.nCities - 2)
        while cidade2 == self.dep:
            cidade2 = random.randint(0, self.nCities - 2)
        a = L[cidade1]
        b = L[cidade2]
        L[cidade1] = b
        L[cidade2] = a
        return L

    def getBestSolution(self):
        return self.melhor_solucao
