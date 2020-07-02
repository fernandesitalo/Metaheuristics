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

    alpha = 0.5
    beta = 0.5
    rho = 0.6
    niter = 1000
    M = 50
    cvrp = read(path2)

    aco = ACO(alpha, beta, rho, niter, default_pheromone(cvrp.get_n()+1), M, cvrp)
    ans = aco.execute()
    print(ans.get_fitness())
    print(ans.get_tour())


if __name__ == '__main__':
    main()
