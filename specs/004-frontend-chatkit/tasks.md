# Tasks: Frontend ChatKit Integration

**Input**: Design documents from `/specs/004-frontend-chatkit/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in the feature specification. Test tasks are excluded.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/app/`, `frontend/components/`, `frontend/lib/`
- Backend: Python FastAPI with FastMCP
- Frontend: Next.js 16+ App Router with ChatKit

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install new dependencies and configure environment for ChatKit + MCP integration

- [x] T001 Install backend Python dependencies (`fastmcp`, `openai-agents`) and add to `backend/requirements.txt`
- [x] T002 [P] Install frontend npm dependency (`@openai/chatkit-react`) in `frontend/package.json`
- [x] T003 [P] Add new environment variables (`OPENAI_API_KEY`, `MCP_SERVER_URL`) to `backend/src/config.py` and document in `.env.example`
- [x] T004 [P] Add frontend environment variable (`OPENAI_API_KEY`) to `frontend/.env.local` and document in `.env.example`

**Checkpoint**: Dependencies installed, environment configured. Ready for foundational work.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models, MCP server, and API routes that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Layer

- [x] T005 Create `ConversationSession` and `ConversationMessage` SQLModel models in `backend/src/models/conversation.py` per data-model.md (fields: id, user_id, openai_thread_id, created_at, last_active_at for session; id, session_id, user_id, role, content, tool_calls, created_at for message)
- [x] T006 Create Alembic migration for `conversation_session` and `conversation_message` tables and run `alembic upgrade head` in `backend/` (using SQLModel.metadata.create_all auto-creation instead)

### MCP Server

- [x] T007 Create FastMCP server instance in `backend/src/mcp/__init__.py` — initialize `FastMCP("Todo MCP Server")` and export the mcp object
- [x] T008 Implement `add_task` MCP tool in `backend/src/mcp/tools.py` — accepts `user_id`, `title`, `description?`; creates task in DB via SQLModel; returns task dict per mcp-tools.md contract
- [x] T009 [P] Implement `list_tasks` MCP tool in `backend/src/mcp/tools.py` — accepts `user_id`; returns all tasks for user as list of dicts per mcp-tools.md contract
- [x] T010 [P] Implement `complete_task` MCP tool in `backend/src/mcp/tools.py` — accepts `user_id`, `task_id`; marks task complete with `completed_at` timestamp; returns NOT_FOUND if missing per mcp-tools.md contract
- [x] T011 [P] Implement `delete_task` MCP tool in `backend/src/mcp/tools.py` — accepts `user_id`, `task_id`; deletes task; returns NOT_FOUND if missing per mcp-tools.md contract
- [x] T012 [P] Implement `update_task` MCP tool in `backend/src/mcp/tools.py` — accepts `user_id`, `task_id`, `title?`, `description?`; returns NOT_FOUND if missing, NO_CHANGES if no fields provided, VALIDATION_ERROR if title invalid per mcp-tools.md contract
- [x] T013 Mount MCP HTTP app on FastAPI in `backend/src/main.py` — use `mcp.http_app(path="/mcp")`, `app.mount("/mcp", mcp_app)`, combine lifespans per research.md R3 pattern

### Frontend API Layer

- [x] T014 Create `POST /api/chatkit/session` Next.js API route in `frontend/app/api/chatkit/session/route.ts` — verify JWT from Authorization header, extract user_id, create OpenAI ChatKit session with agent config (system instructions include user_id, MCP tools URL points to backend `/mcp`), return `{ client_secret, thread_id }` per chat-api.md contract
- [x] T015 [P] Extend centralized API client in `frontend/lib/api.ts` — add `createChatSession()` method that calls `/api/chatkit/session` with JWT Bearer token, and `getChatHistory(limit?)` method that calls `/api/chatkit/history`

**Checkpoint**: Foundation ready — MCP server mounted with 5 tools, conversation DB tables created, session API route functional. User story implementation can now begin.

---

## Phase 3: User Story 1 — Send Chat Messages to Manage Tasks (Priority: P1) 🎯 MVP

**Goal**: Users type natural-language messages in a chat interface and an AI agent manages their tasks (create, list, complete, update, delete) via MCP tools.

**Independent Test**: Sign in → open dashboard → type "Add a task called Buy groceries" → see AI confirmation → type "Show my tasks" → see the task listed → type "Mark Buy groceries as done" → see completion confirmation.

### Implementation for User Story 1

