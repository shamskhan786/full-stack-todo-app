# Quickstart Guide: MCP Tools & Backend Agent Core

## Prerequisites

- Python 3.11+
- Node.js 18+
- Neon PostgreSQL database (existing from Phase-II)
- OpenAI API key
- Phase-II authentication already deployed

## Environment Variables

Add to `backend/.env`:

```env
# Existing from Phase-II
DATABASE_URL=postgresql://...@...neon.tech/...
BETTER_AUTH_SECRET=your-auth-secret

# New for Phase-III
OPENAI_API_KEY=your-openai-api-key
```

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
# Run database migrations for new tables (Conversation, Message)
python -m alembic upgrade head
# Start the server
uvicorn src.main:app --reload
```

## Development Workflow

1. **Database Models**: Define/update SQLModel models in `backend/src/models/`
2. **MCP Tools**: Implement tools in `backend/src/mcp/`
3. **Agent Config**: Configure agent in `backend/src/agents/`
4. **Chat Endpoint**: Implement in `backend/src/api/chat.py`
5. **Test**: Run `pytest backend/tests/`

## Testing the Chat Endpoint

```bash
# Get a JWT token first (via Phase-II auth)
TOKEN="your-jwt-token"
USER_ID="your-user-id"

# Send a chat message
curl -X POST "http://localhost:8000/api/${USER_ID}/chat" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task: Buy groceries"}'

# Expected response:
# {
#   "response": "I've added 'Buy groceries' to your task list!",
#   "conversation_id": "uuid-here"
# }
```

## Key Files

| File | Purpose |
|------|---------|
| `backend/src/models/conversation.py` | Conversation & Message SQLModel models |
| `backend/src/models/task.py` | Task SQLModel model (existing, may need updates) |
| `backend/src/mcp/tools.py` | MCP tool implementations |
| `backend/src/agents/todo_agent.py` | OpenAI Agent configuration |
| `backend/src/api/chat.py` | Chat endpoint handler |
| `backend/src/services/conversation.py` | Conversation context management |

## Architecture Flow

```
User Message → FastAPI /api/{user_id}/chat
  → JWT Verification (extract user_id)
  → Load Conversation History (from DB)
  → OpenAI Agent (with MCP tools)
    → MCP Tool Calls (add_task, list_tasks, etc.)
      → Database Operations (via SQLModel)
    → Agent Response
  → Persist Message + Response (to DB)
  → Return Response to User
```