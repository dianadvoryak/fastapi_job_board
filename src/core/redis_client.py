import redis.asyncio as aioredis
from src.core.config import settings

class RedisBackend:
    def __init__(self):
        self.client: aioredis.Redis | None = None

    def init(self):
        self.client = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf-8",
            decode_responses=True
        )

    async def close(self):
        if self.client:
            await self.client.close()

redis_backend = RedisBackend()

# Dependency для получения клиента Redis
async def get_redis():
    return redis_backend.client
