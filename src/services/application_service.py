from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.repositories.application_repository import ApplicationRepository
from src.services.rate_limiter import RateLimiter
from src.models.application import Application


class ApplicationService:
    def __init__(self, db_session: AsyncSession, redis_client: Redis):
        self.app_repo = ApplicationRepository(db_session)
        self.rate_limiter = RateLimiter(redis_client)

    async def apply_to_job(self, job_id: int, user_id: int, cover_letter: str) -> Application:
        # 1. Проверяем Rate Limiter в Redis (максимум 5 откликов в минуту)
        await self.rate_limiter.check_rate_limit(user_id=user_id, limit=5, window_seconds=60)

        # 2. Формируем данные для создания модели
        data = {
            "job_id": job_id,
            "user_id": user_id,
            "cover_letter": cover_letter
        }

        # 3. Сохраняем в Postgres через репозиторий
        new_application = await self.app_repo.add(data)
        await self.app_repo.session.commit()

        return new_application
