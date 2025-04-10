"""Фикстуры для интеграционных тестов эндпоинтов."""

from typing import AsyncGenerator

import httpx
import pytest_asyncio
from fastapi import APIRouter, FastAPI

from src.dependencies import get_session


class EndpointTestHelper:
    """Базовый класс для изолированного тестирования роутеров FastAPI."""

    router: APIRouter

    @pytest_asyncio.fixture(scope="function")
    async def async_test_client(
        self, session
    ) -> AsyncGenerator[httpx.AsyncClient, None]:
        """
        Предоставляет httpx.AsyncClient, направляющий запросы напрямую в ASGI-приложение.
        Используется FastAPI-приложение, в которое подключён нужный роутер.
        """

        test_app = FastAPI()
        test_app.include_router(self.router)
        test_app.dependency_overrides[get_session] = lambda: session

        client_transport = httpx.ASGITransport(app=test_app)
        async with httpx.AsyncClient(
            transport=client_transport, base_url="http://local.test"
        ) as test_client:
            yield test_client
