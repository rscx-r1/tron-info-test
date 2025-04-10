from fastapi import HTTPException, status


class InvalidTRONAddressException(HTTPException):
    """
    Возникает, если адрес Tron кошелька неверный.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Адрес кошелька должен начинаться с символа 'T'.",
        )
        

class TronAPIException(HTTPException):
    """
    Возникает, если API Tron возвращает ошибку.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при получении информации о кошельке.",
        )


class InternalServerException(HTTPException):
    """
    Возникает, если произошла внутренняя ошибка сервера.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера.",
        )

