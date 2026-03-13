# Implementation Plan: Frontend ChatKit Integration

**Branch**: `004-frontend-chatkit` | **Date**: 2026-02-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-frontend-chatkit/spec.md`

## Summary

Build a ChatKit-powered conversational UI that replaces the existing task list dashboard with a natural-language chat interface. The frontend uses `@openai/chatkit-react` to communicate with OpenAI's Responses API, which invokes an agent configured with MCP tools served from our FastAPI backend via `fastmcp`. Users manage todos (add, list, complete, delete, update) through chat messages. Conversation history is persisted in Neon PostgreSQL for cross-session continuity.

## Technical Context

**Language/Version**: TypeScript 5.x (frontend), Python 3.11+ (backend)
**Primary Dependencies**: Next.js 16+ (App Router), `@openai/chatkit-react` v1.6.0, FastAPI, `fastmcp`, `openai-agents`, Better Auth (JWT)
**Storage**: Neon Serverless PostgreSQL (existing) — new tables: `conversation_session`, `conversation_message`
**Testing**: Vitest (frontend), pytest (backend)
**Target Platform**: Web (responsive: 375px–1920px)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Chat response within 5s end-to-end (SC-001), conversation history loads within 2s for ≤100 messages (SC-002)
**Constraints**: ChatKit requires OpenAI-hosted agent sessions; MCP server must be publicly accessible (ngrok for dev); backend remains stateless per Principle XV/XIX
**Scale/Scope**: Single-user conversations up to 500 messages; 5 MCP tools; 2 new DB tables; ~10 new/modified files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Gate (Phase 0)

| Principle | Status | Notes |
|-----------|--------|-------|
| V: Agent-First API Design | PASS | Chat endpoint + MCP tools only; no direct CRUD from frontend |
| VI: Chat Protocol & Response Standards | PASS | Messages validated; agent handles ambiguity; friendly errors |
| VII: Usability (Chat-First) | PASS | ChatKit is the primary UI; conversation history visible |
| X: Frontend–Backend Alignment | PASS | Agent responses rendered verbatim; centralized API client used |
| XII: Security-First | PASS | JWT required for session creation; user_id from verified token |
| XIII: User Isolation | PASS | user_id injected at API layer; MCP tools scope queries |
| XVII: Agent Sovereignty | PASS | All task ops via OpenAI agent → MCP tools |
| XVIII: MCP Tool Boundary | PASS | FastMCP serves tools; no direct DB access from routes |
| XIX: Conversation Persistence | PASS | Messages persisted in `conversation_message` table |
| XX: Traceability | PASS | `tool_calls` JSON field captures MCP invocations |
| XXI: Graceful Degradation | PASS | Error states mapped; friendly messages; no silent failures |

### Post-Design Gate (Phase 1)

| Principle | Status | Notes |
|-----------|--------|-------|
| V: Agent-First API Design | PASS | Session creation route only; no task CRUD endpoints exposed to frontend |
| XIII: User Isolation | PASS | user_id extracted from JWT in API route, injected into agent instructions; MCP tools validate ownership |
| XIV: Auth Consistency | PASS | Same BETTER_AUTH_SECRET; JWT verified in Next.js API route before OpenAI session creation |
| XV: Statelessness | PASS | No server-side sessions; context rebuilt from DB + OpenAI thread |
| XVIII: MCP Tool Boundary | PASS | 5 tools registered via FastMCP; no direct DB access outside tools |
| XIX: Conversation Persistence | PASS | `conversation_session` + `conversation_message` tables in data model |

**Gate result**: PASS — No violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/004-frontend-chatkit/
├── plan.md              # This file
├── research.md          # Phase 0 output (complete)
├── data-model.md        # Phase 1 output (complete)
├── quickstart.md        # Phase 1 output (complete)
├── contracts/
│   ├── chat-api.md      # ChatKit session + history endpoints
│   └── mcp-tools.md     # MCP tool contracts (5 tools)
└── tasks.md             # Phase 2 output (/sp.tasks — pending)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── health.py          # Existing health endpoint
│   │   ├── router.py          # Existing router — add MCP mount
│   │   └── tasks.py           # Existing CRUD (retained for backward compat)
│   ├── models/
│   │   ├── task.py            # Existing Task model (no changes)
│   │   └── conversation.py    # NEW: ConversationSession, ConversationMessage
│   ├── mcp/
│   │   ├── __init__.py        # NEW: FastMCP server instance
│   │   └── tools.py           # NEW: 5 MCP tool functions
│   ├── schemas/
│   │   └── task.py            # Existing schemas (no changes)
│   ├── config.py              # Add OPENAI_API_KEY, MCP_SERVER_URL
│   ├── database.py            # Existing DB setup (no changes)
│   ├── dependencies.py        # Existing JWT verification (no changes)
│   └── main.py                # Mount MCP app, combine lifespans
└── tests/
    ├── test_mcp_tools.py      # NEW: MCP tool unit tests
    └── ...

frontend/
├── app/
│   ├── api/
│   │   └── chatkit/
│   │       ├── session/
│   │       │   └── route.ts   # NEW: POST — create ChatKit session
│   │       └── history/
│   │           └── route.ts   # NEW: GET — conversation history
│   ├── dashboard/
│   │   ├── layout.tsx         # Existing
│   │   └── page.tsx           # MODIFY: Replace task list with ChatKit
│   └── ...
├── components/
│   ├── chat/
│   │   ├── chat-container.tsx # NEW: ChatKit wrapper with session init
│   │   └── welcome-message.tsx# NEW: First-visit welcome with examples
│   ├── task-form.tsx          # Existing (can be removed post-migration)
│   ├── task-item.tsx          # Existing (can be removed post-migration)
│   └── task-list.tsx          # Existing (can be removed post-migration)
├── lib/
│   ├── api.ts                 # MODIFY: Add chatkit session/history methods
│   ├── auth.ts                # Existing (no changes)
│   └── auth-client.ts         # Existing (no changes)
└── ...
```

