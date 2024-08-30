from src.application.ports.datawarehouse_interface import DataWarehouseInterface
from typing import Type

class GetDataFromDWService:
    def __init__(self, datawarehouse: Type[DataWarehouseInterface]):
        self.datawarehouse = datawarehouse

    def execute(self, query: str):
        return self.datawarehouse.get_data(query)