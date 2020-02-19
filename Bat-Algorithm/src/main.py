from math import sqrt

import matplotlib.pyplot as plt
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
        dp = dp + (vetor[i] - average) ** 2
    dp = sqrt((dp / size))
    arq.write("Media: " + str(average) + "\n")
    arq.write("Desvio Padrão: " + str(dp) + "\n")


def graphicHalf(index, title, xLegend, yLegend, dataArrayX, dataArrayY):
    plt.subplot(2, 2, index)
    plt.title(title)
    plt.xlabel(xLegend)
    plt.ylabel(yLegend)
    plt.plot(dataArrayX, dataArrayY)

def graphicOtherHalf(index, title, xLegend, yLegend, dataArrayX, dataArrayY):
    plt.subplot(2, 2, index)
    plt.title(title)
    plt.xlabel(xLegend)
    plt.ylabel(yLegend)
    plt.plot(dataArrayX, dataArrayY)


def showGraphics():
    plt.subplots_adjust(left=0.10, bottom=0.09, right=0.97, top=0.94, wspace=0.25, hspace=0.27)
    plt.show()


if __name__ == '__main__':

    arq = open('novo-arquivo.txt', 'w')

    # se execultar mais de uma vez, vai plotar o grafico de convergencia somente da ultima execução...
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
    arq.write("lowerFrequency: " + str(lowerFrequency) + "\n")
    arq.write("upperFrequency: " + str(upperFrequency) + "\n")

    arq.write("function : " + "ROSENBROCK" + "\n")

    resultsDefault = []
    resultsHybrid = []
    INI = time.time()
    arq.write("\n\n\nNUMBER OF EXECUTIONS: " + str(qtdExe) + "\n")
    arq.write("RESULTS FOR BAT ALGORITHM DEFAULT" + "\n")

    bestsBatIteractionDefault = [0 for i in range(nIterations)]

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
        arq.write(str(result[0]) + " BESTS/ITERACTION: " + str(result[2]))
        resultsDefault.append(result[0])

        for i in range(nIterations):
            bestsBatIteractionDefault[i] = bestsBatIteractionDefault[i] + result[2][i]

        # arq.write(result)
    fim = time.time()

    bestsBatIteractionHybrid = [0 for i in range(nIterations)]
    arq.write("Tempo de execução: " + str(fim - ini) + "\n")
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
        # arq.write(str(result[0]) + " BESTS/ITERACTION: " + str(result[2]))
        arq.write(str(result[0]))
        resultsHybrid.append(result[0])
        for i in range(nIterations):
            bestsBatIteractionHybrid[i] = bestsBatIteractionHybrid[i] + result[2][i]
    # arq.write(result)
    FIM = time.time()
    fim = time.time()

    arq.write("tempo de execução: " + str(fim - ini) + "\n")
    arq.write("tempo total de execução: " + str(FIM - INI) + "\n")

    arq.write("\n\n\nDEAFAULT BAT ALGORITHM\n")
    analise(resultsDefault)

    arq.write("\n\n\nHYBRID BAT ALGORITHM\n")
    analise(resultsHybrid)
    arq.close()

# make the arrays auxiliares
    # building the dataArrayY -> is the eixo x
    dataArrayX = [t for t in range(qtdExe)]

    # building the arrayX for plot converge bestBat
    arrayX = [t for t in range(nIterations)]

    # build average of the vetor bestsBatsIteraction
    for i in range(nIterations):
        bestsBatIteractionHybrid[i] = bestsBatIteractionHybrid[i] / qtdExe
        bestsBatIteractionDefault[i] = bestsBatIteractionDefault[i] / qtdExe


# mostra resultados
    graphicHalf(1, "Results for default Bat Algorithm",
                "Execution",
                "Best Value",
                dataArrayX,
                resultsDefault)
    graphicOtherHalf(3, "Convergence of the best value - AVERAGE Default Bat Algorithm.",
                     "Iteraction",
                     "Best Value",
                     arrayX,
                     bestsBatIteractionDefault)
    graphicHalf(2, "Results for Hybrid Bat Algorithm",
                "Execution",
                "Best Value",
                dataArrayX,
                resultsHybrid)
    graphicOtherHalf(4, "Convergence of the best value - AVERAGE Hybrid Bat Algorithm",
                     "Iteraction",
                     "Best Value",
                     arrayX,
                     bestsBatIteractionHybrid)
    showGraphics()
