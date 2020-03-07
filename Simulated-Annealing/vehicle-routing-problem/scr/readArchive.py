import math


def scan_with_points(myfile, nCities, travelCost, x, y):
    for i in range(nCities):
        lixo, xx, yy = map(int, myfile.readline().split())
        x.append(xx)
        y.append(yy)
    for i in range(nCities):
        for j in range(nCities):
            if i == j:
                travelCost[i][j] = math.inf
            else:
                travelCost[i][j] = int(math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) + 0.5)


def scan_matrix(myfile, nCities, travelCost):
    for i in range(nCities):
        distancias = list(map(int, myfile.readline().split(' ')))
        for j in range(nCities):
            travelCost[i][j] = distancias[j]
            if i == j:
                travelCost[i][j] = math.inf


def makeMatrix(myfile, nCities, travelCost, x, y):
    for i in range(nCities):
        for j in range(nCities):
            travelCost[i][j] = math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2)


def readDemands(myfile, nCities, demand):
    for i in range(nCities):
        lixo, dem = map(int, myfile.readline().split())
        demand.append(dem)


def readArchive(myfile):
    x = []
    y = []
    demand = []
    nCities = int(myfile.readline())
    capacity = int(myfile.readline())
    travelCost = [[0 for _ in range(nCities)] for _ in range(nCities)]
    scan_with_points(myfile, nCities, travelCost, x, y)
    readDemands(myfile, nCities, demand)
    dep = int(myfile.readline()) - 1
    return nCities,travelCost,capacity,x,y,demand,dep
