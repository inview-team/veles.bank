from typing import Protocol, Annotated
from uuid import UUID

from fastapi import Depends

from src.apps.account.schema import AccountReadSchema
from src.apps.account.service import AccountServiceProtocol, AccountService


class AccountListUseCaseProtocol(Protocol):
    """
    Базовый интерфейс юз-кейса получения списка аккаунтов
    """

    async def __call__(self) -> list[AccountReadSchema]:
        ...


class AccountListUseCaseImpl:
    """
    Реализация юз-кейса получения списка аккаунтов
    """

    def __init__(
        self,
        account_service: AccountServiceProtocol,
        user_id: UUID,
    ):
        self.account_service = account_service
        self.user_id = user_id

    async def __call__(self) -> list[AccountReadSchema]:
        return await self.account_service.get_all_accounts(user_id=self.user_id)


async def get_account_list_use_case(
    account_service: AccountService,
    user_id: UUID,
) -> AccountListUseCaseProtocol:
    return AccountListUseCaseImpl(account_service, user_id)


AccountListUseCase = Annotated[AccountListUseCaseProtocol, Depends(get_account_list_use_case)]
