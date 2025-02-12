from models.product import Product
from repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(self, unit_id: str, name: str,
                       barcode: str, price: int) -> Product:
        """Create a new product."""
        return self.repository.create_product(unit_id, name, barcode, price)

    def get_product(self, product_id: str) -> Product:
        """Retrieve a product by ID."""
        return self.repository.get_product_by_id(product_id)

    def list_products(self) -> list[Product]:
        """List all products."""
        return self.repository.list_products()

    def update_product_price(self, product_id: str, price: int) -> None:
        """Update a product's price."""
        self.repository.update_product_price(product_id, price)
