"""Schemas for the authentication service"""

from enum import Enum
from typing import List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str
    message: str = "Service is healthy"


class StatusEnum(str, Enum):
    """Status enum"""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    TERMINATED = "TERMINATED"


class SearchQuery(BaseModel):
    """Search query"""

    organization_id: int
    locations: Optional[List[str]] = None
    companies: Optional[List[str]] = None
    departments: Optional[List[str]] = None
    positions: Optional[List[str]] = None
    statuses: Optional[List[StatusEnum]] = None

    page: int = 1
    page_size: int = 50


class Employee(BaseModel):
    """Employee output"""

    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_info: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    status: Optional[StatusEnum] = None


class EmployeeResponse(BaseModel):
    """Employee response"""

    results: List[Employee]
    page: int
    page_size: int
    total: int
