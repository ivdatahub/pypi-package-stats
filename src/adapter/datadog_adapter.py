## This is the adapter class for the DataDog
import time
from datetime import datetime, timedelta
import random

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries
from src.application.ports.metrics_interface import MetricsPort
from src.application.use_cases.get_secrets import GetSecretValueUseCase


class DataDogAPIAdapter(MetricsPort):
    def __init__(
        self,
        metric_name: str,
        tags: list,
        value: int,
        timestamp=datetime.now().timestamp(),
    ):
        self.metric_name = metric_name
        self.tags = tags
        self.value = value
        self.timestamp = timestamp

    def get_dd_api_key(self):
        return GetSecretValueUseCase(secret_id="datadog-pypi-package-stats").get()

    def get_dd_agent(self):
        return GetSecretValueUseCase(secret_id="datadog-agent-server-address").get()

    def increment(self):
        body = MetricPayload(
            series=[
                MetricSeries(
                    metric=self.metric_name,
                    type=MetricIntakeType.COUNT,
                    points=[
                        MetricPoint(
                            # """ Add historical timestamp here """
                            timestamp=int(self.timestamp),
                            # """ *********************** """
                            value=self.value,
                        ),
                    ],
                    tags=self.tags,
                ),
            ],
        )

        configuration = Configuration()
        configuration.api_key["apiKeyAuth"] = self.get_dd_api_key()
        with ApiClient(configuration) as api_client:
            api_instance = MetricsApi(api_client)
            response = api_instance.submit_metrics(body=body)

            if response.to_dict()["errors"]:
                raise Exception(response.to_dict()["errors"])

            return response
