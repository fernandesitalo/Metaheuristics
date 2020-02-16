from math import sqrt
import numpy as np
from src import BatAlgorithm, BatAlgorithmHybritization
from src.Functions import rosenbrock


def analise(vetor):
    average = np.mean(vetor)
    dp = 0
    for i in range(len(vetor)):
        dp = dp + (vetor[i]-average)**2
    dp = sqrt(dp/len(vetor))
    print ("Media: ", average)
    print ("Desvio Padrão: ", dp)



if __name__ == '__main__':

    populationSize = 50
    nIterations = 100
    amplitudeInitial = 0.95
    pulseEmissionRateInitial = 0.3
    alfaP = 0.9999
    lambdaP = 0.001
    lowerFrequency = 0
    upperFrequency = 100
    targetFunctionAndLimits = rosenbrock

    qtdExe = 10
    # MEDIA
    # DESVIO PADRÃO

    resultsDefault = []
    resultsHybrid = []

    print("NUMBER OF EXECUTIONS: 30")
    print("RESULTS FOR BAT ALGORITHM DEFAULT")
    for _ in range(qtdExe):
        result = BatAlgorithm.RunBatAlgorithm(targetFunctionAndLimits[1],
                                              targetFunctionAndLimits[0],
                                              populationSize,
                                              nIterations,
                                              amplitudeInitial,
                                              pulseEmissionRateInitial,
                                              alfaP,
                                              lambdaP,
                                              lowerFrequency,
                                              upperFrequency)
        resultsDefault.append(result[0])
        print(result)
    analise(resultsDefault)
    print("RESULTS FOR BAT ALGORITHM WITH HYBRITIZATION ")
    for _ in range(qtdExe):
        result = BatAlgorithmHybritization.RunBatAlgorithmHybrid(targetFunctionAndLimits[1],
                                                                 targetFunctionAndLimits[0],
                                                                 populationSize,
                                                                 nIterations,
                                                                 amplitudeInitial,
                                                                 pulseEmissionRateInitial,
                                                                 alfaP,
                                                                 lambdaP,
                                                                 lowerFrequency,
                                                                 upperFrequency)
        resultsHybrid.append(result[0])
        print(result)
    analise(resultsHybrid)
