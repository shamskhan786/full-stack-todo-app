# Tasks: MCP Tools & Backend Agent Core

**Input**: Design documents from `/specs/005-mcp-tools-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests included as Phase 4 validation tasks per user request.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Backend Python source in `backend/src/`
- Tests in `backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install new dependencies and configure environment for OpenAI Agents SDK + MCP SDK integration

- [x] T001 Add openai-agents and fastmcp dependencies to backend/requirements.txt and verify installation with `pip install -r backend/requirements.txt` — ALREADY PRESENT (fastmcp>=2.0.0, openai-agents>=0.1.0)
- [x] T002 Add OPENAI_API_KEY to backend/.env.example and verify backend/src/config.py loads it correctly (already has OPENAI_API_KEY field) — ALREADY CONFIGURED in config.py:10
- [x] T003 [P] Verify MCP server mount point in backend/src/main.py is correctly configured at `/mcp` path — VERIFIED at main.py:112

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database models and MCP tool infrastructure that MUST be complete before user story implementation

**NOTE**: The Phase-II codebase already has Task model, ConversationSession/ConversationMessage models, MCP tools skeleton, JWT verification, and API routes. This phase focuses on validating and upgrading existing infrastructure to meet Phase-III requirements.

- [x] T004 Review and update Task model in backend/src/models/task.py to ensure fields align with data-model.md — VERIFIED: has id(UUID), user_id, title, description, is_completed, created_at, updated_at
- [x] T005 [P] Review and update ConversationSession model in backend/src/models/conversation.py — VERIFIED: has id(UUID), user_id, openai_thread_id, created_at, last_active_at
- [x] T006 [P] Review and update ConversationMessage model in backend/src/models/conversation.py — VERIFIED: has id(UUID), session_id(FK), user_id, role, content, tool_calls(JSON), created_at
- [x] T007 Create Alembic migration for any model changes — NO CHANGES NEEDED, existing models are aligned
- [x] T008 Validate MCP tool schemas in backend/src/mcp/tools.py match contracts/mcp-tools.json — VERIFIED: all 5 tools present with user_id parameter
- [x] T009 Verify JWT verification dependency in backend/src/dependencies.py — VERIFIED: extracts user_id from JWT sub claim at line 46
- [x] T010 [P] Configure structured logging in backend/src/main.py with Python logging module for traceability of agent actions and MCP tool calls — DONE

**Checkpoint**: Foundation ready — all models migrated, MCP tools schema-validated, JWT verified, logging configured

---

## Phase 3: User Story 1 — AI Agent Interacts with Todo System (Priority: P1) MVP

**Goal**: AI agent can invoke all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) to manage tasks for authenticated users

**Independent Test**: Send a chat message like "Add a task: Buy groceries" and verify the agent calls add_task MCP tool, task is persisted in DB, and agent returns a human-readable confirmation

### Implementation for User Story 1

- [x] T011 [US1] Implement add_task MCP tool in backend/src/mcp/tools.py — ALREADY IMPLEMENTED with user_id scoping, title validation (1-500 chars)
- [x] T012 [US1] Implement list_tasks MCP tool in backend/src/mcp/tools.py — ALREADY IMPLEMENTED with user_id filter, ordered by created_at
- [x] T013 [P] [US1] Implement complete_task MCP tool in backend/src/mcp/tools.py — ALREADY IMPLEMENTED with user_id ownership check, completed_at timestamp
- [x] T014 [P] [US1] Implement delete_task MCP tool in backend/src/mcp/tools.py — ALREADY IMPLEMENTED with user_id ownership check
- [x] T015 [P] [US1] Implement update_task MCP tool in backend/src/mcp/tools.py — ALREADY IMPLEMENTED with user_id ownership check
- [x] T016 [US1] Create OpenAI Agent configuration in backend/src/agents/todo_agent.py — DONE: agent with system prompt, MCP server connection, user_id injection
- [x] T017 [US1] Create chat endpoint POST /api/{user_id}/chat in backend/src/api/chat.py — DONE: JWT verification, context rebuild, agent invocation, message persistence
- [x] T018 [US1] Register chat router in backend/src/api/router.py — DONE: chat_router added to api_router
- [x] T019 [US1] Add error handling to all MCP tools in backend/src/mcp/tools.py — ALREADY IMPLEMENTED: error dicts for NOT_FOUND, VALIDATION_ERROR, ALREADY_COMPLETED, NO_CHANGES

**Checkpoint**: Agent can process chat messages and invoke all 5 MCP tools. Task CRUD operations work end-to-end through agent → MCP tools → database pathway.

---

## Phase 4: User Story 2 — Persistent Chat Interaction (Priority: P2)

**Goal**: Conversations and messages persist in the database so context is rebuilt on each request and survives server restarts

**Independent Test**: Send multiple chat messages in a conversation, restart the server, send another message with the same conversation_id, and verify the agent has full prior context

### Implementation for User Story 2

- [x] T020 [US2] Create conversation service in backend/src/services/conversation.py — DONE: create_conversation(), get_or_create_conversation(), load_conversation_history(), save_message()
- [x] T021 [US2] Implement context rebuilding in backend/src/services/conversation.py — DONE: loads messages chronologically, formats as [{role, content}] for agent
- [x] T022 [US2] Integrate conversation persistence into chat endpoint in backend/src/api/chat.py — DONE: create/load conversation, rebuild context, save user+agent messages
- [x] T023 [US2] Store tool call metadata in ConversationMessage.tool_calls JSON field — DONE: save_message() accepts tool_calls parameter, model has JSON column
- [x] T024 [US2] Add conversation management endpoints in backend/src/api/conversations.py — ALREADY EXISTS: POST /sessions, POST /messages, GET /messages

