from _scr.Crvp.Crvp import read
from _scr.aco.aco import default_pheromone
from _scr.controle.Aco_X import Aco_X
from _scr.criterioDeParada.MaxIterations import MaxIterations
from _scr.criterioDeParada.MaxNoImprove import MaxNoImprove

path = "../FunctionsBenchmark/Vrp-Set-A/"
path2 = "../FunctionsBenchmark/Vrp-Set-A/A-n80-k10.vrp"


def main():
    # pheromone ---> feromonio inicial
    # alpha -------> ?
    # beta --------> ?
    # rho ---------> evaporação do feromonio
    # nIter -------> condição de parada
    # M -----------> numero de formigas
    # cvrp --------> instancia do crvp lida

    M = 10
    cvrp = read(path2)
    aco = Aco_X(MaxIterations(10), default_pheromone(cvrp.get_n() + 1), M, cvrp)
    ans = aco.execute()
    print(ans.get_fitness())
    print(ans.get_tour())


if __name__ == '__main__':
    main()
