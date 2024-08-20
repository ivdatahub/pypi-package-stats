"""
Submit metrics returns "Payload accepted" response
"""
import time
from datetime import datetime, timedelta
import random
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries

from src.application.ports.metrics import MetricsPort


class DataDogAdapter(MetricsPort):
    def increment(self, metric_name: str, tags: list, value: int):
        body = MetricPayload(
            series=[
                MetricSeries(
                    metric=metric_name,
                    type=MetricIntakeType.COUNT,
                    points=[
                        MetricPoint(
                            # """ Add historical timestamp here """
                            timestamp=int(
                                (datetime.now() - timedelta(hours=24)).timestamp()
                            ),
                            # """ *********************** """
                            value=value,
                        ),
                    ],
                    resources=[
                        MetricResource(
                            name="dummyhost",
                            type="host",
                        ),
                    ],
                ),
            ],
        )

        configuration = Configuration()
        configuration.debug = True
        configuration.api_key["apiKeyAuth"] = "x"
        configuration.api_key["appKeyAuth"] = "y"
        with ApiClient(configuration) as api_client:
            api_instance = MetricsApi(api_client)
            response = api_instance.submit_metrics(body=body)

            if response.to_dict()["errors"]:
                raise Exception(response.to_dict()["errors"])


for i in range(10):
    print("sending: ", i)
    DataDogAdapter().increment(
        metric_name="local_metric", tags=["env:test"], value=random.randint(1001, 2000)
    )
    time.sleep(60)
