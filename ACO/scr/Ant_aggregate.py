from scr.Ant import Ant


class Ant_aggregate(Ant):

    def __init__(self, alfa, beta, rho, cvrp):
        self.__rho = rho
        self.__alfa = alfa
        self.__beta = beta
        super().__init__(cvrp)

    def build_solution(self, pheromone, quality):
        super().build_solution(self.__alfa, self.__beta, pheromone, quality)

    def update_delta(self, delta):
        super().update_delta(delta)

    def get_fitness(self):
        return super(Ant_aggregate, self).get_fitness()

    def get_tour(self):
        return super(Ant_aggregate, self).get_tour()

    def _evaluate_fitness(self):
        return super(Ant_aggregate, self)._evaluate_fitness()

    def ranges_truck(self):
        return super(Ant_aggregate, self).ranges_truck()

    def get_rho(self):
        return self.__rho

    def update(self, delta):
        self.__rho += delta
        self.__alfa += delta
        self.__beta += delta