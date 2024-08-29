from src.application.ports.secret_manager_interface import ISecretManager
from typing import Type


class GetSecretValueService:
    def __init__(self, secret_manager: Type[ISecretManager]):
        self.manager = secret_manager

    def get(self, secret_id: str) -> str:
        return self.manager.get_secret_value(secret_id=secret_id)
