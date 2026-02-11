<!--
=== Sync Impact Report ===
Version change: 1.1.0 → 1.2.0
Modified principles: None (all existing principles unchanged)
Added sections:
  - Core Principles — Authentication & Security (new heading)
  - Principle XII: Security-First (Data Protection at Every Layer)
  - Principle XIII: User Isolation (Cross-User Data Leakage Prevention)
  - Principle XIV: Auth Consistency (Frontend–Backend Alignment)
  - Principle XV: Statelessness (JWT-Based, No Shared Sessions)
  - Principle XVI: Auth Clarity (Understandable Auth Flow)
  - Section: Authentication Standards
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md — Constitution Check section
    dynamically derives gates from constitution; no edits needed
    ✅ compatible
  - .specify/templates/spec-template.md — FR numbering and entity
    definitions remain aligned ✅ compatible
  - .specify/templates/tasks-template.md — Phase structure accommodates
    auth tasks via existing Auth Agent delegation ✅ compatible
  - .specify/templates/commands/ — No command files exist ✅ N/A
Follow-up TODOs: None
===========================
-->

# Todo Full-Stack Web Application Constitution

## Core Principles — Backend

### I. Accuracy (API Correctness)

All API endpoints MUST behave exactly as specified in the feature
spec. Responses MUST match documented schemas. Deviations from
specified behavior are treated as defects regardless of intent.

- Every endpoint MUST return the documented response shape.
- Status codes MUST follow HTTP semantics (2xx success, 4xx client
  error, 5xx server error).
- Database state changes MUST be atomic per request; partial writes
  are prohibited.

### II. Security (Data Protection & Authorization)

All user data MUST be correctly filtered and protected. No endpoint
may expose data belonging to a different user. Authorization is
enforced at the API layer via JWT tokens issued by Better Auth.

- Every data-returning endpoint MUST scope queries to the
  authenticated user's `user_id`.
- Secrets and tokens MUST never be hardcoded; use `.env` files and
  environment variables exclusively.
- Passwords MUST be hashed before storage; plaintext passwords MUST
  never be persisted or logged.
- JWT verification MUST occur before any protected route handler
  executes.

### III. Reproducibility (Consistent Behavior)

API responses and database interactions MUST be consistent and
deterministic. The same valid request with the same state MUST
produce the same result.

- All database operations MUST use SQLModel with proper ORM
  practices; raw SQL is prohibited unless explicitly justified.
- Migrations MUST be versioned and reversible.
- Test data and seed scripts MUST produce identical state across
  environments.

### IV. Clarity (Code Structure & Documentation)

Code structure and documentation MUST be clear enough for any
developer to understand without oral explanation. This applies to
both backend API documentation and frontend component organization.

- Every API endpoint MUST be documented via FastAPI's automatic
  OpenAPI/Swagger generation with typed request/response models.
- Frontend components MUST be modular and reusable; each component
  MUST have a single, well-defined responsibility.
- File and directory naming MUST follow the project structure
  conventions defined in the implementation plan.
- Functions MUST have clear names; comments are reserved for
  non-obvious logic only.

### V. RESTful API Design

All endpoints MUST follow RESTful design principles. Resource naming,
HTTP methods, and status codes MUST be semantically correct.

- Resource URLs MUST use nouns (e.g., `/tasks`), not verbs.
- HTTP methods MUST map to operations: GET (read), POST (create),
  PUT (full update), PATCH (partial update), DELETE (remove).
- The defined API contract is:
  - `GET    /api/{user_id}/tasks` — List all tasks for user
  - `POST   /api/{user_id}/tasks` — Create a new task
  - `GET    /api/{user_id}/tasks/{id}` — Get a single task
  - `PUT    /api/{user_id}/tasks/{id}` — Update a task (full)
  - `DELETE /api/{user_id}/tasks/{id}` — Delete a task
  - `PATCH  /api/{user_id}/tasks/{id}/complete` — Mark task complete
- All responses MUST use a clear, consistent JSON structure.

### VI. Input Validation & Response Standards

All API requests MUST be validated before processing. Invalid input
MUST be rejected with descriptive error messages.

- Request bodies MUST be validated using Pydantic/SQLModel schemas.
- Validation errors MUST return HTTP 422 with a structured error
  response listing each invalid field.
- Successful responses MUST include the resource representation.
- Collection endpoints MUST support consistent pagination structure.

## Core Principles — Frontend

### VII. Usability (Simple & Intuitive Interface)

The user interface MUST be simple, intuitive, and easy to use.
Users MUST be able to accomplish primary tasks (create, view, edit,
complete, delete) without needing instructions or guidance.

- Navigation MUST be self-evident; all primary actions MUST be
  reachable within two clicks from the dashboard.
- Forms MUST provide inline validation feedback before submission.
- Loading, error, and empty states MUST be explicitly handled in
  every view that fetches data.
- Destructive actions (delete) MUST require confirmation.

### VIII. Consistency (Uniform UI Behavior)

UI behavior MUST be consistent across all pages and interaction
states. Users MUST be able to predict how elements behave based on
prior interactions within the application.

