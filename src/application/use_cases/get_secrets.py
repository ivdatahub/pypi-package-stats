from src.application.services.get_secret_value_service import GetSecretValueService
from src.adapter.secret_manager import SecretManagerAdapter
from src.application.utils.singleton import Singleton


class GetSecretValueUseCase(Singleton):
    def __init__(self, secret_id: str) -> None:
        self.secret_id = secret_id

        if not hasattr(self, "initialized"):
            self.repository = SecretManagerAdapter(secret_id=secret_id)
            self.secret_service = GetSecretValueService(secret_manager=self.repository)
            self.initialized = True

    def get(self) -> str:
        return self.secret_service.get()
