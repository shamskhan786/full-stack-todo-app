---
id: 002
title: Frontend Principles Amendment
stage: constitution
date: 2026-02-10
surface: agent
model: claude-opus-4-6
feature: none
branch: 001-todo-backend-api
user: user
command: /sp.constitution
labels: ["constitution", "frontend", "principles", "amendment"]
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

Project: Todo Full-Stack Web Application – Frontend & Basic Features

Core principles:
- Usability: Interface simple, intuitive, and easy to use
- Consistency: UI behavior consistent across all pages and states
- Responsiveness: Fully responsive design for mobile, tablet, and desktop
- Accuracy: Frontend behavior accurately reflects backend API responses
- Accessibility: Basic accessibility best practices followed

Key standards:
- Use Next.js 16+ App Router architecture
- Components should be modular and reusable
- State management must correctly reflect task data (loading, error, success states)
- API communication must be done through a centralized API client
- Authentication state must be handled reliably on the client side

Constraints:
- Frontend framework: Next.js 16+ (App Router)
- Styling: Responsive layout (mobile-first approach)
- Authentication: Better Auth (session + JWT handling on frontend)
- API integration: REST API secured with JWT tokens
- No direct database access from

## Response snapshot

Amended constitution from v1.0.0 to v1.1.0 (MINOR bump — new principles added, none removed or redefined). Added five new frontend-focused principles (VII–XI): Usability, Consistency, Responsiveness, Frontend–Backend Accuracy, and Accessibility. Added a Frontend Standards section codifying architecture, state management, API integration, auth, and styling conventions. Expanded Principle IV (Clarity) to cover frontend component modularity. Added constraint: frontend MUST NOT access database directly. All three dependent templates verified compatible with no edits required.

## Outcome

- Impact: Constitution now covers full-stack principles (backend I–VI, frontend VII–XI) plus frontend standards section
- Tests: N/A — governance document, no code tests
- Files: .specify/memory/constitution.md updated
- Next prompts: Continue with frontend implementation tasks using the updated principles as guidance
- Reflection: The v1.0.0 constitution was backend-heavy; this amendment ensures frontend work has equally clear, testable governance

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
