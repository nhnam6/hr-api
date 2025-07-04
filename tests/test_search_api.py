from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db import get_db
from main import app
from models import Base, ColumnConfig, Employee, Status

# Use in-memory SQLite DB
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)


# Override get_db with testing DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Seed data
    db.add_all(
        [
            Employee(
                first_name="Alice",
                last_name="Nguyen",
                contact_info="alice@example.com",
                location="Hà Nội",
                location_search="ha noi",
                company="TechCorp",
                company_search="techcorp",
                department="Engineering",
                department_search="engineering",
                position="Backend Developer",
                position_search="backend developer",
                status=Status.ACTIVE,
                organization_id=1,
            ),
            Employee(
                first_name="Bob",
                last_name="Tran",
                contact_info="bob@example.com",
                location="Hồ Chí Minh",
                location_search="ho chi minh",
                company="TechCorp",
                company_search="techcorp",
                department="Engineering",
                department_search="engineering",
                position="Frontend Developer",
                position_search="frontend developer",
                status=Status.INACTIVE,
                organization_id=1,
            ),
        ]
    )

    db.add_all(
        [
            ColumnConfig(organization_id=1, column_name="first_name"),
            ColumnConfig(organization_id=1, column_name="position"),
        ]
    )

    db.commit()
    db.close()
    yield TestClient(app)


def test_search_employees(client):
    """Test search employees"""
    with patch("main.is_rate_limited", return_value=False):
        payload = {
            "organization_id": 1,
            "locations": ["ha noi"],
            "page": 1,
            "page_size": 10,
        }

        response = client.post("/search", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "results" in data
        assert len(data["results"]) == 1
        assert data["results"][0]["first_name"] == "Alice"
        assert "position" in data["results"][0]


def test_search_with_no_match(client):
    """Test search with no match"""
    with patch("main.is_rate_limited", return_value=False):
        payload = {
            "organization_id": 1,
            "locations": ["tokyo"],
            "page": 1,
            "page_size": 10,
        }

        response = client.post("/search", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 0
