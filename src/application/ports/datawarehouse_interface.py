# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from abc import ABC, abstractmethod
from typing import Type
from pandas.core.frame import DataFrame


class DataWarehousePort(ABC):
    @abstractmethod
    def fetch_dataframe(self, query: str) -> Type[DataFrame]:
        pass
