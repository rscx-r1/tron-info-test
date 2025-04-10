"""Сервисный слой для работы с Tron."""

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import Tron
from tronpy.providers import HTTPProvider

from src import constants, exceptions
from src.config import project_settings
from src.tron.dao import TronRequestDAO
from src.tron.models.tron import TronRequestModel
from src.tron.schemas import (
    TronRequestCreateSchema,
    TronRequestReadListSchema,
    TronRequestReadSchema,
    TronWalletSchema,
)


class TronService:
    """Класс для работы с Tron."""

    @classmethod
    async def get_wallet_info(
        cls,
        session: AsyncSession,
        data: TronWalletSchema,
    ) -> TronRequestReadSchema:
        client = Tron(
            HTTPProvider(
                endpoint_uri=constants.TRON_API_URL,
                api_key=project_settings.TRON_API_KEY,
            )
        )

        try:
            account = client.get_account(data.address)
            balance = client.get_account_balance(data.address)

            tron_request_db = await TronRequestDAO.add(
                session=session,
                obj_in=TronRequestCreateSchema(
                    address=data.address,
                    bandwidth=account.get("data", [{}])[0].get("net_limit", 0),
                    energy=account.get("data", [{}])[0].get("energy_limit", 0),
                    trx_balance=balance,
                ),
            )
            if not tron_request_db:
                raise exceptions.InternalServerException

            return TronRequestReadSchema(
                id=tron_request_db.id,
                address=data.address,
                bandwith=tron_request_db.bandwidth,
                energy=tron_request_db.energy,
                trx_balance=tron_request_db.trx_balance,
                created_at=tron_request_db.created_at,
            )
        except Exception:
            raise exceptions.TronAPIException

    @classmethod
    async def get_requests(
        cls,
        session: AsyncSession,
        data: TronWalletSchema,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> TronRequestReadListSchema:
        tron_requests: List[TronRequestModel] = await TronRequestDAO.find_all(
            session=session,
            address=data.address,
            offset=offset,
            limit=limit,
        )

        return TronRequestReadListSchema(
            items=[
                TronRequestReadSchema.model_validate(tron_request)
                for tron_request in tron_requests
            ],
            total=len(tron_requests),
        )
