from pydantic import BaseModel
from sqlalchemy import delete as delete_sql
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models import Repositories


class RepositoryRepo:
    def __init__(self, session: AsyncSession):
        self._model = Repositories
        self._session = session

    @staticmethod
    def _dump_data(data: BaseModel, exclude_unset: bool = True) -> dict:
        return data.model_dump(exclude_unset=exclude_unset)

    def _apply_filters(self, stmt, filters: dict):
        for key, value in filters.items():
            if not hasattr(self._model, key):
                raise ValueError(f"Unknown filter field: {key}")
            stmt = stmt.where(getattr(self._model, key) == value)
        return stmt

    async def create(self, data: BaseModel) -> Repositories:
        payload = self._dump_data(data, exclude_unset=True)
        obj = self._model(**payload)
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def commit(self) -> None:
        await self._session.commit()

    async def update(self, data: BaseModel, **filters) -> Repositories | None:
        obj = await self.find_single(**filters)

        if not obj:
            return None

        payload = self._dump_data(data, exclude_unset=True)

        for k, v in payload.items():
            setattr(obj, k, v)

        await self._session.flush()
        return obj

    async def find_single(self, **filters) -> Repositories | None:
        stmt = self._apply_filters(select(self._model), filters)
        res = await self._session.execute(stmt)
        return res.scalars().one_or_none()

    async def find_many(self, **filters) -> list[Repositories]:
        stmt = self._apply_filters(select(self._model), filters)
        res = await self._session.execute(stmt)
        return list(res.scalars().all())

    async def delete(self, **filters) -> bool:
        stmt = delete_sql(self._model)
        stmt = self._apply_filters(stmt, filters)
        res = await self._session.execute(stmt)
        return res.rowcount > 0