- Visual patterns (buttons, forms, cards, feedback messages) MUST
  use the same styling and placement conventions throughout.
- State transitions (loading → success, loading → error) MUST
  follow the same pattern on every page.
- Error messages MUST use a consistent format and tone across all
  forms and API failure states.

### IX. Responsiveness (Mobile-First Adaptive Layout)

The application MUST be fully responsive across mobile (375px),
tablet (768px), and desktop (1920px) viewports using a mobile-first
design approach.

- Layouts MUST stack vertically on mobile and use side-by-side
  arrangements on tablet and desktop.
- Touch targets MUST be at least 44x44px on mobile viewports.
- No horizontal scrolling MUST occur at any supported viewport width.
- Typography and spacing MUST scale appropriately across breakpoints.

### X. Accuracy (Frontend–Backend Alignment)

Frontend behavior MUST accurately reflect backend API responses.
The UI MUST never display stale, fabricated, or inconsistent data.

- All task data displayed in the UI MUST originate from API responses;
  client-side data MUST NOT diverge from server state after refresh.
- Optimistic UI updates are permitted but MUST reconcile with the
  actual API response and revert on failure.
- API communication MUST go through a centralized API client
  (`frontend/lib/api.ts`); direct `fetch` calls scattered across
  components are prohibited.

### XI. Accessibility (Inclusive Design Baseline)

Basic accessibility best practices MUST be followed to ensure the
application is usable by people with diverse abilities.

- All interactive elements MUST be keyboard-navigable.
- Form inputs MUST have associated labels (visible or `aria-label`).
- Color MUST NOT be the sole means of conveying information (e.g.,
  completion status MUST also use text or icons).
- Page structure MUST use semantic HTML elements (`main`, `nav`,
  `header`, `section`, `button`).

## Core Principles — Authentication & Security

### XII. Security-First (Data Protection at Every Layer)

User data MUST be protected at every layer of the application stack.
Security is not an afterthought; it is a prerequisite for every
feature, endpoint, and data flow.

- All API endpoints that access user data MUST require a valid JWT
  token in the `Authorization` header.
- Unauthenticated requests to protected endpoints MUST be rejected
  with HTTP 401 before any business logic executes.
- Sensitive data (passwords, tokens, secrets) MUST never appear in
  logs, error messages, API responses, or client-side storage
  beyond secure HTTP-only mechanisms.
- The `BETTER_AUTH_SECRET` environment variable MUST be the sole
  source of the signing secret; it MUST never be committed to
  version control.

### XIII. User Isolation (Cross-User Data Leakage Prevention)

One user MUST never access, modify, or observe another user's data.
User isolation is enforced at both the API and database query layers.

- Every database query that returns or modifies user-owned resources
  MUST include a `WHERE user_id = <authenticated_user_id>` clause
  (or ORM equivalent).
- The `user_id` used for authorization MUST be extracted from the
  verified JWT payload, never from URL path parameters, query
  strings, or request bodies.
- Path parameters containing `user_id` (e.g., `/api/{user_id}/tasks`)
  MUST be validated against the JWT-derived identity; mismatches
  MUST return HTTP 403.
- No endpoint MUST exist that returns data across multiple users
  unless explicitly designed as an admin endpoint with separate
  authorization.

### XIV. Auth Consistency (Frontend–Backend Alignment)

Authentication behavior MUST be consistent and predictable across
the frontend and backend. A user who is authenticated on the
frontend MUST be recognized as authenticated on the backend, and
vice versa.

- The frontend MUST use Better Auth to manage user sessions, issue
  JWT tokens, and handle sign-up/sign-in flows.
- The backend MUST verify JWT tokens using the same
  `BETTER_AUTH_SECRET` that Better Auth uses for signing.
- Token format and claims MUST be agreed upon: the JWT `sub` claim
  MUST contain the user ID used for all backend authorization.
- Authentication failures on the backend (expired token, invalid
  signature) MUST result in the frontend redirecting the user to
  the sign-in page, not silently failing.

### XV. Statelessness (JWT-Based, No Shared Sessions)

Backend authentication MUST be stateless. The backend MUST NOT
maintain session state, session stores, or server-side session
cookies. All authentication context MUST be derived from the JWT
token accompanying each request.

- Every API request MUST be self-contained: the JWT token in the
  `Authorization: Bearer <token>` header MUST provide all identity
  information needed to authorize the request.
- The backend MUST NOT use database-backed sessions, Redis session
  stores, or any server-side session mechanism for authentication.
- Token expiration and refresh MUST be handled by the frontend
  (Better Auth client); the backend only validates token validity
  at request time.
- If a JWT is expired or invalid, the backend MUST reject the
  request with HTTP 401; it MUST NOT attempt to refresh or reissue
  tokens.

### XVI. Auth Clarity (Understandable Auth Flow)

The authentication flow MUST be easy to understand, trace, and
debug. Any developer reading the codebase MUST be able to follow
the complete auth lifecycle without external documentation.

- The auth flow MUST follow a single, well-documented path:
  Better Auth (frontend) → JWT token → `Authorization` header →
  FastAPI dependency (`verify_jwt`) → user identity extraction.
