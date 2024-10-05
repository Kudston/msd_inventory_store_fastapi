from sqlalchemy.orm import Session
from utils import OrderBy, OrderDirection
from orders.models import Carts,Orders
from products.models import Products
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import sum
from sqlalchemy import and_
from datetime import datetime, timezone, timedelta
import pandas as pd

class OrdersCrud:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_order(
        self,
        product_id: UUID,
        counts: int,
        cart_id: UUID
    ):
        try:
            db_product: Products = self.db.query(Products).filter(Products.id==product_id).first()
            db_order = Orders(
                product_id = product_id,
                cart_id = cart_id,
                counts = counts,
                total_amount = round(counts*db_product.price, 2)
            )

            db_product = self.db.query(Products).filter(Products.id==product_id).first()
            
            if db_product.units - counts<0:
                raise Exception('Units Specified Greater than remaining product units.')

            setattr(db_product, 'units', db_product.units-counts)

            self.db.add(db_order)
            self.db.add(db_product)

            self.db.commit()

            self.db.refresh(db_order)
            return db_order
        except Exception as raised_exception:
            raise raised_exception
    
    def get_order(
        self,
        order_id: UUID
    ):
        return self.db.query(Orders).filter(Orders.id==order_id).first()
    
    def get_orders(
        self,
        cart_id: UUID,
        order_by: OrderBy,
        order_direction: OrderDirection,
    ):
        try:
            orders = self.db.query(Orders).filter(Orders.cart_id==cart_id)
            order_object = Orders.date_created
            if order_by == OrderBy.date_modified.value:
                order_object = Orders.date_modified
            order_object = order_object.desc()
            if order_direction == OrderDirection.asc.value:
                order_object = order_object.asc()
            
            orders = orders.order_by(order_object).all()
            
            return orders
        except Exception as raised_exception:
            raise raised_exception
    
    def update_order_units(
        self,
        order_id: UUID,
        counts: int,
        increase: bool,
        just_assign: bool = False
    ):
        try:
            db_order = self.get_order(order_id=order_id)
            db_product = self.db.query(Products).filter(Products.id==db_order.product_id).first()

            if increase:
                if counts>db_order.product.units:
                    raise Exception('New quantity surpass available quantity.')
                setattr(db_order, "counts", db_order.counts+counts)
                setattr(db_product, "units", db_product.units-counts)

            elif not increase:
                if db_order.counts - counts<0:
                    raise Exception('counts cannot be less than available quantity.')
                if db_order.counts>counts:
                    raise Exception('You are requesting to decrease the order past it existing value.')
                
                setattr(db_order, "counts", db_order.counts-counts)
                setattr(db_product, "units", db_product.units+counts)

            if just_assign:
                if counts<0:
                    raise Exception('counts cannot be less than 0')
                if counts>db_order.product.units + db_order.counts:
                    raise Exception("New Counts Surpass the available quantity for this product.")
                
                new_product_count = ((counts - db_order.counts) if
                                     (counts>db_order.counts) else (db_order.counts-counts))
                setattr(db_product, 'units', db_product.units + new_product_count if
                        (counts>db_order.counts) else db_product - new_product_count)
                setattr(db_order, "counts", counts)

            self.db.add(db_order)
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_order)
            
            return db_order
        except Exception as raised_exception:
            raise raised_exception
        
    ##cart functions
    def create_new_cart(self):
        try:
            db_cart = Carts()

            self.db.add(db_cart)
            self.db.commit()
            self.db.refresh(db_cart)
            
            return db_cart
        except Exception as raised_exception:
            print(str(raised_exception))
            raise raised_exception
    
    def get_cart(
        self,
        cart_id:UUID
    ):
        db_cart = self.db.query(Carts).filter(Carts.id==cart_id).first()

        return db_cart
    
    def get_carts_statistics(
        self,
        start_date: datetime,
        days_back: int,
        skip,
        limit,
        order_direction: OrderDirection = OrderDirection.desc,
        order_by: OrderBy = OrderBy.date_created,
    ):
        try:
            end_date = start_date - timedelta(days=days_back)

            #if no days specified it means we only need record of that day
            if days_back==0:
                end_date = datetime(start_date.year, start_date.month, start_date.day)
            
            carts = self.db.query(Carts)

            carts = carts.filter(
                and_(
                    Carts.date_created>=end_date,
                    Carts.date_created<=start_date,
                )
            )
            #Set ordering by
            order_object = Carts.date_created
            if order_by==OrderBy.date_modified:
                order_object = Carts.date_modified
            
            #Set ordering direction
            order_object = order_object.desc()
            if order_direction==OrderDirection.asc:
                order_object = order_object.asc()
            
            carts = carts.order_by(order_object).offset(skip).limit(limit).all()

            ##get statistic on product level
            # products_list = []

            for cart in carts:
                cart_orders = cart.orders

                for order in cart_orders:
                    prod_information = {}
                    order_product = order['product']

                    print(order_product)
            #         ##assign the 
            #         prod_information['cartId'] = cart['id']
            #         prod_information['pd_id'] = order_product['id']
            #         prod_information['pd_name'] = order_product['title']
            #         prod_information['pd_price'] = order_product['price']
            #         prod_information['pd_quantity'] = order['counts']
            #         products_table = products_list.append(prod_information)
            
            # print(products_list)
            # products_table = pd.DataFrame(products_list,)

            return carts
        except Exception as raised_exception:
            return str(raised_exception)


    def get_carts(
        self,
        order_by: OrderBy,
        order_direction: OrderDirection,
        skip: int = 0,
        limit: int = 10,
        uncleared_only: bool = False,
    ):
        try:
            db_carts = self.db.query(Carts)
            
            if uncleared_only:
                db_carts = db_carts.filter(Carts.status==False)
            
            order_object = Carts.date_modified
            if order_by==OrderBy.date_created:
                order_object = Carts.date_created
            
            order_object = order_object.asc()
            if order_direction==OrderDirection.desc.value:
                order_object = order_object.desc()

            db_carts = db_carts.order_by(order_object).offset(skip).limit(limit).all()

            return db_carts
        except Exception as raised_exception:
            raise raised_exception

    def checkout_cart(
        self,
        cart_id: UUID
    ):
        try:
            db_cart = self.db.query(Carts).join(Carts.orders).filter(Carts.id==cart_id).first()

            ##more work on reducing the quantity of items.

            setattr(db_cart, "status", True)
            self.db.add(db_cart)
            self.db.commit()
            self.db.refresh(db_cart)

            return db_cart
        except Exception as raised_exception:
            raise raised_exception
    
    def delete_cart(
        self,
        cart_id: UUID
    ):
        db_cart = self.db.query(Carts).filter(Carts.id==cart_id)
        cart_orders_query = self.db.query(Orders).filter(Orders.cart_id==cart_id)
        cart_orders = cart_orders_query.all()
        new_products = []
        for order in cart_orders:
            db_product = self.db.query(Products).filter(Products.id==order.product_id).first()
            setattr(db_product, 'units', db_product.units+order.counts)
            new_products.append(db_product)
        
        self.db.add_all(new_products)

        orders_delete_res = cart_orders_query.delete(synchronize_session=False)
        print("deleted orders : ", orders_delete_res)

        result = db_cart.delete(synchronize_session=False)
        self.db.commit()
        return result