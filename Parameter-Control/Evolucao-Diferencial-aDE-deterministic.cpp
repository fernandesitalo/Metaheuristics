// artigo = An Adaptive Differential Evolution Algorithm
// ano = 2011

// bibliotecas
#include <cassert>
#include <cmath>
#include <algorithm>
#include <chrono>
#include <functional>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

#include <locale.h>
using namespace std;

// cabeçalhos
typedef double lf;
typedef vector<lf> Vetor;
const lf pi = acos(-1.0);
mt19937 rng(chrono::high_resolution_clock::now().time_since_epoch().count()); // rand
// uso das funcoes de distribuiçao real/inteira uniforme. Funçao pronta do C++


Vetor cruzamentoBinomial(const Vetor& v, const Vetor& x, lf Pc){
  static uniform_real_distribution<lf> urd(0, 1);
  Vetor u(v.size());
  for(int i = 0; i < (int)u.size(); ++i){
		u[i] = (urd(rng) <= Pc ? v[i] : x[i]);
	}
  return u;
}

Vetor ed(const function<lf(Vetor)> &funcao,
				 const vector<pair<lf,lf>>& limites,
				 int maxIteracoes, // numero de iteracoes, esse foi definido pelo usuario, eventualmente.
				 int Np,	// tamanho da população, tbm foi eventualmente escolhido pelo usuario
				 const function<Vetor(Vetor, Vetor, lf)> &cruzamento = cruzamentoBinomial){
	
	// distribuicao real para criaçao dos atributos individuais da populacao.
	uniform_real_distribution<lf> urd(0,1);
  lf Fp[Np],Pc[Np];
  for(int i = 0 ; i < Np ; ++i){
		Fp[i] = urd(rng);
		Pc[i] = urd(rng);
	}
	
  // criar população inicial
  vector<Vetor> populacao(Np, Vetor(limites.size()));
  for(int i = 0; i < (int)limites.size(); ++i){
    uniform_real_distribution<lf> urd(limites[i].first, limites[i].second); // distribuição real uniforme
    for(int j = 0; j < Np; ++j){
      populacao[j][i] = urd(rng);
		} 
  }
	
  uniform_int_distribution<int> uid(0, Np - 2); // distribuição inteira uniforme _ para selecionar os agentes
	
	auto melhor = populacao[0];
	lf melhorFp = Fp[0], melhorPc = Pc[0];
	
	//calcula fitness medio da geracao inicial
	lf Favg = 0;
	for(int i = 0 ; i < Np ; ++i){ 
		Favg += funcao(populacao[i]);
		if(funcao(populacao[i]) < funcao(melhor)){
			melhor = populacao[i];
			melhorFp = Fp[i];
			melhorPc = Pc[i];
		}
	}
	Favg /= Np;
	
  uniform_real_distribution<lf> urd1(0.1,1); 
  
  vector< vector<lf> > analise;
  
  for(int iteracoes = 0; iteracoes < maxIteracoes; ++iteracoes){
    for(int s = 0; s < Np; ++s){
			
      // escolhe alfa beta e gama
      int x[] = { uid(rng), uid(rng), uid(rng) };
      for(int &k : x)
        if(k >= s)
          ++k;

      // mutação
      Vetor v(limites.size());
      for(int j = 0; j < (int)limites.size(); ++j)
        v[j] = min( max(populacao[x[0]][j] + Fp[s] * (populacao[x[1]][j] - populacao[x[2]][j]), limites[j].first), limites[j].second);

      // cruzamento
      auto u = cruzamento(v, populacao[s], Pc[s]);
	
			// controle dos parametros deste individuo
			// agregado e deterministico ao mesmo tempo
			Fp[s] = Favg > funcao(u) ? Fp[s] : urd1(rng);
			Pc[s] = Favg > funcao(u) ? Pc[s] : urd(rng);
			
      // seleção
      if(funcao(u) < funcao(populacao[s])){
        populacao[s] = u;
        
        // atualiza o melhor
				if(funcao(populacao[s]) < funcao(melhor)){ 
					melhor = populacao[s];
					melhorFp = Fp[s];
					melhorPc = Pc[s];
				}
			}
    }
    
    vector<lf> aux;
    aux.push_back(funcao(melhor));
    aux.push_back(melhorFp);
    aux.push_back(melhorPc);
		analise.push_back(aux);
		
		// calcula fitness da geracao atual
		Favg = 0;
		for(int i = 0 ; i < Np ; ++i){ 
			Favg += funcao(populacao[i]);
		}
		Favg /= Np;
  }
  
 
	for(int idx = 0 ; idx < (int)analise[0].size() ; ++idx){
		if(idx == 0) cout << "funcao(melhor)\t";
		if(idx == 1) cout << "FP->melhor\t";
		if(idx == 2) cout << "PC->melhor\t";
		for(int iteracoes = 0 ; iteracoes < maxIteracoes ; ++iteracoes){		
			if(iteracoes) cout << '\t';
			cout << analise[iteracoes][idx];
		}
		cout <<'\n';
	}
    
  return melhor;
}


inline lf easom(const Vetor& x){
  return -cos(x[0]) * cos(x[1]) * exp(-pow(x[0] - pi, 2) - pow(x[1] - pi, 2));
}

inline lf rosenbrock(const Vetor& x){
	return (1 - x[0]) * (1 - x[0]) + 100 * (x[1] - x[0]) * (x[1] - x[0]); 
}


int main(){
  cout << setprecision(12) << fixed;
  freopen("out.txt","w",stdout);
  
  
  
  int numIter = 1000; // 
  int tamPop = 100; // 
  int execucoes = 100000; // 100.000
  
  for(int i = 1 ; i <= numIter ; ++i){
		cout << "\titeracao "<<i;
	}
	cout << '\n';
  
  for(int i = 0 ; i < execucoes ; ++i){
		//~ auto begin = clock();
		Vetor ans = ed(rosenbrock, {{-1000,100}, {-1000,1000}},numIter,tamPop);
		//~ cout << easom(ans) << ": ";
		//~ for(double x : ans){
			//~ cout << ' ' << x;
		//~ }
		//~ cout << '\n';
		
		//~ cout << "Tempo total: " << (double)clock() / CLOCKS_PER_SEC << "s\n";
	}
  return 0;
}
