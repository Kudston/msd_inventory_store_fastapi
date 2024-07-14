from src.schemas import ParentPydantic
from pydantic import UUID4
from typing import List

class OrderCreate(ParentPydantic):
    product_id: UUID4
    purchase_id: UUID4
    counts: int

class OrderOut(ParentPydantic):
    id: UUID4
    purchase_id: UUID4
    product_id: UUID4
    counts: int
    total_amount: float

class ManyOrdersOut(ParentPydantic):
    orders:List = List[OrderOut]

class PurchaseOut(ManyOrdersOut):
    id: UUID4
    status: bool

class MiniPurchaseOut(ParentPydantic):
    id: UUID4
    status: bool

class ManyMiniPurchaseOut(ParentPydantic):
    purchases: List[MiniPurchaseOut]