from fastapi import Depends, APIRouter, Query, Security
from src.orders.dependencies import initiate_order_service
from src.orders.schemas import (
    OrderOut, 
    ManyOrdersOut, 
    PurchaseOut, 
    OrderCreate,
    ManyMiniPurchaseOut,
    )
from src.orders.service import OrdersService
from src.services import handle_result
from pydantic import UUID4
from typing import Optional

router = APIRouter(tags=['orders'], prefix='/order')

@router.get(
    '/get-order',
    response_model=OrderOut
)
def get_order(
    order_id: Optional[UUID4],
    order_service: OrdersService = Security(initiate_order_service),
):
    result = order_service.get_order(order_id=order_id)
    return handle_result(result, expected_schema=OrderOut)

@router.get(
    '/get-orders',
    response_model=ManyOrdersOut
)
def get_orders(
    purchase_id: Optional[UUID4],
    order_service: OrdersService = Security(initiate_order_service),
):
    result = order_service.get_orders(purchase_id=purchase_id)
    return handle_result(result=result, expected_schema=ManyOrdersOut)

@router.get(
    '/get-purchase',
    response_model=PurchaseOut
)
def get_purchase(
    purchase_id: UUID4,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.get_purchase(purchase_id=purchase_id)
    return handle_result(result=result, expected_schema=PurchaseOut)

@router.get(
    '/get-purchases',
    response_model=ManyMiniPurchaseOut,
)
def get_purchases(
    skip: int = 0,
    limit: int = 10,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.get_purchases(skip=skip, limit=limit)
    return handle_result(result=result, expected_schema=ManyMiniPurchaseOut)

@router.post(
    '/',
    response_model=OrderOut 
)
def create_order(
    order_info: OrderCreate,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.create_order(order_info=order_info)
    return handle_result(result=result, expected_schema=OrderOut)

@router.post(
    '/purchase-initiate',
    response_model=PurchaseOut,
)
def initiate_purchase(
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.create_purchase()
    return handle_result(result=result, expected_schema=PurchaseOut)

@router.put(
    '/decrease-units',
    response_model=OrderOut
)
def decrease_order_counts(
    order_id: UUID4,
    counts: int,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.decrease_order_count(order_id=order_id, counts=counts)
    return handle_result(result=result, expected_schema=OrderOut)

@router.put(
    '/increase-units',
    response_model=OrderOut
)
def increase_order_counts(
    order_id: UUID4,
    counts: int,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.increase_order_count(order_id=order_id, counts=counts)
    return handle_result(result=result, expected_schema=OrderOut)

@router.post(
    '/check-out',
    response_model=PurchaseOut
)
def checkout_purchase(
    purchase_id: UUID4,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.checkout_purchase(purchase_id=purchase_id)
    return handle_result(result, expected_schema=PurchaseOut)
