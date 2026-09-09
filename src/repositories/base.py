from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")

class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filter_by) -> T | None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository[T]):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: dict) -> T:
        instance = self.model(**data)
        self.session.add(instance)
        return instance

    async def find_all(self) -> List[T]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def find_one(self, **filter_by) -> T | None:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()