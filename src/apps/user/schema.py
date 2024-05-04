from uuid import UUID

from pydantic import BaseModel


class UserReadSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str


class UserRegistrySchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    password2: str


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    ...


class LoginSchema(BaseModel):
    email: str
    password: str
