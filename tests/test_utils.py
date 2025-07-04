"""Test utils"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from models import Base, ColumnConfig, Employee, Status
from schemas import SearchQuery
from utils import filter_query, get_visible_columns, normalize


@pytest.fixture(scope="module")
def db_session():
    """Test database session"""
    # In-memory SQLite for testing
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    # Seed data
    employees = [
        Employee(
            first_name="Alice",
            last_name="Nguyen",
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
            location="Đà Nẵng",
            location_search="da nang",
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

    db.add_all(employees)

    db.add_all(
        [
            ColumnConfig(organization_id=1, column_name="first_name"),
            ColumnConfig(organization_id=1, column_name="position"),
        ]
    )

    db.commit()
    yield db
    db.close()


def test_normalize():
    """Test normalize"""
    assert normalize(" Hà Nội ") == "ha noi"
    assert normalize("") is None
    assert normalize(None) is None
    assert normalize("  TechCorp") == "techcorp"


def test_get_visible_columns(db_session: Session):
    """Test get visible columns"""
    cols = get_visible_columns(db_session, org_id=1)
    assert cols == ["first_name", "position"]


def test_filter_query_by_location(db_session: Session):
    """Test filter query by location"""
    query_obj = db_session.query(Employee)
    filters = SearchQuery(organization_id=1, locations=["hà nội"])
    filtered = filter_query(query_obj, filters).all()

    assert len(filtered) == 1
    assert filtered[0].first_name == "Alice"


def test_filter_query_by_status(db_session: Session):
    """Test filter query by status"""
    query_obj = db_session.query(Employee)
    filters = SearchQuery(organization_id=1, statuses=["INACTIVE"])
    filtered = filter_query(query_obj, filters).all()

    assert len(filtered) == 1
    assert filtered[0].first_name == "Bob"
