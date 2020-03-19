import math

from scr.min_queue import MinQueue


def optimal_split(cvrp, permutation):
    tour = permutation
    dist = cvrp.distance
    n = cvrp.number_of_clients
    demand = cvrp.demand
    capacity = cvrp.capacity

    distances = [dist(tour[i], tour[i + 1]) for i in range(n - 1)]
    split = [dist(tour[i], 0) + dist(0, tour[i + 1]) - distances[i] for i in range(n - 1)]
    path = [None] * n
    used = 0
    best = None
    i = 0
    queue = MinQueue()
    queue.push((0, -1))
    for j in range(n):
        used += demand[tour[j]]
        while used > capacity:
            used -= demand[tour[i]]
            i += 1
            queue.pop()
        assert i <= j
        best, path[j] = queue.min()
        if j < n - 1:
            queue.push((split[j] + best, j))
    fitness = best + dist(0, tour[0]) + sum(distances) + dist(tour[-1], 0)
    return fitness


def optimal_split_N2(nCities, sequence, capacity, travelCost, demand, dep):
    """
    Esta solução foi feita inicialmente para teste. Está legada.
    """
    memo = [[(travelCost[dep][sequence[0]] if i >= demand[sequence[0]] else math.inf) for i in range(capacity + 2)],
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
            memo[not (linha)][cap] = min(pd1, pd2)
        linha = not (linha)
    return memo[linha][capacity] + travelCost[sequence[nCities - 2]][dep]
