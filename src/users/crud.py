from src.users.models import User
from sqlalchemy.orm import Session
from src.security import get_password_hash
from typing import Union

class UserCrud:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(
        self,
        user_name,
        password,
        is_admin
    ):
        try:
            user = User(
            user_name=user_name,
            hashed_password=get_password_hash(password),
            is_admin=is_admin,
            )
        
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as raised_exception:
            raise raised_exception

    def get_users(
        self,
        is_admin: Union[bool] = None
    ):
        query_result = self.db.query(User)
        if is_admin is not None:
            query_result.filter(is_admin=is_admin)
        
        return query_result.all()

    def get_user_by_username(
        self,
        username: str
    ):
        return self.db.query(User).filter(User.user_name==username).first()