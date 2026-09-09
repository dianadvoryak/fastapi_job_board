from src.repositories.base import SQLAlchemyRepository
from src.models.user import User


class UserRepository(SQLAlchemyRepository[User]):
    model = User
