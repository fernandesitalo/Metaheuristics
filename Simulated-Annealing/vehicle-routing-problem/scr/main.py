from scr.CalculateCostOfPermutation import dynamicProgrammingIterativeN2
from scr.SimulatedAnnealing import SimulatedAnnealing
from scr.readArchive import readArchive

if __name__ == '__main__':
    temperatura_inicial = 10000000000
    temperatura_final = 10
    alfa = 0.99
    numero_iter = 100
    calcCost = dynamicProgrammingIterativeN2

    with open("A-n32-k5.in", "r") as myfile:
        nCities, travelCost, capacity, x, y, demand, dep = readArchive(myfile)
        SA = SimulatedAnnealing(temperatura_inicial,
                                temperatura_final,
                                alfa,
                                numero_iter,
                                nCities,
                                calcCost,
                                dep,
                                demand,
                                capacity,
                                travelCost)
        best = [21,31,19,17,13,7,26,12,1,16,30,27,24 ,29 ,18 ,8 ,9 ,22 ,15 ,10, 25, 5 ,20 ,14 ,28, 11, 4 ,23 ,3 ,2 ,6]
        SA.execute()
        SA.solucao_atual = SA.getBestSolution()
        SA.custo_atual = calcCost(nCities,SA.getBestSolution(),capacity,travelCost,demand,dep)
        SA.execute()
        print(SA.getBestSolution())
        print("RESULT: ", calcCost(nCities,SA.getBestSolution(),capacity,travelCost,demand,dep))
        print("BEST RESULT: ", calcCost(nCities,best,capacity,travelCost,demand,dep))
    myfile.close()