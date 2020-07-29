import os
import sys

from os import listdir
from time import time

from _scr.Crvp.Crvp import read
from _scr.aco.aco import default_pheromone
from _scr.controle.Aco_X import Aco_X
from _scr.criterioDeParada.MaxIterations import MaxIterations
from _scr.criterioDeParada.MaxNoImprove import MaxNoImprove

path = "Metaheuristics/ACO/FunctionsBenchmark/Vrp-Set-A/{}"


def soma(a, b):
    if a == []:
        return b
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] += b[i][j]
    return a


def average(a, qtd , qtd2):
    s = [0,0,0,0]
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = a[i][j] / qtd
            s[j] += a[i][j]
    for i in range(4):
        s[i] = s[i]/ qtd2
    return a,s


def main():
    # pheromone ---> feromonio inicial
    # alpha -------> ?
    # beta --------> ?
    # rho ---------> evaporação do feromonio
    # nIter -------> condição de parada
    # M -----------> numero de formigas
    # cvrp --------> instancia do crvp lida

    param = sys.argv[1:]
    archive = param[0]
    M = 10
    cvrp = read(path.format(archive))
    qtd = 30
    sum_ans = []
    best_all = float('inf')

    #roda 30x, pego a media de cada iteração e depois a media geral de cada parametro e do melhor fintess


    init = time()
    print("ALFA;BETA;RHO;BEST_FINTESS;")
    for _ in range(qtd):
        aco = Aco_X(MaxIterations(10), default_pheromone(cvrp.get_n() + 1), M, cvrp)
        ans, v = aco.execute()
        best_all = min(ans, best_all)
        sum_ans = soma(sum_ans, v)
    end = time()

    sum_ans,media = average(sum_ans, qtd, 10)
    print(sum_ans)
    print(media)
    print("best_fintess: {}".format(best_all))
    print("time: {}".format(end-init))

if __name__ == '__main__':
    main()
