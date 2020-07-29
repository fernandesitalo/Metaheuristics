from math import sqrt


class Cvrp:
    def __init__(self, number_of_clients, capacity, demand, locations):
        assert number_of_clients >= 2, "number of clients = {} < 2".format(number_of_clients)
        assert len(locations) == number_of_clients + 1, "Missing node location"
        assert len(demand) == number_of_clients + 1, "Missing demand"
        assert min(demand[1:]) > 0, "Client has demand = {}!".format(min(demand))
        assert max(demand) <= capacity, "Found demand ({}) > capacity ({})".format(max(demand), capacity)
        assert demand[0] == 0, "Depot must have demand = 0, but was {}".format(demand[0])

        self.__number_of_clients = number_of_clients
        self.__capacity = capacity
        self.__demand = demand
        self.__locations = locations

    def dist_(self, u, v):
        diff = lambda i: self.__locations[u][i] - self.__locations[v][i]
        a = diff(0)
        b = diff(1)
        return int(sqrt(a * a + b * b) + 0.5)

    def get_demand(self, u):
        return self.__demand[u]

    def get_n(self):
        return self.__number_of_clients

    def get_capacity(self):
        return self.__capacity


    def get_all_demands(self):
        return self.__demand


def read(filename):
    with open(filename) as file:
        content = [x.strip().split() for x in file.readlines()]

    c = content.index(["NODE_COORD_SECTION"])
    d = content.index(["DEMAND_SECTION"])

    number_of_clients = next(int(x[2]) - 1 for x in content if x[0] == "DIMENSION")
    capacity = next(int(x[2]) for x in content if x[0] == "CAPACITY")
    demand = [int(x[1]) for x in content[d + 1: d + number_of_clients + 2]]
    locations = [(int(x[1]), int(x[2])) for x in content[c + 1: c + number_of_clients + 2]]

    # print("====> {} ".format(len(locations)))

    return Cvrp(number_of_clients, capacity, demand, locations)


def read2(filename):
    with open(filename) as reader:
        content = [x.strip().split() for x in reader.readlines()]

    n, c = map(int, content[0])
    demand = list(map(int, content[1]))
    locations = list(tuple(map(int, x)) for x in content[2:])
    # noinspection PyTypeChecker
    return Cvrp(n - 1, c, demand, locations)
