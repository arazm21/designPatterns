from fastapi import APIRouter

from models.sales import SalesReport
from repositories.sales_repository import SalesRepository
from services.sales_service import SalesService

router = APIRouter()
service = SalesService(repository=SalesRepository())

@router.get("/sales", response_model=SalesReport)
def get_sales_report() -> SalesReport:
    return service.get_sales_report()
