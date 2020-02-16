#include <bits/stdc++.h>
using namespace std;


const int maxn = 1e4; // tamanho maximo da mochila
const int maxi = 300; // tamanho maximo de itens

int memo[maxi][maxn];
int peso_item[maxi],valor_item[maxi];
int QTD_ITENS,CAP_MOCHILA;

int pd(int idx, int pesoAtual){

  // caso base
  if(idx == QTD_ITENS || pesoAtual == CAP_MOCHILA ) return 0;

  // memorização
  int &ref = memo[idx][pesoAtual];
  if(ref != -1) return ref;

  // pegar o item
  if(pesoAtual+ peso_item[idx] <= CAP_MOCHILA) // posso pegar?
    ref = pd(idx+1,pesoAtual+peso_item[idx])+valor_item[idx];

  // não pegar o item atual
  ref = max(ref,pd(idx+1,pesoAtual) );

  return ref;
}


int main(){
  //~ freopen("in","r",stdin);
  freopen("in","w",stdout);
  
  // variaveis globais mesmo
  //~ cin >> QTD_ITENS >> CAP_MOCHILA;
  QTD_ITENS = 50;
  CAP_MOCHILA = 1000;
  cout << QTD_ITENS << " " << CAP_MOCHILA << '\n';

  // leitura do valor e dos pegos de cada item
  for(int i = 0 ; i < QTD_ITENS ; ++i){
    //~ cin  >> valor_item[i] >> peso_item[i];
    valor_item[i] = rand()%1000;
    peso_item[i] = rand()%1000;
    cout << valor_item[i] << " " << peso_item[i] << '\n';
  }

  // limpa a matriz de memorizacao
  memset(memo,-1,sizeof memo);

  // resultado final
  cout << pd(0,0) << '\n';

  return 0;
}
