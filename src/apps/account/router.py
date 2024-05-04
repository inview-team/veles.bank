__all__ = ('account_router',)

from fastapi import APIRouter

from src.apps.account.use_cases.account_list_use_case import AccountListUseCase
from src.apps.account.use_cases.account_use_case import AccountGetUseCase

account_router = APIRouter(prefix='/account')


@account_router.get('/{user_id}')
async def get_list_of_accounts(account_use_case: AccountListUseCase):
    """
    :param account_use_case:
    :return:
    """

    return await account_use_case()


@account_router.post('/{user_id}/account/{account_id}')
async def get_account_by_id(account_use_case: AccountGetUseCase):
    """
    :param account_use_case:
    :return:
    """

    return await account_use_case()
