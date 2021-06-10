from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
from setup.start_app import start_app
from telethon import TelegramClient
from setup.config import get_settings
import pytest


@pytest.fixture
def test_app() -> FastAPI:
    return start_app()


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)


@pytest.fixture
def test_telegram_client() -> TelegramClient:
    return TelegramClient(
        get_settings().telegram_session_name,
        int(get_settings().telegram_api_id),
        get_settings().telegram_api_hash,
    )


@pytest.fixture
def test_start_telegram_client(test_telegram_client: TelegramClient) -> None:
    test_telegram_client.start()
