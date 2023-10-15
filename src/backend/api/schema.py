from pydantic import (
    BaseModel,
    EmailStr,
)  # noqa
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class UserAuth(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: Optional[str] = None