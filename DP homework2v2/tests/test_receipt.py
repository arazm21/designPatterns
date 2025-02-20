import uuid

from fastapi.testclient import TestClient
from httpx import Response


def test_create_receipt_success(test_client: TestClient) -> None:
    """Test creating a receipt successfully."""
    response = test_client.post("/receipts")
    assert response.status_code == 201
    data = response.json()
    assert data["receipt"]["status"] == "open"
    assert data["receipt"]["total"] == 0
    assert "id" in data["receipt"]


def make_example_products(test_client: TestClient) -> Response:
    # Create unit and product
    unit_response = test_client.post("/units", json={"name": "kg"})
    assert unit_response.status_code == 201
    unit_id = unit_response.json()["unit"]["id"]

    response = test_client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product"]["name"] == "Apple"
    assert data["product"]["barcode"] == "1234567890"
    assert data["product"]["price"] == 520
    assert data["product"]["unit_id"] == unit_id

    return response


def test_add_product_to_receipt_success(test_client: TestClient) -> None:
    """Test adding a product to a receipt."""
    # Create unit and product
    product_response1 = make_example_products(test_client)
    product_response = product_response1.json()
    product_id = product_response["product"]["id"]
    # Create a receipt
    receipt_response = test_client.post("/receipts")
    receipt_id = receipt_response.json()["receipt"]["id"]

    # Add product to receipt
    response = test_client.post(
        f"/receipts/{receipt_id}/products",
        json={"id": product_id, "quantity": 2}
    )

    assert response.status_code == 201
    data = response.json()
    assert any(
        p["id"] == product_id and p["quantity"] == 2 and p["total"] == 1040
        for p in data["receipt"]["products"]
    )
    assert data["receipt"]["total"] == 1040


def test_get_receipt_success(test_client: TestClient) -> None:
    """Test retrieving a receipt successfully."""
    response = test_client.post("/receipts")
    receipt_id = response.json()["receipt"]["id"]

    response = test_client.get(f"/receipts/{receipt_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["receipt"]["id"] == receipt_id
    assert data["receipt"]["status"] == "open"


def test_get_receipt_with_products_success(test_client: TestClient) -> None:
    """Test retrieving a receipt with products successfully."""
    # Create a new receipt
    response = test_client.post("/receipts")
    receipt_id = response.json()["receipt"]["id"]

    # Create a test product
    data2 = make_example_products(test_client)
    data1 = data2.json()
    # Add the product to the receipt
    response = test_client.post(
        f"/receipts/{receipt_id}/products",
        json={"id": data1["product"]["id"], "quantity": 123},
    )
    assert response.status_code == 201

    # Retrieve the receipt and verify product details
    response = test_client.get(f"/receipts/{receipt_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["receipt"]["id"] == receipt_id
    assert data["receipt"]["status"] == "open"
    assert len(data["receipt"]["products"]) == 1
    assert data["receipt"]["products"][0]["id"] == data1["product"]["id"]
    assert data["receipt"]["products"][0]["quantity"] == 123
    assert data["receipt"]["products"][0]["price"] == 520
    assert data["receipt"]["products"][0]["total"] == 123 * 520
    assert data["receipt"]["total"] == 123 * 520


def test_get_receipt_not_found(test_client: TestClient) -> None:
    """Test retrieving a non-existent receipt."""
    receipt_id = uuid.uuid4()
    response = test_client.get(f"/receipts/{receipt_id}")
    assert response.status_code == 404
    data = response.json()
    assert (data["detail"]["error"]["message"] ==
            f"Receipt with id<{receipt_id}> does not exist.")


def test_update_receipt_status_success(test_client: TestClient) -> None:
    """Test updating a receipt status successfully."""
    response = test_client.post("/receipts")
    receipt_id = response.json()["receipt"]["id"]

    response = test_client.patch(f"/receipts/{receipt_id}", json={"status": "closed"})
    assert response.status_code == 200

    get_response = test_client.get(f"/receipts/{receipt_id}")
    assert get_response.status_code == 200
    assert get_response.json()["receipt"]["status"] == "closed"


def test_delete_receipt_success(test_client: TestClient) -> None:
    """Test deleting an open receipt successfully."""
    response = test_client.post("/receipts")
    receipt_id = response.json()["receipt"]["id"]

    response = test_client.delete(f"/receipts/{receipt_id}")
    assert response.status_code == 200

    response = test_client.get(f"/receipts/{receipt_id}")
    assert response.status_code == 404
# __________________________________----


def test_add_product_to_receipt_failure_invalid_receipt(test_client: TestClient) -> None:
    """Test adding a product to a non-existent receipt."""
    receipt_id = uuid.uuid4()
    product_id = uuid.uuid4()

    response = test_client.post(
        f"/receipts/{receipt_id}/products",
        json={"id": str(product_id), "quantity": 2},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"]["error"]["message"] == f"Receipt with id<{receipt_id}> does not exist."


def test_add_product_to_receipt_failure_invalid_product(test_client: TestClient) -> None:
    """Test adding a non-existent product to a receipt."""
    response = test_client.post("/receipts")
    receipt_id = response.json()["receipt"]["id"]
    product_id = uuid.uuid4()

    response = test_client.post(
        f"/receipts/{receipt_id}/products",
        json={"id": str(product_id), "quantity": 2},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"]["error"]["message"] == f"Product with id<{product_id}> does not exist."




