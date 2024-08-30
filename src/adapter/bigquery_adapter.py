from src.application.ports.datawarehouse_interface import DataWarehousePort
from google.cloud import bigquery
from pandas.core.frame import DataFrame
from typing import Type


class BigQueryAdapter(DataWarehousePort):
    def __init__(self):
        self.bigquery_conn = bigquery.Client()

    def get_data(self, query: str) -> Type[DataFrame]:
        # Perform a query.
        QUERY = query
        query_job = self.bigquery_conn.query(QUERY)  # API request
        rows = query_job.to_dataframe()
        return rows
