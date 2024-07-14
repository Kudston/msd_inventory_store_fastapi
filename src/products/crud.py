from src.products.models import Products
from sqlalchemy.orm import Session
from src.utils import OrderDirection,OrderBy
from src.products.enumerations import ProductsCategories
from typing import Union
from sqlalchemy import asc, desc
from src.users.models import User

class ProductsCrud:
    def __init__(self, db:Session) -> None:
        self.db = db

    def get_products(
        self,
        min_left: Union[int,None] = None,
        max_left: Union[int,None] = None,
        skip: int = 0,
        limit: int = 100,
        order_by: OrderBy = OrderBy.date_modified,
        order_direction: OrderDirection = OrderDirection.desc,
    ):
        try:
            products = self.db.query(Products)

            if min_left:
                products = products.filter(Products.units>=min_left)

            if max_left:
                products = products.filter(Products.units<=max_left)
            
            order_by_object = Products.date_modified

            if order_by==OrderBy.date_created.value:
                order_by_object = Products.date_created
            
            order_by_object = (order_by_object.desc() if (order_direction.value==OrderDirection.desc.value) 
                               else order_by_object.asc())

            products = products.order_by(order_by_object).offset(skip).limit(limit).all()
            
            return products
        except Exception as raised_exception:
            raise raised_exception
        
    def create_product(
        self,
        title,
        category,
        units,
        price,
        created_by_id,
    ):
        try:
            db_product = Products(
                title = title,
                category = category,
                units = units,
                price = price,
                creator_id = created_by_id
            )
            
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            return db_product
        except Exception as raised_exception:
            raise raised_exception
        
    def get_product(
        self,
        product_title
    ):
        return self.db.query(Products).filter(Products.title==product_title).first()

    def update_product(
        self,
        product_title,
        new_title: Union[str] = None,
        category: Union[ProductsCategories] = None,
        units: Union[int] = None,
        price: Union[float] = None,
    ):
        try:
            product = self.get_product(product_title=product_title)
            
            if not product:
                raise Exception(f"Product with title {product_title} does not exist")
            
            if new_title is not None:
                setattr(product, 'title', new_title)

            if category is not None:
                setattr(product, 'category', category)

            if units is not None:
                setattr(product, 'units', product.units+units)

            if price is not None:
                setattr(product, 'price', price)
            
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            print(product)
            return product
        except Exception as raised_exception:
            raise raised_exception
    
    def delete_product(
        self,
        product_title
    ):
        try:
            product = self.db.query(Products).filter(Products.title==product_title)
            
            res = product.delete(synchronize_session=False)
            self.db.commit()
            return res
        except Exception as raised_exception:
            raise raised_exception