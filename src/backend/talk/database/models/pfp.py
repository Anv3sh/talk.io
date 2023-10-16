from uuid import UUID, uuid4

from typing import Optional, Dict, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

from datetime import datetime, timezone
import sqlalchemy as sa

from talk.database.models.base import SQLModelSerializable

if TYPE_CHECKING:
    from talk.database.models.user import User

class PFP(SQLModelSerializable, table = True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    data: bytes = Field(nullable= False)
    last_updated: Optional[datetime] = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.utcnow().replace(tzinfo=timezone.utc),
    )
    user_id: UUID = Field(foreign_key= "user.user_id")
    user: Optional["User"] = Relationship(back_populates="pfp")