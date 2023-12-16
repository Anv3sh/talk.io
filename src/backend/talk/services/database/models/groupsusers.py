from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship
from talk.services.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from talk.services.database.models.users import User
    from talk.services.database.models.groups import Group

class GroupUser(SQLModelSerializable, table=True):
    __tablename__ = "groupsusers"
    groupuser_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, unique=True)
    group_id: int = Field(foreign_key="group.group_id", nullable=False)
    user_id: int = Field(foreign_key="user.user_id", nullable=False)

    user: "User" = Relationship(back_populates="user.user_id")
    group: "Group" = Relationship(back_populates="group.group_id")

