from typing import Optional, Dict

from passlib.context import CryptContext

from backend.database.operations.user import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)

    if not user:
        return None
    
    return user if verify_password(password, user.password) else None
        

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)
