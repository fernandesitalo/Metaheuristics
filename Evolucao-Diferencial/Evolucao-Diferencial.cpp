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

typedef double lf;
typedef vector<lf> Vetor;

const lf pi = acos(-1.0);

mt19937 rng(chrono::high_resolution_clock::now().time_since_epoch().count());

Vetor cruzamentoBinomial(const Vetor& v, const Vetor& x, lf Pc){
  static uniform_real_distribution<lf> urd(0, 1);
  
  Vetor u(v.size());
  for(int i = 0; i < (int)u.size(); ++i)
		u[i] = (urd(rng) <= Pc ? v[i] : x[i]);
  
  return u;
}

Vetor ed(const function<lf(Vetor)> &funcao, const vector<pair<lf,lf>>& limites,
				 int maxIteracoes = 1000,
				 int Np = 100,
				 const function<Vetor(Vetor, Vetor, lf)> &cruzamento = cruzamentoBinomial,
				 lf Fp = 0.5,
				 lf Pc = 0.7){
  
  // população inicial
  vector<Vetor> populacao(Np, Vetor(limites.size()));
  for(int i = 0; i < (int)limites.size(); ++i){
    uniform_real_distribution<lf> urd(limites[i].first, limites[i].second);
    for(int j = 0; j < Np; ++j)
      populacao[j][i] = urd(rng);
  }

  uniform_int_distribution<int> uid(0, Np - 2);
  
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
        v[j] = min( max(populacao[x[0]][j] + Fp * (populacao[x[1]][j] - populacao[x[2]][j]), limites[j].first), limites[j].second);

      // cruzamento
      auto u = cruzamento(v, populacao[s], Pc);

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


int main(){
  Vetor ans = ed(easom, {{-1000,1000}, {-1000,1000}});
  cout << setprecision(12) << fixed;
  //*
  cout << easom(ans) << ": ";
  for(double x : ans)
    cout << ' ' << x;
  cout << '\n';
  //*/
  cout << "Tempo total: " << (double)clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
