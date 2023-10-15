from uuid import UUID, uuid4

from typing import Optional, Dict, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

from datetime import datetime, timezone
import sqlalchemy as sa

from backend.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from backend.database.models.pfp import PFP

class User(SQLModelSerializable, table=True):
    user_id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    first_name: str
    last_name: str
    password: Optional[str] = None
    email: str = Field(unique=True)
    pfp: Optional["PFP"] = Relationship(back_populates="user")
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
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False),
    )