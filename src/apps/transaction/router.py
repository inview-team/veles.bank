from fastapi import APIRouter, Depends

from src.apps.auth.depends import get_current_user
from src.apps.transaction.use_case import TransferCreateUseCase

transaction_router = APIRouter(prefix='/transfer')


@transaction_router.post('/', dependencies=[Depends(get_current_user)])
async def transfer(transfer_use_case: TransferCreateUseCase):
    return await transfer_use_case()