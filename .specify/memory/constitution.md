<!--
=== Sync Impact Report ===
Version change: 1.2.0 → 2.0.0 (MAJOR)
Bump rationale: Architectural paradigm shift from CRUD REST API
  to agent-based chat with MCP tools. Backward-incompatible changes
  to data flow, frontend interaction model, and backend architecture.

Modified principles:
  - V: "RESTful API Design" → "Agent-First API Design"
    (endpoints change from CRUD REST to chat-based agent invocation)
  - VI: "Input Validation & Response Standards" →
    "Chat Protocol & Response Standards"
    (validation now applies to natural-language input and MCP tool calls)
  - VII: "Usability" updated to reflect chat-based interaction model
  - X: "Frontend–Backend Alignment" updated for ChatKit + agent flow

Added sections:
  - Core Principles — Agentic Architecture (Principles XVII–XXI)
    - XVII: Agent Sovereignty (Agents Own All Task Actions)
    - XVIII: MCP Tool Boundary (Tools Are the Only DB Access Path)
    - XIX: Conversation Persistence (Stateful Context, Stateless Server)
    - XX: Traceability (Every Action Has an Audit Trail)
    - XXI: Graceful Degradation (Friendly Errors, No Silent Failures)
  - Agentic Architecture Standards section
  - Updated Technology Stack with OpenAI Agents SDK and MCP SDK
  - Updated Development Workflow and Agent Delegation Rules

Removed sections: None (all Phase-II principles retained)

Templates requiring updates:
  - .specify/templates/plan-template.md — Constitution Check section
    dynamically derives gates from constitution; no edits needed
    ✅ compatible
  - .specify/templates/spec-template.md — FR numbering and entity
    definitions remain aligned ✅ compatible
  - .specify/templates/tasks-template.md — Phase structure accommodates
    agent/MCP tasks via existing agent delegation ✅ compatible
  - .specify/templates/commands/ — No command files exist ✅ N/A

Follow-up TODOs: None
===========================
-->

# AI-Powered Todo Chatbot Constitution

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

### V. Agent-First API Design

All task operations MUST be performed through AI agents that invoke
MCP tools. The backend MUST NOT expose traditional CRUD REST
endpoints for direct task manipulation by the frontend.

- The primary API surface MUST be a chat endpoint that accepts
  natural-language user messages and returns agent responses.
- Task operations (add, list, complete, delete, update) MUST be
  executed exclusively via MCP tool invocations by the agent.
- The frontend MUST NOT call task-manipulation endpoints directly;
  all task actions flow through the chat interface.
- Agent responses MUST include friendly, human-readable confirmations
  of the actions taken.

### VI. Chat Protocol & Response Standards

All chat requests MUST be validated before processing. The agent
MUST handle ambiguous, malformed, or off-topic input gracefully.

- Chat messages MUST be validated for minimum content (non-empty
  string) before agent invocation.
- The agent MUST respond with clear, actionable messages even when
  user intent is ambiguous.
- MCP tool call results MUST be translated into user-friendly
  natural-language responses; raw tool output MUST NOT be exposed.
- Error responses MUST be friendly and suggest corrective action
  (e.g., "I couldn't find that task. Try listing your tasks first.").

## Core Principles — Frontend

### VII. Usability (Chat-First Intuitive Interface)

The user interface MUST be a chat-based experience where users
manage todos through natural-language conversation. Users MUST be
able to accomplish all task operations (create, view, edit,
complete, delete) by typing messages.

- The primary interaction model MUST be a ChatKit-powered
  conversational UI.
- Users MUST receive immediate visual feedback when a message is
  sent (typing indicator, loading state).
- Conversation history MUST be visible and scrollable within the
  chat window.
- The chat MUST resume prior conversation context after page
  refresh or server restart.

### VIII. Consistency (Uniform UI Behavior)

UI behavior MUST be consistent across all interaction states.
Users MUST be able to predict how the chat interface behaves based
on prior interactions within the application.

- Visual patterns (message bubbles, system responses, error states)
  MUST use the same styling conventions throughout.
- State transitions (sending → processing → response) MUST follow
  the same pattern for every interaction.
- Error messages MUST use a consistent format and tone across all
  failure states.

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

Frontend behavior MUST accurately reflect backend agent responses.
The UI MUST never display stale, fabricated, or inconsistent data.

- All task data displayed in the chat MUST originate from agent
  responses backed by MCP tool calls; client-side data MUST NOT
  diverge from server state after refresh.
