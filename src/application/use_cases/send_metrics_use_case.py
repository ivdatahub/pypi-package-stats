from src.application.services.get_data_from_dw_service import GetDataFromDWService
from src.application.services.send_metrics_service import SendMetricsService

from src.adapter.bigquery_adapter import BigQueryAdapter
from src.adapter.datadog_adapter import DataDogAPIAdapter

from pandas.core.frame import DataFrame


class SendPypiStatsUseCase:
    def __init__(self):
        self.datawarehouse_adapter = BigQueryAdapter()
        self.metrics_repository = DataDogAPIAdapter(metric_name="pypi")

    def get_stats(self, package_name: str):
        query = f"""
            SELECT
            DTTM, COUNTRY_CODE, PROJECT, PACKAGE_VERSION, INSTALLER_NAME, PYTHON_VERSION, TOTAL_DOWNLOADS
            FROM `ivanildobarauna.DW.PYPI_PROJ`
            WHERE PROJECT = {package_name}
            AND PUSHED is null limit 1
            """
        return self.datawarehouse_adapter.get_data(query=query)
    
    def send_stats(self, df: DataFrame):
        for index, row in df.iterrows():
            tags = [
                f"country_code:{row['COUNTRY_CODE']}",
                f"project:{row['PROJECT']}",
                f"package_version:{row['PACKAGE_VERSION']}",
                f"installer_name:{row['INSTALLER_NAME']}",
                f"python_version:{row['PYTHON_VERSION']}",
            ]
            self.metrics_repository.increment(tags=tags, value=row['TOTAL_DOWNLOADS'], timestamp=row['DTTM'])
