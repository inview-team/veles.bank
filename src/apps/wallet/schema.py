from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class WalletReadSchema(BaseModel):
    id: UUID
    balance: float
    type: str
    number: str
    status: bool
    user_id: UUID | None
    company_id: UUID | None


class WalletSmallReadSchema(BaseModel):
    id: UUID
    type: str
    number: str


class WalletCreateSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: str
    number: str
    status: bool
    user_id: UUID | None
    company_id: UUID | None


class WalletUpdateSchema(BaseModel):
    id: UUID
    balance: float


class WalletSearchSchema(BaseModel):
    type: str
    source: str
    value: str
