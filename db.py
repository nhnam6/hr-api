"""Database configuration"""

from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI
def get_db() -> Any:
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
