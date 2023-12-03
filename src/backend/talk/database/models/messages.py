from uuid import UUID, uuid4
from typing import Optional, Dict, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
import sqlalchemy as sa
from pydantic import EmailStr


if TYPE_CHECKING:
    from talk.database.models.pfp import pfp


class Message(SQLModelSerializable, table=True):
    message_id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    sender_id: UUID = Field(foreign_key="sender.sender_id")
    receiver_id: UUID = Field(foreign_key="receiver.receiver_id")
    content: str
    time: Optional[datetime] = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc),
    )
    message_recipient: Optional[bool] = Field(default=False)
    content_type: Optional[str] = Field(default="text")

    sender: Optional['Sender'] = Relationship(foreign_key=(sender_id, "Sender.sender_id"))
    receiver: Optional['Receiver'] = Relationship(foreign_key=(receiver_id, "Receiver.receiver_id"))


class Sender(SQLModelSerializable, table=True):
    sender_id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    email: EmailStr
    messages: List[Message] = Relationship(back_populates="sender")


class Receiver(SQLModelSerializable, table=True):
    receiver_id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    email: EmailStr
    received_messages: List[Message] = Relationship(back_populates="receiver")
