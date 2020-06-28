from scr.Crvp import read
from scr.aco import ACO, default_pheromone

path = "../FunctionsBenchmark/Vrp-Set-A/"
path2 = "../FunctionsBenchmark/Vrp-Set-A/A-n32-k5.vrp"


def main():
    # pheromone ---> todas aretas 1
    # alpha ------->
    # beta --------> ?
    # rho ---------> evaporação do feromonio
    #  -------> condição de parada
    # M -----------> numero de formigas
    # cvrp --------> instancia do crvp lida

    alpha = 0.4
    beta = 0.6
    rho = 0.7
    niter = 7600
    M = 10
    cvrp = read(path2)

    # L = [0, 31, 6, 18, 24, 21, 19, 20, 26, 0, 2, 9, 22, 15, 28, 7, 0, 16, 13, 8, 14, 27, 1, 0, 12, 5, 11, 3, 10, 29, 25, 0, 23, 4, 30, 0, 17]
    #
    # s = 0
    # for i in range(1,len(L)):
    #     s += cvrp.dist(L[i-1],L[i])
    # print(s)

    aco = ACO(alpha, beta, rho, niter, default_pheromone(cvrp.get_n()), M, cvrp)
    ans = aco.execute()
    print(ans.get_fitness())
    print(ans.get_tour())

if __name__ == '__main__':
    main()
