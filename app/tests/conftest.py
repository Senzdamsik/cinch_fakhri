"""Test configuration and fixtures."""

from __future__ import annotations

import os
import socket
import time
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from alembic.command import upgrade
from alembic.config import Config
from app.db.database import Base  # Added import for Base


def get_test_db_url(include_db_name: bool = True) -> str:
    """Get database URL based on environment."""
    # Default credentials
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_name = "test-cinch-dev"  # Always use test-cinch-dev for testing

    # Try to detect if we're running in Docker
    try:
        socket.gethostbyname("db")
        host = "db"
        port = "5432"  # Docker environment uses internal port 5432
    except socket.gaierror:
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")  # Local environment uses 5432

    # Base URL without database name
    base_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}"

    # If TEST_DATABASE_URL is explicitly set, use that
    if test_url := os.getenv("TEST_DATABASE_URL"):
        return test_url

    # Return full URL with database name if requested
    return f"{base_url}/{db_name}" if include_db_name else base_url


def wait_for_db(timeout: int = 30) -> bool:
    """Wait for database to be ready."""
    print("Waiting for database to be ready...")
    start_time = time.time()
    db_url = get_test_db_url()  # Get the full URL including database name

    while True:
        try:
            print(f"Attempting to connect to database at {db_url}")
            engine = create_engine(db_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("Successfully connected to database")
            return True
        except OperationalError as e:
            print(f"Database not ready: {e}")
            if time.time() - start_time > timeout:
                print("Timeout waiting for database")
                return False
            time.sleep(2)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Iterator[None]:
    """Setup test database before running tests."""
    print("\nSetting up test environment...")

    # Wait for database to be ready
    if not wait_for_db():
        pytest.fail("Database is not available")

    # Set environment variable for other parts of the application
    os.environ["DATABASE_URL"] = get_test_db_url()

    # Get a connection to the database
    engine = create_engine(get_test_db_url())

    # Drop all tables and recreate them (clean slate for testing)
    print("Cleaning database...")
    Base.metadata.drop_all(engine)

    print("Running migrations...")
    # Run migrations
    alembic_cfg = Config("alembic.ini")
    upgrade(alembic_cfg, "head")
    print("Migrations completed")

    yield

    # Clean up after tests (optional, since we already drop tables at start)
    print("\nCleaning up after tests...")
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session() -> Iterator[Session]:
    """Create a new database session for a test."""
    engine = create_engine(get_test_db_url())
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    try:
        yield session
    finally:
        session.close()
