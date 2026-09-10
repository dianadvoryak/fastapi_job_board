from src.models.base import BaseModel
from src.models.user import User
from src.models.job import Job
from src.models.application import Application

# Экспортируем все для Alembic
__all__ = ["BaseModel", "User", "Job", "Application"]
