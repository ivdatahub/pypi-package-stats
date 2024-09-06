from typing import Type
from src.application.ports.metrics_interface import MetricsPort


class SendMetricsService:
    def __init__(self, MetricsRepository: Type[MetricsPort]):
        self.metrics_repository = MetricsRepository

    def send(
        self,
        tags: list,
        value: int,
        timestamp: float,
    ):
        self.metrics_repository.increment(tags=tags, value=value, timestamp=timestamp)
