# Implementation Plan: Todo Full-Stack Web Application – Backend & REST API

**Branch**: `001-todo-backend-api` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-backend-api/spec.md`

## Summary

Build a multi-user todo web application with a Python FastAPI backend,
Neon Serverless PostgreSQL database (via SQLModel ORM), Better Auth
JWT authentication (on Next.js 16+ frontend), and a responsive UI.
The backend exposes 6 RESTful endpoints for task CRUD + completion,
all scoped to the authenticated user via JWT verification against
Better Auth's JWKS endpoint.

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript/Node.js 20+ (frontend)
**Primary Dependencies**: FastAPI 0.115+, SQLModel 0.0.22+, Pydantic 2.9+, PyJWT 2.9+, Next.js 16+, Better Auth, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL (shared between Better Auth and app)
**Testing**: pytest (backend), vitest (frontend)
**Target Platform**: Web (desktop + mobile responsive)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Standard web app expectations (<500ms p95 for API calls)
**Constraints**: JWT-based stateless auth; no shared secrets (asymmetric JWKS); Neon pooled connections with NullPool
**Scale/Scope**: Single-user to small team; ~5 screens; 2 entities (User, Task)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. Accuracy | All 6 endpoints return documented response shapes | PASS — OpenAPI contract defined in `contracts/openapi.yaml` |
| II. Security | JWT verified before route handlers; data scoped to user_id | PASS — PyJWT + JWKS verification; query scoped by `user_id` from JWT `sub` claim |
| III. Reproducibility | SQLModel ORM only; versioned migrations | PASS — Alembic for migrations; no raw SQL |
| IV. Clarity | OpenAPI auto-generated from typed models | PASS — FastAPI + Pydantic/SQLModel response models |
| V. RESTful Design | All 6 endpoints follow REST conventions | PASS — matches constitution API contract exactly |
| VI. Input Validation | Pydantic schemas validate all inputs; 422 on failure | PASS — TaskCreate/TaskUpdate schemas with constraints |

**Gate result**: ALL PASS — proceed to implementation.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-backend-api/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── openapi.yaml     # Phase 1 output
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, exception handlers
│   ├── config.py            # Pydantic Settings (.env loading)
│   ├── database.py          # SQLModel engine + session (NullPool)
│   ├── dependencies.py      # get_session(), verify_jwt()
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task SQLModel (table=True)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py          # TaskCreate, TaskUpdate, TaskRead
│   │   └── responses.py     # SuccessResponse[T], ErrorResponse
│   └── api/
│       ├── __init__.py
│       ├── router.py        # Main API router
│       └── tasks.py         # 6 task endpoints
├── tests/
│   ├── conftest.py          # Fixtures (test DB, mock JWT)
│   └── test_tasks.py        # Endpoint tests
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── requirements.txt
├── .env.example
└── pyproject.toml

frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home / redirect
│   ├── (auth)/
│   │   ├── signin/
│   │   │   └── page.tsx     # Sign in page
│   │   └── signup/
│   │       └── page.tsx     # Sign up page
│   ├── dashboard/
│   │   ├── layout.tsx       # Auth-protected layout
│   │   └── page.tsx         # Task list + CRUD UI
│   └── api/
│       └── auth/
│           └── [...all]/
│               └── route.ts # Better Auth handler
├── lib/
│   ├── auth.ts              # Better Auth server config
│   ├── auth-client.ts       # Better Auth client config
│   └── api.ts               # Backend API client (fetch wrapper)
├── components/
│   ├── task-list.tsx         # Task list component
│   ├── task-form.tsx         # Create/edit task form
│   ├── task-item.tsx         # Single task row
│   └── auth-form.tsx        # Sign in/up form
├── package.json
├── tailwind.config.ts
├── tsconfig.json
├── next.config.ts
├── .env.example
└── .env.local
```

**Structure Decision**: Web application layout with separate `backend/`
(Python/FastAPI) and `frontend/` (Next.js) directories. Each has
independent dependency management, testing, and startup scripts.
The two services communicate via HTTP (frontend → backend API calls
with JWT Bearer tokens).

## Key Technical Decisions

### D1: Asymmetric JWT via JWKS (not shared secret)

Better Auth issues JWTs signed with EdDSA (asymmetric). The FastAPI
backend fetches the public key from `{FRONTEND_URL}/api/auth/jwks`
using PyJWT's `PyJWKClient`. No shared secret is synchronized
between services.

### D2: Neon Pooled Connection + NullPool

Use Neon's `-pooler` hostname (built-in PgBouncer) and set
SQLAlchemy to `NullPool` to avoid double-pooling. Connection string
stored in `.env` with `?sslmode=require`.

### D3: UUID Primary Keys

Both `User` (Better Auth) and `Task` use UUID primary keys. Prevents
ID enumeration attacks; PostgreSQL has native UUID type with good
index performance.

### D4: Uniform Response Envelope

All endpoints return `{"success": bool, "data": ..., "message": ...}`
for success and `{"success": false, "error": ..., "details": [...],
"code": ...}` for errors. Implemented via Pydantic generics.

### D5: Better Auth Manages User Table

The `user` table is created and owned by Better Auth (via its CLI
migrations). The FastAPI `Task` model references `user.id` as a
foreign key. The backend never writes to the `user` table.

### D6: Agent Delegation

Implementation follows the constitution's agent delegation order:
1. **DB Agent** (`neon-postgres-manager`) — Task table + migrations
2. **Backend Agent** (`fastapi-backend`) — FastAPI app + all endpoints
3. **Auth Agent** (`auth-security`) — Better Auth + JWT verification
4. **Frontend Agent** (`nextjs-frontend-builder`) — Next.js UI

## Complexity Tracking

No constitution violations detected. No complexity justifications needed.
