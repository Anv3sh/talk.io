import os
from uuid import UUID

from typing import Optional, Dict, Annotated
from datetime import timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlmodel import Session
from datetime import datetime,timedelta,timezone

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from talk.database.operations.user import get_user_by_email, update_user
from talk.database.connections import get_db_session
from talk.database.models.user import User, UserPatchModel


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = (
    os.getenv("JWT_SECRET_KEY") or "talkiosecret"
)  # should be kept secret  # noqa
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY") or "talkiosecret"  # noqa

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/talk/api/users/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)],
    db: Session = Depends(get_db_session),  # noqa
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        user_id: UUID = payload.get("sub")  # type: ignore
        token_type: str = payload.get("type")  # type: ignore

        if user_id is None or token_type:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    user = get_user_by_id(db, user_id, object=True)  # type: ignore
    if user is None:
        raise credentials_exception
    return user


def create_user_tokens(
    user_id: UUID,
    db: Session = Depends(get_db_session),
    update_last_login: bool = False,  # noqa
) -> dict:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": str(user_id)},
        expires_delta=access_token_expires,
    )

    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(
        data={"sub": str(user_id), "type": "rf"},
        expires_delta=refresh_token_expires,
    )

    # Update: last_login_at
    if update_last_login:
        update_user_last_login_at(user_id, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def create_refresh_token(
    refresh_token: str, db: Session = Depends(get_db_session)
):  # noqa
    try:
        payload = jwt.decode(
            refresh_token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        user_id: UUID = payload.get("sub")  # type: ignore
        token_type: str = payload.get("type")  # type: ignore

        if user_id is None or token_type is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",  # noqa
            )

        return create_user_tokens(user_id, db)

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from e

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=ALGORITHM,
    )


def update_user_last_login_at(
    user_id: UUID, db: Session = Depends(get_db_session)
):
    user_data = UserPatchModel(last_login_at=datetime.now(timezone.utc))  # type: ignore

    return update_user(user_id, user_data, db)


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(db,email)

    if not user:
        return None
    
    return user if verify_password(password, user.password) else None
        

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)
