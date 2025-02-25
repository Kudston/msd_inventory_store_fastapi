from fastapi import Depends, APIRouter, Query, Security
from orders.dependencies import initiate_order_service
from orders.schemas import (
    OrderOut, 
    ManyOrdersOut, 
    CartOut, 
    OrderCreate,
    ManyMiniCartOut,
    OrderUpdate,
    StatisticsResponseOut,
    )
from datetime import datetime
from utils import OrderDirection, OrderBy, DateRangeType
from orders.utils import StatisticsOrderBy
from orders.service import OrdersService
from services import handle_result
from pydantic import UUID4
from typing import Optional

router = APIRouter(tags=['orders'], prefix='/orders')

@router.post(
    '',
    response_model=OrderOut 
)
def create_order(
    order_info: OrderCreate,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.create_order(order_info=order_info)
    return handle_result(result=result, expected_schema=OrderOut)

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
    cart_id: Optional[UUID4],
    order_service: OrdersService = Security(initiate_order_service),
):
    result = order_service.get_orders(cart_id=cart_id)
    return handle_result(result=result, expected_schema=ManyOrdersOut)

@router.get(
    '/get-carts',
    response_model=ManyMiniCartOut,
)
def get_carts(
    skip: int = 0,
    limit: int = 10,
    order_by: OrderBy = OrderBy.date_created,
    order_direction: OrderDirection = OrderDirection.desc,
    uncleared_only: bool = Query(False, description="Only returns carts that have not been cleared."),
    order_service: OrdersService = Security(initiate_order_service),
):
    result = order_service.get_carts(
        skip=skip, 
        limit=limit, 
        uncleared_only=uncleared_only, 
        order_by=order_by,
        order_direction=order_direction,
        )
    return handle_result(result=result, expected_schema=ManyMiniCartOut)

@router.get(
        '/get-carts-statistics',
        response_model=StatisticsResponseOut,
)
def get_carts_statistics(
    skip = 0,
    limit = 100,
    end_date: datetime = datetime.now(),
    date_range_type: DateRangeType = DateRangeType.weeks,
    range_counts: int = 5,
    order_direction: OrderDirection = OrderDirection.desc,
    order_by: StatisticsOrderBy = StatisticsOrderBy.amount,
    order_service: OrdersService = Security(initiate_order_service),
):
    result = order_service.get_carts_statistics(
        date_range_type=date_range_type,
        range_counts=range_counts,
        end_date=end_date,
        skip=skip,
        limit=limit,
        order_direction=order_direction,
        order_by=order_by
    )
    return handle_result(result=result, expected_schema=StatisticsResponseOut)

@router.get(
    '/get-cart',
    response_model=CartOut
)
def get_cart(
    cart_id: UUID4,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.get_cart(cart_id=cart_id)
    return handle_result(result=result, expected_schema=CartOut)

@router.post(
    '/cart-initiate',
    response_model=CartOut,
)
def initiate_cart(
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.create_cart()
    return handle_result(result=result, expected_schema=CartOut)

@router.put(
    '/decrease-units',
    response_model=OrderOut
)
def decrease_order_counts(
    order_info: OrderUpdate,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.decrease_order_count(order_id=order_info.order_id, counts=order_info.counts)
    return handle_result(result=result, expected_schema=OrderOut)

@router.put(
    '/increase-units',
    response_model=OrderOut
)
def increase_order_counts(
    order_info: OrderUpdate,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.increase_order_count(order_id=order_info.order_id, counts=order_info.counts)
    return handle_result(result=result, expected_schema=OrderOut)

@router.put(
    '/update-units',
    response_model=OrderOut
)
def update_order_counts(
    order_id: UUID4,
    order_counts: int,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.update_orders_count(order_id=order_id, counts=order_counts)
    return handle_result(result=result, expected_schema=OrderOut)

@router.post(
    '/checkout',
    response_model=CartOut
)
def checkout_cart(
    cart_id: UUID4,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.checkout_cart(cart_id=cart_id)
    return handle_result(result, expected_schema=CartOut)

@router.delete(
    '/delete-cart',
    response_model=None
)
def delete_cart(
    cart_id: UUID4,
    order_service: OrdersService = Security(initiate_order_service)
):
    result = order_service.delete_cart(cart_id=cart_id)
    return {'detail':result.message}