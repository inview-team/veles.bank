import uuid
from uuid import UUID

from pydantic import BaseModel, Field


class UserReadSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    phone_number: str


class UserRegistrySchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    password2: str


class UserCreateSchema(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str


class UserUpdateSchema(BaseModel):
    ...


class LoginSchema(BaseModel):
    email: str
    password: str


class UserResponseSchema(UserReadSchema):
    access: str


class UserMeSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
