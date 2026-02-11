# Data Model: Backend Self-Healing & Standalone Operation

**Feature**: 001-backend-self-healing
**Date**: 2026-02-12

## Existing Entities (No Changes)

### Task

The `task` table is already defined in `backend/src/models/task.py` as a
SQLModel. No schema changes are needed for this feature.

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | Primary key, default uuid4 |
| user_id | UUID | Indexed, not null |
| title | str | Max 500 chars, not null |
| description | str or null | Optional |
| is_completed | bool | Default false |
| completed_at | datetime or null | Set when completed |
| created_at | datetime | Default UTC now |
| updated_at | datetime | Default UTC now |

### Auto-Creation Behavior

On startup, `SQLModel.metadata.create_all(engine)` will:
1. Check if the `task` table exists in the connected Neon PostgreSQL
2. If missing: create it with all columns, indexes, and constraints
3. If present: no-op (does not modify existing tables)

This ensures the Task model is always available without requiring manual
Alembic migration execution.

## New Response Models (No Database Tables)

### Health Check Response

Not a database entity. Returned by `GET /api/health`:

| Field | Type | Description |
|-------|------|-------------|
| status | str | "healthy" or "unhealthy" |
| database | str | "connected" or "disconnected" |
