from typing import Protocol, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException

from src.apps.transaction.schema import TransactionReadSchema, TransferRequestSchema
from src.apps.transaction.service import TransactionServiceProtocol, TransactionService
from src.apps.wallet.repository import WalletRepositoryProtocol, WalletRepository


class TransferCreateUseCaseProtocol(Protocol):

    def __call__(self, from_wallet_id: UUID, to_wallet_id: UUID, amount: float) -> TransactionReadSchema:
        ...


class TransferCreateUseCaseImpl:

    def __init__(
            self,
            transaction_service: TransactionServiceProtocol,
            wallet_repository: WalletRepositoryProtocol,
            params: TransferRequestSchema
    ):
        self.transaction_service = transaction_service
        self.wallet_repository = wallet_repository
        self.params = params

    async def __call__(self) -> TransactionReadSchema:
        return await self.transaction_service.transfer(self.params)


async def get_transaction_create_user_case(
        transaction_service: TransactionService,
        wallet_repository: WalletRepository,
        params: TransferRequestSchema
) -> TransferCreateUseCaseImpl:
    return TransferCreateUseCaseImpl(transaction_service, wallet_repository, params)


TransferCreateUseCase = Annotated[TransferCreateUseCaseProtocol, Depends(get_transaction_create_user_case)]
