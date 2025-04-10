from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.tron.schemas import (
    TronRequestReadListSchema,
    TronRequestReadSchema,
    TronWalletSchema,
)
from src.tron.services import TronService

tron_router = APIRouter(prefix="/tron", tags=["Кошелек Tron"])


# MARK: POST
@tron_router.post(
    "/read_info",
    summary="Получить информацию о кошельке.",
    status_code=status.HTTP_200_OK,
)
async def read_info(
    data: TronWalletSchema,
    session: AsyncSession = Depends(get_session),
) -> TronRequestReadSchema:
    """
    Получить информацию о кошельке
    """

    return await TronService.get_wallet_info(
        data=data,
        session=session,
    )


# MARK: GET
@tron_router.get(
    "/get",
    summary="Получить информацию о кошельке.",
    status_code=status.HTTP_200_OK,
)
async def get_requests(
    address: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
) -> TronRequestReadListSchema:
    """
    Получить информацию о запросах, которые были созданы по определённому адресу.
    """

    return await TronService.get_requests(
        address=address,
        offset=offset,
        limit=limit,
        session=session,
    )
