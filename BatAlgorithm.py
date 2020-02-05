# run the algorithm in python 3!
# author: Ítalo Fernandes Gonçalves, italofernandes.fg@gmail.com
# the last update in: 04/02/2020 
# for install the pip3: sudo apt install python3-pip
# for install the package numpy: pip3 install numpy

from random import random,randint
from math import pi,cos,exp
import numpy as np
np.random.seed(100)

class BatAlgorithm():
  def __init__(self, nDimensions, populationSize, nIterations, pulseEmissionRateInitial, Alfa, Lambda ,lowerFrequency, upperFrequency, lowerLimit, upperLimit, targetFunction):
    self.nDimensions = nDimensions
    self.populationSize = populationSize
    self.nIterations = nIterations
    self.Alfa = Alfa
    self.Lambda = Lambda
    self.lowerFrequency = lowerFrequency
    self.upperFrequency = upperFrequency
    self.lowerLimitValue = lowerLimit 
    self.upperLimitValue = upperLimit        
    self.targetFunction = targetFunction       
    self.pulseEmissionRateInitial = pulseEmissionRateInitial
    # convenções 
    self.amplitude = [0.95 for i in range(self.populationSize)]
    self.pulseEmissionRate = [pulseEmissionRateInitial for i in range(self.populationSize)]
    
    # can be different limits for each dimension... change the code for this after
    self.lowerLimit = [0 for dimension in range(self.nDimensions)]
    self.upperLimit = [0 for dimension in range(self.nDimensions)]
    
    # the population of bats
    self.frequency = [0.0] * self.populationSize
    self.velocity = [[0.0 for dimension in range(self.nDimensions)] for j in range(self.populationSize)]
    self.bats = [[0.0 for dimension in range(self.nDimensions)] for bat in range(self.populationSize)]
    self.fitness = [0.0] * self.populationSize
    self.bestBat = [0] * self.nDimensions
    self.bestFitness = 0.0
    self.aAverage = None

  def updateBestBat(self):# define bestBat morcego 
    indexBestBat = 0
    for bat in range(self.populationSize):
      if self.fitness[bat] < self.fitness[indexBestBat]:
        indexBestBat = bat
    for dimension in range(self.nDimensions):
      self.bestBat[dimension] = self.bats[indexBestBat][dimension]
    self.bestFitness = self.fitness[indexBestBat]

  def init(self):
    for dimension in range(self.nDimensions): # same limits for each variable
      self.lowerLimit[dimension] = self.lowerLimitValue
      self.upperLimit[dimension] = self.upperLimitValue
    for bat in range(self.populationSize):
      self.frequency[bat] = 0
      for dimension in range(self.nDimensions):
        self.velocity[bat][dimension] = 0.0 # velocity equal zero for all bats
        self.bats[bat][dimension] = self.lowerLimit[dimension] + (self.upperLimit[dimension] - self.lowerLimit[dimension]) * np.random.uniform(0,1) # atribui uma "frequencia aleatoria"
      self.fitness[bat] = self.targetFunction(self.nDimensions, self.bats[bat])
    self.updateBestBat()


  def adjustLimits(self, value, dimension):
    if value < self.lowerLimit[dimension]:
      value = self.lowerLimit[dimension]
    if value > self.upperLimit[dimension]:
      value = self.upperLimit[dimension]
    return value

  def runBatAlgorithm(self):
    # 'S' is the current solution 
    S = [[0.0 for dimension in range(self.nDimensions)] for bat in range(self.populationSize)]
    self.init()
    for iteration in range(self.nIterations):
      # get the average of the array amplitude
      self.aAverage = np.mean(self.amplitude) 

      for bat in range(self.populationSize):
        self.frequency[bat] = self.lowerFrequency + (self.upperFrequency - self.lowerFrequency) * np.random.uniform(0,1)                                # EQ (1)
        for dimension in range(self.nDimensions):
          self.velocity[bat][dimension] = self.velocity[bat][dimension] + (self.bats[bat][dimension] - self.bestBat[dimension]) * self.frequency[bat]   # EQ (2)
          S[bat][dimension] = self.bats[bat][dimension] + self.velocity[bat][dimension]                                                                 # EQ (3)
          S[bat][dimension] = self.adjustLimits(S[bat][dimension],dimension)

        # local search
        if np.random.uniform(0,1) > self.pulseEmissionRate[bat]:
          for dimension in range(self.nDimensions):
            S[bat][dimension] = self.bestBat[dimension] + np.random.uniform(-1.0,1.0) * self.aAverage
            S[bat][dimension] = self.adjustLimits(S[bat][dimension],dimension)

        # get the fitness of the bat in this position
        possibleFitness = self.targetFunction(self.nDimensions, S[bat])

        # update or not the bat
        if (possibleFitness < self.fitness[bat]) and (np.random.uniform(0,1) < self.amplitude[bat]):
          for dimension in range(self.nDimensions):
            self.bats[bat][dimension] = S[bat][dimension]
          # update the fitness
          self.fitness[bat] = possibleFitness  
          # update the pulse emission rate                
          self.pulseEmissionRate[bat] = self.pulseEmissionRateInitial * ( 1 - exp(-self.Lambda * iteration) )
          # update the amplitude
          self.amplitude[bat] = self.amplitude[bat] * self.Alfa 
        
        # update the with a best bat ....
        if self.fitness[bat] < self.bestFitness:
          for dimension in range(self.nDimensions):
            self.bestBat[dimension] = S[bat][dimension]
          self.bestFitness = self.fitness[bat]

def functionTest(nDimensions,x):
  return -cos(x[0])*cos(x[1])*exp(-(x[0]-pi)**2 -(x[1]-pi)**2)

if __name__ == '__main__':
  nDimensions = 2
  populationSize = 1000
  nIterations = 200
  pulseEmissionRateInitial = 0.3
  Alfa = 0.9999
  Lambda = 0.001
  lowerFrequency = 0
  upperFrequency = 10000
  lowerLimit = -100
  upperLimit = +100
  targetFunction = functionTest
  
  while (True) :
    batAlgorithm = BatAlgorithm( nDimensions,
                        populationSize,
                        nIterations,
                        pulseEmissionRateInitial,
                        Alfa,
                        Lambda,
                        lowerFrequency,
                        upperFrequency,
                        lowerLimit,
                          upperLimit,
                        targetFunction)
    batAlgorithm.runBatAlgorithm()
    
    print (batAlgorithm.bestFitness,batAlgorithm.bestBat)

