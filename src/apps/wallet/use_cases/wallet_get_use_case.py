from typing import Protocol, Annotated
from uuid import UUID

from fastapi import Depends

from src.apps.wallet.schema import WalletReadSchema
from src.apps.wallet.service import WalletServiceProtocol, WalletService
from src.apps.auth.depends import CurrentUser
from src.apps.user.schema import UserReadSchema


class WalletGetUseCaseProtocol(Protocol):
    async def __call__(self) -> list[WalletReadSchema]:
        ...


class WalletGetUseCaseImpl:
    def __init__(
        self,
        wallet_service: WalletServiceProtocol,
        current_user: UserReadSchema,
    ):
        self.wallet_service = wallet_service
        self.user = current_user

    async def __call__(self) -> WalletReadSchema:
        return await self.wallet_service.get_all_wallets(user_id=self.user.id)


async def get_wallet_list_use_case(
    account_service: WalletService,
    current_user: CurrentUser,
) -> WalletGetUseCaseImpl:
    return WalletGetUseCaseImpl(account_service, current_user)


WalletGetUseCase = Annotated[WalletGetUseCaseProtocol, Depends(get_wallet_list_use_case)]
