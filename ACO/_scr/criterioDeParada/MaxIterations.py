from _scr.criterioDeParada.StoppingCondition import StoppingCondition


class MaxIterations(StoppingCondition):
    def __init__(self, max_iterations: int):
        self.counter = 0
        self.max_iterations = max_iterations

    def start(self) -> None:
        self.counter = 0

    def finished(self):
        return self.counter >= self.max_iterations

    def update(self, improved: bool):
        self.counter += 1

    def timing(self) -> float:
        return self.counter / self.max_iterations
