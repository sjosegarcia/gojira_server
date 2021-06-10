from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from utils.config import get_settings
from typing import AsyncGenerator

engine = create_async_engine(get_settings().database_url)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSession(engine)
    try:
        yield session
    finally:
        await session.close()
