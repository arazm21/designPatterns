from typing import Dict

from fastapi import APIRouter, HTTPException

from models.receipt import Receipt, ReceiptProductAdd, ReceiptStatusUpdate
from repositories.receipt_repository import ReceiptRepository
from services.receipt_service import ReceiptService

router = APIRouter()
service = ReceiptService(repository=ReceiptRepository())


@router.post("/receipts", status_code=201)
def create_receipt() -> Dict[str, Receipt]:
    return {"receipt": service.create_receipt()}


@router.post("/receipts/{receipt_id}/products", status_code=201)
def add_product_to_receipt(receipt_id: str,
                           product: ReceiptProductAdd) -> Dict[str, Receipt]:
    try:
        return {"receipt":
                    service.add_product_to_receipt(receipt_id,
                                                   str(product.id), product.quantity)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": {"message": str(e)}})


@router.get("/receipts/{receipt_id}")
def get_receipt(receipt_id: str) -> Dict[str, Receipt]:
    try:
        return {"receipt": service.get_receipt(receipt_id)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": {"message": str(e)}})


@router.patch("/receipts/{receipt_id}")
def update_receipt_status(receipt_id: str,
                          update: ReceiptStatusUpdate) -> None:
    try:
        service.update_receipt_status(receipt_id, update.status)
        return
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"error": {"message": str(e)}})


@router.delete("/receipts/{receipt_id}")
def delete_receipt(receipt_id: str) -> None:
    try:
        service.delete_receipt(receipt_id)
        return
    except ValueError as e:
        status_code = 403 if "closed" in str(e) else 404
        raise HTTPException(status_code=status_code,
                            detail={"error": {"message": str(e)}})

# from fastapi import APIRouter, HTTPException
# from uuid import UUID
# from services.receipt_service import ReceiptService
# from repositories.receipt_repository import ReceiptRepository
# from schemas.receipt import Receipt, ReceiptProduct
# from controllers.product_controller import get_product
# from services.product_service import ProductService
#
# router = APIRouter()
# service = ReceiptService(repository=ReceiptRepository())
# from models.product import Product
#
#
# @router.post("/receipts", status_code=201)
# def create_receipt():
#     try:
#         receipt = service.create_receipt()
#         return {"receipt": receipt}
#     except ValueError as e:
#         raise HTTPException(status_code=409, detail={"error": {"message": str(e)}})
#
#
# @router.post("/receipts/{receipt_id}/products", status_code=201)
# def add_product(product_id: UUID, quantity: int):
#     try:
#         returned_product = ProductService.get_product(product_id=str(product_id))
#         price = returned_product.price
#         receipt_product = ReceiptProduct(product_id=product_id, quantity=quantity,
#                                          price=price, total=price * quantity)
#
#         return {"receipt": receipt_product}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail={"error": {"message": str(e)}})
#
#
# @router.get("/receipts/{receipt_id}", status_code=200)
# def get_receipt(receipt_id: UUID):
#     try:
#         return {"receipt": service.get_receipt(receipt_id)}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail={"error": {"message": str(e)}})
#
#
# @router.patch("/receipts/{receipt_id}", status_code=200)
# def close_receipt(receipt_id: UUID, status: str):
#     try:
#         service.update_receipt_status(receipt_id, status)
#         return {}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail={"error": {"message": str(e)}})
#
#
# @router.delete("/receipts/{receipt_id}", status_code=200)
# def delete_receipt(receipt_id: UUID):
#     try:
#         service.delete_receipt(receipt_id)
#         return {}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail={"error": {"message": str(e)}})
#     except PermissionError as e:
#         raise HTTPException(status_code=403, detail={"error": {"message": str(e)}})
