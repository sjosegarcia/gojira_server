from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
from setup.start_app import start_app
import pytest


@pytest.fixture
def test_app() -> FastAPI:
    return start_app()


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)
