from uuid import UUID, uuid4
from typing import Optional, Dict, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
import sqlalchemy as sa
from pydantic import EmailStr, BaseModel, Field
from user import User

from talk.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from talk.database.models.pfp import PFP


class Message(SQLModelSerializable):
    __tablename__ = 'messages'
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    sender_id: UUID = Field(sa.ForeignKey("user.user_id"))
    receiver_id: UUID = Field(sa.ForeignKey("user.user_id"))
    content_type: Optional[str] = Field(default="")
    content: Optional[bytes] = Field(default=None)
    sender: User = Relationship(back_populates="sent_messages", foreign_key="Message.sender_id")
    receiver: User = Relationship(back_populates="received_messages", foreign_key="Message.receiver_id")



