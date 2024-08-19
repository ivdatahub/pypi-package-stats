from abc import ABC, abstractmethod


class MetricsPort(ABC):
    @abstractmethod
    def increment(self, metric_name: str, tags: list, value: int) -> None:
        pass
