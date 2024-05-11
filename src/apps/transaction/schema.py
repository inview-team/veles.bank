from uuid import uuid4, UUID

from fastapi import HTTPException
from pydantic import BaseModel, Field, validator


class TransactionReadSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    sender_id: UUID
    receiver_id: UUID
    amount: float


class TransactionCreateSchema(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    amount: float


class TransactionUpdateSchema(BaseModel):
    ...


class TransferRequestSchema(BaseModel):
    from_wallet_id: UUID
    to_wallet_id: UUID
    amount: float

    @validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than zero")
        return value
