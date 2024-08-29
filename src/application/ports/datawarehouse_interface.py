from abc import ABC, abstractmethod


class DataWarehousePort(ABC):
    @abstractmethod
    def fetch_dataframe(self, query: str) -> object:
        pass
