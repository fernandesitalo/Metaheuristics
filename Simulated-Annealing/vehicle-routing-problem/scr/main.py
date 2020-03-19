from scr.Crvp import read
from scr.SimulatedAnnealing import SimulatedAnnealing
from scr.SplitPermutation import optimal_split


path = "../FunctionsBenchmark/Vrp-Set-A/"

if __name__ == '__main__':
    temperatura_inicial = 10000000
    temperatura_final = 10
    alfa = 0.999
    numero_iter = 100
    calcCost = optimal_split

    instance = read(path + "A-n32-k5.vrp")
    result = SimulatedAnnealing(temperatura_inicial,
                                temperatura_final,
                                alfa,
                                numero_iter,
                                instance)
    result.execute()
    print("tour final: ", result.melhor_solucao)
    print("custo final: ", optimal_split(result.cvrp, result.melhor_solucao))
