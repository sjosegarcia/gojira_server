from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from setup.config import get_settings
from typing import AsyncGenerator
from setup.gcp import get_secrets
from loguru import logger
import os


class DatabaseService:
    def __init__(self) -> None:
        self.engine = create_async_engine(create_db_url(), echo=False)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.async_session()
        try:
            yield session
        except SQLAlchemyError as error:
            logger.error(f"{error}")
            await session.rollback()
        finally:
            await session.close()


def get_db_password() -> str:
    settings = get_settings()
    password = get_secrets(
        settings.database_password_secret, settings.database_password_secret_version
    )
    return password


def create_db_url() -> str:
    settings = get_settings()
    env = os.getenv("ENV", "")
    if env == "DEV":
        return "postgresql+asyncpg://local:local@api-db:5432/test_db"
    if env == "TEST":
        return "postgresql+asyncpg://test:test@api-test-db:5432/test_db"
    db_url = settings.database_url
    db_url = db_url.replace("postgresql", "postgresql+asyncpg")
    db_url = db_url.replace("?sslmode=require", "")
    return f"{db_url}"


db = DatabaseService()
