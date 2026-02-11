# Research: Todo Full-Stack Web Application – Backend & REST API

**Feature Branch**: `001-todo-backend-api`
**Date**: 2026-02-09

## R1: FastAPI + SQLModel Project Structure

**Decision**: Module-functionality layout with `backend/` and `frontend/` top-level directories.

**Rationale**: Clear separation of Python backend (FastAPI) and Node.js frontend (Next.js). Each has its own dependency management, testing, and deployment. The backend uses `src/` with sub-packages: `models/`, `schemas/`, `api/`, `services/`.

**Alternatives considered**:
- Single `src/` directory: rejected — conflates Python and Node.js code.
- Domain-driven (feature-per-folder): rejected — over-engineering for a todo app with 2 entities.

## R2: Neon PostgreSQL Connection Strategy

**Decision**: Use Neon's pooled connection string (`-pooler` hostname) with SQLAlchemy `NullPool`.

**Rationale**: Neon provides built-in PgBouncer pooling (up to 10,000 concurrent connections). Using `NullPool` in SQLAlchemy avoids double-pooling. The `?sslmode=require` parameter is mandatory for Neon.

**Alternatives considered**:
- SQLAlchemy `QueuePool` with direct connection: rejected — wastes resources on a serverless database; double-pooling causes connection leaks.
- `asyncpg` with async SQLModel: considered but rejected for v1 — adds complexity; sync `psycopg2-binary` is sufficient for initial load.

## R3: Primary Key Strategy

**Decision**: Use UUID primary keys (Python `uuid4`, PostgreSQL native `UUID` type).

**Rationale**: UUIDs prevent ID enumeration attacks (required by FR-009 security scope). PostgreSQL has native UUID indexing with good performance. IDs appear in URLs (`/tasks/{id}`), so non-guessable IDs are important.

**Alternatives considered**:
- Auto-increment integers: rejected — exposes record count, enables enumeration.
- Hybrid (int internal, UUID external): rejected — unnecessary complexity for a todo app.

## R4: JWT Authentication Architecture

**Decision**: Better Auth with JWT plugin on Next.js frontend; PyJWT with JWKS verification on FastAPI backend.

**Rationale**: Better Auth issues asymmetric JWTs (EdDSA) and exposes a `/api/auth/jwks` endpoint. The FastAPI backend fetches the public key from JWKS to verify tokens — no shared secret needed. This is more secure than symmetric HS256.

**Alternatives considered**:
- Shared HS256 secret: rejected — requires secret synchronization between services; less secure.
- python-jose: rejected — PyJWT has better JWKS support and is more actively maintained.
- Session-based auth: rejected — constitution mandates JWT tokens.

## R5: Response Envelope Pattern

**Decision**: Uniform JSON envelope with `success`, `data`, `message` for successes and `success`, `error`, `details`, `code` for errors.

**Rationale**: Constitution Principle VI requires consistent JSON structure. A typed envelope using Pydantic generics (`SuccessResponse[T]`) enables FastAPI's automatic OpenAPI documentation while keeping responses uniform.

**Alternatives considered**:
- Raw response (no envelope): rejected — violates FR-010 (consistent JSON structure).
- HTTP Problem Details (RFC 7807): considered for errors but adds complexity; simple error envelope is sufficient.

## R6: Python Version and Dependencies

**Decision**: Python 3.12 with FastAPI 0.115+, SQLModel 0.0.22+, Pydantic 2.9+.

**Rationale**: Python 3.12 offers best performance for async workloads and has long-term support until 2028. SQLModel 0.0.22+ supports Pydantic v2. FastAPI 0.115+ has the latest security patches.

**Key dependencies**:
- `fastapi>=0.115.0` — web framework
- `uvicorn[standard]>=0.34.0` — ASGI server
- `sqlmodel>=0.0.22` — ORM (wraps SQLAlchemy + Pydantic)
- `psycopg2-binary>=2.9.9` — PostgreSQL driver
- `pyjwt[crypto]>=2.9.0` — JWT verification
- `pydantic-settings>=2.7.0` — `.env` configuration
- `alembic>=1.14.0` — database migrations

## R7: Better Auth Database Sharing

**Decision**: Better Auth and the application share the same Neon PostgreSQL database.

**Rationale**: Better Auth creates its own tables (`user`, `session`, `account`, `verification_token`, `jwks`). Sharing the database reduces infrastructure costs and simplifies connection management. The `user` table created by Better Auth will be the authoritative user table — the FastAPI `Task` model references it via foreign key.

**Alternatives considered**:
- Separate database for auth: rejected — adds latency and complexity for a todo app.
- Separate PostgreSQL schema: considered but rejected — unnecessary isolation for this scale.

## R8: Frontend Framework Configuration

**Decision**: Next.js 16+ with App Router, Better Auth client plugin, and Tailwind CSS for styling.

**Rationale**: Constitution mandates Next.js 16+ with App Router. Better Auth provides a `@better-auth/react` client with hooks (`useSession`, `signIn`, `signUp`). Tailwind CSS is the standard styling choice for Next.js projects.

**Alternatives considered**:
- Pages Router: rejected — constitution mandates App Router.
- CSS Modules / styled-components: considered but Tailwind provides faster development for a todo app.
