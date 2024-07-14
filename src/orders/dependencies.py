from fastapi import Depends
from src.dependencies import get_current_active_user
from src.orders.service import OrdersService
from src.users.schemas import UserOut
from src.database import get_db_sess, Session

def initiate_order_service(
    requesting_user: UserOut = Depends(get_current_active_user),
    db: Session = Depends(get_db_sess)
):
    order_service = OrdersService(db=db, requesting_user=requesting_user)
    return order_service
