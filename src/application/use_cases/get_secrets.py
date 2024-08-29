from src.application.services.get_secret_value_service import GetSecretValueService
from src.adapter.secret_manager_adapter import SecretManagerAdapter
from src.application.utils.singleton import Singleton


class GetSecretValueUseCase:
    def __init__(self) -> None:
        self.repository = SecretManagerAdapter()
        self.secret_service = GetSecretValueService(secret_manager=self.repository)

    def get(self, secret_id: str) -> str:
        return self.secret_service.get(secret_id=secret_id)
