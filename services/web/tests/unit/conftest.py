import pytest
import os
from setup.config import get_settings
from fastapi.applications import FastAPI
from httpx import AsyncClient
from setup.start_app import start_app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from services.database_service import create_db_url, db
from typing import AsyncGenerator
from alembic import config

os.environ["ENV"] = "TEST"
engine = create_async_engine(create_db_url(), echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
config.main(argv=["upgrade", "head"])


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(scope="session")
def fastapi_app_mock() -> FastAPI:
    app = start_app()
    app.dependency_overrides[db.get_db] = get_test_db
    return app


@pytest.fixture(scope="session")
def test_client(fastapi_app_mock: FastAPI) -> AsyncClient:
    return AsyncClient(
        app=fastapi_app_mock, base_url=f"http://localhost{get_settings().api_v1_str}"
    )
