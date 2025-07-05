# HR Service

## Approach

The system is a **FastAPI-based microservice** that exposes a search API for employee data, with the following goals:

- Support **multi-criteria filtering**: location, department, status, etc.
- Enable **dynamic column configuration** via `ColumnConfig`
- andle **millions of records** efficiently using indexed and normalized fields
- Prevent abuse via **custom rate-limiting**
- Run in a fully **containerized environment** with Docker and optional Redis

## Key decisions

- Framework: `FastAPI` for lightweight/speed, aysnc support, and automatic OpenAPI docs

- Data Layer: `SQLAlchemy` ORM with `PostgreSQL`, `*_search` field used for normalized filters

- Rate Limiting: custom built native rate limiter using in-memory

- Pagination: Offset based pagination with support page and page_size

- Dynamic columns: each org can configure visible fields via ColumnConfig table

- Testing: unitest using pytest, FastAPI using TestClient

- Containerzation: `Docker`, `docker-compose`

## Assumption

- `ornigazation_id` is always know at query time

- Rate limiting is per IP per route, and Redis is available in production

- Each filterable field is normalized before query using `*_search` field

- Search does not require fuzzy/full-text ranking, only strict matching

## Trade-offs

| Feature             | Implemented Approach                            | Alternatives                                  | Trade-offs                                                     |
| ------------------- | ----------------------------------------------- | --------------------------------------------- | -------------------------------------------------------------- |
| **Filtering**       | `.in_()` queries on `*_search` fields           | LIKE, ILIKE, or full-text search              | Faster, indexable but no partial matching                      |
| **Normalization**   | Python-based text normalization (`unicodedata`) | Database-native FTS or trigram match          | More portable, but less powerful for fuzzy search              |
| **Pagination**      | Offset-based `LIMIT / OFFSET`                   | Keyset/cursor-based pagination                | Simple, but slower for deep paging                             |
| **Rate Limiting**   | Custom in-memory or Redis limiter               | NGINX/Kong/LB or `slowapi`/`limits` libraries | No external lib (as required), but not resilient to multi-node |
| **Dynamic Columns** | `ColumnConfig` in DB, applied via `to_output()` | GraphQL or projection fields in request       | Simpler for backend, less dynamic for client-side control      |
| **Testing DB**      | SQLite in-memory, model seeding                 | PostgreSQL + transactional rollback           | Lightweight and fast, but may miss PG-specific edge cases      |
