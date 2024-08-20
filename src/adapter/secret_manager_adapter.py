from google.cloud import secretmanager
from src.application.ports.secret_manager_interface import ISecretManager


class SecretManagerAdapter(ISecretManager):
    def __init__(self, secret_id: str):
        self.secret_id = secret_id

    def get_secret_value(self) -> str:
        secret_client = secretmanager.SecretManagerServiceClient()

        request = {
            "name": f"projects/ivanildobarauna/secrets/{self.secret_id}/versions/latest",
        }

        secret_request = secret_client.access_secret_version(request=request)

        return secret_request.payload.data.decode("UTF-8")
