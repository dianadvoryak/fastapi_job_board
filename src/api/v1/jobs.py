from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from typing import List, Dict

from src.core.db import get_async_session
from src.core.redis_client import get_redis
from src.services.job_service import JobService
from src.api.schemas.jobs import JobCreateSchema, JobResponseSchema

router = APIRouter(prefix="/jobs", tags=["Jobs & Trends"])


@router.post("/", response_model=JobResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_new_job(
        job_in: JobCreateSchema,
        db: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(get_redis)
):
    """Создать новую вакансию."""
    job_service = JobService(db, redis)
    new_job = await job_service.create_job(job_in.model_dump())
    return new_job


@router.get("/trends/skills", response_model=Dict[str, float])
async def get_trending_skills(
        db: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(get_redis)
):
    """
    ФИЧА REDIS: Получить топ-10 самых популярных навыков/тегов
    на основе просмотров вакансий соискателями.
    """
    job_service = JobService(db, redis)
    trends = await job_service.get_top_skills()

    # Превращаем список кортежей [('python', 5.0), ('fastapi', 3.0)] в удобный словарь
    return {skill: score for skill, score in trends}


@router.get("/{job_id}", response_model=JobResponseSchema)
async def get_job_by_id(
        job_id: int,
        db: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(get_redis)
):
    """
    Получить вакансию по ID.
    При каждом запросе теги этой вакансии инкрементируются в Redis.
    """
    job_service = JobService(db, redis)
    job = await job_service.get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Вакансия с ID {job_id} не найдена"
        )
    return job