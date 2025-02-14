from typing import Generator

import pytest
from fastapi.testclient import TestClient

from database.connection import (
    close_db,
    disable_test_mode,
    enable_test_mode,
    get_connection,
    init_db,
)
from main import app


@pytest.fixture(scope="function", autouse=True)
def test_client() -> Generator[TestClient, None, None]:
    """Fixture for setting up the test client and database."""

    enable_test_mode()  # Enable test mode for in-memory database
    init_db()  # Initialize the test database schema

    client = TestClient(app)  # Create client BEFORE clearing tables

    connection = get_connection()
    cursor = connection.cursor()

    # Clear all relevant tables
    tables_to_clear = ["units", "products", "receipts", "receipt_products"]
    for table in tables_to_clear:
        cursor.execute(f"DELETE FROM {table}")

    connection.commit()

    yield client  # Yield client for use in tests

    disable_test_mode()  # Disable test mode AFTER test execution
    close_db()  # Ensure database connection is properly closed
# @pytest.fixture(scope="function")
# def clean_db():
#     """Fixture to clean the database after a test."""
#     yield  # Wait until the test is done
#     connection = get_connection()
#     cursor = connection.cursor()
#     cursor.execute("DELETE FROM units")
#     cursor.execute("DELETE FROM products")
#     cursor.execute("DELETE FROM receipts")
#     cursor.execute("DELETE FROM receipt_products")
#     connection.commit()
#
#



# @pytest.fixture(scope="function", autouse=True)
# def clean_database():
#     """Clean the database before each test."""
#     connection = get_connection()
#     cursor = connection.cursor()
#     cursor.execute("DELETE FROM units")  # Clear the units table
#     connection.commit()
