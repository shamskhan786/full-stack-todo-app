# Quickstart: Backend Self-Healing & Standalone Operation

**Feature**: 001-backend-self-healing
**Date**: 2026-02-12

## Prerequisites

- Python 3.11+
- Neon PostgreSQL database (connection string)
- Backend dependencies installed (`pip install -r requirements.txt`)

## Environment Variables

### Backend (`backend/.env`)

```env
# Neon database connection (REQUIRED — server won't start without it)
DATABASE_URL=postgresql://user:pass@host/db

# JWKS URL for JWT verification (defaults to localhost:3000)
JWKS_URL=http://localhost:3000/api/auth/jwks

# Frontend URL for CORS (defaults to localhost:3000)
FRONTEND_URL=http://localhost:3000

# Environment (defaults to "development")
ENVIRONMENT=development
```

## Start the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### Expected Startup Behavior

On startup, the backend will:
1. Load settings from `.env`
2. Auto-create missing database tables (if any)
3. Validate database connectivity
4. Log startup status

You should see logs like:
```
INFO: Starting backend self-healing checks...
INFO: Database tables verified/created successfully
INFO: Database connectivity: OK
INFO: Backend startup complete
```

## Verification Checklist

### 1. Health Check

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status": "healthy", "database": "connected"}
```

### 2. Auto-Table Creation

1. Connect to Neon PostgreSQL and drop the `task` table:
   ```sql
   DROP TABLE IF EXISTS task;
   ```
2. Restart the backend:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```
3. Verify the table was recreated:
   ```sql
   SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public' AND table_name = 'task';
   ```
   Expected: `task` row present.

### 3. API Endpoints (with auth)

All 6 API endpoints require a valid JWT from Better Auth:

```bash
# List tasks (requires running frontend for JWT)
curl -H "Authorization: Bearer <jwt>" \
     http://localhost:8000/api/<user-id>/tasks
```

### 4. Error Handling

```bash
# Invalid UUID format
curl http://localhost:8000/api/not-a-uuid/tasks
# Expected: 422 with structured validation error

# No auth token
curl http://localhost:8000/api/11111111-1111-1111-1111-111111111111/tasks
# Expected: 403 (HTTPBearer rejects missing credentials)
```

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

All existing tests (22+) should pass, plus new health check tests.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Server won't start | Missing DATABASE_URL | Create `backend/.env` with connection string |
| Health check returns 503 | DB unreachable | Verify DATABASE_URL and Neon status |
| Tables not created | Model not imported | Ensure Task model is imported before `create_all` |
| Auth errors | JWKS_URL wrong | Verify frontend is running (serves JWKS) |
