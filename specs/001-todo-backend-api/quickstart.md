# Quickstart: Todo Full-Stack Web Application

## Prerequisites

- Python 3.12+
- Node.js 20+
- A Neon PostgreSQL database (free tier: https://neon.tech)
- Git

## 1. Clone and Setup

```bash
git clone <repo-url>
cd PHASE-2
git checkout 001-todo-backend-api
```

## 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Environment

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

Required environment variables:

```env
# Neon PostgreSQL (use pooled connection string)
DATABASE_URL=postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require

# JWKS endpoint (Better Auth on frontend)
JWKS_URL=http://localhost:3000/api/auth/jwks

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

### Run Migrations

```bash
alembic upgrade head
```

### Start Backend

```bash
uvicorn src.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

## 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### Configure Environment

```bash
cp .env.example .env.local
```

Required environment variables:

```env
# Better Auth
BETTER_AUTH_SECRET=<random-secret-string>
BETTER_AUTH_URL=http://localhost:3000

# Database (same Neon database)
DATABASE_URL=postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Run Better Auth Migrations

```bash
npx @better-auth/cli@latest migrate
```

### Start Frontend

```bash
npm run dev
```

Frontend available at: http://localhost:3000

## 4. Verify Setup

1. Open http://localhost:3000 — you should see the sign-up page
2. Create an account
3. Open http://localhost:8000/docs — you should see the Swagger UI
4. Create a task via the frontend or Swagger UI
5. Verify the task appears in your task list

## Common Issues

| Issue | Fix |
|-------|-----|
| `SSL SYSCALL error` | Ensure `?sslmode=require` in DATABASE_URL |
| `connection refused` on port 8000 | Ensure backend is running with `uvicorn` |
| JWT verification fails | Ensure JWKS_URL matches your frontend URL |
| CORS errors in browser | Ensure FRONTEND_URL matches your frontend origin |
| `relation "task" does not exist` | Run `alembic upgrade head` |
| Better Auth tables missing | Run `npx @better-auth/cli@latest migrate` |
