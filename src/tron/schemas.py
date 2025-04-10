"""Схемы для работы с запросами на получение информации о Tron кошельке."""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from src import exceptions


# MARK: TronRequest
class TronRequestReadSchema(BaseModel):
    """
    Схема чтения запроса на получение информации о Tron кошельке.
    """

    id: uuid.UUID = Field(description="`id` запроса в БД.")
    address: str = Field(description="Адрес кошелька.")
    bandwith: int = Field(
        description="Количество использованной пропускной способности."
    )
    energy: int = Field(description="Количество использованной энергии.")
    trx_balance: Decimal = Field(description="Количество TRX на кошельке.")
    created_at: datetime = Field(description="Время создания запроса.")

    model_config = ConfigDict(from_attributes=True)


class TronRequestReadListSchema(BaseModel):
    """
    Схема чтения списка запросов на получение информации о Tron кошельке.
    """

    items: List[TronRequestReadSchema] = Field(description="Список запросов.")
    total: int = Field(description="Общее количество запросов.")

    model_config = ConfigDict(from_attributes=True)


class TronWalletSchema(BaseModel):
    """
    Схема адреса Tron кошелька
    """

    address: str = Field(description="Адрес кошелька.")

    @field_validator("address")
    def validate_address(cls, value: str) -> str:
        if not value.startswith("T"):
            raise exceptions.InvalidTRONAddressException(
                "Адрес кошелька должен начинаться с символа 'T'."
            )
        return value


class TronRequestCreateSchema(TronWalletSchema):
    """
    Схема создания запроса на получение информации о Tron кошельке.
    """

    bandwidth: int = Field(
        description="Количество использованной пропускной способности."
    )
    energy: int = Field(description="Количество использованной энергии.")
    trx_balance: Decimal = Field(description="Количество TRX на кошельке.")

    model_config = ConfigDict(from_attributes=True)
