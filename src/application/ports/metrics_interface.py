from abc import ABC, abstractmethod
from datetime import datetime


class MetricsPort(ABC):
    def __init__(
        self,
        metric_name: str,
        tags: list,
        value: int,
        timestamp: float,
        is_historical_metrics: bool,
    ):
        pass

    @abstractmethod
    def increment(self) -> None:
        pass
