import uuid
from sqlalchemy import (
    String,
    ForeignKey,
    Integer,
    DateTime,
    Column,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.functions import func
from src.database import Base
from src.users.models import User

class Products(Base):
    __tablename__ = "products"
    id = Column(postgresql.UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4)
    title  = Column(String(), unique=True)
    category = Column(String(), default="None")
    units   = Column(Integer(), default=0)
    price   = Column(Float(precision=2))

    date_created = Column(DateTime, server_default=func.now())
    date_modified = Column(DateTime, onupdate=func.now())

    creator_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('users.id'))
    created_by = relationship("User", foreign_keys=[creator_id], lazy='joined')
