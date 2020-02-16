from random import random,choice, randint
from math import sin,pi

class ga(object):
    populacao = 100
    lista_cromossomos = []
    geracoes = 20
    taxa_mutacao = 0.1
    taxa_cruzamento = 0.7


    def __init__(self):
        self.cria_populacao()

        for i in range(self.geracoes):
            for _ in range(int(self.populacao * self.taxa_mutacao)):
                self.mutacao()
            for _ in range(int(self.populacao * self.taxa_cruzamento)):
                self.cruzamento()
            self.classificacao()
            self.elitismo()

        # impressao
        #for cromo in self.lista_cromossomos:
         #   print(cromo.valor_objetivo)

        print("tamanho da populacao: ",len(self.lista_cromossomos))
        print(self.lista_cromossomos[0].valor_real)
        print(self.lista_cromossomos[0].valor_ajustado)
        print(self.lista_cromossomos[0].valor_objetivo)

    def cria_populacao(self):
        for i in range(self.populacao):
            self.lista_cromossomos.append(Cromossomo(None))

    def mutacao(self):
        mutado = self.lista_cromossomos[randint(0,self.populacao)]
        pos = randint(0,19)
        mutado.bits[pos] = 1 if (mutado.bits[pos] == 0) else 0
        novo = Cromossomo(mutado.bits)
        self.lista_cromossomos.append(novo)

    def cruzamento(self):
        pai1 = self.lista_cromossomos[randint(0,self.populacao-1)]
        pai2 = self.lista_cromossomos[randint(0, self.populacao - 1)]
        pos = randint(0, 19)

        filho1 = []
        filho2 = []

        for i in range(20):
            if pos >= i:
                filho1.append(pai1.bits[i])
                filho2.append(pai2.bits[i])
            else:
                filho1.append(pai2.bits[i])
                filho2.append(pai1.bits[i])

     #  print("pos   :",pos)
     #   print("pai1  : ", pai1.bits)
     #   print("pai2  : ", pai2.bits)
     #   print("filho1: ",filho1)
     #   print()

        self.lista_cromossomos.append(Cromossomo(filho1))
        self.lista_cromossomos.append(Cromossomo(filho2))

    def classificacao(self):
        self.lista_cromossomos = sorted(self.lista_cromossomos,key = Cromossomo.get_valor_objetivo,reverse = False)

    def elitismo(self):
        for i in range(self.populacao,len(self.lista_cromossomos)):
            del self.lista_cromossomos[-1]


class Cromossomo(object):
    bits = []
    valor_real = None
    valor_ajustado = None
    valor_objetivo = None

    def __init__(self, bits):
        if bits is None:
            self.bits = self.gerar_bits()
        else:
            self.bits = bits
        self.valor_real = self.convercao_decimal(self.bits)
        self.valor_ajustado = self.valor_ajustado(self.valor_real)
        self.valor_objetivo = self.funcao(self.valor_ajustado)

    def gerar_bits(self):
        aux = []
        for i in range(20):
            aux.append(1 if random() > 0.5 else 0)
        return aux

    def convercao_decimal(self, dig):
        num = 0
        for i in range(20):
           num += dig[i] * (2**(20-i-1))
        return num

    def valor_ajustado(self,inteiro):
        limite_inferior = 0.5
        limite_superior = 2.5
        return limite_inferior + ( limite_superior - limite_inferior ) *(inteiro/((2**20) - 1))

    def funcao(self,x):
        #return x*sin(10*pi*x)+1
        return sin(10*pi*x)/(2*x) + (x-1)**4

    def get_valor_objetivo(self):
        return self.valor_objetivo

if __name__ == '__main__':
    a = ga()
