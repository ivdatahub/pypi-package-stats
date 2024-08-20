from src.application.services.send_metrics_service import SendMetricsService
from src.adapter.metrics_adapter import DataDogAdapter


class SendMetricsUseCase:
    def __init__(self, metric_name: str, tags: list, value: int):
        self.metrics_repository = DataDogAdapter(metric_name, tags, value)
    
    
        

