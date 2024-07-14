from src.schemas import ParentPydantic
from pydantic import constr
from typing import List, Annotated, Optional
from uuid import uuid4

class UserCreate(ParentPydantic):
    user_name:str = constr(max_length=20)
    is_admin: bool = False
    password:str = constr(max_length=32)
    super_admin_token: Optional[str] = None

class UserOut(ParentPydantic):
    user_name:str = constr(max_length=20, min_length=3)
    is_admin: bool = False

class ManyUsersOut(ParentPydantic):
    users:List = List[UserOut]

class UserInDb(UserOut):
    id:uuid4 = None