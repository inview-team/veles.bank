__all__ = ('wallet_router',)

from fastapi import APIRouter

from src.apps.wallet.use_cases.account_list_use_case import WalletListUseCase
from src.apps.wallet.use_cases.wallet_search_use_case import WalletSearchUseCase

wallet_router = APIRouter(prefix='/wallet')


@wallet_router.get('')
async def get_list_of_wallets(wallet_use_case: WalletListUseCase):
    return await wallet_use_case()


@wallet_router.get('/search')
async def search(wallet_use_case: WalletSearchUseCase):
    return await wallet_use_case()
