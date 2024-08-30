from src.application.services.get_data_from_dw_service import GetDataFromDWService
from src.application.services.get_secret_value_service import GetSecretValueService
from src.application.services.send_metrics_service import SendMetricsService

from src.adapter.bigquery_adapter import BigQueryAdapter
from src.adapter.secret_manager_adapter import SecretManagerAdapter
from src.adapter.datadog_adapter import DataDogAPIAdapter


class SendPypiStatsUseCase:
    def __init__(self, metric_name: str, tags: list, value: int):
        self.metrics_repository = DataDogAPIAdapter(metric_name, tags, value)

    def send(self):
        SendMetricsService(MetricsRepository=self.metrics_repository).send()
