from random import random,choice, randint
from math import sin,pi

numero_itens = None
valor_item = [] # colocar os valores de cada item
peso_item =  [] # colocar os pesos de cada item
peso_limite = None

class GA(object):
  tamanho_populacao = None
  populacao = []  # lista de mochilas
  geracoes = None
  taxa_mutacao = None
  taxa_cruzamento = None

  # colocar parametros depois ... populacao,taxas ....
  def __init__(self,tamanho_populacao,numero_geracoes,taxa_mutacao,taxa_cruzamento):
    self.tamanho_populacao = tamanho_populacao
    self.geracoes = numero_geracoes
    self.taxa_cruzamento = taxa_cruzamento
    self.taxa_mutacao = taxa_mutacao
    self.cria_populacao() # gera a populacao inicial
    for i in range(self.geracoes): # realizar todas geracoes desta populacao
      for _ in range(int(self.tamanho_populacao*self.taxa_mutacao)):    # aplicacao da mutacao - variabilidade genetica
        self.mutacao()
      for _ in (range(int(self.tamanho_populacao*self.taxa_cruzamento))):  # aplicacao do cruzamento - variabilidade genetica
        self.cruzamento()
      self.classificacao()  # classifica os individuos desta populacao
      self.elitismo()     # deixa somente os melhores da populacao gerada

  def cria_populacao(self):
    for i in range(self.tamanho_populacao):
      self.populacao.append(mochila(None))
      #  print(self.populacao[-1].get_bits(), self.populacao[-1].get_valor() , "   " , self.populacao[-1].get_peso())

  def mutacao(self):
    qual = randint(0,self.tamanho_populacao-1)
    bits_mutado = self.populacao[qual].get_bits()
    pos = randint(0,numero_itens-1)
    bits_mutado[pos] = (1 if bits_mutado[pos] == 0 else 0)
    self.populacao.append(mochila(bits_mutado))

  def cruzamento(self):
    pai1 = self.populacao[randint(0,self.tamanho_populacao-1)]
    pai2 = self.populacao[randint(0,self.tamanho_populacao-1)]
    pos = randint(1,numero_itens-1)
    filho1 = []
    filho2 = []
    for i in range(numero_itens):
      if pos >= i:
        filho1.append(pai1.bits[i])
        filho2.append(pai2.bits[i])
      else:
        filho1.append(pai2.bits[i])
        filho2.append(pai1.bits[i])
    self.populacao.append(mochila(filho1))
    self.populacao.append(mochila(filho2))

  def classificacao(self):
  # criar uma lista com as mochilas validas isto eh, as que tem peso menor ou igual a do permitido
  # ordenara lista de mochilas validas pelo valor
  # adcionar o resto no final, tbm ordenada pelo valores mais proximos do permitido (sort crescente)
    validos = []
    invalidos = []
    for i in range(len(self.populacao)):
      if self.populacao[i].get_peso() > peso_limite:
        invalidos.append(self.populacao[i])
      else:
        validos.append(self.populacao[i])
    validos = sorted(validos,key = mochila.get_valor,reverse = True)
    invalidos = sorted(invalidos,key = mochila.get_valor,reverse = False)
    self.populacao = validos + invalidos

  def elitismo(self):
    for i in range(self.tamanho_populacao,len(self.populacao)):
      del self.populacao[-1] # deleta a ultima posicao da lista populacao

  def get_populacao(self):
    return self.populacao

# populacao de mochilas
class mochila(object):
  bits = []
  valor_mochila = None
  peso_mochila = None

  def __init__(self, bits):
    if bits is None:
      self.bits = self.gerar_bits()
    else:
      self.bits = bits
    self.valor_mochila = self.calc_valor()
    self.peso_mochila = self.calc_peso()

  def calc_valor(self):
    valor = 0
    for i in range(numero_itens):
      if self.bits[i] == 1:
        valor = valor + valor_item[i]
    return valor

  def calc_peso(self):
    peso = 0
    for i in range(numero_itens):
      if self.bits[i] == 1:
        peso = peso + peso_item[i]
    return peso

  def gerar_bits(self): # vai gerar uma mochila com seu peso e seu valor
    aux = []
    for i in range(numero_itens):
      aux.append(1 if random() > 0.5 else 0)
    return aux

  def get_peso(self):
    return self.peso_mochila

  def get_bits(self):
    return self.bits.copy()

  def get_valor(self):
    return self.valor_mochila

if __name__ == '__main__':

  with open("in", "r") as myfile:###########
    numero_itens,peso_limite = map(int,myfile.readline().split(' '))
    for i in range(numero_itens):
      val,pes = map(int,myfile.readline().split(' '))
      valor_item.append(val)
      peso_item.append(pes)
    aux = GA(200,100,0.1,0.7)
    lista = aux.get_populacao()
    for i in range(1):
      print(lista[i].get_bits(), "  Valor: " , lista[i].get_valor(), "  Peso: ",lista[i].get_peso() )
  myfile.close() ###########################
