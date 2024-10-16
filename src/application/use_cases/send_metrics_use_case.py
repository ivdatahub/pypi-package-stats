import os
import time
from dotenv import load_dotenv
from tqdm import tqdm
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
            WHERE DTTM >= DATETIME_SUB(CURRENT_DATETIME, INTERVAL 2 DAY)
            AND NOT PUSHED
            """
        return self.get_data_from_dw_service.query_to_dataframe(query=query)

    def send_stats(self, df: DataFrame):
        if len(df) == 0:
            return

        downloads_list = []

        for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing data"):
            tags = [
                f"country_code:{row['COUNTRY_CODE']}",
                f"project:{row['PROJECT']}",
                f"package_version:{row['PACKAGE_VERSION']}",
                f"installer_name:{row['INSTALLER_NAME']}",
                f"python_version:{row['PYTHON_VERSION']}",
            ]

            result, err = self.send_metrics_service.send(
                tags=tags,
                value=1,
                timestamp=row["DTTM"],
            )

            if err:
                raise Exception(str(err))

            downloads_list.append(row["DOWNLOAD_ID"])

            if len(downloads_list) == 100:
                result, err = self._update_dw(
                    downloads_list=downloads_list, project_name=row["PROJECT"]
                )

                if err:
                    raise Exception(str(err))

                downloads_list = []

        if len(downloads_list) > 0:
            result, err = self._update_dw(
                downloads_list=downloads_list, project_name=row["PROJECT"]
            )

            if err:
                raise Exception(str(err))

    def _update_dw(self, downloads_list: list, project_name: str):
        downloads_list_str = ",".join(map(str, downloads_list))

        query = f"""
            UPDATE {os.getenv('PROJECT_ID')}.STG.PYPI_PROJ_DOWNLOADS
            SET PUSHED = true
            WHERE DOWNLOAD_ID in ({downloads_list_str})
            and PROJECT = '{project_name}'
            AND NOT PUSHED
            """
        return self.get_data_from_dw_service.query_execute(query=query)