**Checkpoint**: Conversations persist across requests. Context is rebuilt from DB on each chat message. Server restart does not lose conversation history.

---

## Phase 5: User Story 3 — Secure Task Isolation (Priority: P3)

**Goal**: Users can only access and modify their own tasks and conversations. Cross-user access is rejected at every layer.

**Independent Test**: Create tasks for User A, authenticate as User B, attempt to list/modify/delete User A's tasks through chat — all attempts must fail with appropriate error messages

### Implementation for User Story 3

- [x] T025 [US3] Add user_id validation to chat endpoint in backend/src/api/chat.py — DONE: chat.py:58-64 verifies user_id matches JWT sub, returns 403 on mismatch
- [x] T026 [US3] Enforce user_id scoping in all MCP tools in backend/src/mcp/tools.py — ALREADY ENFORCED: all tools filter by user_id in DB queries
- [x] T027 [US3] Enforce conversation isolation in backend/src/services/conversation.py — DONE: load_conversation_history() verifies conversation belongs to user
- [x] T028 [US3] Add user_id injection into agent context in backend/src/api/chat.py — DONE: user_id passed to run_agent() and injected into system prompt

**Checkpoint**: Cross-user data access is impossible. All MCP tools, conversations, and chat endpoints enforce user isolation via JWT-derived user_id.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T029 [P] Add structured logging for all MCP tool invocations in backend/src/mcp/tools.py — DONE: all 5 tools log name, user_id, params, duration
- [x] T030 [P] Add structured logging for chat endpoint in backend/src/api/chat.py — DONE: logs request, context rebuild, agent invocation, completion
- [x] T031 Add graceful error handling in chat endpoint in backend/src/api/chat.py — DONE: try/except around agent invocation returns friendly message
- [x] T032 [P] Update backend/src/main.py to ensure MCP server and chat endpoint coexist properly — VERIFIED: CORS allows *, MCP at /mcp, API at /api
- [x] T033 Validate full end-to-end flow — DONE: server boots, DB connected, health=200, chat requires auth (401), MCP mounted, all 5 tools registered, logging configured
- [x] T034 Run quickstart.md validation — DONE: TestClient validates server startup, route registration, auth enforcement, and MCP integration

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) — MVP target
- **User Story 2 (Phase 4)**: Depends on User Story 1 (Phase 3) — needs chat endpoint and MCP tools to exist
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) — can run in parallel with US2 if needed
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 completion (needs chat endpoint and MCP tools)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) — Can run in parallel with US2

### Within Each User Story

- Models before services
- Services before endpoints
- MCP tools before agent configuration
- Agent configuration before chat endpoint
- Core implementation before error handling

### Parallel Opportunities

- T005 and T006 (conversation models) can run in parallel
- T013, T014, T015 (complete_task, delete_task, update_task MCP tools) can run in parallel
- T029 and T030 (logging tasks) can run in parallel
- US2 and US3 can potentially overlap if US1 is complete

---

## Parallel Example: User Story 1

```bash
# Launch parallel MCP tool implementations (after add_task and list_tasks are done):
Task: "Implement complete_task MCP tool in backend/src/mcp/tools.py"
Task: "Implement delete_task MCP tool in backend/src/mcp/tools.py"
Task: "Implement update_task MCP tool in backend/src/mcp/tools.py"
```

## Parallel Example: Foundational Phase

```bash
# Launch parallel model reviews:
Task: "Review and update ConversationSession model in backend/src/models/conversation.py"
Task: "Review and update ConversationMessage model in backend/src/models/conversation.py"
Task: "Configure structured logging in backend/src/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T010)
3. Complete Phase 3: User Story 1 (T011-T019)
4. **STOP and VALIDATE**: Test agent can invoke all 5 MCP tools via chat
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test MCP tools via chat → Deploy/Demo (MVP!)
3. Add User Story 2 → Test conversation persistence → Deploy/Demo
4. Add User Story 3 → Test user isolation → Deploy/Demo
5. Polish → Logging, error handling, validation → Final release

### Agent Delegation

Per CLAUDE.md agent delegation rules, tasks should be delegated as follows:
- **T004-T007** (DB models/migrations) → `neon-postgres-manager` agent
- **T008, T011-T015, T019, T026, T029** (MCP tools) → `fastapi-backend` agent
- **T016** (Agent SDK setup) → `fastapi-backend` agent
- **T017-T018, T022, T025, T028, T030-T032** (API endpoints) → `fastapi-backend` agent
- **T009** (JWT verification) → `auth-security` agent
- **T020-T021, T023-T024, T027** (Conversation service) → `fastapi-backend` agent

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Phase-II codebase already has significant infrastructure (models, MCP tools skeleton, JWT auth, API routes)
- Tasks focus on upgrading and integrating existing code rather than building from scratch
- All MCP tools MUST receive user_id from JWT, never from chat messages (constitution Section XIII)
- Agent MUST be the sole invoker of MCP tools (constitution Section XVII)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
