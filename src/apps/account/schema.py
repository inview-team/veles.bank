from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AccountReadSchema(BaseModel):
    id: UUID
    balance: float
    type: str
    number: str
    status: bool
    user_id: UUID


class AccountSmallReadSchema(BaseModel):
    id: UUID
    type: str
    number: str


class AccountCreateSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    number: str
    status: bool
    user_id: UUID


class AccountUpdateSchema(BaseModel):
    id: UUID
    type: str
    balance: float
    status: bool
