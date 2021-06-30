# mypy: ignore-errors
from models.base import Base
from services.firebase_service import get_current_active_user
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
from schema.user_schema import User, UserInDB
from typing import Generator
from _pytest.fixtures import SubRequest
from asyncio import get_event_loop_policy


os.environ["ENV"] = "TEST"
engine = create_async_engine(create_db_url(), echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(scope="session")
def test_user() -> User:
    return User(
        uid="123",
        username="DefiKid123",
        email="defikid123@maxfarms.zil",
        firstname="James",
        lastname="Holden",
        deleted=False,
    )


@pytest.fixture(scope="session")
def test_user_in_db() -> User:
    return UserInDB(
        id=1,
        uid="123",
        username="DefiKid123",
        email="defikid123@maxfarms.zil",
        firstname="James",
        lastname="Holden",
        deleted=False,
    )


@pytest.fixture(scope="session")
def event_loop(request: SubRequest) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def fastapi_app_mock(test_user_in_db: UserInDB) -> FastAPI:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    app = start_app()
    app.dependency_overrides[db.get_db] = get_test_db
    app.dependency_overrides[get_current_active_user] = lambda: test_user_in_db
    return app


@pytest.fixture(scope="session")
def test_client(fastapi_app_mock: FastAPI) -> AsyncClient:
    return AsyncClient(
        app=fastapi_app_mock, base_url=f"http://localhost{get_settings().api_v1_str}"
    )
