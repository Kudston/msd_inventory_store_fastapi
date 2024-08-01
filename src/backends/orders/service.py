from sqlalchemy.orm import Session
from src.backends.orders.schemas import (
    OrderCreate, 
    OrderOut, 
    ManyOrdersOut, 
    CartOut, 
    MiniCartOut, 
    ManyMiniCartOut,
    ProductOut,
    )
from src.backends.utils import OrderBy, OrderDirection
from src.backends.services import ServiceResult
from typing import Union
from src.backends.orders.crud import OrdersCrud
from src.backends.users.schemas import UserOut
from sqlalchemy import UUID

class OrdersService:
    def __init__(self, db:Session, requesting_user: UserOut) -> None:
        self.crud: OrdersCrud = OrdersCrud(db=db)
        self.requesting_user = requesting_user

    def validate_order(self, order_object):
        order_obj = order_object.__dict__
        order_obj['product'] = ProductOut.model_validate(order_obj['product'].__dict__)
        return OrderOut.model_validate(order_obj)
    
    def create_order(
        self,
        order_info: OrderCreate,
    )->Union[ServiceResult, Exception]:
        try:
            db_order = self.crud.create_order(
                product_id=order_info.product_id,
                counts=order_info.counts,
                cart_id=order_info.cart_id
            )
            return ServiceResult(self.validate_order(db_order), success=True)
        except Exception as raised_exception:
            return ServiceResult({},success=False, exception=raised_exception)
    
    def get_order(
        self,
        order_id: UUID
    )->Union[ServiceResult, Exception]:
        try:
            db_order = self.crud.get_order(order_id)
            return ServiceResult(self.validate_order(db_order), success=True)
        except Exception as raised_exception:
            return ServiceResult({},success=False, exception=raised_exception)
    

    def get_orders(
        self,
        cart_id: UUID,
        order_by: OrderBy,
        order_direction: OrderDirection,
    )->Union[ServiceResult, Exception]:
        try:
            db_orders = self.crud.get_orders(cart_id, order_by=order_by, order_direction=order_direction)
            db_orders = {
                "orders": [self.validate_order(order) for order in db_orders],
            }
            return ServiceResult(ManyOrdersOut.model_validate(db_orders), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)
    
    def update_orders_count(
        self,
        order_id: UUID,
        counts: int
    )->Union[ServiceResult, Exception]:
        try:
            db_order = self.crud.update_order_units(
                order_id=order_id,
                counts=counts,
                increase=True,
                just_assign=True
            )
            return ServiceResult(self.validate_order(db_order), success=True)
        except Exception as raised_exception:
            return ServiceResult(success=False, data={}, message=str(raised_exception))

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
            return ServiceResult(self.validate_order(db_order), success=True)
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
            return ServiceResult(self.validate_order(db_order), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)

    def create_cart(
        self,
    )->Union[ServiceResult, Exception]:
        try:
            db_cart = self.crud.create_new_cart()
            return ServiceResult(CartOut.model_validate(db_cart.__dict__), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=True, exception=raised_exception)

    def checkout_cart(
        self,
        cart_id,
    )->Union[ServiceResult, Exception]:
        try:
            db_cart = self.crud.checkout_cart(cart_id=cart_id).__dict__
            db_cart['orders'] = [OrderOut.model_validate(order) for order in db_cart['orders']]
            return ServiceResult(CartOut.model_validate(db_cart), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception= raised_exception)
    
    def get_carts(
        self,        
        order_by: OrderBy,
        order_direction: OrderDirection,
        skip: int = 0,
        limit: int = 10,
        uncleared_only: bool = False,
    )->Union[ServiceResult, Exception]:
        try:
            db_carts = self.crud.get_carts(skip=skip, limit=limit, uncleared_only=uncleared_only, order_by=order_by, order_direction=order_direction)
            
            db_carts = {
                'carts':[MiniCartOut.model_validate(cart.__dict__) for cart in db_carts]
            }
            return ServiceResult(ManyMiniCartOut.model_validate(db_carts), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)
    
    def get_cart(
        self,
        cart_id: UUID
    )->Union[ServiceResult, Exception]:
        try:
            db_cart = self.crud.get_cart(cart_id=cart_id).__dict__
            db_cart['orders'] = [self.validate_order(order) for order in db_cart['orders']]
            return ServiceResult(CartOut.model_validate(db_cart), success=True)
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)
        
    def delete_cart(
        self,
        cart_id: UUID
    )->Union[ServiceResult, Exception]:
        try:
            result = self.crud.delete_cart(cart_id)
            if result>0:
                return ServiceResult({}, success=True, message='deleted_successfully')
            else:
                return ServiceResult({}, success=True, message='An error might have occured in the system')
        except Exception as raised_exception:
            return ServiceResult({}, success=False, exception=raised_exception)
        