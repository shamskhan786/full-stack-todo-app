# Implementation Plan: Backend Self-Healing & Standalone Operation

**Branch**: `001-backend-self-healing` | **Date**: 2026-02-12 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-backend-self-healing/spec.md`

## Summary

Make the backend standalone and self-healing: auto-create missing database
tables on startup, add a health check endpoint, add startup validation for
configuration/database connectivity, and improve error resilience. The
backend already has full API routes, JWT auth, and user isolation — this
feature adds the reliability and auto-recovery layer.

## Technical Context

**Language/Version**: Python 3.11+ (backend only — no frontend changes)
**Primary Dependencies**: FastAPI >=0.115, SQLModel >=0.0.22, PyJWT[crypto] >=2.9, Alembic >=1.14
**Storage**: Neon Serverless PostgreSQL (via SQLModel + NullPool)
**Testing**: pytest >=8.0 + httpx >=0.27
**Target Platform**: Linux/Windows server (uvicorn)
**Project Type**: Web application (backend only for this feature)
**Performance Goals**: Startup < 30s with auto-table creation; API responses < 2s
**Constraints**: Backend-only changes; no frontend modifications
**Scale/Scope**: Single `task` table; 6 API routes + 1 new health check

## Existing Implementation Audit

The backend is **already functional** with all API routes, JWT auth, and
user isolation. This plan identifies gaps and adds self-healing capabilities.

| Component | Current State | Gap |
|-----------|--------------|-----|
| DB connection | `database.py` — engine with NullPool | No startup validation |
| Table creation | Alembic migration exists | No `create_all` fallback for missing tables |
| API routes | All 6 routes match constitution spec | No health check endpoint (FR-009) |
| JWT validation | `verify_jwt` via JWKS + PyJWT | Already handles expired/invalid tokens |
| User filtering | `_verify_user_id()` on all 6 routes | Already enforces user isolation |
| Error handling | Exception handlers for validation + HTTP | No generic 500 handler, no startup checks |
| Health check | Missing | FR-009 requires health check endpoint |
| Startup validation | Missing | FR-005 requires config/DB validation on boot |
| Logging | Missing | FR-008 requires auth event logging |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Accuracy (API Correctness) | PASS | All 6 endpoints return documented response shapes |
| II. Security (Data Protection) | PASS | `verify_jwt` on all routes, `_verify_user_id` enforces user scoping |
| III. Reproducibility | PASS | SQLModel ORM, Alembic migrations versioned |
| IV. Clarity | PASS | FastAPI auto-docs, typed request/response models |
| V. RESTful API Design | PASS | Routes match constitution contract exactly |
| VI. Input Validation | PASS | Pydantic schemas, 422 structured errors |
| XII. Security-First | PASS | JWT required on all protected routes |
| XIII. User Isolation | PASS | All queries scoped by `user_id` from JWT `sub` |
| XIV. Auth Consistency | PASS | JWKS-based verification aligned with Better Auth |
| XV. Statelessness | PASS | No server-side sessions; JWT-only auth |
| XVI. Auth Clarity | PASS | Single `verify_jwt` dependency; no duplication |

All gates pass. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-backend-self-healing/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── health-endpoint.md
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (backend only — no frontend changes)

```text
backend/
├── src/
│   ├── __init__.py
│   ├── config.py           # Settings (existing)
│   ├── database.py         # Engine + create_all on startup (MODIFY)
│   ├── main.py             # App + lifespan startup handler (MODIFY)
│   ├── dependencies.py     # verify_jwt, get_session (existing)
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py         # Task SQLModel (existing)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py         # TaskCreate/Read/Update (existing)
│   │   └── responses.py    # SuccessResponse/ErrorResponse (existing)
│   └── api/
│       ├── __init__.py
│       ├── router.py       # API router (MODIFY — add health route)
│       ├── tasks.py        # Task CRUD routes (existing)
│       └── health.py       # Health check endpoint (NEW)
├── tests/
│   ├── conftest.py         # Test fixtures (existing)
│   ├── test_tasks.py       # 22 task tests (existing)
│   └── test_health.py      # Health check tests (NEW)
├── alembic/                # Migration framework (existing)
├── alembic.ini             # Alembic config (existing)
├── requirements.txt        # Dependencies (existing)
└── pyproject.toml          # Project config (existing)
```

**Structure Decision**: Backend-only web application structure. Files
marked (MODIFY) receive changes; files marked (NEW) are created. All
other files remain unchanged.

## Implementation Approach

### Gap 1: Auto-Create Missing Tables on Startup (FR-001, FR-005)

**Current**: `database.py` creates the engine but never calls
`SQLModel.metadata.create_all(engine)`. Tables only exist if Alembic
migrations have been run manually.

**Fix**: Add a `lifespan` context manager to `main.py` that calls
`SQLModel.metadata.create_all(engine)` on startup. This is idempotent —
if tables already exist, it's a no-op. This satisfies FR-001 (auto-create)
and FR-005 (auto-recovery on startup).

**Alembic coexistence**: `create_all` creates tables that don't exist but
does not modify existing tables. Alembic remains the authority for schema
migrations. This is the standard SQLModel/SQLAlchemy pattern for
development and self-healing environments.

### Gap 2: Health Check Endpoint (FR-009)

**Current**: No health check endpoint exists.

**Fix**: Add `GET /api/health` returning `{"status": "healthy",
"database": "connected"}`. The endpoint attempts a lightweight DB query
(`SELECT 1`) and reports connectivity. No authentication required.

### Gap 3: Startup Configuration Validation (FR-005)

**Current**: `Settings` uses `pydantic-settings` which already validates
`DATABASE_URL` is present (required field, no default). But there's no
explicit startup check for DB connectivity.

**Fix**: In the `lifespan` handler, after `create_all`, execute a test
query to validate the DB connection. Log the result. If it fails, log
the error but still allow the server to start (endpoints will fail
individually with appropriate errors).

### Gap 4: Auth Event Logging (FR-008)

**Current**: No logging configured.

**Fix**: Add Python `logging` to `verify_jwt` to log authentication
attempts (success/failure). Use standard library logging — no new
dependencies.

### Gap 5: Generic Exception Handler (FR-005, FR-007)

**Current**: Only `RequestValidationError` and `HTTPException` are
handled. Unhandled exceptions result in raw 500 responses.

**Fix**: Add a catch-all `Exception` handler that returns a structured
`ErrorResponse` with code `INTERNAL_ERROR`. This prevents stack traces
from leaking to clients.

## Complexity Tracking

No constitution violations. No complexity justifications needed.
