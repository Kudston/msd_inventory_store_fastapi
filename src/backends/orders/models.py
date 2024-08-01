import uuid
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Column,
    ForeignKey,
    DECIMAL,
    Boolean,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql.functions import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import select
from src.backends.database import Base
from src.backends.products.models import Products

class Orders(Base):
    __tablename__ = "orders"
    id = Column(postgresql.UUID(as_uuid=True), index=True, unique=True, primary_key=True, default=uuid.uuid4)
    product_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Products.id))
    product  = relationship("Products", foreign_keys=[product_id], lazy='joined')
    counts   = Column(Integer, nullable=False)
    total_amount = column_property(
        select(func.round(Products.price*counts))
        .where(Products.id==product_id)
        .correlate_except(Products)
        .scalar_subquery()
    )
    cart_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('carts.id'))
    cart = relationship("Carts", back_populates="orders")

    date_created = Column(DateTime, server_default=func.now())
    date_modified = Column(DateTime, onupdate=func.now())
    __table_args__ = (UniqueConstraint("product_id", "cart_id", name="product_id_cart_id_constraint"),)

class Carts(Base):
    __tablename__ = "carts"
    id = Column(postgresql.UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4)
    orders = relationship("Orders", lazy='joined')

    total_amount = column_property(
        select(func.sum(Orders.total_amount))
        .where(Orders.cart_id==id)
        .correlate_except(Orders)
        .scalar_subquery()
    )
    status = Column(Boolean, default=False)
    date_created = Column(DateTime, server_default=func.now())
    date_modified = Column(DateTime, onupdate=func.now())

