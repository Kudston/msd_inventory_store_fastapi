from sqlalchemy.orm import Session
from src.orders.schemas import (
    OrderCreate, 
    OrderOut, 
    ManyOrdersOut, 
    PurchaseOut, 
    MiniPurchaseOut, 
    ManyMiniPurchaseOut
    )
from src.services import ServiceResult
from typing import Union
from src.orders.crud import OrdersCrud
from src.users.schemas import UserOut
from sqlalchemy import UUID

class OrdersService:
    def __init__(self, db:Session, requesting_user: UserOut) -> None:
        self.crud: OrdersCrud = OrdersCrud(db=db)
        self.requesting_user = requesting_user

    def create_order(
        self,
        order_info: OrderCreate,
    )->Union[ServiceResult, Exception]:
        try:
            db_order = self.crud.create_order(
                product_id=order_info.product_id,
                counts=order_info.counts,
                purchase_id=order_info.purchase_id
            )
            return ServiceResult(OrderOut.model_validate(db_order.__dict__), success=True)
        except Exception as raised_exception:
            return ServiceResult({},success=False, exception=raised_exception)
    
    def get_order(
        self,
        order_id: UUID
    )->Union[ServiceResult, Exception]:
        try:
            db_order = self.crud.get_order(order_id)
            return ServiceResult(OrderOut.model_validate(db_order.__dict__), success=True)
        except Exception as raised_exception:
            return ServiceResult({},success=False, exception=raised_exception)
        
    def get_orders(
        self,
        purchase_id: UUID,
    )->Union[ServiceResult, Exception]:
        try:
            db_orders = self.crud.get_orders(purchase_id)
            db_orders = {
                "orders": [OrderOut.model_validate(order) for order in db_orders],
            }
            return ServiceResult(ManyOrdersOut.model_validate(db_orders), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)
    
    def increase_order_count(
        self,
        order_id: UUID,
        counts: int
    )->Union[ServiceResult, Exception]:
        try:
            db_order = self.crud.update_order_units(
                order_id=order_id,
                counts=counts,
                increase=True,
            )
            return ServiceResult(OrderOut.model_validate(db_order), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)

    def decrease_order_count(
        self,
        order_id: UUID,
        counts: int
    )->Union[ServiceResult, Exception]:
        try:
            db_order = self.crud.update_order_units(
                order_id=order_id,
                counts=counts,
                increase=False,
            )
            return ServiceResult(OrderOut.model_validate(db_order), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)

    def create_purchase(
        self,
    )->Union[ServiceResult, Exception]:
        try:
            db_purchase = self.crud.create_new_purchase()
            return ServiceResult(PurchaseOut.model_validate(db_purchase.__dict__), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=True, exception=raised_exception)

    def checkout_purchase(
        self,
        purchase_id,
    )->Union[ServiceResult, Exception]:
        try:
            db_purchase = self.crud.checkout_purchase(purchase_id=purchase_id)
            return db_purchase
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception= raised_exception)
    
    def get_purchases(
        self,
        skip: int = 0,
        limit: int = 10,
    )->Union[ServiceResult, Exception]:
        try:
            db_purchases = self.crud.get_purchases(skip=skip, limit=limit)
            
            db_purchases = {
                'purchases':[MiniPurchaseOut.model_validate(purchase.__dict__) for purchase in db_purchases]
            }
            return ServiceResult(ManyMiniPurchaseOut.model_validate(db_purchases), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)
    
    def get_purchase(
        self,
        purchase_id: UUID
    )->Union[ServiceResult, Exception]:
        try:
            db_purchase = self.crud.get_purchase(purchase_id=purchase_id).__dict__
            db_purchase['orders'] = [OrderOut.model_validate(order) for order in db_purchase['orders']]
            return ServiceResult(PurchaseOut.model_validate(db_purchase), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)