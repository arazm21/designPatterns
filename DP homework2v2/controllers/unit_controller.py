from uuid import UUID

from fastapi import APIRouter, HTTPException

from models.unit import Unit, UnitCreate
from repositories.unit_repository import UnitRepository
from services.unit_service import UnitService

router = APIRouter()
service = UnitService(repository=UnitRepository())


# # Service dependency
# def get_unit_service(db: Database = Depends(get_db)) -> UnitService:
#     return UnitService(UnitRepository(db))


@router.post("/units", response_model=Unit, status_code=201)
def create_unit(unit: UnitCreate) -> Unit:
    try:
        created_unit = service.create_unit(name=unit.name)
        return created_unit
    except ValueError as e:
        raise HTTPException(status_code=409, detail={"error": {"message": str(e)}})


@router.get("/units/{unit_id}", response_model=Unit)
def get_unit(unit_id: str) -> Unit:
    try:
        # Validate if the unit_id is a valid UUID
        uuid_obj = UUID(unit_id)
        uuid_str = str(uuid_obj)
        return service.get_unit(uuid_str)
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": {"message": str(e)}})


@router.get("/units", response_model=list[Unit])
def list_units() -> list[Unit]:
    return service.list_units()
