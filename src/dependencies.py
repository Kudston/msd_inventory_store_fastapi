"""Dependencies"""


from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from jose import jwt, JWTError

from pydantic import ValidationError

from fastapi import Header, HTTPException, status, Depends, Security
from fastapi.security import SecurityScopes
from src.exceptions import invalid_auth_credentials_exception
from src.schemas import TokenData
from src.database import get_db_sess

from src.security import get_user, oauth2_scheme
from src.config import Settings
from src.users.schemas import UserOut


def has_admin_token_in_header(admin_access_token: str = Header()):
    """Verifies if the header has an admin token"""

    if admin_access_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin-Access-Token header invalid",
        )

def is_admin_token(
        admin_token: str,
):
    app_settings: Settings = Settings()
    if admin_token != app_settings.admin_secret_key:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Admin secret key not correct."
        )

def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_sess),
    app_settings: Settings = Depends(Settings),
):

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = invalid_auth_credentials_exception(authenticate_value)

    try:
        payload = jwt.decode(
            token=token,
            key=app_settings.secret_key,
            algorithms=[app_settings.algorithm],
        )
        
        user_name: str = payload.get('user_name', None)
        user_id: str = payload.get("id", None)  # type: ignore
        is_super_admin: bool = payload.get("is_admin", None)  # type: ignore

        if not user_name:
            raise credentials_exception
        
        token_scopes = payload.get("scopes", [])
        

        token_data = TokenData(
            id=UUID(user_id),
            user_name=user_name,
            is_admin=is_super_admin,
            scopes=token_scopes
        )
        
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = get_user(db, username=token_data.user_name)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: UserOut = Security(get_current_user, scopes=[])
):
    return current_user


def user_must_be_admin(current_user: UserOut = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return current_user