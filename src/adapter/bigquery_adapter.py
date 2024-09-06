from google.cloud import bigquery
from pandas.core.frame import DataFrame
from typing import Type
from src.application.ports.datawarehouse_interface import DataWarehousePort


class BigQueryAdapter(DataWarehousePort):
    """
    A class used to represent a BigQueryAdapter

    """

    def __init__(self):
        self.bigquery_conn = bigquery.Client()

    def fetch_dataframe(self, query: str) -> Type[DataFrame]:
        """
        Get data from BigQuery
        """
        # Perform a query.
        QUERY = query
        query_job = self.bigquery_conn.query(QUERY)  # API request
        rows = query_job.to_dataframe()
        return rows
