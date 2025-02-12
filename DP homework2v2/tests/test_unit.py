import uuid

from fastapi.testclient import TestClient


def test_create_unit_success(test_client: TestClient) -> None:
    """Test creating a unit successfully."""
    response = test_client.post("/units", json={"name": "kg"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "kg"


def test_create_unit_conflict(test_client: TestClient) -> None:
    """Test creating a unit with a duplicate name."""
    test_client.post("/units", json={"name": "kg"})  # Initial creation
    response = test_client.post("/units", json={"name": "kg"})
    assert response.status_code == 409
    data = response.json()
    assert data["detail"]["error"]["message"] == "Unit with name<kg> already exists."


def test_read_unit_success(test_client: TestClient) -> None:
    """Test retrieving a unit by ID successfully."""
    create_response = test_client.post("/units", json={"name": "g"})
    unit_id = create_response.json()["id"]

    response = test_client.get(f"/units/{unit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == unit_id
    assert data["name"] == "g"


def test_read_unit_not_found(test_client: TestClient) -> None:
    """Test retrieving a unit with a non-existent ID."""
    uid = uuid.uuid4()
    response = test_client.get(f"/units/{uid}")
    assert response.status_code == 404
    data = response.json()
    print(response)
    assert data["detail"]["error"]["message"] == f"Unit with id<{uid}> does not exist."


def test_list_units(test_client: TestClient) -> None:
    """Test listing all units."""
    test_client.post("/units", json={"name": "liters"})
    test_client.post("/units", json={"name": "pieces"})

    response = test_client.get("/units")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    unit_names = [unit["name"] for unit in data]
    assert "liters" in unit_names
    assert "pieces" in unit_names













#
# @pytest.fixture(scope="module")
# def test_client():
#     """Fixture for setting up the test client and database."""
#     init_db()
#     client = TestClient(app)
#     yield client
#     close_db()
#
#
# # def test_create_unit_success(test_client):
# def test_create_unit_success(mock_get_connection, test_client):
#     mock_connection = mock_get_connection.return_value
#     mock_cursor = mock_connection.cursor.return_value
#
#     mock_cursor.fetchone.return_value = None  # Simulate no existing unit
#     response = test_client.post("/units", json={"name": "kg"})
#
#     assert response.status_code == 201
#
#
#
# def test_create_unit_conflict(test_client):
#     """Test creating a unit with a duplicate name."""
#     test_client.post("/units", json={"name": "kg"})  # Initial creation
#     response = test_client.post("/units", json={"name": "kg"})
#     assert response.status_code == 409
#     data = response.json()
#     assert "error" in data
#     assert data["error"]["message"] == "Unit with name<kg> already exists."
#
#
# def test_read_unit_success(test_client):
#     """Test retrieving a unit by ID successfully."""
#     create_response = test_client.post("/units", json={"name": "g"})
#     unit_id = create_response.json()["unit"]["id"]
#
#     response = test_client.get(f"/units/{unit_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert "unit" in data
#     assert data["unit"]["id"] == unit_id
#     assert data["unit"]["name"] == "g"
#
#
# def test_read_unit_not_found(test_client):
#     """Test retrieving a unit with a non-existent ID."""
#     response = test_client.get("/units/non-existent-id")
#     assert response.status_code == 404
#     data = response.json()
#     assert "error" in data
#     assert data["error"]["message"] == "Unit with id<non-existent-id> does not exist."
#
#
# def test_list_units(test_client):
#     """Test listing all units."""
#     test_client.post("/units", json={"name": "liters"})
#     test_client.post("/units", json={"name": "pieces"})
#
#     response = test_client.get("/units")
#     assert response.status_code == 200
#     data = response.json()
#     assert "units" in data
#     assert len(data["units"]) >= 2
#     unit_names = [unit["name"] for unit in data["units"]]
#     assert "liters" in unit_names
#     assert "pieces" in unit_names
