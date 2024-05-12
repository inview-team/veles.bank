from typing import Protocol, Annotated

from fastapi import Depends, Body

from src.apps.wallet.schema import WalletReadSchema, WalletSearchSchema
from src.apps.wallet.service import WalletServiceProtocol, WalletService


class WalletSearchUseCaseProtocol(Protocol):

    def __call__(self) -> WalletReadSchema:
        ...


class WalletSearchUseCaseImpl:
    def __init__(self, wallet_service: WalletServiceProtocol):
        self.wallet_service = wallet_service

    async def __call__(self, params: WalletSearchSchema) -> WalletReadSchema:
        return await self.wallet_service.get_wallet_by_value(params)


async def get_wallet_search_use_case(wallet_service: WalletService) -> WalletSearchUseCaseImpl:
    return WalletSearchUseCaseImpl(wallet_service)


WalletSearchUseCase = Annotated[WalletSearchUseCaseProtocol, Depends(get_wallet_search_use_case)]
