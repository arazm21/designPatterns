from uuid import uuid4

from database.connection import get_connection
from models.product import Product


class ProductRepository:
    @staticmethod
    def create_product(unit_id: str, name: str, barcode: str, price: int) -> Product:
        """Create a new product in the database."""
        connection = get_connection()
        cursor = connection.cursor()

        # Check if the product already exists
        cursor.execute("SELECT id FROM products WHERE barcode = ?", (barcode,))
        if cursor.fetchone():
            raise ValueError(f"Product with barcode<{barcode}> already exists.")

        # Generate a new UUID and insert the product
        product_id = uuid4()
        cursor.execute(
            "INSERT INTO products (id, unit_id, name, barcode, price) "
            "VALUES (?, ?, ?, ?, ?)",
            (str(product_id), unit_id, name, barcode, price),
        )
        connection.commit()

        # Return the created product
        return Product(id=product_id, unit_id=unit_id, name=name,
                       barcode=barcode, price=price)

    @staticmethod
    def get_product_by_id(product_id: str) -> Product:
        """Retrieve a product by its ID."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, unit_id, name, barcode, "
            "price FROM products WHERE id = ?", (product_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Product with "
                             f"id<{product_id}> does not exist.")

        return Product(
            id=row["id"], unit_id=row["unit_id"],
            name=row["name"], barcode=row["barcode"], price=row["price"]
        )

    @staticmethod
    def list_products() -> list[Product]:
        """Retrieve all products from the database."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, unit_id, "
                       "name, barcode, price FROM products")
        rows = cursor.fetchall()

        # Convert rows to a list of Product instances
        return [Product(id=row["id"], unit_id=row["unit_id"],
                        name=row["name"], barcode=row["barcode"],
                        price=row["price"]) for row in rows]

    @staticmethod
    def update_product_price(product_id: str, price: int) -> None:
        """Update the price of a product."""
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM products "
                       "WHERE id = ?", (product_id,))
        if not cursor.fetchone():
            raise ValueError(f"Product with "
                             f"id<{product_id}> does not exist.")

        cursor.execute("UPDATE products SET price = ? "
                       "WHERE id = ?", (price, product_id))
        connection.commit()
