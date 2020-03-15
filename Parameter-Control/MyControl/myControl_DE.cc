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


lf rand_(){
	return ((double) rng() / (RAND_MAX));	
}

vector<Vetor> criaPopInicial(int &Np, const vector<pair<lf,lf>>& limites){
	vector<Vetor> populacao(Np, Vetor(limites.size()));
  for(int i = 0; i < (int)limites.size(); ++i){
    uniform_real_distribution<lf> urd(limites[i].first, limites[i].second);
    for(int j = 0; j < Np; ++j)
      populacao[j][i] = urd(rng);
  }
  return populacao;
}

Vetor mutacao(lf &Fp, const vector<pair<lf,lf>>& limites, vector<Vetor> &populacao,int x[]){
	Vetor v(limites.size());
	for(int j = 0; j < (int)limites.size(); ++j)
		v[j] = min( max(populacao[x[0]][j] + Fp * (populacao[x[1]][j] - populacao[x[2]][j]), limites[j].first), limites[j].second);
	return v;
}

void iteracao(int &Np, lf &Pc, lf& Fp, const vector<pair<lf,lf>>& limites, vector<Vetor>& populacao, const function<Vetor(Vetor, Vetor, lf)> &cruzamento,const function<lf(Vetor)> &funcao){
	uniform_int_distribution<int> uid(0, Np - 2);
	for(int s = 0; s < Np; ++s){
		int x[] = { uid(rng), uid(rng), uid(rng) };
		//~ for(int &k : x)
			//~ if(k >= s)
				//~ ++k;
		Vetor v = mutacao(Fp,limites,populacao, x);
		auto u = cruzamento(v, populacao[s], Pc);
		
		if(funcao(u) < funcao(populacao[s])) populacao[s] = u;
	}
}


lf media(vector<Vetor> populacao, const function<lf(Vetor)> &funcao){
	lf sum = 0;
	for(int i = 0 ; i < (int)populacao.size() ; ++i)
		sum += funcao(populacao[i]);
	sum /= populacao.size();
	return sum;
}

lf ajustaFp(lf Fp){ 
	if(Fp > 1) return 1;
	if(Fp < 0) return 0;
	return Fp;
}

lf ajustaPc(lf Pc){
	if(Pc > 1) return 1;
	if(Pc < 0) return 0;
	return Pc;
}


Vetor ed(const function<lf(Vetor)> &funcao, const vector<pair<lf,lf>>& limites,
				 int maxIteracoes = 100,
				 int Np = 50,
				 const function<Vetor(Vetor, Vetor, lf)> &cruzamento = cruzamentoBinomial,
				 lf Fp = 0.5,
				 lf Pc = 0.7){

  vector<Vetor> populacao = criaPopInicial(Np, limites);
  
  lf mediaAnterior = media(populacao,funcao);
  
  lf delta = 0.5;	// variação inicial
  lf alfa = 0.9; // alfa de decaimento
  
  for(int iteracoes = 0; iteracoes < maxIteracoes; ++iteracoes){
    iteracao(Np,Pc,Fp,limites,populacao,cruzamento,funcao);  
		
		lf mediaAtual = media(populacao,funcao);
		
    if(mediaAtual > mediaAnterior){ // criterio de atualização dos parametros
			lf var[] = { delta,-delta,0,rand_(),-rand_()};
			lf melhorConf = 0;
			vector<lf> conf = {Fp,Pc};
			vector<Vetor> melhorPop;
			
			for(int i = 0 ; i < 5 ; ++i){
					for( int j = 0 ; j < 5 ; ++j){
						
						lf newFp = ajustaFp(Fp + var[i]);
						lf newPc = ajustaPc(Pc + var[j]);
						
						vector<Vetor> pop = populacao;
						
						for(int k = 0 ; k < 10 ; ++k){
							iteracao(Np,newPc,newFp,limites,pop,cruzamento,funcao);  
						}
						
						lf mediaPop = media(pop,funcao);
						
						if(mediaPop < melhorConf){
							conf[0] = newFp;
							conf[1] = newPc;
							melhorPop = pop;
							melhorConf = mediaPop;
						}
					}
			}		
			delta *= alfa;
			// atualização dos parametros
			populacao = melhorPop;
			Fp = conf[0];
			Pc = conf[1];
		}
		mediaAnterior = mediaAtual;
  }

  auto melhor = populacao[0];
  for(auto &p : populacao)
    if(funcao(p) < funcao(melhor))
      melhor = p;
      
  return melhor;
}


inline lf Easom(const Vetor& x){
  return -cos(x[0]) * cos(x[1]) * exp(-pow(x[0] - pi, 2) - pow(x[1] - pi, 2));
}


inline lf Rosenbrock(const Vetor& x){
	lf ret = 0;
	for(int i = 0 ; i < (int)x.size()-1 ; ++i)
		ret += (100 * (x[i]*x[i] - x[i+1]) * (x[i]*x[i] - x[i+1]) + (1-x[i])*(1-x[i]));	
	return ret;
}


inline lf Ackley(const Vetor& x){
	lf x2 = 0;
	lf cos2pix = 0;
	for(int i = 0 ; i < (int)x.size() ; ++i){
		x2 += (x[i]*x[i]);
		cos2pix += (cos(2*pi*x[i]));
	}
	lf ret = -20 * exp(-0.2 * sqrt(x2/(lf)x.size())) - exp(cos2pix/(lf)x.size()) + 20 + exp(1);
	return ret;
}

inline lf Rastrigin(const Vetor& x){
	lf ret = 10 * x.size();
	for (int i = 0 ; i < (int)x.size(); ++i){
			ret += (x[i]*x[i] - 10*cos(2*pi*x[i]));
	}
	return ret;
}


lf media(vector<lf> a){
	lf sum = 0;
	for(int i = 0 ; i < (int) a.size() ; ++i){
		sum += a[i];
	}
	return sum/(lf)a.size();
}


lf DP(vector<lf> a){
	lf m = media(a);
	lf dp = 0;
	for(int i = 0 ; i < (int) a.size() ; ++i){
		dp += (a[i]-m)*(a[i]-m);
	}
	dp /= a.size();
	dp = sqrt(dp);
	return dp;
}

void run(const function<lf(Vetor)> &funcao, lf limInf, lf limSup){
	vector<lf> v;
	lf best = 1e50;
	for(int t = 0 ; t < 1000 ; ++t){
		Vetor ans = ed(funcao, {{limInf,limSup}, {limInf,limSup},{limInf,limSup}, {limInf,limSup}, {limInf,limSup}});
		v.push_back(funcao(ans));
		if(best > funcao(ans)){
				best = funcao(ans);
		}
	}
	cout << best << "\t&\t" << media(v) << "\t&\t" << DP(v) << "\t\\\\" << '\n';
}

int main(){

	cout << setiosflags(ios::scientific);
	run(Rastrigin,-5.12,5.12);
	run(Rosenbrock,-2.048,2.048);
	run(Easom,-100,100);
	run(Ackley,-32,32);
	
  return 0;
}
