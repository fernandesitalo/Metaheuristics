# dep is 'deposito'
# memo is matriz of dynamic Programming
import math



def dynamicProgrammingIterativeN2(nCities, sequence, capacity, travelCost, demand, dep):
    # make matrix of dynamic programming
    memo = [ [(travelCost[dep][sequence[0]] if i >= demand[sequence[0]] else math.inf) for i in range(capacity + 2)] ,
             [math.inf for _ in range(capacity + 2)]]
    linha = 0
    for idx in range(1, nCities - 1):
        for cap in range(capacity + 1):
            pd1, pd2 = math.inf, math.inf
            nextCity = sequence[idx - 1]
            curCity = sequence[idx]
            if cap >= demand[curCity]:
                pd1 = memo[linha][cap - demand[curCity]] + travelCost[curCity][nextCity]
                pd2 = memo[linha][capacity] + travelCost[curCity][dep] + travelCost[dep][nextCity]
            memo[not(linha)][cap] = min(pd1, pd2)
        linha = not(linha)

    # print(memo[N_cidades-2])
    # minimum = min([memo[N_cidades - 2][i] for i in range(capacity + 1)])
    # assert (minimum == memo[N_cidades-2][capacity])
    return memo[linha][capacity] + travelCost[sequence[nCities - 2]][dep]

# def pd2(idx, cap):
#     global N_cidades,sequence,memo,capacity,custo_viagem,a
#     if idx == N_cidades - 2:
#         if cap + a[sequence[idx]] <= capacity:
#             return custo_viagem[sequence[idx]][dep]
#         else:
#             return 123456789
#     if memo[idx][cap] != -1:
#         return memo[idx][cap]
#     A,B = 123456789,123456789
#     if cap + a[sequence[idx]] <= capacity:
#         A = pd2(idx + 1, cap + a[sequence[idx]]) + custo_viagem[sequence[idx]][sequence[idx + 1]]
#         B = pd2(idx + 1, 0) + custo_viagem[sequence[idx]][dep] + custo_viagem[dep][sequence[idx + 1]]
#     memo[idx][cap] = min(A,B)
#     return memo[idx][cap]


# def pd(idx, cap):
#
#     if idx == N_cidades - 2:
#         if cap >= a[sequence[idx]]:
#             return custo_viagem[sequence[idx]][dep]
#         else:
#             return 123456789
#
#     if memo[idx][cap] != -1:
#         return memo[idx][cap]
#
#     A,B = 123456789,123456789
#
#     if cap >= a[sequence[idx]]:
#         A = pd(idx + 1, cap - a[sequence[idx]]) + custo_viagem[sequence[idx]][sequence[idx + 1]]
#         B = pd(idx + 1, capacity) + custo_viagem[sequence[idx]][dep] + custo_viagem[dep][sequence[idx + 1]]
#
#     memo[idx][cap] = min(A,B)
#
#     return memo[idx][cap]


#
# def calc_cost2(p):  # p is permutation
#     cost, i = 0, 0
#     while len(p) > i:
#         cargaAtual = a[i]
#         cost = cost + custo_viagem[dep][p[i]]  # saida do deposito
#         print('-----------')
#         print(p[i])
#         while (len(p) > i + 1) and (cargaAtual + a[i + 1] <= capacity):
#             print(p[i + 1])
#             cargaAtual = cargaAtual + a[i + 1]
#             cost = cost + custo_viagem[p[i]][p[i + 1]]  # entre clientes
#             i = i + 1
#         cost = cost + custo_viagem[p[i]][dep]  # volta para o deposito
#         i = i + 1
#     return cost


# def calc_cost(p):  # p is permutation
#     cost, i = 0, 0
#     while len(p) > i:
#         cargaAtual = a[i]
#         cost = cost + custo_viagem[dep][p[i]]  # saida do deposito
#         while (len(p) > i + 1) and (cargaAtual + a[i + 1] <= capacity):
#             cargaAtual = cargaAtual + a[i + 1]
#             cost = cost + custo_viagem[p[i]][p[i + 1]]  # entre clientes
#             i = i + 1
#         cost = cost + custo_viagem[p[i]][dep]  # volta para o deposito
#         i = i + 1
#     return cost