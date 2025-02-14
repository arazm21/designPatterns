import uuid

from fastapi.testclient import TestClient


def test_create_product_success(test_client: TestClient) -> None:
    """Test creating a product successfully."""
    # Create a unit to associate with the product
    unit_response = test_client.post("/units", json={"name": "kg"})
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


def test_create_product_conflict(test_client: TestClient) -> None:
    """Test creating a product with a duplicate barcode."""
    # Create a unit to associate with the product
    unit_response = test_client.post("/units", json={"name": "kg"})
    unit_id = unit_response.json()["unit"]["id"]

    # Create the product
    test_client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520
        },
    )

    # Attempt to create the product again with the same barcode
    response = test_client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520
        },
    )
    assert response.status_code == 409
    data = response.json()
    assert (data["detail"]["error"]["message"] ==
            "Product with barcode<1234567890> already exists.")


def test_read_product_success(test_client: TestClient) -> None:
    """Test retrieving a product by ID successfully."""
    # Create a unit and a product
    unit_response = test_client.post("/units", json={"name": "kg"})
    unit_id = unit_response.json()["unit"]["id"]

    product_response = test_client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520
        },
    )
    product_id = product_response.json()["product"]["id"]

    # Retrieve the product
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product"]["id"] == product_id
    assert data["product"]["name"] == "Apple"
    assert data["product"]["barcode"] == "1234567890"
    assert data["product"]["price"] == 520


def test_read_product_not_found(test_client: TestClient) -> None:
    """Test retrieving a product with a non-existent ID."""
    product_id = uuid.uuid4()
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 404
    data = response.json()
    assert (data["detail"]["error"]["message"] ==
            f"Product with id<{product_id}> does not exist.")


def test_list_products(test_client: TestClient) -> None:
    """Test listing all products."""
    # Create a unit and some products
    unit_response = test_client.post("/units", json={"name": "kg"})
    unit_id = unit_response.json()["unit"]["id"]

    test_client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520
        },
    )
    test_client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "Banana",
            "barcode": "9876543210",
            "price": 300
        },
    )

    # List the products
    response = test_client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) >= 2
    product_names = [product["name"] for product in data["products"]]
    assert "Apple" in product_names
    assert "Banana" in product_names


def test_update_product_success(test_client: TestClient) -> None:
    """Test updating a product successfully."""
    # Create a unit and a product
    unit_response = test_client.post("/units", json={"name": "kg"})
    unit_id = unit_response.json()["unit"]["id"]

    product_response = test_client.post(
        "/products",
        json={
            "unit_id": unit_id,
            "name": "Apple",
            "barcode": "1234567890",
            "price": 520
        },
    )
    product_id = product_response.json()["product"]["id"]

    # Update the product price
    response = test_client.patch(f"/products/{product_id}", json={"price": 530})
    assert response.status_code == 200

    # Verify the update
    get_response = test_client.get(f"/products/{product_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["product"]["price"] == 530


def test_update_product_not_found(test_client: TestClient) -> None:
    """Test updating a product with a non-existent ID."""
    product_id = uuid.uuid4()
    response = test_client.patch(f"/products/{product_id}", json={"price": 530})
    assert response.status_code == 404
    data = response.json()
    assert (data["detail"]["error"]["message"] ==
            f"Product with id<{product_id}> does not exist.")
