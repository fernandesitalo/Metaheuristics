from math import sqrt
import numpy as np
from src import BatAlgorithm, BatAlgorithmHybritization
from src.Functions import rosenbrock
import time

# ATENCAO!!!!!!

# executa a main que vai gerar um arquivo de texto na pasta src!!!!!!!!!!!

# se quiser mudar a quantidade de dimensões da funcao, vai no arquivo function.py!!!!!!!!!

# =D


def analise(vetor):
    average = np.mean(vetor)
    dp = 0
    size = len(vetor)
    for i in range(size):
        dp = dp + (vetor[i]-average)**2
    dp = sqrt((dp/size))
    arq.write ("Media: " + str(average) + "\n")
    arq.write ("Desvio Padrão: " + str(dp) + "\n")



if __name__ == '__main__':

    arq = open('novo-arquivo.txt', 'w')

    qtdExe = 30

    populationSize = 30
    nIterations = 1000
    amplitudeInitial = 0.95
    pulseEmissionRateInitial = 0.3
    alfaP = 0.9999
    lambdaP = 0.001
    lowerFrequency = 0
    upperFrequency = 100
    targetFunctionAndLimits = rosenbrock

    arq.write("populationSize: " + str(populationSize) + "\n")
    arq.write("nIterations: " + str(nIterations) + "\n")
    arq.write("amplitudeInicial: " + str(amplitudeInitial) + "\n")
    arq.write("pulseEmissionRateInitial: " + str(pulseEmissionRateInitial) + "\n")
    arq.write("alfaP: " + str(alfaP) + "\n")
    arq.write("lowerFrequency: " +str(lowerFrequency) + "\n")
    arq.write("upperFrequency: " + str(upperFrequency) + "\n")


    arq.write("function : " + "ROSENBROCK" + "\n")

    resultsDefault = []
    resultsHybrid = []
    INI = time.time()
    arq.write("\n\n\nNUMBER OF EXECUTIONS: "+ str(qtdExe) + "\n")
    arq.write("RESULTS FOR BAT ALGORITHM DEFAULT"+"\n")

    ini = time.time()
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
        arq.write(str(result[0]) + "\n")
        resultsDefault.append(result[0])
        # arq.write(result)
    fim = time.time()
    arq.write("Tempo de execução: " + str(fim-ini) + "\n")
    arq.write("RESULTS FOR BAT ALGORITHM WITH HYBRITIZATION " + "\n")
    ini = time.time()
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
        arq.write(str(result[0]) + "\n")
        resultsHybrid.append(result[0])
        # arq.write(result)
    FIM = time.time()
    fim = time.time()
    arq.write("tempo de execução: "+str(fim-ini) + "\n")
    arq.write("tempo total de execução: " +str(FIM-INI) + "\n")

    arq.write("\n\n\nDEAFAULT BAT ALGORITHM\n")
    analise(resultsDefault)

    arq.write("\n\n\nHYBRID BAT ALGORITHM\n")
    analise(resultsHybrid)
    arq.close()
