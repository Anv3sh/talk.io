from uuid import UUID, uuid4
from typing import Optional, Dict, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
import sqlalchemy as sa
from pydantic import EmailStr, BaseModel, Field

from talk.database.models.base import SQLModelSerializable


if TYPE_CHECKING:
    from talk.database.models.pfp import PFP


class Message(SQLModelSerializable):
    sender_id: UUID = Field(default_factory=uuid4, primary_key=True)
    message: Optional[str] = Field(default="")
    content_type: Optional[str] = Field(default="")
    content: Optional[bytes] = Field(default=None)
    group_id: UUID = Field(sa.ForeignKey("group.id"))
    group: Group = Relationship(back_populates="messages")

class Group(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    messages: List[Message] = Relationship(back_populates="group")


