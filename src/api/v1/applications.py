from fastapi import APIRouter, Depends, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.services.application_service import ApplicationService
from src.core.redis_client import get_redis
from src.api.schemas.applications import ApplyJobSchema

router = APIRouter(prefix="/jobs", tags=["Applications"])

@router.post("/{job_id}/apply", status_code=status.HTTP_200_OK)
async def apply_to_job(
    job_id: int,
    apply_in: ApplyJobSchema,
    db: AsyncSession = Depends(get_async_session),
    redis: Redis = Depends(get_redis)
):
    """
       Откликнуться на вакансию.
       Запрос проверяется в Redis Rate Limiter и сохраняется в PostgreSQL.
       """
    # Инициализируем сервис откликов и передаем туда всю работу
    app_service = ApplicationService(db, redis)

    new_app = await app_service.apply_to_job(
        job_id=job_id,
        user_id=apply_in.user_id,
        cover_letter=apply_in.cover_letter
    )
    return new_app
