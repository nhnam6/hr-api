"""Auth service"""

from typing import Any, Dict

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import get_db
from models import Employee
from rate_limiter import is_rate_limited
from schemas import EmployeeResponse, HealthResponse, SearchQuery
from utils import filter_query, get_visible_columns

app = FastAPI(title="HR Service")


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limit middleware"""
    if is_rate_limited(request):
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded. Try again later.",
            },
        )
    return await call_next(request)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    description="Check if the API service is running and healthy",
    response_description="Health status of the service",
)
def health_check_api() -> Dict[str, Any]:
    """
    Health check endpoint
    """
    return {"status": "ok", "message": "Service is healthy"}


@app.post(
    "/search",
    response_model=EmployeeResponse,
    tags=["Search"],
    summary="Search employees",
    description="Search employees",
    response_description="List of employees",
)
def search_employees_api(query: SearchQuery, db: Session = Depends(get_db)):
    """Search employees"""
    org_id = query.organization_id
    offset = (query.page - 1) * query.page_size

    base_query = db.query(Employee).filter(Employee.organization_id == org_id)
    base_query = filter_query(base_query, query)

    total = base_query.count()
    employees = base_query.limit(query.page_size).offset(offset).all()

    columns = get_visible_columns(db, org_id)
    results = [e.to_output(columns) for e in employees]

    return {
        "results": results,
        "page": query.page,
        "page_size": query.page_size,
        "total": total,
    }
