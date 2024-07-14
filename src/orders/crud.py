from sqlalchemy.orm import Session
from src.orders.models import Purchases,Orders
from src.products.models import Products
from sqlalchemy.dialects.postgresql import UUID

class OrdersCrud:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_order(
        self,
        product_id: UUID,
        counts: int,
        purchase_id: UUID
    ):
        try:
            db_product: Products = self.db.query(Products).filter(Products.id==product_id).first()
            db_order = Orders(
                product_id = product_id,
                purchase_id = purchase_id,
                counts = counts,
                total_amount = round(counts*db_product.price, 2)
            )

            self.db.add(db_order)
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
        purchase_id: UUID
    ):
        try:
            orders = self.db.query(Orders).filter(Orders.purchase_id==purchase_id).all()
            return orders
        except Exception as raised_exception:
            raise raised_exception
    
    def update_order_units(
        self,
        order_id: UUID,
        counts: int,
        increase: bool,
    ):
        try:
            db_order = self.get_order(order_id=order_id)
            
            if increase:
                setattr(db_order, "counts", db_order.counts+counts)
            elif not increase:
                setattr(db_order, "counts", db_order.counts-counts)

            setattr(db_order, "total_amount", db_order.counts*db_order.product.price)

            self.db.add(db_order)
            self.db.commit()
            self.db.refresh(db_order)
            
            return db_order
        except Exception as raised_exception:
            raise raised_exception
        
    ##purchase functions
    def create_new_purchase(self):
        try:
            db_purchase = Purchases()

            self.db.add(db_purchase)
            self.db.commit()
            self.db.refresh(db_purchase)

            return db_purchase
        except Exception as raised_exception:
            raise raised_exception
    
    def get_purchase(
        self,
        purchase_id:UUID
    ):
        db_purchase = self.db.query(Purchases).filter(Purchases.id==purchase_id).first()

        return db_purchase
    
    def get_purchases(
        self,
        skip: int = 0,
        limit: int = 10,
    ):
        try:
            db_purchases = self.db.query(Purchases)
            
            db_purchases = db_purchases.offset(skip).limit(limit).all()
            
            return db_purchases
        except Exception as raised_exception:
            raise raised_exception

    def checkout_purchase(
        self,
        purchase_id: UUID
    ):
        try:
            db_purchase = self.db.query(Purchases).join(Purchases.orders).filter(Purchases.id==purchase_id)

            ##more work on reducing the quantity of items.

            setattr(db_purchase, "status", True)
            self.db.add(db_purchase)
            self.db.commit()
            self.db.refresh(db_purchase)

            return db_purchase
        except Exception as raised_exception:
            raise raised_exception