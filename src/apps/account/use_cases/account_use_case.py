from typing import Protocol, Annotated
from uuid import UUID

from fastapi import Depends

from src.apps.account.repository import AccountRepositoryProtocol
from src.apps.account.schema import AccountReadSchema
from src.apps.account.service import AccountServiceProtocol, AccountService


class AccountGetUseCaseProtocol(Protocol):
    """
    Базовый интерфейс юз-кейса получения аккаунта по id и пользователю
    """

    async def __call__(self) -> AccountReadSchema:
        ...


class AccountGetUseCaseImpl:
    """
    Юз-кейс получения аккаунта по id и пользователю
    """

    def __init__(
        self,
        user_id: UUID,
        account_id: UUID,
        account_service: AccountServiceProtocol,
    ):
        self.user_id = user_id
        self.account_id = account_id
        self.account_service = account_service

    async def __call__(self) -> AccountReadSchema:
        return await self.account_service.get_by_user_and_account_id(self.user_id, self.account_id)


async def get_account_use_case(
    user_id: UUID,
    account_id: UUID,
    account_service: AccountService
) -> AccountGetUseCaseImpl:
    return AccountGetUseCaseImpl(user_id, account_id, account_service)


AccountGetUseCase = Annotated[AccountGetUseCaseProtocol, Depends(get_account_use_case)]
