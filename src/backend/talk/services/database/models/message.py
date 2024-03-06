from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship
from talk.services.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from talk.services.database.models.group import Group
    from talk.services.database.models.user import User
    from talk.services.database.models.user_message_link import UserMessageLink


class MessageType(str, Enum):
    text = "text"
    media_video = "media_video"
    media_image = "media_image"
    media_doc = "media_doc"


class Message(SQLModelSerializable, table=True):
    __tablename__ = "message"
    message_id: Optional[UUID] = Field(
        default_factory=uuid4, primary_key=True, unique=True
    )

    message_content: str
    message_type: MessageType = Field(default="text")
    time_sent: datetime = Field(
        default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc)
    )

    is_delivered: bool
    delivered_at: datetime = Field(
        default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc)
    )

    is_read: bool
    read_at: datetime = Field(
        default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc)
    )

    is_group_message: bool = Field(default=False)
    group_id: UUID = Field(foreign_key="group.group_id", nullable=True)

    users: List["UserMessageLink"] = Relationship(back_populates="message")
    group: "Group" = Relationship(back_populates="messages")
