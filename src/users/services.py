from sqlalchemy.orm import Session
from src.users.crud import UserCrud
from src.users.schemas import UserCreate, UserOut, ManyUsersOut
from src.exceptions import GeneralException
from typing import Union
from src.services import ServiceResult
from src.config import Settings

class UserService:
    def __init__(self, requesting_user:UserOut, db: Session, app_settings: Settings) -> None:
        self.user_crud = UserCrud(db=db)
    
    def CreateUser(
        self,
        user_info: UserCreate
    )->Union[ServiceResult, Exception]:
        try:
            print(user_info.is_admin)
            db_user = self.user_crud.create_user(
                user_name=user_info.user_name,
                password=user_info.password,
                is_admin=user_info.is_admin
            )
            return ServiceResult(UserOut.model_validate(db_user.__dict__), success=True)
        except Exception as raised_exception:
            return ServiceResult(data={},exception=raised_exception,success=False)

    def GetUser(
        self,
        user_name: str
    )->Union[ServiceResult, Exception]:
        try:
            db_user = self.user_crud.get_user_by_username(username=user_name)
            return ServiceResult(UserOut.model_validate(db_user.__dict__), success=True)
        except Exception as raised_exception:
            return ServiceResult(data={},exception=raised_exception, success=False)
    
    def GetUsers(
        self,
        is_admin: Union[bool] = None,
    )->Union[ServiceResult, Exception]:
        try:
            db_users = self.user_crud.get_users(is_admin=is_admin)
            users_dict = {
                'users':[UserOut.model_validate(db_user.__dict__) for db_user in db_users]
            }
            
            return ServiceResult(ManyUsersOut.model_validate(users_dict), success=True)
        except Exception as raised_exception:
            return ServiceResult(data={},exception=raised_exception, success=False)   