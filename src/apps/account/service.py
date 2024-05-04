from typing import Protocol, Annotated
from uuid import UUID

from fastapi import Depends

from src.apps.account.repository import AccountRepositoryProtocol, AccountRepository
from src.apps.account.schema import AccountReadSchema


class AccountServiceProtocol(Protocol):
    """
    Account service protocol
    """

    async def get_all_accounts(self, user_id: UUID) -> list[AccountReadSchema]:
        ...

    async def get_by_user_and_account_id(self, user_id: UUID, account_id: UUID) -> AccountReadSchema | None:
        ...

class AccountServiceImpl(AccountServiceProtocol):
    """
    Account service
    """

    def __init__(self, account_repository: AccountRepositoryProtocol):
        self.account_repository = account_repository

        ...

    async def get_all_accounts(self, user_id: UUID) -> list[AccountReadSchema]:
        """
        Get all accounts
        :param user_id:
        :return:
        """

        return await self.account_repository.list(user_id)

    async def get_by_user_and_account_id(self, user_id: UUID, account_id: UUID) -> AccountReadSchema | None:
        """
        Get account by user id and account id
        :param user_id: UUID
        :param account_id: UUID
        :return: AccountReadSchema | None
        """

        return await self.account_repository.get_by_user_and_account_id(user_id, account_id)

async def get_account_service(account_repository: AccountRepository) -> AccountServiceProtocol:
    return AccountServiceImpl(account_repository)


AccountService = Annotated[AccountServiceProtocol, Depends(get_account_service)]
