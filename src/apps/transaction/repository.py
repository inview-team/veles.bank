from typing import Protocol, Annotated

from fastapi import Depends

from src.apps.transaction.model import Transaction
from src.apps.transaction.schema import TransactionReadSchema, TransactionCreateSchema, TransactionUpdateSchema
from src.core.db import Session
from src.core.repository import BaseRepositoryProtocol, BaseRepositoryImpl


class TransactionRepositoryProtocol(BaseRepositoryProtocol[Transaction, TransactionReadSchema, TransactionCreateSchema, TransactionUpdateSchema]):
    """
    Transaction Repository Protocol
    """
    ...


class TransactionRepositoryImpl(
    BaseRepositoryImpl[Transaction, TransactionReadSchema, TransactionCreateSchema, TransactionUpdateSchema], TransactionRepositoryProtocol
):
    """
    Transaction Repository Implementation
    """

    ...


async def get_transaction_repository(session: Session) -> TransactionRepositoryProtocol:
    return TransactionRepositoryImpl(session)


TransactionRepository = Annotated[TransactionRepositoryProtocol, Depends(get_transaction_repository)]
