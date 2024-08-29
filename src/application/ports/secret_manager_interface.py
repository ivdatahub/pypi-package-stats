from abc import ABC, abstractmethod


class ISecretManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_secret_value(self, secret_id: str) -> str:
        pass
