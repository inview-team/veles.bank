from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.apps.user.schema import UserReadSchema


class AuthReadSchema(BaseModel):
    token: str
    type: str
    user_id: UUID


class AuthGenerateSchema(BaseModel):
    sub: str
    email: str
    exp: datetime


class AuthCreateSchema(BaseModel):
    token: str
    type: str
    user_id: UUID


class AuthUpdateSchema(BaseModel):
    ...


class AuthSmallReadSchema(BaseModel):
    access: str
    refresh: str


class LoginResponseSchema(UserReadSchema, AuthSmallReadSchema):
    ...


class RefreshRequestSchema(BaseModel):
    refresh: str
