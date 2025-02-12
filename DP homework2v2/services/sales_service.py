from models.sales import SalesReport
from repositories.sales_repository import SalesRepository


class SalesService:
    def __init__(self, repository: SalesRepository):
        self.repository = repository

    def get_sales_report(self) -> SalesReport:
        return self.repository.get_sales_report()
