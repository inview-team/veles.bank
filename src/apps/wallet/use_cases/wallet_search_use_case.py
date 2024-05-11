from typing import Protocol, Annotated

from fastapi import Depends

from src.apps.wallet.schema import WalletReadSchema, WalletSearchSchema
from src.apps.wallet.service import WalletServiceProtocol, WalletService


class WalletSearchUseCaseProtocol(Protocol):

    def __call__(self) -> WalletReadSchema:
        ...


class WalletSearchUseCaseImpl:
    def __init__(self, wallet_service: WalletServiceProtocol, params: WalletSearchSchema):
        self.wallet_service = wallet_service
        self.params = params

    async def __call__(self) -> WalletReadSchema:
        return await self.wallet_service.get_wallet_by_value(self.params)


async def get_wallet_search_use_case(wallet_service: WalletService, params: WalletSearchSchema) -> WalletSearchUseCaseImpl:
    return WalletSearchUseCaseImpl(wallet_service, params)

WalletSearchUseCase = Annotated[WalletSearchUseCaseProtocol, Depends(get_wallet_search_use_case)]
