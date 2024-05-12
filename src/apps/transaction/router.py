from fastapi import APIRouter, Depends

from src.apps.auth.depends import get_current_user
from src.apps.transaction.schema import TransactionReadSchema
from src.apps.transaction.use_case import TransferCreateUseCase

transaction_router = APIRouter(prefix='/transfer')


@transaction_router.post('/', response_model=TransactionReadSchema)
async def transfer(transfer_use_case: TransferCreateUseCase):
    return await transfer_use_case()
