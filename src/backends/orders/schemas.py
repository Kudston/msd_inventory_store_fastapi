from datetime import datetime
from src.backends.schemas import ParentPydantic
from pydantic import UUID4
from typing import List, Optional
from src.backends.products.schemas import ProductOut

class OrderCreate(ParentPydantic):
    product_id: UUID4
    cart_id: UUID4
    counts: int

class OrderOut(ParentPydantic):
    id: UUID4
    cart_id: UUID4
    product_id: UUID4
    product: ProductOut
    counts: int
    total_amount: float

class ManyOrdersOut(ParentPydantic):
    orders:List = List[OrderOut]

class CartOut(ManyOrdersOut):
    id: UUID4
    status: bool
    total_amount: Optional[float] = None

class MiniCartOut(ParentPydantic):
    id: UUID4
    status: bool
    total_amount: Optional[float] = None
    date_created: datetime

class ManyMiniCartOut(ParentPydantic):
    carts: List[MiniCartOut]

class OrderUpdate(ParentPydantic):
    order_id: UUID4
    counts: int