from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import constants
from src.tron.schemas import TronRequestReadListSchema, TronRequestReadSchema, TronWalletSchema
from src.dependencies import get_session
from src.tron.services import TronService

auth_router = APIRouter(prefix="/tron/", tags=["Кошелек Tron"])


# MARK: POST
@auth_router.post(
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
    
    return await TronService.read_wallet_info(
        data=data,
        session=session,
    )

# MARK: GET
@auth_router.get(
    "/get",
    summary="Получить информацию о кошельке.",
    status_code=status.HTTP_200_OK,
)
async def read_info(
    data: TronWalletSchema,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
) -> TronRequestReadListSchema:
    """
    Получить информацию о запросах, которые были созданы по определённому адресу.
    """
    
    return await TronService.get_requests(
        data=data,
        offset=offset,
        limit=limit,
        session=session,
    )