from database.connection import get_connection
from models.sales import SalesReport


class SalesRepository:
    @staticmethod
    def get_sales_report() -> SalesReport:
        """Fetch total number of receipts and revenue."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(id) AS n_receipts, "
                       "SUM(total) AS revenue FROM receipts")
        result = cursor.fetchone()

        return SalesReport(
            n_receipts=result["n_receipts"] or 0,
            revenue=result["revenue"] or 0
        )
