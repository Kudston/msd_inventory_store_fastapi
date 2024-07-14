from fastapi import APIRouter, Query, Depends, Response
from src.products.schemas import (
    ProductOut, 
    ProductCreate, 
    ManyProductsOut, 
    ProductUpdate,
    )
from src.products.service import ProductService
from src.products.dependencies import initiate_product_service
from typing import Optional
from src.utils import OrderBy, OrderDirection
from src.services import handle_result

router = APIRouter(prefix='/products', tags=['products'])

@router.get(
    '/',
    response_model= ManyProductsOut
)
def get_products(
    skip: int = Query(0),
    limit: int = Query(10),
    min_left: Optional[int] = Query(None, description="Only products with this minimum units"),
    max_left: Optional[int] = Query(None, description="Only products with this max units"),
    order_by: OrderBy = Query(OrderBy.date_created),
    order_direction: OrderDirection = Query(OrderDirection.desc),
    product_service: ProductService = Depends(initiate_product_service),
):
    result = product_service.get_products(
        min_left=min_left,
        max_left=max_left,
        skip=skip,
        limit=limit,
        order_by=order_by,
        order_direction=order_direction
    )
    return handle_result(result, expected_schema=ManyProductsOut)

@router.get(
    '/product',
    response_model=ProductOut,
)
def get_product(
    title: str,
    product_service: ProductService = Depends(initiate_product_service),
):
    result = product_service.get_product(product_title=title)
    return handle_result(result, expected_schema=ProductOut)

@router.post(
    '/product-create',
    response_model=ProductOut,
)
def create_product(
    product_info: ProductCreate,
    product_service: ProductService = Depends(initiate_product_service),
):
    result = product_service.create_product(product_info=product_info)
    return handle_result(result, expected_schema=ProductOut)

@router.put(
    '/product-update',
    response_model=ProductOut,
)
def update_product(
    title: str,
    product_info: ProductUpdate,
    product_service: ProductService = Depends(initiate_product_service),
):
    result = product_service.update_product(
        product_title=title,
        product_update_info=product_info
        )
    return handle_result(result, expected_schema=ProductOut)

@router.delete(
    '/product-delete',
    response_model=None
)
def delete_product(
    title: str,
    product_service: ProductService = Depends(initiate_product_service)
):
    result = product_service.delete_product(title=title)
    return Response(result)