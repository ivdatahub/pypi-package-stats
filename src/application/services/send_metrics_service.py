from src.application.ports.metrics_interface import MetricsPort


class SendMetricsService:
    def __init__(self, MetricsRepository: MetricsPort):
        self.metrics_repository = MetricsRepository

    def send(self):
        self.metrics_repository.increment()
