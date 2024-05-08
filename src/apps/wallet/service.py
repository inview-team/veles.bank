from typing import Protocol, Annotated
from uuid import UUID

from fastapi import Depends

from src.apps.wallet.repository import WalletRepositoryProtocol, WalletRepository
from src.apps.wallet.schema import WalletReadSchema


class WalletServiceProtocol(Protocol):
    """
    Account service protocol
    """

    async def get_all_accounts(self, user_id: UUID) -> list[WalletReadSchema]:
        ...

    async def get_by_user_and_account_id(self, user_id: UUID, account_id: UUID) -> WalletReadSchema | None:
        ...


class WalletServiceImpl(WalletServiceProtocol):
    """
    Account service
    """

    def __init__(self, wallet_repository: WalletRepositoryProtocol):
        self.wallet_repository = wallet_repository

        ...

    async def get_all_wallets(self, user_id: UUID) -> list[WalletReadSchema]:
        """
        Get all accounts
        :param user_id:
        :return:
        """

        return await self.wallet_repository.list(user_id)

    async def get_by_user_and_wallet_id(self, user_id: UUID, wallet_id: UUID) -> WalletReadSchema | None:
        """
        Get wallet by user id and wallet id
        :param wallet_id:
        :param user_id: UUID
        :return: AccountReadSchema | None
        """

        return await self.wallet_repository.get_by_user_and_account_id(user_id, wallet_id)


async def get_account_service(wallet_repository: WalletRepository) -> WalletServiceProtocol:
    return WalletServiceImpl(wallet_repository)


WalletService = Annotated[WalletServiceProtocol, Depends(get_account_service)]
