# Tasks: Todo Backend Self-Healing & Standalone Operation

**Input**: Design documents from `/specs/001-backend-self-healing/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Not explicitly requested. Existing backend tests (22/22 passing) already cover CRUD and auth. New tests added for health check only.

**Organization**: Tasks are grouped by user story. The backend is already functional — tasks add self-healing capabilities on top of the existing implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Verify existing backend is healthy before making changes

- [x] T001 Run existing backend test suite to confirm baseline: `cd backend && python -m pytest tests/ -v` — all 22 tests must pass
- [x] T002 [P] Verify all dependencies are installed: `pyjwt[crypto]`, `sqlmodel`, `fastapi`, `pydantic-settings` in `backend/requirements.txt`

**Checkpoint**: Existing backend confirmed healthy; safe to add self-healing features

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Import Task model into database module so `create_all` can discover it

- [x] T003 Ensure Task model is importable before `create_all` by adding import in `backend/src/database.py`

**Checkpoint**: Model discovery ready for auto-table creation

---

## Phase 3: User Story 1 — Backend Self-Healing Startup (Priority: P1)

**Goal**: Auto-create missing database tables on startup, validate DB connectivity, log startup status

**Independent Test**: Drop the `task` table, restart the backend, verify table is recreated and service is operational

### Implementation for User Story 1

- [x] T004 [US1] Add `lifespan` async context manager to `backend/src/main.py` that calls `SQLModel.metadata.create_all(engine)` on startup
- [x] T005 [US1] Add startup DB connectivity check inside the `lifespan` handler: execute `SELECT 1` and log result in `backend/src/main.py`
- [x] T006 [US1] Configure Python `logging` at module level in `backend/src/main.py` for startup event logging
- [x] T007 [US1] Wire the `lifespan` context manager into the `FastAPI(lifespan=...)` app constructor in `backend/src/main.py`
- [x] T008 [US1] Add generic catch-all `Exception` handler in `backend/src/main.py` returning structured `ErrorResponse` with code `INTERNAL_ERROR`
- [x] T009 [US1] Run backend test suite to verify no regressions: `cd backend && python -m pytest tests/ -v`

**Checkpoint**: US1 complete — backend auto-creates tables and validates DB on startup

---

## Phase 4: User Story 2 — API Endpoint Self-Healing (Priority: P2)

**Goal**: Add health check endpoint and improve error resilience

**Independent Test**: Hit `GET /api/health` and verify structured JSON response with DB status

### Implementation for User Story 2

- [x] T010 [P] [US2] Create health check endpoint in `backend/src/api/health.py` with `GET /api/health` that pings DB via `SELECT 1`
- [x] T011 [US2] Register health router in `backend/src/api/router.py` alongside existing tasks router
- [x] T012 [P] [US2] Create health check test file `backend/tests/test_health.py` with tests for healthy and connectivity scenarios
- [x] T013 [US2] Run full test suite including new health tests: `cd backend && python -m pytest tests/ -v`

**Checkpoint**: US2 complete — health endpoint operational, error handling improved

---

## Phase 5: User Story 3 — Better Auth Integration Logging (Priority: P3)

**Goal**: Add authentication event logging to `verify_jwt` for observability

**Independent Test**: Make authenticated and unauthenticated API requests, verify auth events are logged

### Implementation for User Story 3

- [x] T014 [US3] Add Python `logging` to `backend/src/dependencies.py` with auth success/failure log messages in `verify_jwt`
- [x] T015 [US3] Run full test suite to verify logging doesn't break auth: `cd backend && python -m pytest tests/ -v`

**Checkpoint**: US3 complete — auth events logged for observability

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across all user stories

- [x] T016 Run full backend test suite: `cd backend && python -m pytest tests/ -v` — all tests must pass (22 existing + new health tests)
- [x] T017 Verify auto-table creation works by confirming `create_all` is called in lifespan handler in `backend/src/main.py`
- [x] T018 Verify health check returns correct JSON structure at `GET /api/health`
- [x] T019 Validate quickstart checklist from `specs/001-backend-self-healing/quickstart.md` (manual)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 passing
- **Phase 3 (US1 — Startup Self-Healing)**: Depends on Phase 2
- **Phase 4 (US2 — Health Check)**: Depends on Phase 2 (independent of US1)
- **Phase 5 (US3 — Auth Logging)**: Depends on Phase 2 (independent of US1/US2)
- **Phase 6 (Polish)**: Depends on all user story phases complete

### User Story Dependencies

- **US1 (Startup Self-Healing)**: Independent — modifies `main.py` and `database.py`
- **US2 (Health Check)**: Independent — creates new `health.py` and modifies `router.py`
- **US3 (Auth Logging)**: Independent — modifies `dependencies.py` only

### Within Each User Story

- Implementation tasks are sequential within each story (same files)
- Test runs at the end of each story validate no regressions

### Parallel Opportunities

- Phase 1: T001 and T002 can run in parallel
- Phase 4: T010 and T012 can run in parallel (different files)
- US1, US2, US3 can all proceed in parallel after Phase 2 (different files)

---

## Parallel Example: After Phase 2

```bash
# All three user stories touch different files — run in parallel:
Task: "Add lifespan handler in backend/src/main.py" (US1)
Task: "Create health endpoint in backend/src/api/health.py" (US2)
Task: "Add auth logging in backend/src/dependencies.py" (US3)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Verify baseline tests pass
2. Complete Phase 2: Import model for discovery
3. Complete Phase 3 (US1): Add lifespan + create_all + error handler
4. **STOP and VALIDATE**: Drop table, restart, verify auto-creation

### Incremental Delivery

1. Setup + Foundational → Baseline confirmed
2. Add US1 → Self-healing startup (MVP)
3. Add US2 → Health check endpoint
4. Add US3 → Auth event logging
5. Polish → Final validation

---

## Notes

- **Files modified**: `main.py` (US1), `database.py` (Phase 2), `router.py` (US2), `dependencies.py` (US3)
- **Files created**: `api/health.py` (US2), `tests/test_health.py` (US2)
- **Files unchanged**: `config.py`, `models/task.py`, `schemas/`, `api/tasks.py`, `tests/test_tasks.py`
- Total code changes are minimal — 4 files modified, 2 files created
- [P] tasks = different files, no dependencies
- Stop at any checkpoint to validate independently
