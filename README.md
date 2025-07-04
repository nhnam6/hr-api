# HR Service API

# Features

- **Dynamic employee search** – Filter by location, department, position, etc.
- **Configurable columns** – Organizations control which fields appear.
- **Pagination support** – Page and page size-based offset pagination.
- **Custom rate-limiting** – Naive per-IP limit (5 requests/minute), no libraries used.
- **Containerized** – Fully dockerized with PostgreSQL and Redis compatibility.
- **OpenAPI ready** – API documentation available at `/docs`.

## Technologies

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy** (ORM)
- **PostgreSQL** (Relational DB)
- **Redis** (Optional for rate limiting)
- **Docker + Docker Compose**

## Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hr-service.git
cd hr-service
```

## 2. Configure environment variables

Create `.env` file

```bash
COMPOSE_PROJECT_NAME=hr

DATABASE_URL=postgresql://admin:admin123@db:5432/master_db

REDIS_HOST=redis
REDIS_PORT=6379
```

## 3. Build and start services

```bash
docker-compose up --build
```

## 4. Access the API

- Docs: http://localhost:8000/docs

## Sample API Request

```bash
curl --location 'http://localhost:8000/search' \
--header 'Content-Type: application/json' \
--data '{
    "organization_id": 1,
    "locations": ["ha noi", "ho chi minh"],
    "departments": ["engineering"],
    "positions": ["backend developer"],
    "statuses": ["ACTIVE", "INACTIVE"],
    "page": 1,
    "page_size": 10
  }'

```

Response 200:

```bash
{
    "results": [
        {
            "id": null,
            "first_name": "Alice",
            "last_name": "Nguyen",
            "contact_info": "alice@example.com",
            "location": "Hà Nội",
            "company": "TechCorp",
            "department": "Engineering",
            "position": "Backend Developer",
            "status": "ACTIVE"
        }
    ],
    "page": 1,
    "page_size": 10,
    "total": 1
}
```

Rate limit:

```bash
{
    "detail": "Rate limit exceeded. Try again later."
}
```

## Running Tests

```bash
docker exec -it hr-service pytest -v --cov
```

```
============================================================================================================ test session starts ============================================================================================================
platform darwin -- Python 3.13.2, pytest-8.4.1, pluggy-1.6.0 -- /Users/0x442/workspace/labs/hr-api/.venv/bin/python3.13
cachedir: .pytest_cache
rootdir: /Users/0x442/workspace/labs/hr-api
configfile: pytest.ini
plugins: anyio-4.9.0, cov-6.2.1
collected 7 items

tests/test_health_check_api.py::test_health_check PASSED                                                                                                                                                                              [ 14%]
tests/test_search_api.py::test_search_employees PASSED                                                                                                                                                                                [ 28%]
tests/test_search_api.py::test_search_with_no_match PASSED                                                                                                                                                                            [ 42%]
tests/test_utils.py::test_normalize PASSED                                                                                                                                                                                            [ 57%]
tests/test_utils.py::test_get_visible_columns PASSED                                                                                                                                                                                  [ 71%]
tests/test_utils.py::test_filter_query_by_location PASSED                                                                                                                                                                             [ 85%]
tests/test_utils.py::test_filter_query_by_status PASSED                                                                                                                                                                               [100%]

============================================================================================================= warnings summary ==============================================================================================================
.venv/lib/python3.13/site-packages/pydantic/fields.py:1093
.venv/lib/python3.13/site-packages/pydantic/fields.py:1093
.venv/lib/python3.13/site-packages/pydantic/fields.py:1093
  /Users/0x442/workspace/labs/hr-api/.venv/lib/python3.13/site-packages/pydantic/fields.py:1093: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'env'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warn(

.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /Users/0x442/workspace/labs/hr-api/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

models.py:10
  /Users/0x442/workspace/labs/hr-api/models.py:10: MovedIn20Warning: The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base(). (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
    Base = declarative_base()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================================================================== tests coverage ===============================================================================================================
_____________________________________________________________________________________________ coverage: platform darwin, python 3.13.2-final-0 ______________________________________________________________________________________________

Name              Stmts   Miss  Cover
-------------------------------------
config.py            12      0   100%
db.py                11      4    64%
main.py              29      1    97%
models.py            33      0   100%
rate_limiter.py      19      0   100%
schemas.py           35      0   100%
utils.py             29      6    79%
-------------------------------------
TOTAL               168     11    93%
======================================================================================================= 7 passed, 5 warnings in 2.59s =======================================================================================================
/Users/0x442/workspace/labs/hr-api/.venv/lib/python3.13/site-packages/_pytest/unraisableexception.py:33: ResourceWarning: unclosed database in <sqlite3.Connection object at 0x10c8ac5e0>
  gc.collect()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
```

## Design Notes

### Performance Considerations

- Queries are always scoped by organization_id

- Indexes added on all searchable fields (\*\_search, status)

- Results are paginated with LIMIT/OFFSET

- Keyset pagination or sharding strategies can be added for very large datasets

### Rate Limiting

- Naive custom in-memory (or Redis-based) implementation

- 5 requests per IP per minute per route

### Security & Data Isolation

- All results are filtered by organization_id

- Only configured columns (ColumnConfig) are returned in response
