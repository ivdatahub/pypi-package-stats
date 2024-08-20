from src.application.services.get_secret_value_service import GetSecretValueService
from src.adapter.secret_manager_adapter import SecretManagerAdapter
from src.application.utils.singleton import Singleton


class GetSecretValueUseCase:
    def __init__(self, secret_id: str) -> None:
        self.repository = SecretManagerAdapter
        self.secret_id = secret_id
        self.secret_service = GetSecretValueService(secret_manager=self.repository)

    def get(self) -> str:
        return self.secret_service.get()
