__all__ = ('wallet_router',)

from fastapi import APIRouter

from src.apps.wallet.use_cases.account_list_use_case import WalletListUseCase
from src.apps.wallet.use_cases.account_use_case import WalletGetUseCase

wallet_router = APIRouter(prefix='/wallet')


@wallet_router.get('/{user_id}')
async def get_list_of_wallets(wallet_use_case: WalletListUseCase):
    """
    :param wallet_use_case:
    :return:
    """

    return await wallet_use_case()


@wallet_router.get('/{user_id}/wallet/{wallet_id}')
async def get_wallet_by_id(wallet_use_case: WalletGetUseCase):
    """
    :param wallet_use_case:
    :return:
    """

    return await wallet_use_case()
