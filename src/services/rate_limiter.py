from redis.asyncio import Redis
from fastapi import HTTPException, status

class RateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def check_rate_limit(self, user_id: int, limit: int = 5, window_seconds: int = 60):
        """
        Проверяет, не превысил ли пользователь лимит запросов.
        Если превысил — выбрасывает HTTPException 429 Too Many Requests.
        """
        if not self.redis:
            return  # Если Redis не подключен, пропускаем (Fail-safe)

        # Формируем уникальный ключ для пользователя
        key = f"rate_limit:{user_id}"

        # Атомарно увеличиваем счетчик запросов в Redis
        current_requests = await self.redis.incr(key)

        # Если это первый запрос в текущем окне, задаем время жизни ключа (60 сек)
        if current_requests == 1:
            await self.redis.expire(key, window_seconds)

        # Если лимит превышен — жестко пресекаем выполнение
        if current_requests > limit:
            # Выясняем, сколько секунд осталось до сброса лимита
            ttl = await self.redis.ttl(key)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Слишком много запросов. Попробуйте снова через {ttl} секунд."
            )
