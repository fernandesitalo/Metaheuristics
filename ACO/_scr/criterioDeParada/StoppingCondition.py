from abc import ABC, abstractmethod


class StoppingCondition(ABC):
    def __bool__(self):
        return self.finished()

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def finished(self) -> bool:
        pass

    @abstractmethod
    def update(self, improved: bool) -> None:
        pass

    @abstractmethod
    def timing(self) -> float:
        pass
