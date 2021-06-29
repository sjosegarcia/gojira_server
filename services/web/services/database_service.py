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
        self.engine = create_async_engine(create_db_url(), echo=True)
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
        return settings.database_url
    if os.getenv("ENV", "") == "TEST":
        return settings.test_database_url

    return f"postgresql+asyncpg://{settings.database_username}:{get_db_password()}@/{settings.database_name}?host={settings.database_host}:{settings.database_instance}"


db = DatabaseService()
