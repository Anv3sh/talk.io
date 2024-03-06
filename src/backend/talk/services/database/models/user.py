from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from talk.services.database.models.base import SQLModelSerializable
from talk.services.database.models.group_user_link import GroupUserLink

if TYPE_CHECKING:
    from talk.services.database.models.group import Group
    from talk.services.database.models.message import Message
    from talk.services.database.models.user_message_link import UserMessageLink


class User(SQLModelSerializable, table=True):
    user_id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    first_name: str
    last_name: str
    password: Optional[str] = None
    email: str = Field(unique=True)
    is_email_verified: bool = Field(default=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: Optional[datetime] = Field(
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
    messages: List["UserMessageLink"] = Relationship(back_populates="user")
    groups: List["GroupUserLink"] = Relationship(back_populates="user")


class UserPatchModel(SQLModel):
    email: Optional[EmailStr] = Field()
    is_active: Optional[bool] = Field()
    is_superuser: Optional[bool] = Field()
    last_login_at: Optional[datetime] = Field()
