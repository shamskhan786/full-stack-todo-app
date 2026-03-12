---
id: 003
title: Auth Security Principles Amendment
stage: constitution
date: 2026-02-10
surface: agent
model: claude-opus-4-6
feature: none
branch: 002-todo-frontend-ui
user: developer
command: /sp.constitution
labels: ["constitution", "authentication", "security", "jwt", "better-auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

/sp.constitution

Project: Todo Full-Stack Web Application – Authentication & Security

Core principles:
- Security-first: User data must be protected at every layer
- User isolation: One user must never access another user's data
- Consistency: Authentication behavior must be consistent across frontend and backend
- Statelessness: Backend authentication must rely on JWT, not shared sessions
- Clarity: Authentication flow must be easy to understand and reason about

Key standards:
- Authentication handled on frontend using Better Auth
- Authorization enforced on backend using JWT verification
- Every API request must require a valid JWT token
- User identity must be derived from the JWT, not from client input
- Task ownership must be enforced on every backend operation

Constraints:
- Frontend: Next.js 16+ with Better Auth
- Backend: FastAPI (Python)
- Auth mechanism: JWT (JSON Web Tokens)
- Shared secret: BETTER_AUTH_SECRET environment variable used by both services
- Token transport: Authorization header

## Response snapshot

Amended constitution from v1.1.0 to v1.2.0 (MINOR bump — new section added, no removals or redefinitions).

Added "Core Principles — Authentication & Security" section with 5 new principles:
- XII. Security-First (Data Protection at Every Layer) — JWT required on all protected endpoints, 401 for unauthenticated, no secrets in logs/responses, BETTER_AUTH_SECRET as sole signing secret
- XIII. User Isolation (Cross-User Data Leakage Prevention) — user_id from JWT only, WHERE clause enforcement, path parameter validation against JWT, no cross-user endpoints
- XIV. Auth Consistency (Frontend–Backend Alignment) — Better Auth on frontend, same secret for verification, JWT sub claim as user ID, auth failures trigger redirect
- XV. Statelessness (JWT-Based, No Shared Sessions) — self-contained requests, no server-side sessions, frontend handles token refresh, backend rejects expired tokens
- XVI. Auth Clarity (Understandable Auth Flow) — single auth path documented, single FastAPI dependency, single auth-client.ts config, specific error messages

Added "Authentication Standards" section codifying: token transport (Bearer header only), token signing (EdDSA/Ed25519), identity source (JWT sub claim), ownership enforcement (service layer), frontend protection (useSession redirect).

Updated Technology Stack & Constraints with BETTER_AUTH_SECRET sharing and token transport constraints.

All templates verified compatible (plan, spec, tasks). No command files to update. No follow-up TODOs.

## Outcome

- ✅ Impact: Constitution expanded from 11 to 16 principles; auth/security now formally governed as cross-cutting concern
- 🧪 Tests: Not applicable (governance document, not code)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Compliance audit of existing backend auth code against new Principles XII–XVI
- 🧠 Reflection: New auth principles formalize patterns already implemented (JWT verification, user_id scoping, Better Auth) but now make them constitutionally enforceable and auditable

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Validation PASS — no unresolved placeholders, dates ISO, all principles declarative and testable
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run compliance audit against existing backend/auth code
