from sqlmodel import Session

from typing import Union

from backend.database.models.user import User

def get_user_by_email(
    db: Session, email: str, object: bool = False
) -> Union[User, None]:  # noqa
    db_user = db.query(User).filter(User.email == email).first()
    if object:
        return db_user
    return Users.from_orm(db_user) if db_user else None  # type: ignore