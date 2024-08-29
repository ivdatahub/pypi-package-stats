from src.application.ports.datawarehouse_interface import DataWarehousePort
from google.cloud import bigquery


class BigQueryAdapter(DataWarehousePort):
    def __init__(self):
        self.bigquery_conn = bigquery.Client()

    def fetch_dataframe(self, query: str):
        # Perform a query.
        QUERY = query
        query_job = self.bigquery_conn.query(QUERY)  # API request
        return query_job.to_dataframe()


bq = BigQueryAdapter()
df = bq.fetch_dataframe(
    "SELECT * FROM `bigquery-public-data.samples.shakespeare` LIMIT 5"
)
print(df)
