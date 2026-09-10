from typing import List

import aio_pika
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.notifications import JobNotificationEvent
from src.repositories.job_repository import JobRepository
from src.models.job import Job


class JobService:
    def __init__(self, db_session: AsyncSession, redis_client: Redis, rabbit_channel: aio_pika.RobustChannel = None):
        self.job_repo = JobRepository(db_session)
        self.redis = redis_client
        self.rabbit_channel = rabbit_channel

    async def create_job(self, job_data: dict) -> Job:
        # 1. Сохраняем вакансию в Postgres
        new_job = await self.job_repo.add(job_data)
        await self.job_repo.session.commit()

        # 2. ФИЧА RABBITMQ: Отправляем задачу в очередь для воркера уведомлений
        if self.rabbit_channel:
            # Формируем объект события
            event_data = JobNotificationEvent(
                job_id=new_job.id,
                title=new_job.title,
                company=new_job.company,
                tags=new_job.tags
            )

            # Отправляем сообщение в очередь "job_notifications"
            await self.rabbit_channel.default_exchange.publish(
                aio_pika.Message(
                    body=event_data.model_dump_json().encode("utf-8"),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT  # Сообщение не пропадет при перезапуске RabbitMQ
                ),
                routing_key="job_notifications"
            )
            print(f"[x] Отправлено событие вакансии {new_job.id} в RabbitMQ")

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