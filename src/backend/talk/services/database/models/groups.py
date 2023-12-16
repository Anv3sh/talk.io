from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlmodel import Field, Relationship
from talk.services.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from talk.services.database.models.groupsusers import GroupUser

class Group(SQLModelSerializable, table=True):
    __tablename__ = "group"
    group_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, unique=True)
    group_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc))
    description: str

    groupuser: "GroupUser" = Relationship(back_populates="groupsusers.groupuser_id")

