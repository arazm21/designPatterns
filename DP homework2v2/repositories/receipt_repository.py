import uuid
from uuid import uuid4

from database.connection import get_connection
from models.receipt import Receipt, ReceiptProduct
from repositories.product_repository import ProductRepository


class ReceiptRepository:
    @staticmethod
    def create_receipt() -> Receipt:
        """Create a new receipt in the database."""
        connection = get_connection()
        cursor = connection.cursor()

        receipt_id = str(uuid4())
        cursor.execute(
            "INSERT INTO receipts (id, status, total) VALUES (?, 'open', 0)",
            (receipt_id,)
        )
        connection.commit()

        return Receipt(id=uuid.UUID(receipt_id), status="open", products=[], total=0)

    @staticmethod
    def add_product_to_receipt(receipt_id: str,
                               product_id: str, quantity: int) -> Receipt:
        """Add a product to a receipt."""
        connection = get_connection()
        cursor = connection.cursor()

        # Check if receipt exists and is open
        cursor.execute("SELECT status FROM receipts WHERE id = ?", (receipt_id,))
        receipt = cursor.fetchone()
        if not receipt:
            raise ValueError(f"Receipt with id<{receipt_id}> does not exist.")
        if receipt["status"] == "closed":
            raise ValueError(f"Receipt with id<{receipt_id}> is closed.")

        # Get product details
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id<{product_id}> does not exist.")

        total_price = product.price * quantity

        # Insert or update the product in the receipt
        cursor.execute(
            "INSERT INTO receipt_products (receipt_id, product_id, "
            "quantity, price, total) "
            "VALUES (?, ?, ?, ?, ?) "
            # "ON CONFLICT(receipt_id, product_id) DO UPDATE SET "
            # "quantity = quantity + ?, total = total + ?"
            ,
            (receipt_id, product_id, quantity, product.price, total_price
             # , quantity, total_price
             )
        )

        # Update receipt total
        cursor.execute(
            "UPDATE receipts SET total = total + ? WHERE id = ?",
            (total_price, receipt_id)
        )

        connection.commit()
        return ReceiptRepository.get_receipt_by_id(receipt_id)

    @staticmethod
    def get_receipt_by_id(receipt_id: str) -> Receipt:
        """Retrieve a receipt by its ID."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, status, "
                       "total FROM receipts WHERE id = ?", (receipt_id,))
        receipt_row = cursor.fetchone()
        if not receipt_row:
            raise ValueError(f"Receipt with id<{receipt_id}> does not exist.")

        cursor.execute(
            "SELECT product_id, quantity, price, "
            "total FROM receipt_products WHERE receipt_id = ?",
            (receipt_id,)
        )
        products = [
            ReceiptProduct(id=row["product_id"], quantity=row["quantity"],
                           price=row["price"], total=row["total"])
            for row in cursor.fetchall()
        ]

        return Receipt(id=receipt_row["id"], status=receipt_row["status"],
                       products=products, total=receipt_row["total"])

    @staticmethod
    def update_receipt_status(receipt_id: str, status: str) -> None:
        """Update the status of a receipt."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM receipts "
                       "WHERE id = ?", (receipt_id,))
        if not cursor.fetchone():
            raise ValueError(f"Receipt with "
                             f"id<{receipt_id}> does not exist.")

        cursor.execute("UPDATE receipts SET status = ? "
                       "WHERE id = ?", (status, receipt_id))
        connection.commit()

    @staticmethod
    def delete_receipt(receipt_id: str) -> None:
        """Delete an open receipt."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT status FROM receipts WHERE id = ?", (receipt_id,))
        receipt = cursor.fetchone()
        if not receipt:
            raise ValueError(f"Receipt with id<{receipt_id}> does not exist.")
        if receipt["status"] == "closed":
            raise ValueError(f"Receipt with id<{receipt_id}> is closed.")

        cursor.execute("DELETE FROM receipts WHERE id = ?", (receipt_id,))
        connection.commit()












