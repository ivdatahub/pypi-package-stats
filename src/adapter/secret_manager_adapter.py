import os
from dotenv import load_dotenv
from typing import Tuple, Optional
from google.cloud import secretmanager
from src.application.ports.secret_manager_interface import ISecretManager
from src.application.utils.logger_module import logger, log_extra_info, LogStatus

load_dotenv()


class SecretManagerAdapter(ISecretManager):
    """
    A class used to represent a SecretManagerAdapter
    """

    def __init__(self) -> None:
        self.secret_client = secretmanager.SecretManagerServiceClient()

    def get_secret_value(self, secret_id: str) -> Tuple[Optional[str], str]:
        request = {
            "name": f"projects/{os.getenv('PROJECT_ID')}/secrets/{secret_id}/versions/latest",
        }

        try:
            secret_request = self.secret_client.access_secret_version(request=request)
        except ValueError as e:
            logger.error(
                "Secret Manager error getting secret value",
                extra=log_extra_info(
                    status=LogStatus.ERROR,
                    msg=f"Error getting secret value: {str(e)}",
                    secret_id=secret_id,
                ),
            )
            return str(e), ""

        return None, secret_request.payload.data.decode("UTF-8")
