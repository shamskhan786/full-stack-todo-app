---
id: 004
title: Phase-III Agentic Architecture Amendment
stage: constitution
date: 2026-02-15
surface: agent
model: claude-opus-4-6
feature: none
branch: 001-backend-self-healing
user: human
command: /sp.constitution
labels: ["constitution", "phase-3", "agentic-architecture", "mcp", "openai-agents-sdk"]
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

/sp.constitution (Phase-III Update)
Project: AI-Powered Todo Chatbot (Phase 2 → Phase 3)

Core Additions:
- Agent-first design using OpenAI Agents SDK
- Stateless FastAPI chat; all task actions via MCP tools
- Agents → MCP tools → Database; no direct DB access
- Frontend ChatKit integrated with backend FastAPI
- Conversation context rebuilt per request; actions traceable
- Phase-II auth & user isolation rules enforced

Constraints:
- Only OpenAI Agents SDK + Official MCP SDK
- Persist conversations & tasks in Neon PostgreSQL
- No manual coding; Claude Code only

Success Criteria:
- Manage todos via natural language
- Correct MCP tool invocation: add, list, complete, delete, update
- Conversation resumes after server restart
- Friendly confirmations; graceful error handling

Deliverables:
- /frontend → ChatKit UI
- /backend → FastAPI + Agents SDK + MCP
- /specs → Phase-III spec files
- DB migration scripts, README

Workflow:
Frontend → Backend agents → MCP tools → DB → Response → Frontend

IMPORTANT: After completing your current task, you MUST address the user's message above. Do not ignore it.

## Response snapshot

Updated constitution from v1.2.0 → v2.0.0 (MAJOR version bump). Key changes:

1. **Modified principles**: V (RESTful → Agent-First API Design), VI (Input Validation → Chat Protocol), VII (Usability → Chat-First), X (updated for ChatKit + agent flow)
2. **Added 5 new principles** (XVII–XXI) under "Core Principles — Agentic Architecture": Agent Sovereignty, MCP Tool Boundary, Conversation Persistence, Traceability, Graceful Degradation
3. **Added sections**: Agentic Architecture Standards (agent SDK, MCP SDK, chat endpoint, context rebuild, tool registration, data flow)
4. **Updated Technology Stack** to include OpenAI Agents SDK, MCP SDK, and ChatKit
5. **Updated constraints** to enforce agent-only DB access, conversation persistence, and stateless server
6. All Phase-II auth/security principles (XII–XVI) retained and updated for agent context

## Outcome

- ✅ Impact: Major constitution rewrite for Phase-III agentic architecture
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify for Phase-III feature spec, /sp.plan for implementation plan
- 🧠 Reflection: MAJOR bump justified by fundamental shift from CRUD REST to agent-based chat architecture

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review — PASS (no unresolved placeholders, all principles declarative and testable)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify template compatibility after first Phase-III spec is generated
