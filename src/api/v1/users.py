from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.user_service import UserService
from src.api.schemas.users import UserCreateSchema, UserResponseSchema
from src.core.db import get_async_session

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=UserResponseSchema)
async def create_new_user(
        user_in: UserCreateSchema,
        db: AsyncSession = Depends(get_async_session)
    ):
    user_service = UserService(db)
    new_user = await user_service.create_user(user_in.model_dump())
    return new_user

