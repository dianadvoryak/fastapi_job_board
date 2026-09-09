from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, status
from src.core.security import hash_password
from src.models.user import User
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.user_repo = UserRepository(db_session)

    async def create_user(self, user_data: dict) -> User:
        """Создает пользователя и проверяет уникальность email."""
        plain_password = user_data.pop("password")
        user_data["hashed_password"] = hash_password(plain_password)

        try:
            new_user = await self.user_repo.add(user_data)
            # Ошибка уникальности вылетает именно в момент коммита (или flush)
            await self.user_repo.session.commit()
            return new_user

        except IntegrityError as error:
            # Откатываем неудавшуюся транзакцию, чтобы сессия осталась рабочей
            await self.user_repo.session.rollback()

            # Проверяем, что ошибка вызвана именно дубликатом email
            # В тексте ошибки Postgres всегда будет присутствовать имя таблицы или поля
            error_msg = str(error.orig)

            if "email" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Пользователь с email '{user_data.get('email')}' уже зарегистрирован."
                )

            # Если вылетела какая-то другая ошибка integrity (например, пустые поля)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка валидации данных на стороне базы данных."
            )