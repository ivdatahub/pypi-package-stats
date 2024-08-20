import time
from datetime import datetime, timedelta
import random
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint

# from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries


from src.application.ports.metrics_interface import MetricsPort
from src.application.use_cases.get_secrets import GetSecretValueUseCase


class DataDogAdapter(MetricsPort):
    def __init__(self, metric_name: str, tags: list, value: int):
        self.metric_name = metric_name
        self.tags = tags
        self.value = value

    def get_dd_api_key(self):
        return GetSecretValueUseCase(secret_id="datadog-pypi-package-stats").get()

    def increment(self):
        ts_now = int(datetime.now().timestamp())
        ts_passed = int((datetime.now() - timedelta(minutes=30)).timestamp())

        body = MetricPayload(
            series=[
                MetricSeries(
                    metric=self.metric_name,
                    type=MetricIntakeType.COUNT,
                    points=[
                        MetricPoint(
                            # """ Add historical timestamp here """
                            timestamp=ts_passed,
                            # """ *********************** """
                            value=self.value,
                        ),
                    ],
                    # resources=[
                    #     MetricResource(
                    #         name="dummyhost",
                    #         type="host",
                    #     ),
                    # ],
                    tags=self.tags,
                ),
            ],
        )

        configuration = Configuration()
        configuration.debug = True
        configuration.api_key["apiKeyAuth"] = self.get_dd_api_key()
        # configuration.api_key["appKeyAuth"] = "y"
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
    time.sleep(10)
