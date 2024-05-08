from typing import Annotated, Self
from uuid import UUID

from fastapi import Depends
import sqlalchemy as sa

from src.apps.auth.model import AuthToken
from src.apps.auth.schema import AuthReadSchema, AuthCreateSchema, AuthUpdateSchema
from src.core.db import Session
from src.core.repository import BaseRepositoryProtocol, BaseRepositoryImpl


class AuthRepositoryProtocol(BaseRepositoryProtocol[AuthToken, AuthReadSchema, AuthCreateSchema, AuthUpdateSchema]):
    """
    Базовый интерфейс репозитория токена аутентификации
    """

    async def get_by_user_id(self: Self, user_id: UUID, token_type: str) -> AuthReadSchema | None:
        ...

    async def delete_by_type_user_id(self, user_id: UUID, token_type: str) -> None:
        ...

    async def get_by_token(self, value: str, type: str) -> AuthReadSchema | None:
        ...


class AuthRepositoryImpl(
    BaseRepositoryImpl[AuthToken, AuthReadSchema, AuthCreateSchema, AuthUpdateSchema], AuthRepositoryProtocol
):
    """
    Репозиторий токена аутентификации
    """

    async def get_by_user_id(self: Self, user_id: UUID, token_type: str) -> AuthReadSchema | None:
        async with self.session as s:
            statement = sa.select(self.model_type).where(
                self.model_type.user_id == user_id,
                self.model_type.type == token_type)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                return None
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def delete_by_type_user_id(self, user_id: UUID, token_type: str) -> None:
        async with self.session as s:
            statement = sa.delete(self.model_type).where(
                self.model_type.user_id == user_id,
                self.model_type.type == token_type
            )
            await s.execute(statement)
            await s.commit()

    async def get_by_token(self, value: str, type: str) -> AuthReadSchema | None:
        async with self.session as s:
            statement = sa.select(self.model_type).where(
                self.model_type.token == value, self.model_type.type == type
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                return None
            return self.read_schema_type.model_validate(model, from_attributes=True)


async def get_auth_repository(session: Session) -> AuthRepositoryProtocol:
    return AuthRepositoryImpl(session)


AuthRepository = Annotated[AuthRepositoryProtocol, Depends(get_auth_repository)]
