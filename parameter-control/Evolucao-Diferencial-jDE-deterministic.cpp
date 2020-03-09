// artigo = Self-Adapting Control Parameters in Differential Evolution: A Comparative Study on Numerical Benchmark Problems
// ano = 2006

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
				 int maxIteracoes = 1000,
				 int Np = 100,	// tamanho da população
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
	
	// limites inferior e superior do parametro Fp - escolhidos na literatura.
	lf Fu = 0.1,Fl = 0.9;
	lf t1 = 0.1,t2 = 0.1;


  uniform_int_distribution<int> uid(0, Np - 2); // distribuição inteira uniforme _ para selecionar os agentes
  uniform_real_distribution<lf> urd1(0.1,1); 
 
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


			// controle de parametros
    lf rand1 = urd1(rng),
       rand2 = urd1(rng),
       rand3 = urd(rng),
       rand4 = urd(rng);
    Fp[s] = (t1 > rand2) ? Fl + rand1*Fu : Fp[s];
    Pc[s] = (t2 > rand4) ? rand3 : Pc[s];
			
      // seleção
      if(funcao(u) < funcao(populacao[s]))
        populacao[s] = u;
    }
    
  }

	// seleciona a melhor
  auto melhor = populacao[0];
  for(auto &p : populacao)
    if(funcao(p) < funcao(melhor))
      melhor = p;
      
  return melhor;
}


inline lf easom(const Vetor& x){
  return -cos(x[0]) * cos(x[1]) * exp(-pow(x[0] - pi, 2) - pow(x[1] - pi, 2));
}

//~ rosenbrock = 
//~ (2 * [(-5, 10)], lambda x : sum(100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2 for i in range(len(x) - 1)))

inline lf rosenbrock(const Vetor& x){
	return (1 - x[0]) * (1 - x[0]) + 100 * (x[1] - x[0]) * (x[1] - x[0]); 
}


int main(){
  cout << setprecision(12) << fixed;
  
  Vetor ans = ed(rosenbrock, {{-100,100}, {-100,100}});
  
  cout << rosenbrock(ans) << ": ";
  for(double x : ans){
		cout << ' ' << x;
	}
  cout << '\n';
  
  cout << "Tempo total: " << (double)clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
