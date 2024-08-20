from abc import ABC, abstractmethod


class MetricsPort(ABC):
    def __init__(self, metric_name: str, tags: list, value: int):
        pass

    @abstractmethod
    def increment(self) -> None:
        pass
