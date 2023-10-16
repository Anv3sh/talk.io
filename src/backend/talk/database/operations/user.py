from sqlmodel import Session
from uuid import UUID

from fastapi import HTTPException, Depends

from sqlalchemy.exc import IntegrityError

from datetime import datetime, timezone

from talk.database.models.user import User, UserPatchModel
from talk.database.connections import get_db_session

from typing import Union

def get_user_by_email(
    db: Session, email: str, object: bool = False
) -> Union[User, None]:  # noqa
    db_user = db.query(User).filter(User.email == email).first()
    if object:
        return db_user
    return User.from_orm(db_user) if db_user else None  # type: ignore


def get_user_by_id(
    db: Session, id: UUID, object: bool = False
) -> Union[User, None]:  # noqa
    db_user = db.query(User).filter(User.user_id == id).first()
    if object:
        return db_user
    return User.from_orm(db_user) if db_user else None  # type: ignore

def update_user(
    user_id: UUID,
    user: UserPatchModel,
    db: Session = Depends(get_db_session),  # noqa
) -> User:
    user_db = get_user_by_email(db, user.email)  # type: ignore
    if user_db and user_db.user_id != user_id:
        raise HTTPException(status_code=409, detail="Username already exists")

    user_db = get_user_by_id(db, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user_db, key, value)

        user_db.updated_at = datetime.now(timezone.utc)
        user_db = db.merge(user_db)
        db.commit()
        if db.identity_key(instance=user_db) is not None:
            db.refresh(user_db)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e

    return user_db