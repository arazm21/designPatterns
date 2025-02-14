from typing import Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from models.unit import Unit, UnitCreate
from repositories.unit_repository import UnitRepository
from services.unit_service import UnitService

router = APIRouter(prefix="/units", tags=["units"])
service = UnitService(repository=UnitRepository())


# # Service dependency
# def get_unit_service(db: Database = Depends(get_db)) -> UnitService:
#     return UnitService(UnitRepository(db))


@router.post("", response_model=Dict[str, Unit], status_code=201)
def create_unit(unit: UnitCreate) -> Dict[str, Unit]:
    try:
        created_unit = service.create_unit(name=unit.name)
        return {"unit": created_unit}
    except ValueError as e:
        raise HTTPException(status_code=409, detail={"error": {"message": str(e)}})


@router.get("/{unit_id}", response_model=Dict[str, Unit])
def get_unit(unit_id: str) -> Dict[str, Unit]:
    try:
        # Validate if the unit_id is a valid UUID
        uuid_obj = UUID(unit_id)
        uuid_str = str(uuid_obj)
        return {"unit": service.get_unit(uuid_str)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": {"message": str(e)}})


@router.get("", response_model=Dict[str, list[Unit]])
def list_units() -> Dict[str, list[Unit]]:
    return {"units": service.list_units()}
