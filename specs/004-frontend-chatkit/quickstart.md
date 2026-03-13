# Quickstart: Frontend ChatKit Integration

**Feature**: 004-frontend-chatkit

## Prerequisites

- Node.js 20+ and npm
- Python 3.11+
- Neon PostgreSQL database (existing from Phase-II)
- OpenAI API key (with ChatKit and Responses API access)
- Better Auth configured (existing from Phase-II)

## Environment Variables

### Backend (.env) — additions to existing

```bash
# Existing
DATABASE_URL=postgresql://...@neon.tech/...
JWKS_URL=http://localhost:3000/api/auth/jwks
FRONTEND_URL=http://localhost:3000

# New for Phase-III
OPENAI_API_KEY=sk-...
MCP_SERVER_URL=http://localhost:8000/mcp  # Public URL in production
```

### Frontend (.env.local) — additions to existing

```bash
# Existing
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000

# New for Phase-III
OPENAI_API_KEY=sk-...
```

## Setup Steps

### 1. Install Backend Dependencies

```bash
cd backend
pip install fastmcp openai-agents
```

Adds to `requirements.txt`:
- `fastmcp>=2.0.0` — MCP server with FastAPI integration
- `openai-agents>=0.1.0` — OpenAI Agents SDK

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install @openai/chatkit-react
```

### 3. Run Database Migration

```bash
cd backend
alembic revision --autogenerate -m "add conversation tables"
alembic upgrade head
```

### 4. Start Backend (with MCP Server)

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

The MCP server is mounted at `http://localhost:8000/mcp`.

### 5. Expose MCP Server (Development Only)

For ChatKit to reach the MCP server via OpenAI, expose it:

```bash
ngrok http 8000
```

Update `MCP_SERVER_URL` in backend `.env` to the ngrok URL.

### 6. Start Frontend

```bash
cd frontend
npm run dev
```

### 7. Verify

1. Open `http://localhost:3000`
2. Sign in via Better Auth
3. Navigate to dashboard (chat page)
4. Type "Show my tasks" — should get an AI response
5. Type "Add a task: Test ChatKit" — should confirm creation
6. Type "Show my tasks" — should list the new task

## Architecture Verification

```
Frontend (ChatKit)     → OpenAI Responses API
                        → Agent calls MCP tools
                        → FastAPI /mcp endpoint
                        → Neon PostgreSQL
                        → Response flows back
```

**Health checks**:
- Backend: `GET http://localhost:8000/api/health`
- MCP: `POST http://localhost:8000/mcp` (MCP protocol handshake)
- Frontend: `http://localhost:3000`
