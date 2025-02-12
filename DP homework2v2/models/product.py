from uuid import UUID

from pydantic import BaseModel


class Product(BaseModel):
    id: UUID
    unit_id: str
    name: str
    barcode: str
    price: int

class ProductCreate(BaseModel):
    unit_id: UUID
    name: str
    barcode: str
    price: int

class ProductPriceUpdate(BaseModel):
    price: int
