from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship
from talk.services.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from talk.services.database.models import Group, User


class GroupUserLink(SQLModelSerializable, table=True):
    __tablename__ = "group_user_link"
    group_id: Optional[UUID] = Field(
        default=None, foreign_key="group.group_id", primary_key=True
    )
    user_id: Optional[UUID] = Field(
        default=None, foreign_key="user.user_id", primary_key=True
    )
    user: "User" = Relationship(back_populates="groups")
    group: "Group" = Relationship(back_populates="users")
