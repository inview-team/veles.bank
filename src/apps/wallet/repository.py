from typing import Protocol, Annotated

from fastapi import Depends

from src.apps.wallet.model import Wallet
from src.apps.wallet.schema import WalletReadSchema, WalletCreateSchema, WalletUpdateSchema
from src.core.db import Session, BASE_ID
from src.core.repository import BaseRepositoryProtocol, BaseRepositoryImpl

import sqlalchemy as sa


class WalletRepositoryProtocol(
    BaseRepositoryProtocol[Wallet, WalletReadSchema, WalletCreateSchema, WalletUpdateSchema]
):
    """
    Базовый интерфейс репозитория банковских счетов.
    """

    ...

    async def first(self, id: BASE_ID) -> WalletReadSchema:
        ...

    async def get_by_user_and_account_id(self, user_id: BASE_ID, wallet_id: BASE_ID) -> WalletReadSchema | None:
        ...

    async def get_by_user_id(self, user_id: BASE_ID) -> WalletReadSchema:
        ...

    async def get_by_holder_id(self, holder_id: BASE_ID) -> WalletReadSchema:
        ...


class WalletRepositoryImpl(
    BaseRepositoryImpl[Wallet, WalletReadSchema, WalletCreateSchema, WalletUpdateSchema], WalletRepositoryProtocol
):

    async def first(self, id: BASE_ID) -> WalletReadSchema:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.holder_id == id)
            model = (await s.execute(statement)).scalars().first()
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def get_by_user_and_account_id(self, user_id: BASE_ID, wallet_id: BASE_ID) -> WalletReadSchema | None:
        async with self.session as s:
            statement = sa.select(self.model_type).where(
                self.model_type.user_id == user_id, self.model_type.id == wallet_id
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                return None
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def get_by_user_id(self, user_id: BASE_ID) -> WalletReadSchema:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.user_id == user_id)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                return None
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def get_by_holder_id(self, holder_id: BASE_ID) -> WalletReadSchema:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.holder_id == holder_id)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                return None
            return self.read_schema_type.model_validate(model, from_attributes=True)


async def get_wallet_repository(session: Session) -> WalletRepositoryProtocol:
    return WalletRepositoryImpl(session)


WalletRepository = Annotated[WalletRepositoryProtocol, Depends(get_wallet_repository)]
