from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr  # noqa


class UserAuth(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: Optional[str] = None


class UserOut(BaseModel):
    first_name: str
    last_name: str
    profile_picture: Optional[str] = None
    email: EmailStr
    is_email_verified: bool


class LoginResponseSchema(BaseModel):
    user: UserOut
    access_token: str
    refresh_token: str
    token_type: str
