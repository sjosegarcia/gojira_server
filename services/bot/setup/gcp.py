from google.cloud import secretmanager
from .config import get_settings


def get_secrets(secrets_id: str, secrets_version: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(
        get_settings().gcp_project_id,
        secrets_id,
        secrets_version,
    )
    response = client.access_secret_version(name=name)
    payload = str(response.payload.data.decode("UTF-8"))
    return payload
