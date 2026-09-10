from src.repositories.base import SQLAlchemyRepository
from src.models.application import Application

class ApplicationRepository(SQLAlchemyRepository[Application]):
    model = Application
