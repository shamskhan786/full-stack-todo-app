# Feature Specification: Todo Full-Stack Web Application – Backend & REST API

**Feature Branch**: `001-todo-backend-api`
**Created**: 2026-02-09
**Status**: Draft
**Input**: User description: "Todo Full-Stack Web Application – Backend & REST API with FastAPI, SQLModel, Neon PostgreSQL, and JWT authentication"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and List Tasks (Priority: P1)

As an authenticated user, I want to create new tasks and view all my
tasks so that I can track my to-do items in a persistent list.

**Why this priority**: This is the foundational CRUD flow. Without
creating and listing tasks, no other feature has value. This delivers
a minimal viable product immediately.

**Independent Test**: Can be fully tested by creating multiple tasks
via the API and listing them back. Delivers core task management value.

**Acceptance Scenarios**:

1. **Given** an authenticated user with no tasks, **When** they
   create a new task with a title and description, **Then** the system
   returns the created task with a unique ID, timestamps, and
   `is_completed: false`.
2. **Given** an authenticated user with 3 existing tasks, **When**
   they request all their tasks, **Then** the system returns exactly
   those 3 tasks in a consistent JSON list — no tasks from other
   users are included.
3. **Given** an unauthenticated request, **When** the user attempts
   to create a task, **Then** the system rejects the request with an
   appropriate error.
4. **Given** an authenticated user, **When** they create a task with
   an empty title, **Then** the system rejects it with a validation
   error listing the invalid field.

---

### User Story 2 - View, Update, and Delete a Single Task (Priority: P2)

As an authenticated user, I want to view, edit, and delete individual
tasks so that I can manage my to-do list with full control over each
item.

**Why this priority**: After creating and listing, users need to
manage individual items. This completes the standard CRUD cycle.

**Independent Test**: Can be tested by creating a task, then
retrieving, updating, and deleting it by ID. Each operation is
independently verifiable.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an existing task, **When**
   they request that task by ID, **Then** the system returns the full
   task details.
2. **Given** an authenticated user, **When** they update a task's
   title and description, **Then** the system saves the changes and
   returns the updated task with a modified timestamp.
3. **Given** an authenticated user, **When** they delete a task by ID,
   **Then** the task is permanently removed and subsequent retrieval
   returns a not-found error.
4. **Given** an authenticated user, **When** they attempt to
   view/update/delete a task belonging to a different user, **Then**
   the system returns a not-found error (does not reveal existence).
5. **Given** an authenticated user, **When** they attempt to update a
   task with invalid data (e.g., empty title), **Then** the system
   returns a validation error.

---

### User Story 3 - Mark Task as Complete (Priority: P3)

As an authenticated user, I want to mark a task as complete so that
I can track my progress and distinguish finished work from pending
items.

**Why this priority**: Completion toggling is a core to-do feature
but depends on tasks already existing (US1) and being retrievable
(US2).

**Independent Test**: Can be tested by creating a task, marking it
complete, and verifying the completion status and timestamp change.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an incomplete task, **When**
   they mark it as complete, **Then** the system sets `is_completed`
   to `true` and records a `completed_at` timestamp.
2. **Given** an authenticated user with an already-completed task,
   **When** they mark it as complete again, **Then** the system
   returns the task unchanged (idempotent operation).
3. **Given** an authenticated user, **When** they attempt to complete
   a task belonging to another user, **Then** the system returns a
   not-found error.
4. **Given** an authenticated user, **When** they attempt to complete
   a non-existent task ID, **Then** the system returns a not-found
   error.

---

### User Story 4 - User Authentication (Priority: P4)

As a new or returning user, I want to sign up and sign in so that my
tasks are private, persistent, and accessible only to me.

**Why this priority**: Authentication is a cross-cutting concern.
While required for all endpoints, the task CRUD logic can be
developed and tested with mock/stub auth. Full auth integration
comes after core API is stable.

**Independent Test**: Can be tested by signing up a new user,
signing in, receiving a JWT token, and using it to access a protected
endpoint.

**Acceptance Scenarios**:

1. **Given** a new user, **When** they sign up with valid email and
   password, **Then** the system creates their account and returns a
   success response.
2. **Given** a registered user, **When** they sign in with correct
   credentials, **Then** the system returns a valid JWT token.
3. **Given** a user with a valid JWT token, **When** they make a
   request to a protected endpoint, **Then** the system accepts the
   request and scopes data to that user.
4. **Given** a user with an expired or invalid JWT token, **When**
   they make a request, **Then** the system rejects it with an
   authentication error.
5. **Given** a new user, **When** they sign up with an already-used
   email, **Then** the system returns a conflict error.

---

### User Story 5 - Responsive Frontend Interface (Priority: P5)

As an end user, I want a responsive web interface to manage my tasks
so that I can create, view, update, complete, and delete tasks from
any device.

**Why this priority**: The frontend depends on the backend API (US1-3)
and authentication (US4) being functional. It is the final layer.

**Independent Test**: Can be tested by opening the application in a
browser, signing in, and performing all task CRUD operations through
the UI on desktop and mobile viewports.

**Acceptance Scenarios**:

