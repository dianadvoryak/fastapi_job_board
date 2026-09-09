from typing import List
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.job_repository import JobRepository
from src.models.job import Job


class JobService:
    def __init__(self, db_session: AsyncSession, redis_client: Redis):
        self.job_repo = JobRepository(db_session)
        self.redis = redis_client

    async def create_job(self, job_data: dict) -> Job:
        # 1. Сохраняем вакансию в Postgres
        new_job = await self.job_repo.add(job_data)
        await self.job_repo.session.commit()

        # TODO: Здесь в будущем мы добавим отправку события в RabbitMQ
        # для уведомления подходящих кандидатов

        return new_job

    async def get_job(self, job_id: int) -> Job | None:
        # 1. Достаем вакансию из БД
        job = await self.job_repo.find_one(id=job_id)

        if job and self.redis:
            # 2. ФИЧА REDIS: Если вакансия найдена, увеличиваем счетчик популярности каждого тега
            # Используем ZINCRBY. Ключ "trending_skills" увеличивает вес тега на 1 при каждом просмотре
            for tag in job.tags:
                await self.redis.zincrby("trending_skills", 1, tag)

        return job

    async def get_top_skills(self) -> List[tuple]:
        """Получить топ-10 самых востребованных навыков по просмотрам."""
        if not self.redis:
            return []
        # Возвращает список элементов от большего к меньшему с их весами (количеством просмотров)
        skills = await self.redis.zrevrange("trending_skills", 0, 9, withscores=True)
        return skills