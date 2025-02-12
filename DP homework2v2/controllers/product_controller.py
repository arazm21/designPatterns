from typing import Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from models.product import Product, ProductCreate, ProductPriceUpdate
from repositories.product_repository import ProductRepository
from services.product_service import ProductService

router = APIRouter()
service = ProductService(repository=ProductRepository())


@router.post("/products", status_code=201)
def create_product(product: ProductCreate) -> Dict[str, Product]:
    try:
        created_product = service.create_product(
            unit_id=str(product.unit_id),
            name=product.name,
            barcode=product.barcode,
            price=product.price,
        )
        return {"product": created_product}
    except ValueError as e:
        raise HTTPException(status_code=409,
                            detail={"error": {"message": str(e)}})


@router.get("/products/{product_id}")
def get_product(product_id: str) -> Dict[str, Product]:
    try:
        # Validate if the product_id is a valid UUID
        uuid_obj = UUID(product_id)
        uuid_str = str(uuid_obj)
        return {"product": service.get_product(uuid_str)}
    except ValueError as e:
        raise HTTPException(status_code=404,
                            detail={"error": {"message": str(e)}})


@router.get("/products")
def list_products() -> dict[str, list[Product]]:
    return {"products": service.list_products()}


@router.patch("/products/{product_id}")
def update_product_price(product_id: str,
                         update: ProductPriceUpdate) -> None:
    try:
        # Call the service to update the product's price
        service.update_product_price(product_id, update.price)
        # Return an empty JSON object on success
        return
    except ValueError:
        # Return a 404 error with the required structure
        raise HTTPException(
            status_code=404,
            detail={"error": {"message": f"Product with id<{product_id}> "
                                         f"does not exist."}}
        )
