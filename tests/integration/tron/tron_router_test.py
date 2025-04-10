"""Модуль для тестирования эндпоинтов `auth_router`."""

from decimal import Decimal

import httpx
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tron.models.tron import TronRequestModel
from src.tron.routers import tron_router
from src.tron.schemas import TronWalletSchema
from tests.integration.conftest import EndpointTestHelper


class TestTronRouter(EndpointTestHelper):
    """Класс для тестирования эндпоинтов `tron_router`."""

    router = tron_router

    # MARK: POST
    async def test_read_info_route(
        self,
        session: AsyncSession,
        async_test_client: httpx.AsyncClient,
        correct_tron_wallet: TronWalletSchema,
    ):
        """
        Возможно получить информацию о правильном кошельке.
        """

        response = await async_test_client.post(
            url="/tron/read_info",
            content=correct_tron_wallet.model_dump_json().encode(),
            headers={"Content-Type": "application/json"},
        )
        response_data = response.json()
        print(response_data)
        assert response.status_code == status.HTTP_200_OK
        assert response_data is not None
        assert response_data["address"] == correct_tron_wallet.address
        assert response_data["trx_balance"] is not None

        result = await session.execute(
            select(TronRequestModel).where(
                TronRequestModel.address == correct_tron_wallet.address
            )
        )
        tron_request = result.scalar_one_or_none()
        assert tron_request is not None
        assert tron_request.address == correct_tron_wallet.address
        assert tron_request.trx_balance == Decimal(response_data["trx_balance"])

    # MARK: GET
    async def test_get_wallet_requests(
        self,
        async_test_client: httpx.AsyncClient,
        correct_tron_wallet: TronWalletSchema,
    ):
        """
        Тест на получение списка запросов с пагинацией.
        """

        await async_test_client.post(
            url="/tron/read_info",
            content=correct_tron_wallet.model_dump_json().encode(),
            headers={"Content-Type": "application/json"},
        )

        response = await async_test_client.get(
            url="/tron/get",
            params={"address": correct_tron_wallet.address, "limit": 10, "offset": 0},
        )

        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert "items" in response_data
        assert "total" in response_data
        assert len(response_data["items"]) > 0
        assert all(
            item["address"] == correct_tron_wallet.address
            for item in response_data["items"]
        )
