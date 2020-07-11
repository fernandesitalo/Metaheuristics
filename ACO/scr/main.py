from scr.Aco_X import Aco_X
from scr.Crvp import read
from scr.aco import default_pheromone

path = "../FunctionsBenchmark/Vrp-Set-A/"
path2 = "../FunctionsBenchmark/Vrp-Set-A/A-n32-k5.vrp"


def main():
    # pheromone ---> feromonio inicial
    # alpha -------> ?
    # beta --------> ?
    # rho ---------> evaporação do feromonio
    # nIter -------> condição de parada
    # M -----------> numero de formigas
    # cvrp --------> instancia do crvp lida

    alpha = 0.5
    beta = 0.5
    rho = 0.6

    niter = 10000
    M = 5
    cvrp = read(path2)

    aco = Aco_X(1000,default_pheromone(cvrp.get_n() + 1),10,cvrp)
    ans = aco.execute()
    print(ans.get_fitness())
    print(ans.get_tour())


    # aco = Aco(alpha, beta, rho, niter, default_pheromone(cvrp.get_n() + 1), M, cvrp)
    # ans = aco.execute()
    # print(ans.get_fitness())
    # print(ans.get_tour())


    # aco = Aco(alpha, beta, rho, niter, default_pheromone(cvrp.get_n() + 1), M, cvrp)
    # aco = Aco_aggregate(niter,default_pheromone(cvrp.get_n() + 1),M,cvrp)
    # ans = aco.execute()
    # print(ans.get_fitness())
    # print(ans.get_tour())


if __name__ == '__main__':
    main()