- JWT verification MUST be implemented as a single FastAPI
  dependency function; auth logic MUST NOT be duplicated across
  route handlers.
- The frontend auth client MUST be configured in a single file
  (`frontend/lib/auth-client.ts`); auth state MUST NOT be managed
  in multiple locations.
- Error messages for auth failures MUST be specific enough to
  diagnose the issue (e.g., "Token expired" vs. "Invalid
  signature") without leaking security-sensitive details.

## Authentication Standards

- **Token Transport**: JWT tokens MUST be sent in the HTTP
  `Authorization` header using the `Bearer` scheme. No other
  transport mechanism (cookies, query parameters) is permitted
  for API authentication.
- **Token Signing**: Better Auth MUST be configured with the JWT
  plugin using EdDSA (Ed25519) signing. The backend MUST verify
  tokens using the corresponding JWKS endpoint or shared secret.
- **Identity Source**: The authenticated user's identity MUST be
  derived exclusively from the verified JWT `sub` claim. Client-
  supplied user IDs in URLs or request bodies MUST be validated
  against the JWT-derived identity.
- **Ownership Enforcement**: Every backend operation that reads,
  creates, updates, or deletes a task MUST verify that the
  requesting user owns the resource. Ownership checks MUST occur
  in the service/repository layer, not solely in route handlers.
- **Frontend Protection**: Protected frontend routes MUST check
  session state via `useSession()` and redirect unauthenticated
  users to `/signin`. The redirect MUST occur before any
  protected content renders.

## Frontend Standards

- **Architecture**: Next.js 16+ App Router; pages in `app/`, shared
  components in `components/`, utilities in `lib/`.
- **State Management**: Component state MUST correctly reflect task
  data across loading, error, and success states. Global auth state
  MUST be handled reliably on the client side via Better Auth client.
- **API Integration**: All API calls MUST use the centralized API
  client in `frontend/lib/api.ts` which attaches JWT Bearer tokens
  from `authClient.token()`.
- **Authentication**: Better Auth handles session and JWT on the
  frontend. Protected routes MUST check session state and redirect
  unauthenticated users to `/signin`.
- **Styling**: Tailwind CSS with mobile-first responsive utilities.
  No external CSS frameworks unless justified in an ADR.

## Technology Stack & Constraints

| Layer          | Technology                   |
|----------------|------------------------------|
| Frontend       | Next.js 16+ (App Router)     |
| Backend        | Python FastAPI               |
| ORM            | SQLModel                     |
| Database       | Neon Serverless PostgreSQL   |
| Spec-Driven    | Claude Code + Spec-Kit Plus  |
| Authentication | Better Auth (JWT tokens)     |

**Constraints:**
- Backend MUST be implemented in Python with FastAPI.
- Database MUST be Neon Serverless PostgreSQL; no other database
  engine is permitted.
- ORM MUST be SQLModel; direct SQL is prohibited unless justified.
- Frontend MUST use Next.js 16+ with the App Router.
- Frontend MUST NOT access the database directly; all data flows
  through the REST API.
- Authentication MUST use Better Auth configured to issue JWT tokens.
- JWT tokens MUST be verified on every protected FastAPI endpoint.
- The `BETTER_AUTH_SECRET` environment variable MUST be shared
  between frontend and backend services as the signing secret.
- Token transport MUST use the `Authorization: Bearer` header
  exclusively; no cookie-based or query-parameter auth is permitted.
- All development MUST follow the Agentic Dev Stack workflow:
  spec → plan → tasks → implement via Claude Code.
- No manual coding is permitted outside the Claude Code workflow.

## Development Workflow

1. **Spec Phase**: Define feature requirements using `/sp.specify`.
2. **Plan Phase**: Generate implementation plan using `/sp.plan`.
3. **Task Phase**: Break plan into tasks using `/sp.tasks`.
4. **Implement Phase**: Execute tasks via Claude Code agents:
   - Database work → DB Agent (`neon-postgres-manager`)
   - API endpoints → Backend Agent (`fastapi-backend`)
   - Authentication → Auth Agent (`auth-security`)
   - UI/pages → Frontend Agent (`nextjs-frontend-builder`)
5. **Review**: Validate against spec acceptance criteria.
6. **Commit**: Use `/sp.git.commit_pr` for version control.

**Agent Delegation Order** (for cross-domain features):
DB Agent → Backend Agent → Auth Agent → Frontend Agent

## Governance

This constitution is the authoritative source of project principles.
All implementation decisions, code reviews, and architectural choices
MUST comply with the principles defined above.

- **Amendments** require explicit documentation of the change, the
  rationale, and a migration plan for any affected artifacts.
- **Version bumps** follow semantic versioning:
  MAJOR for principle removals/redefinitions, MINOR for additions,
  PATCH for clarifications.
- **Compliance** is verified at each phase gate (spec review, plan
  review, task review, implementation review).
- **Conflicts**: If a principle conflicts with an external dependency
  or framework limitation, the conflict MUST be documented in an ADR
  before proceeding with the deviation.

**Version**: 1.2.0 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-10
