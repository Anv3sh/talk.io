from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, List
from uuid import UUID, uuid4

import sqlalchemy as sa
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from talk.services.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from talk.services.database.models.pfp import PFP
    from talk.services.database.models.groups import Group
    from talk.services.database.models.messages import Message
    from talk.services.database.models.groupsuserslink import GroupUserLink


class User(SQLModelSerializable, table=True):
    __tablename__ = "user"
    user_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, unique=True)
    first_name: str
    last_name: str
    password: Optional[str] = None
    email: str = Field(unique=True)
    is_email_verified: bool = Field(default=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    create_at: Optional[datetime] = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc),
    )
    updated_at: Optional[datetime] = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc),
    )
    last_login_at: Optional[datetime] = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=True),
    )

    pfp: Optional["PFP"] = Relationship(back_populates="user")
    messages: List[Message] = Relationship(back_populates="user")
    groups: List[Group] = Relationship(back_populates="users", link_model=GroupUserLink)


class UserPatchModel(SQLModel):
    email: Optional[EmailStr] = Field()
    is_active: Optional[bool] = Field()
    is_superuser: Optional[bool] = Field()
    last_login_at: Optional[datetime] = Field()
