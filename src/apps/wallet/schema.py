from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class WalletReadSchema(BaseModel):
    id: UUID
    balance: float
    type: str
    number: str
    status: bool
    user_id: UUID


class WalletSmallReadSchema(BaseModel):
    id: UUID
    type: str
    number: str


class WalletCreateSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    number: str
    status: bool
    user_id: UUID


class WalletUpdateSchema(BaseModel):
    id: UUID
    type: str
    balance: float
    status: bool