- The chat UI MUST display agent responses verbatim (formatted for
  readability) without client-side alteration of content.
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
User isolation is enforced at the agent, MCP tool, and database
query layers.

- Every MCP tool invocation that returns or modifies user-owned
  resources MUST include the authenticated `user_id` as a parameter.
- The `user_id` used for authorization MUST be extracted from the
  verified JWT payload, never from chat messages, URL path
  parameters, or request bodies.
- Agents MUST NOT be able to override or spoof the `user_id`;
  identity injection into the agent context MUST occur at the
  API layer before agent invocation.
- No MCP tool MUST exist that returns data across multiple users
  unless explicitly designed as an admin tool with separate
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
  FastAPI dependency (`verify_jwt`) → user identity extraction →
  agent context injection.
- JWT verification MUST be implemented as a single FastAPI
  dependency function; auth logic MUST NOT be duplicated across
  route handlers.
- The frontend auth client MUST be configured in a single file
  (`frontend/lib/auth-client.ts`); auth state MUST NOT be managed
  in multiple locations.
- Error messages for auth failures MUST be specific enough to
  diagnose the issue (e.g., "Token expired" vs. "Invalid
  signature") without leaking security-sensitive details.

## Core Principles — Agentic Architecture

### XVII. Agent Sovereignty (Agents Own All Task Actions)

All task management operations MUST be performed by AI agents using
the OpenAI Agents SDK. No task operation may bypass the agent layer.

- The backend MUST instantiate agents via the OpenAI Agents SDK
  for every chat request that requires task manipulation.
- Agents MUST be the sole invokers of MCP tools; no other code
  path may call MCP tools directly.
- Agent behavior MUST be deterministic for the same input and
  state; agents MUST NOT make autonomous decisions beyond the
  user's expressed intent.
- The agent MUST correctly identify and invoke the appropriate MCP
  tool(s) based on user intent: `add_task`, `list_tasks`,
  `complete_task`, `delete_task`, `update_task`.

### XVIII. MCP Tool Boundary (Tools Are the Only DB Access Path)

MCP tools are the exclusive interface between agents and the
database. No agent, route handler, or service layer may access
the database except through registered MCP tools.

- Every database operation (read, write, update, delete) MUST be
  exposed as a registered MCP tool using the official MCP SDK.
- MCP tools MUST validate their inputs (user_id, task_id, etc.)
  before executing database queries.
- MCP tools MUST return structured results that agents can
  interpret and translate into natural-language responses.
- Direct database access from route handlers, middleware, or
  utility functions is prohibited; all DB access flows through
  MCP tools.

### XIX. Conversation Persistence (Stateful Context, Stateless Server)

Conversation history MUST be persisted in the database so that
context can be rebuilt on every request. The server itself MUST
remain stateless.

- Every user message and agent response MUST be stored in the
  `conversations` table in Neon PostgreSQL.
- Conversation context MUST be rebuilt from the database on each
  chat request; the server MUST NOT cache conversation state in
  memory between requests.
- Conversations MUST be scoped to the authenticated user; one
  user's conversation history MUST NOT be visible to another user.
- After a server restart, the chat MUST resume seamlessly by
  loading prior conversation history from the database.

### XX. Traceability (Every Action Has an Audit Trail)

Every agent action and MCP tool invocation MUST be traceable.
It MUST be possible to reconstruct what the agent did, which
tools it called, and what results it received for any given
user interaction.

- Agent tool calls and their results MUST be logged or stored
  alongside the conversation record.
- Each MCP tool invocation MUST include the `user_id` and a
  correlation identifier linking it to the originating chat
  message.
- Error states (tool failures, agent errors) MUST be recorded
  with sufficient detail to diagnose the failure without
  reproducing it.

### XXI. Graceful Degradation (Friendly Errors, No Silent Failures)

When errors occur at any layer (agent, MCP tool, database, or
network), the system MUST respond with a friendly, helpful message.
Silent failures are prohibited.

- If an MCP tool call fails, the agent MUST inform the user with
  a clear, non-technical explanation and suggest a next step.
- If the agent itself encounters an error (e.g., cannot determine
  intent), it MUST respond with a helpful prompt (e.g., "I didn't
  understand that. You can ask me to add, list, complete, update,
  or delete tasks.").
- Network or database errors MUST be caught and translated into
  user-facing messages; stack traces MUST NOT be exposed to users.
- The frontend MUST display a visible error state if the backend
  is unreachable, not silently fail.

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
- **Ownership Enforcement**: Every MCP tool that reads, creates,
  updates, or deletes a task MUST receive the authenticated
  `user_id` as a parameter. Ownership checks MUST occur within
  the MCP tool implementation.
- **Frontend Protection**: Protected frontend routes MUST check
  session state via `useSession()` and redirect unauthenticated
  users to `/signin`. The redirect MUST occur before any
  protected content renders.

## Agentic Architecture Standards

- **Agent SDK**: All agents MUST be implemented using the OpenAI
  Agents SDK. No alternative agent frameworks are permitted.
- **MCP SDK**: All MCP tools MUST be implemented using the official
  MCP SDK. Custom tool protocols are prohibited.
- **Chat Endpoint**: The primary backend endpoint MUST be
  `POST /api/chat` accepting `{ message: string }` with the JWT
  token in the `Authorization` header.
- **Context Rebuild**: On each chat request, the backend MUST:
  1. Verify the JWT token and extract `user_id`.
  2. Load conversation history from the database for the user.
  3. Append the new user message.
  4. Pass the full context to the agent.
  5. Execute agent response (including any MCP tool calls).
  6. Persist the user message and agent response.
  7. Return the agent's response to the frontend.
- **Tool Registration**: MCP tools MUST be registered with the
  agent at initialization. The required tool set is:
  - `add_task` — Create a new task for the user
  - `list_tasks` — List all tasks for the user
  - `complete_task` — Mark a task as complete
  - `delete_task` — Delete a task
  - `update_task` — Update a task's details
- **Data Flow**: Frontend → FastAPI `/api/chat` → Agent (OpenAI
  Agents SDK) → MCP Tools (MCP SDK) → Neon PostgreSQL → Response
  back through each layer.

## Frontend Standards

- **Architecture**: Next.js 16+ App Router; pages in `app/`, shared
  components in `components/`, utilities in `lib/`.
- **Chat UI**: The primary interface MUST use ChatKit for the
  conversational UI. The chat component MUST handle message
  rendering, input, and streaming responses.
- **State Management**: Chat state (messages, loading, errors) MUST
  be managed in the chat component. Global auth state MUST be
  handled reliably on the client side via Better Auth client.
- **API Integration**: All API calls MUST use the centralized API
  client in `frontend/lib/api.ts` which attaches JWT Bearer tokens
  from `authClient.token()`.
- **Authentication**: Better Auth handles session and JWT on the
  frontend. Protected routes MUST check session state and redirect
  unauthenticated users to `/signin`.
- **Styling**: Tailwind CSS with mobile-first responsive utilities.
  No external CSS frameworks unless justified in an ADR.

## Technology Stack & Constraints

| Layer          | Technology                         |
|----------------|------------------------------------|
| Frontend       | Next.js 16+ (App Router)           |
| Chat UI        | ChatKit                            |
| Backend        | Python FastAPI                     |
| Agent SDK      | OpenAI Agents SDK                  |
| MCP Tools      | Official MCP SDK                   |
| ORM            | SQLModel                           |
| Database       | Neon Serverless PostgreSQL          |
| Spec-Driven    | Claude Code + Spec-Kit Plus        |
| Authentication | Better Auth (JWT tokens)           |

**Constraints:**
- Backend MUST be implemented in Python with FastAPI.
- AI agents MUST use the OpenAI Agents SDK exclusively; no
  alternative agent frameworks are permitted.
- MCP tools MUST use the official MCP SDK exclusively; no custom
  tool protocols are permitted.
- Database MUST be Neon Serverless PostgreSQL; no other database
  engine is permitted.
- ORM MUST be SQLModel; direct SQL is prohibited unless justified.
- All database access MUST flow through MCP tools; no direct DB
  queries from route handlers or services.
- Frontend MUST use Next.js 16+ with the App Router.
- Frontend MUST NOT access the database directly; all data flows
  through the chat API and agent layer.
- Authentication MUST use Better Auth configured to issue JWT tokens.
- JWT tokens MUST be verified on every protected FastAPI endpoint.
- The `BETTER_AUTH_SECRET` environment variable MUST be shared
  between frontend and backend services as the signing secret.
- Token transport MUST use the `Authorization: Bearer` header
  exclusively; no cookie-based or query-parameter auth is permitted.
- Conversations and tasks MUST be persisted in Neon PostgreSQL.
- The backend MUST be stateless; conversation context MUST be
  rebuilt from the database on each request.
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

**Version**: 2.0.0 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-15
