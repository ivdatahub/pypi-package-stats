from src.application.ports.datawarehouse_interface import DataWarehousePort
from typing import Type


class GetDataFromDWService:
    def __init__(self, datawarehouse: Type[DataWarehousePort]):
        self.datawarehouse = datawarehouse

    def execute(self, query: str):
        return self.datawarehouse.fetch_dataframe(query)
