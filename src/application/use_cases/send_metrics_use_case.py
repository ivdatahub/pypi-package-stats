import os
from dotenv import load_dotenv
from src.application.services.dw_service import DWService
from src.application.services.send_metrics_service import SendMetricsService
from src.adapter.bigquery_adapter import BigQueryAdapter
from src.adapter.datadog_adapter import DataDogAPIAdapter
from src.application.utils.logger_module import logger, log_extra_info, LogStatus

from pandas.core.frame import DataFrame


load_dotenv()


class SendPypiStatsUseCase:
    def __init__(self):
        self.get_data_from_dw_service = DWService(datawarehouse=BigQueryAdapter())
        self.send_metrics_service = SendMetricsService(
            DataDogAPIAdapter(metric_name="pypi")
        )

    def get_stats(self):
        query = f"""
            SELECT
            DOWNLOAD_ID,
            CAST(UNIX_SECONDS(TIMESTAMP(DTTM)) AS INT64) DTTM,
            COUNTRY_CODE,
            PROJECT,
            PACKAGE_VERSION,
            INSTALLER_NAME,
            PYTHON_VERSION
            FROM {os.getenv('PROJECT_ID')}.STG.PYPI_PROJ_DOWNLOADS
            WHERE DTTM >= DATETIME_SUB(CURRENT_DATETIME, INTERVAL 1 day)
            AND NOT PUSHED
            """
        return self.get_data_from_dw_service.query_to_dataframe(query=query)

    def send_stats(self, df: DataFrame):
        for index, row in df.iterrows():
            tags = [
                f"country_code:{row['COUNTRY_CODE']}",
                f"project:{row['PROJECT']}",
                f"package_version:{row['PACKAGE_VERSION']}",
                f"installer_name:{row['INSTALLER_NAME']}",
                f"python_version:{row['PYTHON_VERSION']}",
            ]
            # 3126033309371667865

            result, err = self.send_metrics_service.send(
                tags=tags,
                value=1,
                timestamp=row["DTTM"],
            )

            if err:
                raise Exception(str(err))

            result, err = self._update_dw(
                id=row["DOWNLOAD_ID"], project_name=row["PROJECT"]
            )

            if err:
                raise Exception(str(err))

    def _update_dw(self, id: int, project_name: str):
        query = f"""
            UPDATE {os.getenv('PROJECT_ID')}.STG.PYPI_PROJ_DOWNLOADS
            SET PUSHED = true
            WHERE DOWNLOAD_ID = {id}
            and PROJECT = '{project_name}'
            AND NOT PUSHED
            """
        return self.get_data_from_dw_service.query_execute(query=query)