**Structure Decision**: Web application structure (Option 2). The project already uses `backend/` + `frontend/` separation established in Phase-II. New files are added within existing directories following established patterns. New `backend/src/mcp/` module encapsulates all MCP server logic. New `frontend/components/chat/` groups chat-specific components.

## Data Flow Architecture

```
┌─────────────────────┐     ┌───────────────────────┐     ┌──────────────┐
│  Frontend (Next.js)  │     │  OpenAI Infrastructure │     │  Backend     │
│                      │     │                        │     │  (FastAPI)   │
│  ChatKit component   │────▶│  Responses API / Agent │────▶│  /mcp        │
│  useChatKit()        │◀────│  (configured w/ MCP)   │◀────│  FastMCP     │
│                      │     │                        │     │  tools       │
│  /api/chatkit/       │     │                        │     │              │
│  session (Next API)  │─────┘                        │     │  Neon PG     │
└─────────────────────┘                               │     └──────────────┘
                                                      │
                                                      ▼
                                                ┌──────────┐
                                                │ Neon DB   │
                                                │ task      │
                                                │ conv_sess │
                                                │ conv_msg  │
                                                └──────────┘
```

**Key interaction**:
1. Frontend calls `POST /api/chatkit/session` (Next.js API route) → verifies JWT, creates OpenAI session with agent config + MCP tools URL → returns `client_secret`
2. ChatKit component uses `client_secret` to communicate directly with OpenAI
3. OpenAI agent processes user messages, invokes MCP tools on our FastAPI `/mcp` endpoint
4. MCP tools execute DB operations against Neon PostgreSQL
5. Results flow back: MCP tool → Agent → ChatKit → UI

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Chat UI library | `@openai/chatkit-react` | Constitution mandates ChatKit; provides streaming, thread management, message rendering |
| Agent hosting | OpenAI Responses API (hosted) | ChatKit requires OpenAI sessions; cannot use local agent execution |
| MCP transport | Streamable HTTP via FastMCP | Required for OpenAI's hosted agent to reach our tools |
| Conversation persistence | Dual: OpenAI threads + Neon PostgreSQL | OpenAI manages threads natively; Neon copy satisfies Principle XIX |
| Session creation | Next.js API route (server-side) | JWT verification + OpenAI API key must stay server-side |
| Dev MCP access | ngrok tunnel | OpenAI infra must reach local MCP server during development |

## Complexity Tracking

> No constitution violations detected. No complexity justifications needed.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |

## Phase Artifacts Summary

| Phase | Artifact | Status | Path |
|-------|----------|--------|------|
| 0 | research.md | Complete | `specs/004-frontend-chatkit/research.md` |
| 1 | data-model.md | Complete | `specs/004-frontend-chatkit/data-model.md` |
| 1 | contracts/chat-api.md | Complete | `specs/004-frontend-chatkit/contracts/chat-api.md` |
| 1 | contracts/mcp-tools.md | Complete | `specs/004-frontend-chatkit/contracts/mcp-tools.md` |
| 1 | quickstart.md | Complete | `specs/004-frontend-chatkit/quickstart.md` |
| 2 | tasks.md | Pending | Run `/sp.tasks` to generate |

## Follow-ups & Risks

- **Risk**: MCP server must be publicly accessible for OpenAI's agent to invoke tools. In development, ngrok introduces latency and requires manual tunnel management. Mitigation: Document setup in quickstart.md; consider Cloudflare Tunnel as alternative.
- **Risk**: user_id injection via agent system instructions is less secure than JWT-verified MCP calls. An attacker who can manipulate agent prompts could spoof user_id. Mitigation: Add API key validation on MCP server for production.
- **Follow-up**: After `/sp.tasks` generates tasks, delegate in order: DB Agent → Backend Agent → Auth Agent → Frontend Agent per constitution's agent delegation order.
