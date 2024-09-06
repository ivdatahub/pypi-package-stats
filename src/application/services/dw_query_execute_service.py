from src.application.ports.datawarehouse_interface import DataWarehousePort
from typing import Type


class QueryExecuteService:
    def __init__(self, datawarehouse: Type[DataWarehousePort]):
        self.datawarehouse = datawarehouse

    def execute(self, query: str):
        return self.datawarehouse.query_execute(query)
