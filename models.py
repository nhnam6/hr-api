"""Models for the HR service"""

import enum

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Status(enum.Enum):
    """Status"""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    TERMINATED = "TERMINATED"


class Employee(Base):
    """Employee"""

    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    contact_info = Column(String)

    location = Column(String)
    location_search = Column(String, index=True)

    company = Column(String)
    company_search = Column(String, index=True)

    department = Column(String)
    department_search = Column(String, index=True)

    position = Column(String)
    position_search = Column(String, index=True)

    status = Column(SqlEnum(Status), default=Status.ACTIVE)

    organization_id = Column(Integer, index=True)

    def to_output(self, columns: list):
        """To output"""
        return {col: getattr(self, col) for col in columns}


class ColumnConfig(Base):
    """Column configuration"""

    __tablename__ = "column_configs"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer)
    column_name = Column(String)
