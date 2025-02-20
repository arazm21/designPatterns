from fastapi.testclient import TestClient
from httpx import Response


def test_create_sale_success(test_client: TestClient) -> None:
    """Test creating a sale successfully."""
    response = test_client.get("/sales")
    assert response.status_code == 200
    data = response.json()
    assert data["n_receipts"] == 0
    assert data["revenue"] == 0


def make_example_products(test_client: TestClient) -> Response:
    # Create unit and product
    unit_response = test_client.post("/units", json={"name": "kg"})
    assert unit_response.status_code == 201
    unit_id = unit_response.json()["id"]

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


def test_add_things_to_cart(test_client: TestClient) -> None:
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
    response = test_client.get("/sales")
    assert response.status_code == 200
    data = response.json()
    assert data["n_receipts"] == 1
    assert data["revenue"] == 1040


