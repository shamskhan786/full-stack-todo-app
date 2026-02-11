# Contract: Health Check Endpoint

**Feature**: 001-backend-self-healing
**Date**: 2026-02-12

## GET /api/health

**Authentication**: None (public endpoint)

**Purpose**: Report backend service health and database connectivity.
Used by monitoring systems, load balancers, and development tooling.

### Request

No request body or parameters.

```
GET /api/health HTTP/1.1
Host: localhost:8000
```

### Response — Healthy (200)

```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Response — Unhealthy (503)

Returned when the database is unreachable:

```json
{
  "status": "unhealthy",
  "database": "disconnected"
}
```

### Behavior

1. Execute `SELECT 1` against Neon PostgreSQL
2. If query succeeds: return 200 with `"database": "connected"`
3. If query fails (connection error, timeout): return 503 with
   `"database": "disconnected"`
4. Never throw an unhandled exception — always return structured JSON

## Existing Endpoints (No Changes)

The following endpoints are already implemented and require no
modifications for this feature:

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /api/{user_id}/tasks | JWT | List all tasks for user |
| POST | /api/{user_id}/tasks | JWT | Create a new task |
| GET | /api/{user_id}/tasks/{id} | JWT | Get a single task |
| PUT | /api/{user_id}/tasks/{id} | JWT | Update a task (full) |
| DELETE | /api/{user_id}/tasks/{id} | JWT | Delete a task |
| PATCH | /api/{user_id}/tasks/{id}/complete | JWT | Mark task complete |
