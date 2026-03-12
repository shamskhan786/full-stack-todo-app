# Quickstart: Authentication & Security

**Feature**: 003-auth-security
**Date**: 2026-02-10

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+ and pip
- Neon PostgreSQL database (connection string)
- Both `frontend/` and `backend/` dependencies installed

## Environment Variables

### Frontend (`frontend/.env.local`)

```env
# Neon database (Better Auth stores user/session tables here)
DATABASE_URL=postgresql://user:pass@host/db

# Better Auth secret (signs sessions, not JWTs)
BETTER_AUTH_SECRET=your-random-secret-min-32-chars

# Better Auth base URL (used by client SDK)
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (`backend/.env`)

```env
# Neon database (task storage)
DATABASE_URL=postgresql://user:pass@host/db

# JWKS URL pointing to Better Auth's public key endpoint
JWKS_URL=http://localhost:3000/api/auth/jwks
```

**Note**: The backend does NOT need `BETTER_AUTH_SECRET`. It only needs
the JWKS URL to fetch public keys for JWT verification.

## Setup Steps

### 1. Install dependencies

```bash
# Frontend
cd frontend && npm install

# Backend
cd backend && pip install -r requirements.txt
```

### 2. Start both servers

```bash
# Terminal 1: Frontend (Better Auth runs here)
cd frontend && npm run dev
# → http://localhost:3000

# Terminal 2: Backend
cd backend && uvicorn src.main:app --reload --port 8000
# → http://localhost:8000
```

### 3. Verify Better Auth tables

On first run, Better Auth auto-creates these tables in the database:
- `user` — registered users
- `session` — active sessions
- `account` — credentials (hashed passwords)
- `jwks` — signing key pairs

Check with:
```sql
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

## Verification Checklist

### Auth Flow

1. **Sign up**: Visit `http://localhost:3000/signup`, create account
   - Expected: Account created, redirected to sign-in page

2. **Sign in**: Visit `http://localhost:3000/signin`, enter credentials
   - Expected: Authenticated, redirected to dashboard

3. **Token issuance**: Open browser DevTools → Network tab
   - Look for request to `/api/auth/token`
   - Expected: Response contains `{ "token": "eyJ..." }`

4. **API call with token**: On dashboard, tasks load automatically
   - Check Network tab for requests to `localhost:8000/api/{user_id}/tasks`
   - Expected: `Authorization: Bearer eyJ...` header present

### Security Boundaries

5. **No token → 401**: Using curl or Postman:
   ```bash
   curl http://localhost:8000/api/some-uuid/tasks
   ```
   - Expected: `403` (HTTPBearer returns 403 for missing credentials)

6. **Wrong user → 403**:
   ```bash
   curl -H "Authorization: Bearer <your-jwt>" \
        http://localhost:8000/api/different-user-uuid/tasks
   ```
   - Expected: `{"detail": "User ID mismatch"}`

7. **JWKS endpoint**:
   ```bash
   curl http://localhost:3000/api/auth/jwks
   ```
   - Expected: JSON with `keys` array containing EdDSA public key

### Sign Out

8. **Sign out**: Click sign-out button on dashboard
   - Expected: Redirected to `/signin`, cannot access `/dashboard`

## Running Backend Tests

```bash
cd backend && python -m pytest tests/ -v
```

All 22 tests should pass, including:
- `test_create_task_no_auth` — verifies 401 without token
- `test_list_tasks_isolation` — verifies cross-user data isolation
- `test_create_task_wrong_user` — verifies 403 on user_id mismatch

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| 401 on all API calls | JWKS_URL misconfigured | Verify `JWKS_URL` in `backend/.env` points to running frontend |
| "Could not validate credentials" | Frontend not running | Start frontend first (Better Auth must serve JWKS) |
| Better Auth tables missing | First run not completed | Visit any auth page to trigger auto-migration |
| CORS errors in browser | Backend CORS not configured | Check `src/main.py` allows `localhost:3000` origin |
| Token not attached to requests | `authClient.token()` failing | Check `NEXT_PUBLIC_BETTER_AUTH_URL` matches frontend URL |