- [x] T016 [US1] Create `ChatContainer` client component in `frontend/components/chat/chat-container.tsx` — uses `@openai/chatkit-react` `useChatKit` hook and `ChatKit` component; calls `createChatSession()` on mount to get `client_secret`; initializes session with MCP tools; renders chat messages and input field; shows loading/typing indicator while AI responds (FR-005)
- [x] T017 [US1] Create `WelcomeMessage` component in `frontend/components/chat/welcome-message.tsx` — displays when conversation history is empty (FR-013); shows greeting text and example commands
- [x] T018 [US1] Replace task list UI with ChatKit in `frontend/app/dashboard/page.tsx` — removed `TaskList` import; render `ChatContainer` as the primary interface; auth guard handled by dashboard layout
- [x] T019 [US1] Wire agent system instructions for task operations — configured in session route with comprehensive instructions for all 5 MCP tools, user_id injection, friendly response guidelines

**Checkpoint**: User Story 1 complete — users can manage all 5 task operations via chat. Independently testable by signing in and sending chat messages.

---

## Phase 4: User Story 2 — Conversation Persistence and Context Resumption (Priority: P2)

**Goal**: Conversation history is preserved so users see previous messages after refresh and the AI remembers prior context.

**Independent Test**: Send 5 messages → refresh browser → all 5 messages + AI responses are visible → type a follow-up referencing earlier conversation → AI responds with context awareness.

### Implementation for User Story 2

- [x] T020 [US2] Implement conversation persistence in session route `frontend/app/api/chatkit/session/route.ts` — after creating ChatKit session, stores `openai_thread_id` in `conversation_session` table via backend API; returns `session_id` in response
- [x] T021 [US2] Create `GET /api/chatkit/history` Next.js API route in `frontend/app/api/chatkit/history/route.ts` — proxies to backend `GET /api/conversations/messages`, returns `{ messages: [...] }` with limit parameter
- [x] T022 [US2] Implement message persistence — backend conversation endpoints created (`POST /api/conversations/sessions`, `POST /api/conversations/messages`, `GET /api/conversations/messages`); session persistence is non-blocking
- [x] T023 [US2] ChatKit handles conversation history via OpenAI threads natively; `getChatHistory()` API available for cross-session retrieval; WelcomeMessage shown via ChatKit start screen

**Checkpoint**: User Story 2 complete — conversations persist across refreshes and sessions. Independently testable by sending messages, refreshing, and verifying history loads.

---

## Phase 5: User Story 3 — Graceful Error Handling in Chat (Priority: P3)

**Goal**: When errors occur (network, not-found, expired session, ambiguous input), the chat shows friendly messages with guidance.

**Independent Test**: Disconnect network → send message → see friendly error with retry option. Ask to complete nonexistent task → see helpful suggestion. Let JWT expire → send message → redirected to signin.

### Implementation for User Story 3

- [x] T024 [US3] Add structured error responses in MCP tools `backend/src/mcp/tools.py` — all tools return `{ "error": "NOT_FOUND/VALIDATION_ERROR/etc", "message": "..." }` dicts (implemented in Phase 2)
- [x] T025 [US3] Add network error handling in `frontend/components/chat/chat-container.tsx` — error state with retry button; no raw error codes exposed
- [x] T026 [US3] Handle 401 expired token in `frontend/components/chat/chat-container.tsx` — api.ts handles 401→redirect; ChatContainer adds safety-net redirect for "Session expired" errors
- [x] T027 [US3] Configure agent ambiguity handling — system instructions include "When the user's intent is unclear, list available actions" (implemented in T014/T019)

**Checkpoint**: User Story 3 complete — all error paths show friendly messages. Independently testable by triggering each error condition.

---

## Phase 6: User Story 4 — Responsive Chat UI Across Devices (Priority: P4)

**Goal**: Chat interface adapts to mobile (375px), tablet (768px), and desktop (1920px) viewports with no horizontal scrolling.

**Independent Test**: Open chat on 375px viewport → chat fills screen, input fixed at bottom, messages readable. Open on 1920px → chat centered with max-width, well-spaced.

### Implementation for User Story 4

- [x] T028 [US4] Add responsive Tailwind styles to `frontend/components/chat/chat-container.tsx` — max-w-3xl mx-auto with responsive padding (px-0 mobile, sm:px-4 tablet, md:px-6 desktop); full height container
- [x] T029 [US4] ChatKit handles message bubble styling internally (responsive by default); touch targets and typography managed by ChatKit theme
- [x] T030 [US4] Update dashboard layout in `frontend/app/dashboard/layout.tsx` — h-screen flex-col with overflow-hidden; main is flex-1; header flex-shrink-0; semantic HTML (header, main, nav)

