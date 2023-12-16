from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship
from talk.services.database.models.base import SQLModelSerializable

class GroupUserLink(SQLModelSerializable, table=True):
    __tablename__ = "groupsusers"
    group_id: Optional[int] = Field(default=None, foreign_key="group.group_id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id", primary_key=True)

