from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship
from talk.services.database.models.base import SQLModelSerializable
from talk.services.database.models.group_user_link import GroupUserLink

if TYPE_CHECKING:
    from talk.services.database.models.message import Message
    from talk.services.database.models.user import User


class Group(SQLModelSerializable, table=True):
    __tablename__ = "group"
    group_id: Optional[UUID] = Field(
        default_factory=uuid4, primary_key=True, unique=True
    )
    group_name: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc)
    )
    modified_at: datetime = Field(
        default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc)
    )
    description: str
    users: List["GroupUserLink"] = Relationship(back_populates="group")
    messages: List["Message"] = Relationship(back_populates="group")
