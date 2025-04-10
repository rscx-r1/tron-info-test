"""Модели для работы с Tron кошельками."""

import uuid
from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.constants import CURRENT_UTC_TIMESTAMP
from src.database import Base

# MARK: TronRequest
class TronRequestModel(Base):
    """Модель запроса информации о Tron кошельке."""

    __tablename__ = "tron_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    address: Mapped[str] = mapped_column(comment="Адрес кошелька.")
    bandwidth: Mapped[int] = mapped_column(comment="Количество использованной пропускной способности.")
    energy: Mapped[int] = mapped_column(comment="Количество использованной энергии.")
    trx_balance: Mapped[Decimal] = mapped_column(comment="Количество TRX на кошельке.")
    created_at: Mapped[datetime] = mapped_column(
        sa.TIMESTAMP(timezone=True),
        server_default=CURRENT_UTC_TIMESTAMP,
        comment="Время создания запроса.",
    )

