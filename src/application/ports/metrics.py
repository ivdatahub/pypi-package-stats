from abc import ABC, abstractmethod


class MetricsPort(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def increment(self, metric_name: str, tags: list, value: int = 1) -> None:
        pass
