from typing import Any, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import constants
from src.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс DAO для операций с моделями в БД.
    """

    model = None

    # MARK: Add
    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        obj_in: Union[CreateSchemaType, dict[str, Any]],
    ) -> ModelType | None:
        """
        Добавить запись в текущую сессию.
        """
        stmt = insert(cls.model).values(**obj_in)
        result = await session.execute(stmt)
        return result.scalars().one()

    # MARK: Find
    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
        offset: Optional[int] = constants.PAGINATION_DEFAULT_OFFSET,
        limit: Optional[int] = constants.PAGINATION_DEFAULT_LIMIT,
        *filter,
        **filter_by,
    ) -> List[ModelType]:
        """
        Возвращает записи, удовлетворяющие фильтру.
        При указании `offset` и `limit` будет выполнена пагинация.
        """
        stmt = (
            select(cls.model)
            .filter(*filter)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
