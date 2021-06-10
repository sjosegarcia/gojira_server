from setup.config import get_settings
from fastapi.testclient import TestClient


def test_bot_set_webhook(test_client: TestClient) -> None:
    response = test_client.get(f"/{get_settings().telegram_bot_api_key}/setwebhook")
    data = response.json()
    assert data["hoooked"]


def test_bot_webhook_info(test_client: TestClient) -> None:
    response = test_client.get(f"/{get_settings().telegram_bot_api_key}/webhookinfo")
    data = response.json()
    assert not data["url"]
