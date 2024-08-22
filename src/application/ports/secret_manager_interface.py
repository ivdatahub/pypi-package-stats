from abc import ABC, abstractmethod


class ISecretManager(ABC):
    def __init__(self, secret_id: str):
        pass

    @abstractmethod
    def get_secret_value(self) -> str:
        pass
