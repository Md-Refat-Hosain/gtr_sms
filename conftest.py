# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from main import app  # Import your FastAPI app
from fastapi.testclient import TestClient
from contextlib import contextmanager

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    # 1. Create all tables for a fresh test database
    Base.metadata.create_all(bind=engine)

    # 2. Yield a session for the test to use
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    # 3. Drop all tables to clean up after the test
    Base.metadata.drop_all(bind=engine)


# Override the get_db dependency in main.py
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Import and patch the get_db dependency
from main import get_db

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    # Use TestClient for synchronous testing of asynchronous endpoints
    with TestClient(app) as c:
        yield c
