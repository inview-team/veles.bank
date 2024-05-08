from typing import Protocol, Annotated
from uuid import UUID

from fastapi import Depends

from src.apps.wallet.schema import WalletReadSchema
from src.apps.wallet.service import WalletServiceProtocol, WalletService
from src.apps.auth.depends import CurrentUser
from src.apps.user.schema import UserReadSchema


class WalletListUseCaseProtocol(Protocol):
    """
    Базовый интерфейс юз-кейса получения списка аккаунтов
    """

    async def __call__(self) -> list[WalletReadSchema]:
        ...


class WalletListUseCaseImpl:
    """
    Реализация юз-кейса получения списка аккаунтов
    """

    def __init__(
        self,
        wallet_service: WalletServiceProtocol,
        user_id: UUID,
        current_user: UserReadSchema,
    ):
        self.wallet_service = wallet_service
        self.user_id = user_id
        self.user = current_user

    async def __call__(self) -> list[WalletReadSchema]:
        return await self.wallet_service.get_all_accounts(user_id=self.user_id)


async def get_wallet_list_use_case(
    account_service: WalletService,
    user_id: UUID,
    current_user: CurrentUser,
) -> WalletListUseCaseProtocol:
    return WalletListUseCaseImpl(account_service, user_id, current_user)


WalletListUseCase = Annotated[WalletListUseCaseProtocol, Depends(get_wallet_list_use_case)]
