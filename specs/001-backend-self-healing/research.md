# Research: Backend Self-Healing & Standalone Operation

**Feature**: 001-backend-self-healing
**Date**: 2026-02-12

## Decision 1: Auto-Table Creation Strategy

**Decision**: Use `SQLModel.metadata.create_all(engine)` in a FastAPI
`lifespan` context manager.

**Rationale**: This is the standard SQLModel/SQLAlchemy pattern. It's
idempotent (no-op if tables exist), requires no additional dependencies,
and coexists with Alembic migrations. Alembic handles schema evolution;
`create_all` handles first-time setup.

**Alternatives considered**:
- Alembic auto-run on startup: Too aggressive — could apply unwanted
  migrations in production. Requires careful version management.
- Manual migration only: Fails the self-healing requirement. Users
  must run `alembic upgrade head` before the server works.
- Custom migration script: Over-engineered for a single table. `create_all`
  achieves the same result with zero additional code.

## Decision 2: FastAPI Lifespan Pattern

**Decision**: Use the `lifespan` async context manager (FastAPI 0.93+)
instead of deprecated `on_startup`/`on_shutdown` events.

**Rationale**: `lifespan` is the current recommended pattern in FastAPI
docs. It provides clean setup/teardown semantics and is the only pattern
that supports shared state between startup and shutdown.

**Alternatives considered**:
- `@app.on_event("startup")`: Deprecated in FastAPI. Still works but
  emits deprecation warnings. Not future-proof.
- Module-level initialization: Runs at import time, not at server start.
  Can cause issues with testing and reloading.

## Decision 3: Health Check Design

**Decision**: Single `GET /api/health` endpoint that checks DB connectivity
via `SELECT 1`. No authentication required. Returns structured JSON.

**Rationale**: Health checks must be accessible without auth (used by load
balancers, monitoring systems). A DB ping validates the most critical
dependency. Placing it under `/api/` keeps it consistent with the existing
router structure.

**Alternatives considered**:
- `GET /health` (root-level): Would require a separate router outside
  `/api/` prefix. Less consistent with existing structure.
- Liveness + Readiness probes (Kubernetes-style): Over-engineered for
  current scope. Can be added later if containerized.
- Deep health check (all dependencies): Only one external dependency
  (database) exists. No need for multi-probe design.

## Decision 4: Logging Strategy

**Decision**: Use Python standard library `logging` module. Configure at
module level in `dependencies.py` and `main.py`. Log auth success/failure
and startup events.

**Rationale**: No additional dependencies needed. Standard library logging
integrates with uvicorn's logging. Structured enough for current needs.

**Alternatives considered**:
- `structlog`: Excellent for structured logging but adds a dependency
  for minimal benefit at this scale.
- `loguru`: Popular but non-standard. Unnecessary dependency.
- Print statements: Not production-grade. No log levels or formatting.

## Decision 5: Generic Error Handler

**Decision**: Add a catch-all `Exception` handler in `main.py` that
returns `ErrorResponse(error="Internal server error", code="INTERNAL_ERROR")`
with HTTP 500. Log the full exception with traceback at ERROR level.

**Rationale**: Prevents raw stack traces from leaking to clients.
Maintains the consistent `ErrorResponse` shape. Logs the full error
for debugging while returning a safe message to the client.

**Alternatives considered**:
- Middleware-based error handling: More complex. Exception handlers
  are the standard FastAPI pattern and integrate with OpenAPI docs.
- Custom exception classes: Over-engineered. The catch-all handler
  plus existing `HTTPException` and `RequestValidationError` handlers
  cover all cases.
