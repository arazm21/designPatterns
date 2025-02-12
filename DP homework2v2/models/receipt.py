from typing import List
from uuid import UUID

from pydantic import BaseModel


class ReceiptProduct(BaseModel):
    id: UUID
    quantity: int
    price: int
    total: int


class Receipt(BaseModel):
    id: UUID
    status: str
    products: List[ReceiptProduct]
    total: int


class ReceiptCreate(BaseModel):
    pass  # No input fields needed for creation


class ReceiptProductAdd(BaseModel):
    id: UUID
    quantity: int


class ReceiptStatusUpdate(BaseModel):
    status: str
