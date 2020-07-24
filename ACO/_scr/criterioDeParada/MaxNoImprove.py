from _scr.criterioDeParada.StoppingCondition import StoppingCondition


class MaxNoImprove(StoppingCondition):
    def __init__(self, max_no_improve: int):
        self.counter = None
        self.phi = None
        self.max_no_improve = max_no_improve

    def start(self) -> None:
        self.counter = 0
        self.phi = 0

    def finished(self):
        return self.counter >= self.max_no_improve

    def update(self, improved: bool):
        if improved:
            self.counter = 0
        else:
            self.counter += 1

    def timing(self) -> float:
        phi = self.phi * .99
        self.phi = phi + (1 - phi) * (self.counter / self.max_no_improve)
        return self.phi
