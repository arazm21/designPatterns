from typing import Dict

from fastapi import APIRouter

from models.sales import SalesReport
from repositories.sales_repository import SalesRepository
from services.sales_service import SalesService

router = APIRouter(prefix="/sales", tags=["sales"])
service = SalesService(repository=SalesRepository())


@router.get("", response_model=Dict[str, SalesReport])
def get_sales_report() -> Dict[str, SalesReport]:
    return {"sales": service.get_sales_report()}
