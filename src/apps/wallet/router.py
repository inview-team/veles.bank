__all__ = ('wallet_router',)

from typing import Annotated

from fastapi import APIRouter, Body, Depends

from src.apps.auth.depends import get_current_user
from src.apps.wallet.schema import WalletSearchSchema, WalletResponseSchema, WalletReadSchema
from src.apps.wallet.use_cases.account_use_case import WalletGetUseCase
from src.apps.wallet.use_cases.wallet_search_use_case import WalletSearchUseCase

wallet_router = APIRouter(prefix='/wallet')


@wallet_router.get('', response_model=WalletReadSchema)
async def get_list_of_wallets(wallet_use_case: WalletGetUseCase):
    return await wallet_use_case()


@wallet_router.get('/search', response_model=WalletResponseSchema, dependencies=[Depends(get_current_user)])
async def search(
    params: Annotated[WalletSearchSchema, Body(example={"type": "phone", "source": "wallet", "value": "+79234567892"})],
    wallet_use_case: WalletSearchUseCase
):
    return await wallet_use_case(params)
