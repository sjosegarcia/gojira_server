import pytest
from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
from setup.start_app import start_app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from services.database_service import db
from typing import AsyncGenerator


engine = create_async_engine("postgresql+asyncpg:///./test.db", echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    except SQLAlchemyError:
        await session.rollback()
    finally:
        await session.close()


@pytest.fixture
def fastapi_app_mock() -> FastAPI:
    app = start_app()
    app.dependency_overrides[db.get_db] = override_get_db
    return app


@pytest.fixture
def test_client(fastapi_app_mock: FastAPI) -> TestClient:
    return TestClient(fastapi_app_mock)
