from uuid import UUID

from pydantic import BaseModel


class UnitCreate(BaseModel):
    name: str

class Unit(BaseModel):
    id: UUID
    name: str
