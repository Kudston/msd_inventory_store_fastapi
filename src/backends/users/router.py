from uuid import UUID
from datetime import timedelta
from fastapi import APIRouter, Depends, Query, Security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from typing import Optional
from dependencies import (
    get_current_active_user,
    user_must_be_admin,
    get_db_sess,
    is_admin_token,
)
from sqlalchemy.orm import Session
from schemas import AccessToken, TokenData
from services import handle_result, success_service_result
from users import schemas
from users.dependencies import (
    initiate_anonymous_user_service,
    initiate_user_service,
    get_settings,
)

from users.schemas import (
    UserOut,
    UserCreate,
)
from security import authenticate_user, create_access_token

from users.services import UserService
from config import Settings

router = APIRouter(prefix='/users',tags=['users'])

@router.get(
    '/',
    response_model=schemas.ManyUsersOut
)
def get_users(
    only_admins: Optional[bool] = Query(
        None, description="returns only admin users."
    ),
    user_services: UserService = Security(initiate_anonymous_user_service),
):
    result = user_services.GetUsers(is_admin=only_admins)
    return handle_result(result=result, expected_schema=schemas.ManyUsersOut)

@router.get(
    '/get-user',
    response_model=UserOut
)
def get_user(
    user_name: str,
    user_service: UserService = Security(initiate_user_service),
):
    result = user_service.GetUser(user_name=user_name)
    return handle_result(result, expected_schema=UserOut)

@router.post(
    '/create-user',
    response_model=schemas.UserOut
)
def create_user(
    user_info: UserCreate,
    user_service: UserService = Security(initiate_anonymous_user_service)
):
    if user_info.is_admin:
        is_admin_token(user_info.super_admin_token)
    
    result = user_service.CreateUser(user_info=user_info)

    return handle_result(result,expected_schema=UserOut)

@router.post("/token", response_model=AccessToken)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_sess),
    app_settings: Settings = Depends(get_settings),
):
    try:
        user = authenticate_user(db, form_data.username, form_data.password)

        user_service = UserService(
            requesting_user=user, db=db, app_settings=app_settings
        )

    except Exception as raised_exception:
        raise raised_exception

    access_token_expires = timedelta(minutes=app_settings.access_code_expiring_minutes)

    access_token_data = {
        "id": str(user.id),
        "user_name":user.user_name,
        "is_admin": user.is_admin,
    }

    access_token = create_access_token(
        data=access_token_data,
        secret_key=app_settings.secret_key,
        algorithm=app_settings.algorithm,
        expires_delta=access_token_expires,
    )
    token_data = TokenData.model_validate(access_token_data)

    token = success_service_result(AccessToken.model_validate({
        "access_token":access_token,
        "token_data":token_data
        }))
    return handle_result(token, expected_schema=AccessToken)