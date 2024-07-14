import uuid
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Column,
    ForeignKey,
    DECIMAL,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.dialects import postgresql

from src.database import Base
from src.products.models import Products

class Orders(Base):
    __tablename__ = "orders"
    id = Column(postgresql.UUID(as_uuid=True), index=True, unique=True, primary_key=True, default=uuid.uuid4)
    product_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Products.id))
    product  = relationship("Products", foreign_keys=[product_id])
    counts   = Column(Integer, nullable=False)
    total_amount = Column(DECIMAL(scale=2), nullable=False)
    purchase_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('purchases.id'))
    purchase = relationship("Purchases", back_populates="orders")

    date_created = Column(DateTime, server_default=func.now())
    

class Purchases(Base):
    __tablename__ = "purchases"
    id = Column(postgresql.UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4)
    orders = relationship("Orders", lazy='joined')

    status = Column(Boolean, default=False)
    date_created = Column(DateTime, server_default=func.now())
    date_modified = Column(DateTime, onupdate=func.now())

