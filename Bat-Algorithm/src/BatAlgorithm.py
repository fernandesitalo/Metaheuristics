import copy
from math import exp
import numpy as np
from src.Bat import Bat


def adjustLimits(value, dimension, limits):
    value = (limits[dimension][0] if limits[dimension][0] > value else value) # lower limit
    value = (limits[dimension][1] if limits[dimension][1] < value else value) # upper limit
    return value

def updateKBest(k,bat,bestKBats):
    bestKBats.append(bat)
    bestKBats.sort(reverse = True)
    while len(bestKBats) > k: bestKBats.pop()
    return bestKBats

def selectSomeGoodBat(bestKBats):
    t = len(bestKBats)
    return bestKBats[np.random.randint(0,t)]

def RunBatAlgorithm(function, limits, populationSize, nIterations, amplitudeInitial,
                 pulseEmissionRateInitial, alfaP, lambdaP, lowerFrequency, upperFrequency):
    nDimensions = len(limits)
    bats = []
    velocityInitial = [0 for _ in range(nDimensions)]
    frequencyInitial = 0

    k = min((populationSize//10),1)
    bestKBats = []

    bestsBatsForPlot = []

    # initialize the population of form random
    for i in range(populationSize):
        location = [limits[dimension][0] + (limits[dimension][1] - limits[dimension][0]) * np.random.uniform(0, 1) for
                    dimension in range(nDimensions)]
        bats.append(Bat(amplitudeInitial, pulseEmissionRateInitial, frequencyInitial, velocityInitial, location,
                        function(location)))
        updateKBest(k,bats[-1],bestKBats)

    bestBat = copy.deepcopy(min(bats))

    for t in range(nIterations):
        aAverage = np.mean([bat.amplitude for bat in bats])

        for bat in bats:
            newBatLocation = copy.deepcopy(bat.location)

            bat.frequency = lowerFrequency + (upperFrequency - lowerFrequency) * np.random.uniform(0, 1)    # EQ(1)
            for d in range(nDimensions):
                bat.velocity[d] = bat.velocity[d] + (bat.location[d] - bestBat.location[d]) * bat.frequency # EQ(2)
                newBatLocation[d] = newBatLocation[d] + bat.velocity[d]                                     # EQ(3)
                newBatLocation[d] = adjustLimits(bat.location[d], d, limits)

            if np.random.uniform(0, 1) > bat.pulseEmissionRate:
                bestBatSelect = selectSomeGoodBat(bestKBats)
                for d in range(nDimensions):
                    newBatLocation[d] = bestBatSelect.location[d] + np.random.uniform(-1.0, 1.0) * aAverage
                    newBatLocation[d] = adjustLimits(newBatLocation[d], d, limits)

            possibleFitness = function(newBatLocation)

            # update or not the bat
            if (possibleFitness < bat.fitness) and (np.random.uniform(0, 1) < bat.amplitude):
                bat.location = copy.deepcopy(newBatLocation)
                bat.fitness = possibleFitness
                bat.pulseEmissionRate = pulseEmissionRateInitial * (1 - exp(-lambdaP * t))
                bat.amplitude = bat.amplitude * alfaP
                updateKBest(k,bat,bestKBats)

            # update the best bat
            if bat.fitness < bestBat.fitness:
                bestBat = copy.deepcopy(bat)

        # storange the value of the best bat for future plot in main
        bestsBatsForPlot.append(bestBat.fitness)

    return (bestBat.fitness, bestBat.location,bestsBatsForPlot)