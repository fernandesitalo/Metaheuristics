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

    alpha = 1
    beta = 1
    rho = 0.5
    niter = 100
    M = 5
    cvrp = read(path2)
    aco = ACO(alpha, beta, rho, niter, default_pheromone(cvrp.get_n()), M, cvrp)
    ans = aco.execute()
    print(ans.get_fitness())
    print(ans.get_tour())

if __name__ == '__main__':
    main()
