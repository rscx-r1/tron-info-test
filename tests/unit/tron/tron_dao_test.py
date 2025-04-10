"""Модуль для юнит-тестирования DAO для работы с Tron."""

from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.tron.dao import TronRequestDAO
from src.tron.schemas import TronRequestCreateSchema, TronWalletSchema


class TestTronRequestDAO:
    """Класс для тестирования DAO для работы с Tron."""

    # MARK: ADD
    async def test_create_tron_request(
        self, correct_tron_wallet: TronWalletSchema, session: AsyncSession
    ):
        """
        Тест на создание записи в БД через TronRequestDAO.
        """
        request_data = TronRequestCreateSchema(
            address=correct_tron_wallet.address,
            bandwidth=1000,
            energy=2000,
            trx_balance=Decimal("100.5"),
        )

        created_request = await TronRequestDAO.add(session=session, obj_in=request_data)

        assert created_request is not None
        assert created_request.address == request_data.address
        assert created_request.bandwidth == request_data.bandwidth
        assert created_request.energy == request_data.energy
        assert created_request.trx_balance == request_data.trx_balance

    # MARK: FIND
    async def test_find_all_tron_requests(
        self, correct_tron_wallet: TronWalletSchema, session: AsyncSession
    ):
        """
        Тест на получение списка записей через TronRequestDAO.
        """

        for i in range(3):
            request_data = TronRequestCreateSchema(
                address=correct_tron_wallet.address,
                bandwidth=1000 + i,
                energy=2000 + i,
                trx_balance=Decimal(f"100.{i}"),
            )
            await TronRequestDAO.add(session=session, obj_in=request_data)

        requests = await TronRequestDAO.find_all(
            session=session, address=correct_tron_wallet.address, limit=2, offset=0
        )

        assert len(requests) == 2
        assert all(r.address == correct_tron_wallet.address for r in requests)
