import random
import math

N_cidades = None# quantidade de cidades que o caxeiro tera de viajar
custo_viagem = []# matriz de custo do grafo completo


def calc_cost(permutacao):
	cost = custo_viagem[permutacao[N_cidades-1]][permutacao[0]]
	for i in range(1,N_cidades):
		cost += custo_viagem[permutacao[i-1]][permutacao[i]]
	return cost

class SA(object):
  temperatura_atual = None
  temperatura_final = None
  alfa = None
  solucao_atual = None
  melhor_solucao = None
  numero_iter = None

  def __init__(self,temperatura_inicial,temperatura_final,alfa,numero_iter,solucao_inicial = None):
    self.temperatura_atual = temperatura_inicial# inicializacao
    self.temperatura_final = temperatura_final# inicializacao
    self.alfa = alfa# inicializacao
    self.numero_iter = numero_iter# inicializacao
  
    if solucao_inicial is None:# gera uma solucao inicial qualquer
      aux = list(range(N_cidades))
      random.shuffle(aux)
      self.solucao_atual = aux
    else:
      self.solucao_atual = solucao_inicial
    self.melhor_solucao = self.solucao_atual# inicializacao
    custo_atual = calc_cost(self.solucao_atual) #inicializacao
    melhor_custo = custo_atual# inicializacao
    #~ print("CUSTO SOLUCAO INICIAL:",melhor_custo)
    #~ print(self.melhor_solucao)
    
    while (self.temperatura_atual > self.temperatura_final):
      for i in range(numero_iter):
        solucao_vizinha = self.move()# move a solucao atual para uma solucao vizinha
        custo_vizinha = calc_cost(solucao_vizinha)# calcula o custo da solucao vizinha

        if custo_atual >= custo_vizinha:# atualiza a solucao atual
          self.solucao_atual = solucao_vizinha
          custo_atual = custo_vizinha
          if(melhor_custo > custo_atual):# atualiza melhor solucao
            melhor_custo = custo_atual
            self.melhor_solucao = self.solucao_atual
        else:
          prob_aceitacao = math.exp(-(custo_vizinha - custo_atual)/self.temperatura_atual)# calculo da probabilidade de aceitacao
          if prob_aceitacao > random.random():# aleatoriamente pode pegar esse estado ou nao (que pode ou nao levar para uma solucao melhor)
            self.solucao_atual = solucao_vizinha
            custo_atual = custo_vizinha
      self.temperatura_atual *= self.alfa# calcula nova temperatura
      #~ print ("MELHOR ATUAL: ", melhor_custo)
      
  def move(self):
    L = self.solucao_atual.copy()
    cidade1 = random.randint(0,N_cidades-1)#pega aleatiro de 0 ate N_cidade-1
    cidade2 = random.randint(0,N_cidades-1)#pega aleatiro de 0 ate N_cidade-1
    a = L[cidade1]
    b = L[cidade2]
    L[cidade1] = b
    L[cidade2] = a
    return L
    
  def getSolucao(self):
    return self.melhor_solucao


def scan_with_points():
  for i in range(N_cidades):
    lixo,xx,yy = map(int,myfile.readline().split())
    x.append(xx)
    y.append(yy)
  for i in range(N_cidades):
    for j in range(i,N_cidades):
      if i == j:
        custo_viagem[i][j] = float("inf")
      else:
        custo_viagem[i][j] = custo_viagem[j][i] = math.sqrt((x[i]-x[j])*(x[i]-x[j]) + (y[i]-y[j])*(y[i]-y[j]))


def scan_matrix():
  for i in range(N_cidades):
      distancias = list(map(int,myfile.readline().split(' ')))
      for j in range(N_cidades):
        custo_viagem[i][j] = distancias[j]
        if i == j:
            custo_viagem[i][j] = float("inf")
        

if __name__ == '__main__':
  
  with open("bays.in", "r") as myfile:###########
    N_cidades = int(myfile.readline())
    custo_viagem = [[0 for x in range(N_cidades)] for y in range(N_cidades)]
    
    scan_matrix()

    L = [0,27,5,11,8,4,25,28,2,1,19,9,3,14,17,16,13,21,10,18,24,6,22,26,7,23,15,12,20]
    print("TOUR OTIMO: ",calc_cost(L))
    
    ct = 1
    while (True):
      aux = SA(10000000000000,10,0.991109,100)
      #~ print(aux.getSolucao())
      print("TOUR HEURISTICO ",ct,"# ",calc_cost(aux.getSolucao()))
      ct += 1
  myfile.close() ###########################

