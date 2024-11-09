from sqlalchemy.orm import Session
from utils import OrderBy, OrderDirection, DateRangeType
from orders.utils import StatisticsOrderBy
from orders.models import Carts,Orders
from products.models import Products
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import sum
from sqlalchemy import and_, func
from datetime import datetime, timezone, timedelta, date
from dateutil.relativedelta import relativedelta
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
                
                new_product_count = counts - db_order.counts
                setattr(db_product, 'units', db_product.units - new_product_count)
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
        date_range_type: DateRangeType,
        range_counts: int,
        end_date: datetime,
        skip,
        limit,
        order_direction: OrderDirection = OrderDirection.desc,
        order_by: StatisticsOrderBy = StatisticsOrderBy.amount,
    ):
        ##NOW QUERY AND RETURN THE RESULTS
        try:
            
            ##SET THE DATE RANGE OBJECT
            end_date:datetime = end_date
            start_date = date(end_date.year, end_date.month, end_date.day)

            if date_range_type==DateRangeType.days:
                if range_counts>1:
                    counts = range_counts - 1
                    start_date = start_date - timedelta(days=counts)
            elif date_range_type==DateRangeType.weeks:
                start_date = start_date - timedelta(days=end_date.weekday())
                if range_counts>1:
                    counts = range_counts -1
                    start_date = start_date - timedelta(weeks=counts)
            elif date_range_type==DateRangeType.months:
                start_date = start_date - timedelta(days=start_date.day)
                if range_counts>1:
                    counts = range_counts - 1
                    start_date = start_date - relativedelta(months=counts)

            carts = self.db.query(Carts)

            carts = carts.filter(
                and_(
                    Carts.date_created>=start_date,
                    Carts.date_created<=end_date,
                )
            )
            
            cleared_carts = carts.filter(Carts.status==True)
            uncleared_carts = carts.filter(Carts.status==False)

            total_amount  = carts.with_entities(func.sum(Carts.total_amount)).scalar()
            cleared_total_amount = cleared_carts.with_entities(func.sum(Carts.total_amount)).scalar()
            uncleared_total_amount = uncleared_carts.with_entities(func.sum(Carts.total_amount)).scalar()
            
            grouped_carts = (carts.join(Carts.orders).
                             join(Orders.product).
                                group_by(Orders.product_id, Products.title).
                                with_entities(
                                    Orders.product_id,
                                    Products.title,
                                    func.sum(Orders.total_amount),
                                    func.sum(Orders.counts),
                                    ))
            products_list_dict = []

            for id, title, totamt, cnts in grouped_carts:
                products_list_dict.append(
                    {
                        "id":id,
                        "title":title,
                        "total_amount":totamt,
                        "total_counts":cnts,
                    }
                )
            
            set_order_by = "total_amount" if (order_by==StatisticsOrderBy.amount) else "total_counts"
            direction = True if order_direction==OrderDirection.desc else False

            products_list_dict = sorted(products_list_dict,
                                        key = lambda product: product[set_order_by], reverse=direction)

            response_object = {
                "total_amount":total_amount if total_amount else 0,
                "total_cleared_amount":cleared_total_amount if cleared_total_amount else 0,
                "total_uncleared_amount":uncleared_total_amount if uncleared_total_amount else 0,
                "products_list":products_list_dict,
            }

            return response_object
        except Exception as raised_exception:
            raise raised_exception


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