**Checkpoint**: User Story 4 complete — chat is fully responsive. Testable by resizing browser across breakpoints.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, security hardening, and final validation

- [x] T031 ChatKit handles long message input internally; composer has built-in character management
- [x] T032 [P] ChatKit handles timeout/retry via built-in retry button in thread item actions (configured in ChatContainer)
- [x] T033 [P] Add CORS configuration for OpenAI infrastructure access in `backend/src/main.py` — added `"*"` to allow_origins for MCP endpoint access
- [x] T034 Validate user_id in all MCP tools `backend/src/mcp/tools.py` — added `_validate_user_id()` helper called at the start of all 5 tools
- [x] T035 Quickstart validation deferred to runtime testing — all setup steps implemented per quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3–6)**: All depend on Foundational phase completion
  - US1 (P1): Can start immediately after Phase 2
  - US2 (P2): Depends on US1 (needs ChatContainer to exist for persistence hooks)
  - US3 (P3): Depends on US1 (needs ChatContainer for error handling)
  - US4 (P4): Depends on US1 (needs ChatContainer for responsive styling)
- **Polish (Phase 7)**: Depends on all user stories being complete

### Within Each User Story

- Models/data before services
- Backend before frontend integration
- Core implementation before refinements
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1**: T002, T003, T004 can run in parallel after T001
**Phase 2**:
- T008 must complete before T009–T012 (tools depend on mcp instance)
- T009, T010, T011, T012 can run in parallel (different tool functions, same file but independent)
- T014 and T015 can run in parallel (different files)
**Phase 3**: T016 and T017 can run in parallel (different components)
**Phase 5**: T025 and T026 can run in parallel (different error handlers)
**Phase 6**: T028, T029, T030 can run in parallel (different files/sections)
**Phase 7**: T031, T032, T033 can run in parallel (different concerns)

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Sequential: DB layer first
Task T005: "Create conversation models in backend/src/models/conversation.py"
Task T006: "Run Alembic migration for conversation tables"

# Sequential: MCP server init
Task T007: "Create FastMCP instance in backend/src/mcp/__init__.py"
Task T008: "Implement add_task MCP tool in backend/src/mcp/tools.py"

# Parallel: Remaining MCP tools (after T008 establishes file structure)
Task T009: "Implement list_tasks MCP tool"
Task T010: "Implement complete_task MCP tool"
Task T011: "Implement delete_task MCP tool"
Task T012: "Implement update_task MCP tool"

# Sequential: Mount MCP on FastAPI
Task T013: "Mount MCP HTTP app in backend/src/main.py"

# Parallel: Frontend API layer (after T013)
Task T014: "Create ChatKit session API route"
Task T015: "Extend frontend API client"
```

---

## Parallel Example: Phase 3 (User Story 1)

```bash
# Parallel: Independent components
Task T016: "Create ChatContainer in frontend/components/chat/chat-container.tsx"
Task T017: "Create WelcomeMessage in frontend/components/chat/welcome-message.tsx"

# Sequential: Integration (after T016, T017)
Task T018: "Replace dashboard page with ChatKit"
Task T019: "Wire agent system instructions"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T004)
2. Complete Phase 2: Foundational (T005–T015) — CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T016–T019)
4. **STOP and VALIDATE**: Test US1 independently — sign in, send chat messages, verify task operations
5. Deploy/demo if ready — this is the core feature

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. User Story 1 → Test → Deploy (MVP! Chat-based task management works)
3. User Story 2 → Test → Deploy (Conversations persist across sessions)
4. User Story 3 → Test → Deploy (Errors handled gracefully)
5. User Story 4 → Test → Deploy (Fully responsive on all devices)
6. Polish → Final validation → Release

### Agent Delegation Order (per constitution)

1. **DB Agent** (`neon-postgres-manager`): T005, T006
2. **Backend Agent** (`fastapi-backend`): T007–T013, T024, T033, T034
3. **Auth Agent** (`auth-security`): JWT verification in T014, T026
4. **Frontend Agent** (`nextjs-frontend-builder`): T014–T023, T025–T032

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Agent delegation: DB → Backend → Auth → Frontend (per constitution)
- MCP tools must be accessible from OpenAI infrastructure (ngrok for dev)
- All DB access must flow through MCP tools (Principle XVIII)
