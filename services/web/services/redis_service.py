from aioredis import Redis
from aioredis.commands import create_redis
from setup.config import get_settings
from loguru import logger


class RedisService:
    async def connect_redis(self) -> None:
        try:
            self.redis = await create_redis(
                get_settings().redis_url, password=get_settings().redis_password
            )
        except ConnectionRefusedError as e:
            logger.error(f"Redis connection refused: {e}")
            raise e

    async def get_redis(self) -> Redis:
        await self.connect_redis()
        yield self.redis


redis = RedisService()
