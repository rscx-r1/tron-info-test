"""DAO для работы с моделями src.tron.models."""

from src.dao import BaseDAO
from src.tron.models import TronRequestModel
from src.tron.schemas import TronRequestCreateSchema


class TronRequestDAO(BaseDAO[TronRequestModel, TronRequestCreateSchema, TronRequestCreateSchema]):
    """DAO для работы с моделью запросов на получение информации о Tron кошельке."""

    model = TronRequestModel
