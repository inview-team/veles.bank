from typing import Protocol, Annotated
from uuid import UUID

from fastapi import Depends

from src.apps.wallet.schema import WalletReadSchema, WalletMeSchema
from src.apps.wallet.service import WalletServiceProtocol, WalletService
from src.apps.auth.depends import CurrentUser
from src.apps.user.schema import UserReadSchema


class WalletGetUseCaseProtocol(Protocol):
    """
    Базовый интерфейс юз-кейса получения аккаунта по id и пользователю
    """

    async def __call__(self) -> WalletReadSchema:
        ...


class WalletGetUseCaseImpl:
    """
    Юз-кейс получения аккаунта по id и пользователю
    """

    def __init__(
        self,
        wallet_service: WalletServiceProtocol,
        user: UserReadSchema,
    ):
        self.wallet_service = wallet_service
        self.user = user

    async def __call__(self) -> WalletReadSchema:
        return await self.wallet_service.get_by_holder_id(self.user.id)


async def get_account_use_case(
    wallet_service: WalletService,
    current_user: CurrentUser,
) -> WalletGetUseCaseImpl:
    return WalletGetUseCaseImpl(wallet_service, current_user)


WalletGetUseCase = Annotated[WalletGetUseCaseProtocol, Depends(get_account_use_case)]
