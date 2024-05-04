from typing import Protocol, Annotated, Self

from fastapi import Depends
import sqlalchemy as sa
from src.apps.user.model import User
from src.apps.user.schema import UserReadSchema, UserCreateSchema, UserUpdateSchema
from src.core.db import Session
from src.core.repository import BaseRepositoryProtocol, BaseRepositoryImpl


class UserRepositoryProtocol(BaseRepositoryProtocol[User, UserReadSchema, UserCreateSchema, UserUpdateSchema]):
    """
    Базовый интерфейс репозитория пользователя.
    """

    async def get_user_by_email(self, email: str) -> UserReadSchema | None:
        ...


class UserRepositoryImpl(
    BaseRepositoryImpl[User, UserReadSchema, UserCreateSchema, UserUpdateSchema], UserRepositoryProtocol
):
    """
    User repository
    """

    async def get_user_by_email(self, email: str) -> UserReadSchema | None:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.email == email)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                return None
            return self.read_schema_type.model_validate(model, from_attributes=True)


async def get_user_repository(session: Session) -> UserRepositoryProtocol:
    return UserRepositoryImpl(session)


UserRepository = Annotated[UserRepositoryProtocol, Depends(get_user_repository)]