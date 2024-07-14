from src.dependencies import get_current_active_user
from fastapi import Depends
from src.config import Settings
from src.database import get_db_sess
from src.services import get_settings
from src.users.schemas import UserOut
from sqlalchemy.orm import Session
from src.products.service import ProductService

def initiate_product_service(
    requesting_user: UserOut = Depends(get_current_active_user),
    db: Session = Depends(get_db_sess),
):
    return ProductService(db, requesting_user)

