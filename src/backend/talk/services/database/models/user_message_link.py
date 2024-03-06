from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship
from talk.services.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from talk.services.database.models import Message, User


class UserMessageLink(SQLModelSerializable, table=True):
    __tablename__ = "user_message_link"
    user_id: Optional[UUID] = Field(
        default=None, foreign_key="user.user_id", primary_key=True
    )
    message_id: Optional[UUID] = Field(
        default=None, foreign_key="message.message_id", primary_key=True
    )
    user: "User" = Relationship(back_populates="messages")
    message: "Message" = Relationship(back_populates="users")
    is_sent_by: bool = False
    is_received_by: bool = False
