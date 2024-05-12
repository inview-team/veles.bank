from typing import Protocol, Annotated

from fastapi import Depends

from src.apps.auth.depends import CurrentUser
from src.apps.user.schema import UserMeSchema, UserReadSchema
from src.apps.user.service import UserServiceProtocol, UserService


class UserMeUseCaseProtocol(Protocol):

    async def __call__(self) -> UserMeSchema:
        ...


class UserMeUseCaseImpl:

    def __init__(self, user_service: UserServiceProtocol, user: UserReadSchema):
        self.user_service = user_service
        self.user = user

    async def __call__(self) -> UserMeSchema:
        return await self.user_service.me(self.user)


async def get_user_me_use_case(user_service: UserService, user: CurrentUser) -> UserMeUseCaseImpl:
    return UserMeUseCaseImpl(user_service, user)


UserMeUseCase = Annotated[UserMeUseCaseProtocol, Depends(get_user_me_use_case)]
