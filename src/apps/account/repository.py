from typing import Protocol, Annotated

from fastapi import Depends

from src.apps.account.model import Account
from src.apps.account.schema import AccountReadSchema, AccountCreateSchema, AccountUpdateSchema
from src.core.db import Session, BASE_ID
from src.core.repository import BaseRepositoryProtocol, BaseRepositoryImpl

import sqlalchemy as sa


class AccountRepositoryProtocol(
    BaseRepositoryProtocol[Account, AccountReadSchema, AccountCreateSchema, AccountUpdateSchema]):
    """
    Базовый интерфейс репозитория банковских счетов.
    """

    ...

    async def list(self, id: BASE_ID) -> list[AccountReadSchema]:
        ...

    async def get_by_user_and_account_id(self, user_id: BASE_ID, account_id: BASE_ID) -> AccountReadSchema | None:
        ...


class AccountRepositoryImpl(BaseRepositoryImpl[Account, AccountReadSchema, AccountCreateSchema, AccountUpdateSchema],
                            AccountRepositoryProtocol):
    """
    Репозиторий банковских счетов.
    """

    async def list(self, id: BASE_ID) -> list[AccountReadSchema]:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.user_id == id)
            models = (await s.execute(statement)).scalars().all()
            return [self.read_schema_type.model_validate(model, from_attributes=True) for model in models]

    async def get_by_user_and_account_id(self, user_id: BASE_ID, account_id: BASE_ID) -> AccountReadSchema | None:
        async with self.session as s:
            statement = sa.select(self.model_type).where(
                self.model_type.user_id == user_id, self.model_type.id == account_id
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                return None
            return self.read_schema_type.model_validate(model, from_attributes=True)


async def get_account_repository(session: Session) -> AccountRepositoryProtocol:
    return AccountRepositoryImpl(session)


AccountRepository = Annotated[AccountRepositoryProtocol, Depends(get_account_repository)]
