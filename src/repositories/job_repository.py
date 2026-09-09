from src.repositories.base import SQLAlchemyRepository
from src.models.job import Job


class JobRepository(SQLAlchemyRepository[Job]):
    model = Job

    # Сюда можно добавлять кастомные методы, например:
    # async def get_jobs_by_employer(self, employer_id: int): ...

