from dependencies import get_current_active_user
from fastapi import Depends
from config import Settings
from database import get_db_sess
from services import get_settings
from users.schemas import UserOut
from sqlalchemy.orm import Session
from products.service import ProductService

def initiate_product_service(
    requesting_user: UserOut = Depends(get_current_active_user),
    db: Session = Depends(get_db_sess),
):
    return ProductService(db, requesting_user)

def initiate_anonymous_product_service(
    db: Session = Depends(get_db_sess),
):
    requesting_user = UserOut(user_name="anonymous",is_admin=False)
    return ProductService(db, requesting_user)
