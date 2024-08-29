from abc import ABC, abstractmethod
from datetime import datetime


class MetricsPort(ABC):
    def __init__(self, metric_name: str):
        pass

    @abstractmethod
    def increment(
        self,
        tags: list,
        value: int,
        timestamp: float,
    ) -> None:
        pass
