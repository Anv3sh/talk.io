from sqlmodel import Session
from uuid import UUID

from fastapi import HTTPException, Depends

from sqlalchemy.exc import IntegrityError

from datetime import datetime, timezone

from talk.database.models.user import User
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
    db:Session, id: UUID
):
    try:    
        user_db = db.get(User,id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found!")
    user_db.updated_at = datetime.now(timezone.utc)
    user_db = db.merge(user_db)
    db.commit()
    if db.identity_key(instance=user_db) is not None:
        db.refresh(user_db)