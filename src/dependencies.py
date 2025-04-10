from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal


# MARK: DB
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессии.
    """

    async with SessionLocal() as session:
        try:
            yield session
        except Exception as ex:
            await session.rollback()
            raise ex
