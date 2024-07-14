from src.database import Base
import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    DateTime,
    UniqueConstraint,
    ARRAY,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.functions import func

class User(Base):
    __tablename__ = 'users'

    id = Column(postgresql.UUID(True), primary_key=True, index=True, default=uuid.uuid4)
    user_name = Column(String(20), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False) ##hashed password
    is_admin = Column(Boolean(), default=False)

    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_modified = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)