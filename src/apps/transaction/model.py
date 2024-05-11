
from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base, BASE_ID


class Transaction(Base):
    id: Mapped[BASE_ID] = mapped_column(primary_key=True, default=uuid4)
    amount: Mapped[float]
    sender_id: Mapped[BASE_ID]
    receiver_id: Mapped[BASE_ID]
    type: Mapped[str]

