# Tasks: Todo Full-Stack Web Application – Backend & REST API

**Input**: Design documents from `/specs/001-todo-backend-api/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/openapi.yaml, quickstart.md

**Tests**: Tests are included per SC-007 (spec requires backend unit tests).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic directory structure for both backend and frontend.

- [x] T001 Create backend project structure with directories: `backend/src/`, `backend/src/models/`, `backend/src/schemas/`, `backend/src/api/`, `backend/tests/`, `backend/alembic/`, and all `__init__.py` files per plan.md
- [x] T002 Create `backend/pyproject.toml` with Python 3.12 requirement and project metadata per research.md R6
- [x] T003 [P] Create `backend/requirements.txt` with dependencies: fastapi>=0.115.0, uvicorn[standard]>=0.34.0, sqlmodel>=0.0.22, psycopg2-binary>=2.9.9, pyjwt[crypto]>=2.9.0, pydantic-settings>=2.7.0, alembic>=1.14.0, pytest>=8.0.0, httpx>=0.27.0
- [x] T004 [P] Create `backend/.env.example` with DATABASE_URL, JWKS_URL, FRONTEND_URL, ENVIRONMENT placeholders per quickstart.md
- [x] T005 Create frontend project: initialize Next.js 16+ App Router in `frontend/` with TypeScript, Tailwind CSS, and create directory structure per plan.md (`app/`, `lib/`, `components/`)
- [x] T006 [P] Create `frontend/.env.example` with BETTER_AUTH_SECRET, BETTER_AUTH_URL, DATABASE_URL, NEXT_PUBLIC_API_URL placeholders per quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T007 Implement `backend/src/config.py` — Pydantic Settings class loading DATABASE_URL, JWKS_URL, FRONTEND_URL, ENVIRONMENT from `.env` using pydantic-settings
- [x] T008 Implement `backend/src/database.py` — SQLModel engine creation with Neon pooled connection string and NullPool (per research.md R2); `get_session()` generator yielding Session with commit/rollback/close
- [x] T009 Implement `backend/src/schemas/responses.py` — SuccessResponse[T] generic model, ErrorResponse with error/details/code fields, ErrorDetail model, DeleteResponse model per contracts/openapi.yaml
- [x] T010 [P] Implement `backend/src/models/task.py` — Task SQLModel (table=True) with UUID pk, user_id FK (UUID, indexed), title (VARCHAR 500, min_length=1), description (nullable TEXT), is_completed (BOOLEAN default false), completed_at (nullable TIMESTAMPTZ), created_at, updated_at per data-model.md
- [x] T011 [P] Implement `backend/src/schemas/task.py` — TaskCreate (title required 1-500 chars, description optional), TaskUpdate (title required 1-500 chars, description optional), TaskRead (all fields) per contracts/openapi.yaml
- [x] T012 Initialize Alembic in `backend/` — create `backend/alembic.ini` and `backend/alembic/env.py` configured to use SQLModel metadata and DATABASE_URL from config; generate initial migration for Task table
- [x] T013 Implement `backend/src/dependencies.py` — `get_session()` dependency (import from database.py) and `verify_jwt()` dependency using PyJWT + PyJWKClient to fetch keys from JWKS_URL, validate exp/iss/aud/sub claims, return payload dict; raise HTTP 401 on failure per research.md R4
- [x] T014 Implement `backend/src/main.py` — FastAPI app instance with CORS middleware (allow_origins from FRONTEND_URL, allow_credentials=True, allow_methods/headers), custom exception handlers for RequestValidationError (422) and HTTPException returning ErrorResponse envelope, include API router
- [x] T015 [P] Implement `backend/src/api/router.py` — main APIRouter that includes task routes with prefix `/api`
- [x] T016 Implement `backend/tests/conftest.py` — pytest fixtures: test database session (SQLite in-memory or test Neon DB), mock JWT dependency override returning a test user_id, FastAPI TestClient with dependency overrides

**Checkpoint**: Foundation ready — user story implementation can now begin.

---

## Phase 3: User Story 1 – Create and List Tasks (Priority: P1) MVP

**Goal**: Authenticated users can create new tasks and list all their tasks.

**Independent Test**: Create multiple tasks via POST, list them via GET, verify correct count and no cross-user leakage.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T017 [P] [US1] Write test for POST /api/{user_id}/tasks — success case: valid title+description returns 201 with TaskRead in SuccessResponse envelope, is_completed=false, timestamps set — in `backend/tests/test_tasks.py`
- [x] T018 [P] [US1] Write test for POST /api/{user_id}/tasks — validation: empty title returns 422 ErrorResponse with field details; title >500 chars returns 422 — in `backend/tests/test_tasks.py`
- [x] T019 [P] [US1] Write test for GET /api/{user_id}/tasks — success case: returns 200 with list of only that user's tasks (create tasks for 2 users, verify isolation) — in `backend/tests/test_tasks.py`
- [x] T020 [P] [US1] Write test for POST and GET — auth failure: request without JWT returns 401 ErrorResponse — in `backend/tests/test_tasks.py`

### Implementation for User Story 1

- [x] T021 [US1] Implement POST /api/{user_id}/tasks endpoint in `backend/src/api/tasks.py` — validate user_id matches JWT sub claim (403 if mismatch), create Task with SQLModel session, return 201 SuccessResponse[TaskRead] with "Task created successfully" message
- [x] T022 [US1] Implement GET /api/{user_id}/tasks endpoint in `backend/src/api/tasks.py` — validate user_id matches JWT sub claim, query all tasks WHERE user_id=authenticated_user, return 200 SuccessListResponse with task list

**Checkpoint**: User Story 1 fully functional — create and list tasks work independently.

---

## Phase 4: User Story 2 – View, Update, and Delete a Single Task (Priority: P2)

**Goal**: Authenticated users can retrieve, modify, and remove individual tasks by ID.

**Independent Test**: Create a task, GET by ID, PUT with new title, DELETE, verify 404 on subsequent GET.

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T023 [P] [US2] Write test for GET /api/{user_id}/tasks/{id} — success: returns 200 with single task; not-found: returns 404; cross-user: returns 404 (not 403) — in `backend/tests/test_tasks.py`
- [x] T024 [P] [US2] Write test for PUT /api/{user_id}/tasks/{id} — success: returns 200 with updated task and new updated_at; validation: empty title returns 422; not-found: returns 404 — in `backend/tests/test_tasks.py`
- [x] T025 [P] [US2] Write test for DELETE /api/{user_id}/tasks/{id} — success: returns 200 DeleteResponse; not-found: returns 404; verify subsequent GET returns 404 — in `backend/tests/test_tasks.py`

### Implementation for User Story 2

- [x] T026 [US2] Implement GET /api/{user_id}/tasks/{task_id} endpoint in `backend/src/api/tasks.py` — query task WHERE id=task_id AND user_id=authenticated_user, return 200 SuccessResponse[TaskRead] or raise 404 NOT_FOUND
- [x] T027 [US2] Implement PUT /api/{user_id}/tasks/{id} endpoint in `backend/src/api/tasks.py` — find task scoped to user, replace title and description, set updated_at=now(), return 200 SuccessResponse[TaskRead] or 404
- [x] T028 [US2] Implement DELETE /api/{user_id}/tasks/{id} endpoint in `backend/src/api/tasks.py` — find task scoped to user, delete from DB, return 200 DeleteResponse with "Task deleted successfully" or 404

**Checkpoint**: User Stories 1 AND 2 both work independently — full CRUD minus completion.

---

## Phase 5: User Story 3 – Mark Task as Complete (Priority: P3)

**Goal**: Authenticated users can mark a task as complete with an idempotent PATCH endpoint.

**Independent Test**: Create a task, PATCH complete, verify is_completed=true and completed_at set. PATCH again, verify idempotent (no change).

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T029 [P] [US3] Write test for PATCH /api/{user_id}/tasks/{id}/complete — success: incomplete task becomes completed with completed_at timestamp; idempotent: already-completed task returns 200 unchanged; not-found: returns 404; cross-user: returns 404 — in `backend/tests/test_tasks.py`

### Implementation for User Story 3

- [x] T030 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in `backend/src/api/tasks.py` — find task scoped to user, if not completed set is_completed=true and completed_at=utcnow() and updated_at=utcnow(), if already completed return as-is (idempotent), return 200 SuccessResponse[TaskRead] or 404

**Checkpoint**: All 6 backend API endpoints functional — complete task CRUD + completion.

---

## Phase 6: User Story 4 – User Authentication (Priority: P4)

**Goal**: Users can sign up and sign in via Better Auth on the frontend; JWT tokens are verified by the backend.

**Independent Test**: Sign up a new user in Next.js, sign in, receive JWT, call a protected backend endpoint, verify data is scoped.

- [x] T031 [US4] Configure Better Auth server in `frontend/lib/auth.ts` — betterAuth instance with Neon PostgreSQL (pg Pool), JWT plugin with EdDSA key pair, export auth object
- [x] T032 [US4] Configure Better Auth client in `frontend/lib/auth-client.ts` — createAuthClient with jwtClient plugin, export authClient
- [x] T033 [US4] Create Better Auth API route handler in `frontend/app/api/auth/[...all]/route.ts` — import auth from lib/auth, export GET and POST handlers via toNextJsHandler
- [x] T034 [US4] Run Better Auth database migrations — execute `npx @better-auth/cli@latest generate` and `npx @better-auth/cli@latest migrate` to create user, session, account, verification_token, jwks tables in Neon
- [x] T035 [US4] Verify JWT integration end-to-end — sign up a test user via Better Auth, obtain JWT token, make authenticated request to backend GET /api/{user_id}/tasks, verify 200 response

**Checkpoint**: Authentication pipeline complete — users can sign up, sign in, and access protected backend endpoints.

---

## Phase 7: User Story 5 – Responsive Frontend Interface (Priority: P5)

**Goal**: Responsive web UI for all task operations (create, list, view, update, complete, delete) on desktop and mobile.

**Independent Test**: Open in browser, sign in, create a task, edit it, mark complete, delete it. Test on 375px and 1920px viewports.

- [x] T036 [US5] Implement API client in `frontend/lib/api.ts` — typed fetch wrapper that adds Authorization Bearer header from authClient.token(), base URL from NEXT_PUBLIC_API_URL, handles JSON responses and errors
- [x] T037 [US5] Implement auth form component in `frontend/components/auth-form.tsx` — reusable sign-in/sign-up form with email and password fields, client-side validation, calls authClient.signIn/signUp, shows error messages
- [x] T038 [US5] Implement sign-in page in `frontend/app/(auth)/signin/page.tsx` — renders auth-form in sign-in mode, redirects to /dashboard on success
- [x] T039 [P] [US5] Implement sign-up page in `frontend/app/(auth)/signup/page.tsx` — renders auth-form in sign-up mode, redirects to /signin on success
- [x] T040 [US5] Implement root layout in `frontend/app/layout.tsx` — HTML structure, Tailwind CSS setup, font configuration, metadata
- [x] T041 [US5] Implement home page in `frontend/app/page.tsx` — redirect authenticated users to /dashboard, unauthenticated to /signin
- [x] T042 [US5] Implement dashboard layout in `frontend/app/dashboard/layout.tsx` — auth-protected layout that checks session via authClient, redirects to /signin if unauthenticated, renders header with user info and sign-out button
- [x] T043 [US5] Implement task item component in `frontend/components/task-item.tsx` — displays single task with title, description, completion status; action buttons for edit, complete, delete; responsive layout
- [x] T044 [US5] Implement task form component in `frontend/components/task-form.tsx` — create/edit task form with title (required, max 500) and description (optional) fields; submit calls API client POST or PUT; inline validation
- [x] T045 [US5] Implement task list component in `frontend/components/task-list.tsx` — fetches tasks from API via GET, renders task-item for each, shows empty state, includes create task button that opens task-form
- [x] T046 [US5] Implement dashboard page in `frontend/app/dashboard/page.tsx` — renders task-list component, handles loading and error states, optimistic UI updates for create/update/delete/complete
- [x] T047 [US5] Apply responsive design — ensure all components work at 375px (mobile) to 1920px (desktop): stack layout on mobile, side-by-side on desktop, touch-friendly tap targets, no horizontal scrolling

**Checkpoint**: Full application functional — users can sign up, sign in, and manage tasks through a responsive web interface.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [x] T048 [P] Create `backend/.env.example` and `frontend/.env.example` with all required variables documented per quickstart.md
- [x] T049 [P] Run all backend tests with `pytest backend/tests/ -v` and fix any failures
- [x] T050 Verify quickstart.md flow end-to-end — follow every step in quickstart.md on a clean checkout, fix any discrepancies
- [x] T051 [P] Validate OpenAPI spec — start backend, visit /docs, verify all 6 endpoints appear with correct request/response schemas matching contracts/openapi.yaml

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — first user story, MVP
- **US2 (Phase 4)**: Depends on Phase 2 — can run in parallel with US1 (different endpoint files) but logically sequential
- **US3 (Phase 5)**: Depends on Phase 2 — can run after US1 (needs task creation)
- **US4 (Phase 6)**: Depends on Phase 1 (frontend setup) — can run in parallel with US1-3 (different codebase: frontend)
- **US5 (Phase 7)**: Depends on US1-4 completion (needs working API + auth)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — no dependencies on other stories
- **US2 (P2)**: Can start after Phase 2 — logically extends US1 but tests independently
- **US3 (P3)**: Can start after Phase 2 — logically extends US1/US2 but tests independently
- **US4 (P4)**: Can start after Phase 1 — independent frontend work, runs in parallel with US1-3
- **US5 (P5)**: Depends on US1-4 — needs working API and auth

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implementation tasks are sequential within each story
- Story complete before moving to next priority

### Parallel Opportunities

- T003, T004 can run in parallel (different files, setup phase)
- T005, T006 can run in parallel (frontend setup)
- T010, T011 can run in parallel (model vs schema, different files)
- T017, T018, T019, T020 can all run in parallel (different test functions)
- T023, T024, T025 can all run in parallel (different test functions)
- US4 (frontend auth) can run in parallel with US1-US3 (backend work)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test POST create task success — backend/tests/test_tasks.py"
Task: "Test POST create task validation — backend/tests/test_tasks.py"
Task: "Test GET list tasks isolation — backend/tests/test_tasks.py"
Task: "Test auth failure 401 — backend/tests/test_tasks.py"

# Then implement sequentially:
Task: "POST /api/{user_id}/tasks — backend/src/api/tasks.py"
Task: "GET /api/{user_id}/tasks — backend/src/api/tasks.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (create + list tasks)
4. **STOP and VALIDATE**: Test US1 independently via pytest and Swagger UI
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Test independently → MVP!
3. Add US2 → Test independently → Full CRUD
4. Add US3 → Test independently → Complete backend API
5. Add US4 → Test independently → Authentication pipeline
6. Add US5 → Test independently → Full application
7. Polish → Final validation

### Agent Delegation Plan

| Phase | Agent | Scope |
|-------|-------|-------|
| Phase 1 (Setup) | Backend + Frontend | Project scaffolding |
| Phase 2 (Foundation) | DB Agent → Backend Agent | Schema, engine, models, dependencies |
| Phase 3 (US1) | Backend Agent | POST + GET endpoints |
| Phase 4 (US2) | Backend Agent | GET/PUT/DELETE by ID |
| Phase 5 (US3) | Backend Agent | PATCH complete |
| Phase 6 (US4) | Auth Agent | Better Auth + JWT |
| Phase 7 (US5) | Frontend Agent | Next.js UI |
| Phase 8 (Polish) | All Agents | Validation |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
