from schemas import ParentPydantic
from datetime import datetime
from pydantic import constr
from users.schemas import UserOut
from typing import List,Optional
from pydantic import UUID4

class ProductCreate(ParentPydantic):
    title: str = constr(max_length=20)
    category: str = constr(max_length=20)
    units: int
    price: float

class ProductUpdate(ParentPydantic):
    title: Optional[str] = None
    category: Optional[str] = None
    units: Optional[int] =  None
    price: Optional[float] = None

class ProductOut(ParentPydantic):
    id: UUID4
    title: str
    category: str
    units: int
    price: float
    date_created: datetime
    date_modified: Optional[datetime]
    created_by: UserOut

class ManyProductsOut(ParentPydantic):
    products: list = List[ProductOut]

