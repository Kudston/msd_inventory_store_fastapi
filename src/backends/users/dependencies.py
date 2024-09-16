from uuid import uuid4

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from dependencies import get_current_active_user
from config import Settings
from database import get_db_sess
from services import get_settings
from users.models import User

from users.schemas import UserOut
from users.services import UserService

def initiate_user_service(
    current_user: UserOut = Depends(get_current_active_user),
    db: Session = Depends(get_db_sess),
    app_settings: Settings = Depends(get_settings),
):
    return UserService(requesting_user=current_user, db=db, app_settings=app_settings)


def anonymous_user():
    return UserOut(
        id=uuid4(),
        username='UnknownUser',
        is_admin=False,
    )


def initiate_anonymous_user_service(
    db: Session = Depends(get_db_sess),
    app_settings: Settings = Depends(get_settings),
    anonymous_user=Depends(anonymous_user),
):
    return UserService(requesting_user=anonymous_user, db=db, app_settings=app_settings)  # type: ignore