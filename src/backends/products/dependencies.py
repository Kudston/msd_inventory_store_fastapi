from src.backends.dependencies import get_current_active_user
from fastapi import Depends
from src.backends.config import Settings
from src.backends.database import get_db_sess
from src.backends.services import get_settings
from src.backends.users.schemas import UserOut
from sqlalchemy.orm import Session
from src.backends.products.service import ProductService

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
