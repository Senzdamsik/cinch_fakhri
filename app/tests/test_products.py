"""Tests for the products endpoints."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session, sessionmaker

from app.db.database import Base, get_db
from app.main import app
from app.tests.conftest import get_test_db_url

engine = create_engine(get_test_db_url())
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db() -> Iterator[Session]:
    """Create a fresh database session for each test.

    This fixture handles the setup and teardown of the test database,
    ensuring each test runs with a clean database state.

    Yields:
        Iterator[Session]: A SQLAlchemy session for test database operations.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db: Session) -> Iterator[TestClient]:
    """Create a test client with a database session.

    Args:
        db (Session): The database session fixture.

    Yields:
        Iterator[TestClient]: A FastAPI test client configured with the test database.
    """
    app.dependency_overrides[get_db] = lambda: db
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


def seed_test_data(db_connection: Connection) -> None:
    """Seed the test database with initial data.

    Args:
        db_connection (Connection): SQLAlchemy database connection.
    """
    with open("scripts/seed_test_data.sql") as file:
        sql = file.read()
        with db_connection.begin():
            db_connection.execute(text(sql))


@pytest.mark.asyncio
async def test_get_product(client: TestClient, db: Session) -> None:
    """Test retrieving a single product.

    Tests the GET /products/{id} endpoint by verifying the response contains
    the expected product data, including attributes and pricing information.

    Args:
        client (TestClient): The test client fixture.
        db (Session): The database session fixture.
    """
    with engine.connect() as connection:
        seed_test_data(connection)

    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"
    assert len(response.json()["attributes"]) == 1
    assert response.json()["attributes"][0]["name"] == "Color"
    assert response.json()["pricings"][0]["price"] == 100.0


@pytest.mark.asyncio
async def test_list_products(client: TestClient, db: Session) -> None:
    """Test listing and filtering products.

    Tests the GET /products endpoint with various filter combinations:
    - List all products
    - Filter by region
    - Filter by rental period
    - Filter by both region and rental period

    Args:
        client (TestClient): The test client fixture.
        db (Session): The database session fixture.
    """
    with engine.connect() as connection:
        seed_test_data(connection)

    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
    assert data["items"][0]["name"] == "Laptop"

    response = client.get("/products?region=Singapore")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    for item in data["items"]:
        assert any(pricing["region"] == "Singapore" for pricing in item["pricings"])

    response = client.get("/products?rental_period=3")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    for item in data["items"]:
        assert any(pricing["rental_period"] == 3 for pricing in item["pricings"])

    response = client.get("/products?region=Singapore&rental_period=3")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    for item in data["items"]:
        assert any(
            pricing["region"] == "Singapore" and pricing["rental_period"] == 3
            for pricing in item["pricings"]
        )
