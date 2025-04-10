from decimal import Decimal
from unittest.mock import patch

import httpx
import pytest
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

    @pytest.mark.asyncio
    @patch("tronpy.Tron.get_account")
    @patch("tronpy.Tron.get_account_balance")
    async def test_read_info_route(
        self,
        mock_get_balance,
        mock_get_account,
        session: AsyncSession,
        async_test_client: httpx.AsyncClient,
        correct_tron_wallet: TronWalletSchema,
    ):
        """
        Возможно получить информацию о правильном кошельке.
        """

        mock_get_account.return_value = {
            "net_window_size": 123456,
            "account_resource": {"energy_window_size": 654321},
        }
        mock_get_balance.return_value = Decimal("100.5")

        response = await async_test_client.post(
            url="/tron/read_info",
            json=correct_tron_wallet.model_dump(),
        )
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["address"] == correct_tron_wallet.address
        assert Decimal(response_data["trx_balance"]) == Decimal("100.5")

        result = await session.execute(
            select(TronRequestModel).where(
                TronRequestModel.address == correct_tron_wallet.address
            )
        )
        tron_request = result.scalar_one_or_none()
        assert tron_request is not None
        assert tron_request.address == correct_tron_wallet.address
        assert tron_request.trx_balance == Decimal("100.5")

    @pytest.mark.asyncio
    @patch("tronpy.Tron.get_account")
    @patch("tronpy.Tron.get_account_balance")
    async def test_get_wallet_requests(
        self,
        mock_get_balance,
        mock_get_account,
        async_test_client: httpx.AsyncClient,
        correct_tron_wallet: TronWalletSchema,
    ):
        """
        Тест на получение списка запросов с пагинацией.
        """

        mock_get_account.return_value = {
            "net_window_size": 222222,
            "account_resource": {"energy_window_size": 333333},
        }
        mock_get_balance.return_value = Decimal("42.42")

        await async_test_client.post(
            url="/tron/read_info",
            json=correct_tron_wallet.model_dump(),
        )

        response = await async_test_client.get(
            url="/tron/get",
            params={"address": correct_tron_wallet.address, "limit": 10, "offset": 0},
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()

        assert "items" in response_data
        assert response_data["total"] > 0
        assert all(
            item["address"] == correct_tron_wallet.address
            for item in response_data["items"]
        )
