# Session 03 — Docker and service bootstrap

## Goal

Create the smallest runnable BusFlow backend foundation: an HTTP API process with explicit configuration, structured logs, liveness, and dependency-aware readiness checks for PostgreSQL and Redis.

## Delivered

- Python package configuration in `pyproject.toml`
- FastAPI application entry point
- Settings loaded from environment variables and `.env`
- JSON logging formatter
- Docker Compose services for PostgreSQL, Redis, and the API
- API container definition
- Liveness endpoint: `GET /health/live`
- Readiness endpoint: `GET /health/ready`
- Initial health and OpenAPI tests
- Make targets for install, test, lint, run, and Compose

## Acceptance criteria

- `/health/live` returns HTTP 200 without requiring PostgreSQL or Redis.
- `/health/ready` reports each dependency separately and returns HTTP 503 when either dependency is unavailable.
- Docker Compose defines health checks for both infrastructure dependencies.
- The API exposes OpenAPI documentation with both health endpoints.
- Python source compiles successfully.

## Verification

Successful in this environment:

```bash
python -m compileall -q src tests
git diff --check
```

Unavailable in this environment:

```bash
python -m ruff check .
python -m pytest -q
```

The configured Python executable does not have `ruff` or `pytest` installed, and the environment's package installer/runtime is unavailable. Docker is also not installed, so `docker compose up` could not be executed here.

These are environment gaps, not claims that the checks passed. They must be run after the development dependencies and Docker Desktop are available.

## Out of scope

- Database migrations
- Domain tables
- Redis Streams
- Authentication
- Frontend
- Production deployment
