from datetime import datetime,timezone, timedelta
from typing import Any

from passlib.context import CryptContext

from sqlalchemy.orm import Session

from jose import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi import status
from exceptions import invalid_auth_credentials_exception
from users import models
from users.exceptions import UserNotFoundException

from users.schemas import UserInDb

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/token", scopes={"me": "Read information about the current user."}
)


def fake_hash_password(password: str):
    return "fakehashed" + password

def decode_token(token: str, secret_key: str, algorithm: str):
    payload = jwt.decode(
        token=token,
        key=secret_key,
        algorithms=[algorithm],
    )

    return payload


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(db: Session, username: str) -> models.User:
    
    user: models.User = db.query(models.User).filter(models.User.user_name == username).first()  # type: ignore

    if not user:
        raise UserNotFoundException(f"User with email {username} not found")

    return user


def authenticate_user(db: Session, username: str, password: str):
    user: UserInDb = get_user(db, username)

    if not verify_password(password, str(user.hashed_password)):
        raise invalid_auth_credentials_exception()

    return user

def create_access_token(
    data: dict[str, Any],
    secret_key: str,
    algorithm: str,
    expires_delta: timedelta = None,  # type: ignore
):
    to_encode: dict[str, Any] = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    
    return encoded_jwt