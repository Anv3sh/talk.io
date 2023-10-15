from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from datetime import datetime, timezone

from sqlmodel import Session

from uuid import uuid4, UUID

from pydantic import EmailStr

from typing import List

user_router = APIRouter(prefix="/users", tags=["Users"])


# User authentication and authorization
@user_router.post(
    "/signup", summary="User registration", status_code=status.HTTP_201_CREATED
)  # noqa
async def signup(data: UserAuth, session: Session = Depends(get_session)):  # noqa
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
    user_model = Users(**user_map)

    session.add(user_model)
    session.commit()

    user_url = get_user_specfic_url(user_id=user_model.user_id)
    email_user(
        email_address=user_model.email,
        name=user_model.first_name + " " + user_model.last_name,
        url=user_url,
    )  # noqa

    return {
        "details": "Signup successful, a confirmation mail is sent to your email.",  # noqa
        "is_email_verified": user_model.is_email_verified,
    }

@user_router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=LoginResponseSchema,
)  # noqa
async def login_to_get_tokens(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
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