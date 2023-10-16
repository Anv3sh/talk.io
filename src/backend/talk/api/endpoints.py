from sqlmodel import Session

from uuid import uuid4, UUID

from pydantic import EmailStr

from typing import List

from datetime import datetime, timezone

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from talk.api.schema import UserAuth, LoginResponseSchema
from talk.api.auth import get_password_hash, authenticate_user, create_user_tokens, get_current_user
from talk.database.connections import get_db_session
from talk.database.models.user import User
from talk.database.operations.user import get_user_by_email

user_router = APIRouter(prefix="/user", tags=["User"])


# User authentication and authorization
@user_router.post(
    "/signup", summary="User registration", status_code=status.HTTP_201_CREATED
)  # noqa
async def signup(data: UserAuth, session:Session = Depends(get_db_session)):  # noqa
    """
    User registration
    """
    user = get_user_by_email(db=session, email=data.email)

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist.",
        )

    user_map = {
        "email": data.email,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "password": get_password_hash(data.password),
        "user_id": str(uuid4()),
    }
    user_model = User(**user_map)

    session.add(user_model)
    session.commit()

    return {
        "details": "Signup successful",  # noqa
    }

@user_router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=LoginResponseSchema,
)  # noqa
async def login_to_get_tokens(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):
    if user := authenticate_user(form_data.username, form_data.password, db):
        tokens = create_user_tokens(
            user_id=user.user_id, db=db, update_last_login=True
        )  # noqa
        return {"user": user, **tokens}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@user_router.get(
    "/health",
    summary="Health check",
    status_code=status.HTTP_200_OK,
)
async def health(user: User = Depends(get_current_user)):
    return {
        "status":200,
        "body": {"message":"Health ok!"},
    }