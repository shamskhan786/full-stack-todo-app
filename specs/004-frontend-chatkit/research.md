# Research: Frontend ChatKit Integration

**Feature**: 004-frontend-chatkit
**Date**: 2026-02-15

## R1: ChatKit Architecture & Constraints

**Decision**: Use `@openai/chatkit-react` v1.6.0 as the chat UI component.

**Rationale**: ChatKit is OpenAI's batteries-included framework for AI
chat experiences. It provides message rendering, streaming, thread
management, and rich interactive widgets out of the box. The
constitution mandates ChatKit for the Chat UI layer.

**Key constraint**: ChatKit requires OpenAI's session management. The
`useChatKit` hook requires a `getClientSecret()` callback that creates
sessions via the OpenAI API. ChatKit communicates directly with
OpenAI's servers — it cannot be pointed at a custom backend endpoint.

**Alternatives considered**:
- Custom React chat component: Full control but violates constitution's
  ChatKit mandate and requires rebuilding streaming, thread management,
  and message rendering from scratch.
- Vercel AI SDK `useChat`: Good streaming support but not ChatKit as
  specified. Could be a fallback if ChatKit integration proves
  impractical.

**Installation**: `npm install @openai/chatkit-react`

## R2: OpenAI Agents SDK + MCP Integration

**Decision**: Use the OpenAI Agents SDK (Python `openai-agents`)
for agent configuration. The agent runs on OpenAI's infrastructure
via the Responses API, invoked through ChatKit sessions. MCP tools
are served from our FastAPI backend via Streamable HTTP transport.

**Rationale**: ChatKit creates sessions that use OpenAI's Responses API.
The agent is configured with MCP tools that point to our publicly
accessible FastAPI MCP server. This satisfies both the ChatKit and
Agents SDK constraints.

**Data flow**:
```
Frontend (ChatKit) → OpenAI (Responses API / Agent)
                     → MCP tool call → our FastAPI MCP server
                     → Neon PostgreSQL
                     → tool result back to OpenAI
                     → agent response back to ChatKit
```

**Key packages**:
- `openai-agents` (Python): Agent definition, MCP server utilities
- `fastmcp` (Python): MCP server with FastAPI integration
- `@openai/chatkit-react` (npm): Frontend chat UI

**Alternatives considered**:
- Local agent execution via `Runner.run()` with custom chat endpoint:
  Would give full control over conversation flow but cannot work with
  ChatKit's session-based architecture.
- HostedMCPTool (entirely on OpenAI): Simpler but less control over
  tool execution. Requires public MCP server URL regardless.

## R3: MCP Server on FastAPI (FastMCP)

**Decision**: Use `fastmcp` Python library to create an MCP server
mounted on the existing FastAPI application at `/mcp`.

**Rationale**: FastMCP provides native FastAPI integration via
`mcp.http_app()` and `app.mount()`. It auto-generates tool schemas
from Python function signatures and docstrings, matching the Agents
SDK's tool registration pattern.

**Integration pattern**:
```python
from fastmcp import FastMCP
from fastapi import FastAPI

mcp = FastMCP("Todo MCP Server")

@mcp.tool
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Create a new task for the user."""
    ...

mcp_app = mcp.http_app(path="/mcp")
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/mcp", mcp_app)
```

**Critical**: Must pass `lifespan=mcp_app.lifespan` to FastAPI or use
`combine_lifespans()` if the app has existing lifespan logic.

**Required MCP tools**:
- `add_task(user_id, title, description?)` → creates task
- `list_tasks(user_id)` → returns all tasks for user
- `complete_task(user_id, task_id)` → marks task complete
- `delete_task(user_id, task_id)` → deletes task
- `update_task(user_id, task_id, title?, description?)` → updates task

**Alternatives considered**:
- Official `mcp` SDK directly: Lower-level, more boilerplate. FastMCP
  is the recommended high-level API and was originally incorporated
  into the official SDK.
- Converting existing FastAPI CRUD endpoints via `FastMCP.from_fastapi()`:
  Possible but the existing endpoints use user_id in URL paths and
  JWT auth. MCP tools have a different contract (user_id as parameter,
  no HTTP auth). Cleaner to write dedicated MCP tool functions.

## R4: Conversation Persistence Strategy

**Decision**: OpenAI manages conversation threads natively via ChatKit.
Additionally, implement a `save_conversation` MCP tool that persists
messages to Neon PostgreSQL, satisfying the constitution's persistence
requirement (Principle XIX).

**Rationale**: ChatKit manages threads on OpenAI's servers automatically.
Duplicating this in Neon ensures we meet the constitution's requirement
that conversations persist in our database. The MCP tool approach lets
the agent save messages as part of its workflow.

**Alternative approach**: Create a separate `conversation_message` table
and have the Next.js API route (session creation) or a background job
sync from OpenAI's thread API to Neon. This is more complex but
ensures all messages are captured regardless of agent behavior.

**Recommended**: Use the Next.js API route approach — after creating a
ChatKit session, store the session/thread ID in Neon. Use OpenAI's
Thread API to retrieve conversation history when needed for our own
persistence layer.

## R5: Authentication Flow with ChatKit

**Decision**: Better Auth JWT tokens authenticate the user on the
frontend. When creating a ChatKit session, the Next.js API route
verifies the JWT and injects the user_id into the agent's instructions
and MCP tool configuration.

**Flow**:
1. User signs in via Better Auth → JWT token
2. Frontend calls `POST /api/chatkit/session` with JWT
3. API route verifies JWT, extracts user_id
4. API route creates OpenAI ChatKit session with agent config that
   includes user_id in system instructions
5. MCP tools on our backend receive user_id as a parameter from the
   agent (injected via system prompt)
6. MCP tools validate user_id before DB operations

**Security consideration**: The user_id is injected into the agent's
system instructions. The agent then includes it when calling MCP tools.
This is not as secure as extracting user_id from a JWT on the MCP
server side. For additional security, the MCP server should validate
the user_id against an API key or session token.

## R6: Public MCP Server Requirement

**Decision**: For development, use a tunneling service (ngrok) to expose
the local FastAPI MCP server. For production, deploy the MCP server to
a public URL.

**Rationale**: OpenAI's agent calls MCP tools via HTTP. The MCP server
must be accessible from OpenAI's infrastructure. In development, this
requires a tunnel.

**Alternatives considered**:
- MCPServerStdio (local subprocess): Only works when the agent runs
  locally via `Runner.run()`. Not compatible with ChatKit's hosted
  agent model.
- Deploy backend first, then develop frontend: Would work but slows
  down the development loop.

**Recommendation**: Use ngrok for development. Document the setup in
quickstart.md.
