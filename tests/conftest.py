import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from src.config import project_settings
from src.tron.schemas import TronWalletSchema

faker = Faker()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def engine(event_loop):
    """
    Создает async engine для тестирования.
    """
    engine = create_async_engine(
        url=(
            f"postgresql+asyncpg://{project_settings.POSTGRES_USER}:{project_settings.POSTGRES_PASSWORD}@"
            f"{project_settings.POSTGRES_HOST}:{project_settings.POSTGRES_PORT}/{project_settings.POSTGRES_DB}"
        ),
        poolclass=NullPool,
    )

    yield engine


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """
    Создает async engine для тестирования.
    """
    engine = create_async_engine(
        url=(
            f"postgresql+asyncpg://{project_settings.POSTGRES_USER}:{project_settings.POSTGRES_PASSWORD}@"
            f"{project_settings.POSTGRES_HOST}:{project_settings.POSTGRES_PORT}/{project_settings.POSTGRES_DB}"
        ),
        poolclass=NullPool,
    )

    async with engine.connect() as conn:
        await conn.run_sync(do_run_migrations)

    yield engine

    async with engine.connect() as conn:
        await conn.run_sync(do_downgrade_migrations)


async def do_run_migrations(connection):
    """Применяет миграции к базе данных."""
    from alembic import command

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


async def do_downgrade_migrations(connection):
    """Откатывает миграции в базе данных."""
    context = MigrationContext.configure(connection)
    script = ScriptDirectory.from_config(Config("alembic.ini"))

    current_rev = context.get_current_revision()

    if current_rev:
        for rev in script.walk_revisions():
            if rev.revision == current_rev:
                await connection.execute(rev.downgrade_script())


@pytest.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Подключение к PostgreSQL и создание сессии.
    """
    AsyncSession = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with engine.connect() as conn:
        tsx = await conn.begin()
        async with AsyncSession(bind=conn) as session:
            nested_tsx = await conn.begin_nested()
            yield session

            if nested_tsx.is_active:
                await nested_tsx.rollback()
            await tsx.rollback()


@pytest.fixture()
async def correct_tron_wallet() -> TronWalletSchema:
    """
    Корректный кошелек Tron.
    """
    return TronWalletSchema(address="TSP8Aw51yk1QQCEgX7rPu81qrfSh2UXDhe")