1. **Given** the application is loaded, **When** a user visits the
   home page, **Then** they see a sign-in/sign-up interface.
2. **Given** an authenticated user, **When** they view the dashboard,
   **Then** they see their task list with options to create, edit,
   complete, and delete tasks.
3. **Given** a mobile viewport (< 768px), **When** the user interacts
   with the interface, **Then** all features remain fully accessible
   and the layout adapts appropriately.
4. **Given** an authenticated user, **When** they create a task via
   the UI, **Then** the task appears in the list without a full page
   reload.

---

### Edge Cases

- What happens when a user creates a task with an extremely long
  title (> 500 characters)? System MUST enforce a maximum length and
  return a validation error.
- What happens when a user requests a task ID that does not exist?
  System MUST return HTTP 404 with a structured error message.
- What happens when the database connection is temporarily unavailable?
  System MUST return HTTP 503 with a retry-friendly error message.
- What happens when a user submits a request with malformed JSON?
  System MUST return HTTP 422 with details about the parsing failure.
- What happens when two requests attempt to update the same task
  simultaneously? The last write wins; no data corruption occurs.
- What happens when a user's JWT token expires mid-session?
  System MUST return HTTP 401; the frontend prompts re-authentication.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `POST /api/{user_id}/tasks`
  endpoint that creates a new task with at minimum a title, and
  returns the created task with a unique ID and timestamps.
- **FR-002**: System MUST provide a `GET /api/{user_id}/tasks`
  endpoint that returns all tasks belonging to the authenticated user.
- **FR-003**: System MUST provide a `GET /api/{user_id}/tasks/{id}`
  endpoint that returns a single task by ID, scoped to the
  authenticated user.
- **FR-004**: System MUST provide a `PUT /api/{user_id}/tasks/{id}`
  endpoint that replaces all mutable fields of a task and returns the
  updated resource.
- **FR-005**: System MUST provide a
  `DELETE /api/{user_id}/tasks/{id}` endpoint that permanently removes
  a task and returns a confirmation response.
- **FR-006**: System MUST provide a
  `PATCH /api/{user_id}/tasks/{id}/complete` endpoint that sets the
  task's completion status to true and records a completion timestamp.
- **FR-007**: System MUST validate all incoming request bodies and
  reject invalid input with HTTP 422 and a structured error response
  listing each invalid field.
- **FR-008**: System MUST verify JWT tokens on every protected
  endpoint before processing the request. Invalid or missing tokens
  MUST result in HTTP 401.
- **FR-009**: System MUST scope all data queries to the authenticated
  user's ID. No endpoint may return or modify data belonging to a
  different user.
- **FR-010**: System MUST return consistent JSON response structures
  across all endpoints (success and error responses follow a uniform
  shape).
- **FR-011**: System MUST support user signup and signin via Better
  Auth, issuing JWT tokens upon successful authentication.
- **FR-012**: System MUST provide a responsive web frontend that
  allows users to perform all task operations (create, list, view,
  update, delete, complete) from desktop and mobile devices.
- **FR-013**: System MUST persist all task data in a PostgreSQL
  database with proper relational integrity.
- **FR-014**: System MUST enforce a maximum task title length of
  500 characters.

### Key Entities

- **User**: Represents an authenticated person. Key attributes:
  unique ID, email, hashed password, creation timestamp. A user owns
  zero or more tasks.
- **Task**: Represents a to-do item. Key attributes: unique ID, owner
  (user reference), title (required, max 500 chars), description
  (optional), completion status (boolean, default false), completion
  timestamp (nullable), creation timestamp, last-modified timestamp.

### Assumptions

- Better Auth is configured on the frontend (Next.js) side and issues
  JWT tokens that the FastAPI backend verifies.
- The `{user_id}` in URL paths matches the authenticated user's ID
  from the JWT token; mismatches are rejected.
- Task deletion is a hard delete (permanent removal), not a soft
  delete.
- The "complete" endpoint is idempotent — completing an already
  completed task is a no-op success.
- No pagination is required for the initial release; the task list
  endpoint returns all tasks for the user.
- No task sorting or filtering query parameters are required for the
  initial release.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 6 API endpoints are functional and return correct
  responses for valid and invalid inputs as defined in the acceptance
  scenarios.
- **SC-002**: No endpoint returns data belonging to a user other than
  the authenticated user — verified by testing with multiple user
  accounts.
- **SC-003**: Users can complete the full task lifecycle (create, view,
  update, complete, delete) in under 2 minutes using the web
  interface.
- **SC-004**: The web interface is fully usable on devices with screen
  widths from 375px (mobile) to 1920px (desktop) — all features
  accessible, no horizontal scrolling, no overlapping elements.
- **SC-005**: 100% of invalid requests (missing fields, wrong types,
  empty titles) are rejected with structured validation errors before
  reaching the database.
- **SC-006**: Requests with missing, expired, or tampered JWT tokens
  are rejected with an authentication error — no protected data is
  exposed.
- **SC-007**: All backend endpoints pass unit tests covering success
  paths, validation errors, authentication failures, and not-found
  scenarios.
