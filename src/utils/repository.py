from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def read_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        obj = await self.session.execute(stmt)
        return obj.scalar_one()

    async def read_one(self, **filters):
        stmt = select(self.model).filter_by(**filters)
        objects = await self.session.execute(stmt)
        obj = objects.first()
        if obj:
            obj = obj[0].to_read_model()
        return obj

    async def update_one(self, obj_id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=obj_id).returning(self.model.id)
        obj = await self.session.execute(stmt)
        return obj.scalar_one()

    async def delete_one(self, obj_id: int,) -> int:
        stmt = delete(self.model).where(id=obj_id).returning(self.model.id)
        obj = await self.session.execute(stmt)
        return obj.scalar_one()

    async def get_all(self, **filters):
        stmt = select(self.model).filter_by(**filters)
        objects = await self.session.execute(stmt)
        result = [obj[0] for obj in objects.all()]
        return result


