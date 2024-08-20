## This is the adapter class for the DataDog
import time
from datetime import datetime, timedelta
import random

import datadog
import datadog.api.metrics


from src.application.ports.metrics_interface import MetricsPort
from src.application.use_cases.get_secrets import GetSecretValueUseCase


class DataDogAPIAdapter(MetricsPort):
    def __init__(
        self,
        metric_name: str,
        tags: list,
        value: int,
        timestamp=datetime.now().timestamp(),
        is_historical_metrics: bool = False,
    ):
        self.metric_name = metric_name
        self.tags = tags
        self.value = value
        self.timestamp = timestamp

    def get_dd_api_key(self):
        return GetSecretValueUseCase(secret_id="datadog-pypi-package-stats").get()

    def increment(self):
        datadog.initialize(api_key=self.get_dd_api_key())

        metric_payload = [
            {
                "metric": self.metric_name,
                "type": "count",
                "points": [(datetime.now(), self.value)],
            }
        ]
        response = datadog.api.Metric.send(metric_payload)

        return response


DataDogAPIAdapter(
    metric_name="local_metric",
    tags=["env:test"],
    value=1,
).increment()
