from pydantic import BaseModel
from typing import List
from uuid import UUID

class TokenData(BaseModel):
    id: UUID
    user_name: str
    is_admin: bool
    scopes: list = []

class AccessToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    token_data: TokenData

    class Config:
        from_attributes = True

class ParentPydantic(BaseModel):
    class Config:
        from_attributes = True