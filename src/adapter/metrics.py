import datadog
from src.application.ports.metrics import MetricsPort


class DataDogAdapter(MetricsPort):
    def __init__(self, client):
        self.options = {"statsd_host": "35.226.251.154", "statsd_port": 8125}
        datadog.initialize(**self.options)

    def increment(self, metric_name: str, tags: list, value: int = 1) -> None:
        datadog.statsd.increment(metric_name, tags=tags, value=value)
