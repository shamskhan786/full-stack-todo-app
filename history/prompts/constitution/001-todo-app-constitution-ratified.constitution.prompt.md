---
id: 001
title: Todo App Constitution Ratified
stage: constitution
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "governance", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

/sp.constitution

Project: Todo Full-Stack Web Application – Backend & REST API

Core principles:
- Accuracy: Ensure all API endpoints behave exactly as specified
- Security: All user data is correctly filtered and protected
- Reproducibility: API responses and database interactions are consistent
- Clarity: Clear code structure and endpoint documentation for developers

Key standards:
- RESTful API design principles must be followed
- All database operations use SQLModel with proper ORM practices
- Endpoints must return appropriate HTTP status codes
- Input validation must be implemented for all API requests
- All responses should include clear JSON structure

Constraints:
- Backend technology: Python FastAPI
- Database: Neon Serverless PostgreSQL
- API Endpoints:
  GET /api/{user_id}/tasks
  POST /api/{user_id}/tasks
  GET /api/{user_id}/tasks/{id}
  PUT /api/{user_id}/tasks/{id}
  DELETE /api/{user_id}/tasks/{id}
  PATCH /api/{user_id}/tasks/{id}/complete
- Authorization: Assume JWT tokens will be verifi

## Response snapshot

Created constitution v1.0.0 for the Todo Full-Stack Web Application with 6 core principles: (I) Accuracy — API correctness, (II) Security — data protection and JWT auth, (III) Reproducibility — consistent behavior, (IV) Clarity — code structure and docs, (V) RESTful API Design — defined contract with 6 endpoints, (VI) Input Validation & Response Standards. Includes technology stack table (Next.js, FastAPI, SQLModel, Neon PostgreSQL, Better Auth), development workflow with agent delegation order, and governance rules with semantic versioning. All templates verified compatible.

## Outcome

- Impact: Project constitution ratified at v1.0.0; all 6 principles defined with testable MUST-level requirements
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md created
- Next prompts: /sp.specify to create feature spec, /sp.plan for implementation plan
- Reflection: User provided 4 core principles; expanded to 6 to cover RESTful design and input validation as separate enforceable principles. API contract endpoints embedded directly in constitution for traceability.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation PASS — no unresolved placeholders, all dates ISO, all principles declarative with MUST language
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
