from fastapi import Depends
from dependencies import get_current_active_user
from orders.service import OrdersService
from users.schemas import UserOut
from database import get_db_sess, Session

def initiate_order_service(
    requesting_user: UserOut = Depends(get_current_active_user),
    db: Session = Depends(get_db_sess)
):
    order_service = OrdersService(db=db, requesting_user=requesting_user)
    return order_service
