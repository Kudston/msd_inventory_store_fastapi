from sqlalchemy.orm import Session
from src.users.schemas import UserOut, UserInDb
from src.products.crud import ProductsCrud
from src.products.schemas import ProductCreate, ProductOut, ManyProductsOut, ProductUpdate
from src.services import ServiceResult
from typing import Union

class ProductService:
    def __init__(self, db:Session, requesting_user:UserInDb) -> None:
        self.crud = ProductsCrud(db)
        self.requesting_user = requesting_user

    def create_product(
        self,
        product_info: ProductCreate
    )->Union[ServiceResult,Exception]:
        try:
            db_product = self.crud.create_product(
                title=product_info.title,
                category=product_info.category,
                units=product_info.units,
                price=product_info.price,
                created_by_id=self.requesting_user.id,
            )
            return ServiceResult(ProductOut.model_validate(db_product.__dict__), success=True)
        except Exception as raised_exception:
            return ServiceResult(data="", exception=raised_exception, success=False)
        
    def get_products(
        self,
        min_left=None,
        max_left=None,
        skip: int = 0,
        limit: int = 10,
        order_by: str = "date_modified",
        order_direction: str = "desc",
    )->Union[ServiceResult, Exception]:
        try:
            db_products = self.crud.get_products(
                min_left=min_left,
                max_left=max_left,
                skip=skip,
                limit=limit,
                order_by=order_by,
                order_direction=order_direction,
            )
            products = {
                "products":[ProductOut.model_validate(product.__dict__) for product in db_products]
            }

            return ServiceResult(ManyProductsOut.model_validate(products), success=True)
        except Exception as raised_exception:
            return ServiceResult(data="",success=False, exception=raised_exception)
    
    def get_product(
        self,
        product_title:str
    )->Union[ServiceResult, Exception]:
        try:
            db_product = self.crud.get_product(product_title=product_title)
            return ServiceResult(ProductOut.model_validate(db_product.__dict__), success=True)
        except Exception as raised_exception:
            return ServiceResult("", False, exception=raised_exception)
        
    def update_product(
        self,
        product_title: str,
        product_update_info: ProductUpdate,
    )->Union[ServiceResult, Exception]:
        try:
            db_product = self.crud.update_product(
                product_title=product_title,
                new_title=product_update_info.title,
                category=product_update_info.category,
                units=product_update_info.units,
                price=product_update_info.price,
                )
            return ServiceResult(ProductOut.model_validate(db_product.__dict__), success=True)
        except Exception as raised_exception:
            return ServiceResult("", success=False, exception=raised_exception)
    
    def delete_product(
        self,
        title
    )->Union[ServiceResult, Exception]:
        try:
            counts_deleted = self.crud.delete_product(title)
            return ServiceResult(counts_deleted, success=True)
        except Exception as raised_exception:
            return ServiceResult("", success=False, exception= raised_exception)