from typing import TYPE_CHECKING, Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
from enum import Enum

from sqlmodel import Field, Relationship
from talk.services.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from talk.services.database.models.users import User
    from talk.services.database.models.groups import Group

class MessageType(str, Enum):
    text = "text"
    media_video = "media_video"
    media_image = "media_image"
    media_doc = "media_doc"

class Message(SQLModelSerializable, table=True):
    __tablename__ = "message"
    message_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, unique=True)
    sender_id: int = Field(foreign_key="user.user_id", nullable=False)
    reciever_id: int = Field(foreign_key="user.user_id", nullable=True)

    message_content: MessageType = Field(default="text")
    time_sent: datetime = Field(default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc))

    is_delivered: bool
    time_delivered: datetime = Field(default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc))

    is_read: bool
    time_delivered: datetime = Field(default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc))

    is_group_message: bool = Field(default=False)
    group_id: int = Field(foreign_key="group.group_id", nullable=True)

    user: "User" = Relationship(back_populates="user.user_id")
    user: "Group" = Relationship(back_populates="group.group_id")

