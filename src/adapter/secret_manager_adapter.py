from google.cloud import secretmanager
from src.application.ports.secret_manager_interface import ISecretManager


class SecretManagerAdapter(ISecretManager):
    def __init__(self):
        self.secret_client = secretmanager.SecretManagerServiceClient()

    def get_secret_value(self, secret_id: str) -> str:
        request = {
            "name": f"projects/ivanildobarauna/secrets/{secret_id}/versions/latest",
        }

        secret_request = self.secret_client.access_secret_version(request=request)

        return secret_request.payload.data.decode("UTF-8")
