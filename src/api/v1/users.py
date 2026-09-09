from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.schemas.users import UserCreateSchema
from src.core.db import get_async_session
from src.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreateSchema, db: AsyncSession = Depends(get_async_session)):
    """Временный роут для создания пользователя, чтобы получить employer_id."""
    new_user = User(
        email=user_in.email,
        hashed_password=user_in.password,  # В пет-проекте потом добавим хеширование (bcrypt/passlib)
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}

