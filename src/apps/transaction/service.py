from typing import Protocol, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException

from src.apps.transaction.repository import TransactionRepository
from src.apps.transaction.schema import TransactionCreateSchema, TransactionReadSchema, TransferRequestSchema
from src.apps.wallet.repository import WalletRepositoryProtocol, WalletRepository
from src.apps.wallet.schema import WalletUpdateSchema


class TransactionServiceProtocol(Protocol):
    async def create(self, transaction_create_schema: TransactionCreateSchema) -> TransactionReadSchema:
        ...

    async def transfer(self, params: TransferRequestSchema, user_id: UUID) -> TransactionReadSchema:
        ...


class TransactionServiceImpl(TransactionServiceProtocol):
    def __init__(self, transaction_repository: TransactionRepository, wallet_repository: WalletRepositoryProtocol):
        self.transaction_repository = transaction_repository
        self.wallet_repository = wallet_repository

    async def create(self, transaction_create_schema: TransactionCreateSchema) -> TransactionReadSchema:
        return await self.transaction_repository.create(transaction_create_schema)

    async def transfer(self, params: TransferRequestSchema, user_id: UUID) -> TransactionReadSchema:
        from_wallet = await self.wallet_repository.get_by_holder_id(user_id)
        to_wallet = await self.wallet_repository.get(params.to_wallet_id)
        if not to_wallet or not from_wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        if params.amount > from_wallet.balance:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        if params.to_wallet_id == from_wallet.id:
            raise HTTPException(status_code=400, detail="You can't transfer money to yourself")
        await self.wallet_repository.update(WalletUpdateSchema(id=from_wallet.id, balance=from_wallet.balance - params.amount))
        await self.wallet_repository.update(WalletUpdateSchema(id=to_wallet.id, balance=to_wallet.balance + params.amount))
        return await self.create(
            TransactionCreateSchema(sender_id=from_wallet.id, receiver_id=to_wallet.id, amount=params.amount)
        )


async def get_transaction_service(
    transaction_repository: TransactionRepository,
    wallet_repository: WalletRepository
) -> TransactionServiceProtocol:
    return TransactionServiceImpl(transaction_repository, wallet_repository)


TransactionService = Annotated[TransactionServiceProtocol, Depends(get_transaction_service)]
