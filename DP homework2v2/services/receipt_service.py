from models.receipt import Receipt
from repositories.receipt_repository import ReceiptRepository


class ReceiptService:
    def __init__(self, repository: ReceiptRepository):
        self.repository = repository

    def create_receipt(self) -> Receipt:
        return self.repository.create_receipt()

    def add_product_to_receipt(self, receipt_id: str,
                               product_id: str, quantity: int) -> Receipt:
        return self.repository.add_product_to_receipt(receipt_id, product_id, quantity)

    def get_receipt(self, receipt_id: str) -> Receipt:
        return self.repository.get_receipt_by_id(receipt_id)

    def update_receipt_status(self, receipt_id: str, status: str) -> None:
        self.repository.update_receipt_status(receipt_id, status)

    def delete_receipt(self, receipt_id: str) -> None:
        self.repository.delete_receipt(receipt_id)



# from repositories.receipt_repository import ReceiptRepository
# from models.receipt import Receipt, Product
# from uuid import UUID
#
# class ReceiptService:
#     def __init__(self, repository: ReceiptRepository):
#         self.repository = repository
#
#     def create_receipt(self) -> Receipt:
#         return self.repository.create_receipt()
#
#     def add_product_to_receipt(self, receipt_id: UUID, product: Product) -> None:
#         self.repository.add_product_to_receipt(receipt_id, product)
#
#     def get_receipt(self, receipt_id: UUID) -> Receipt:
#         return self.repository.get_receipt(receipt_id)
#
#     def update_receipt_status(self, receipt_id: UUID, status: str) -> None:
#         self.repository.update_receipt_status(receipt_id, status)
#
#     def delete_receipt(self, receipt_id: UUID) -> None:
#         self.repository.delete_receipt(receipt_id)
