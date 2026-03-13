---
id: 002
title: ChatKit MCP Implementation Plan
stage: plan
date: 2026-02-15
surface: agent
model: claude-opus-4-6
feature: 004-frontend-chatkit
branch: 004-frontend-chatkit
user: human
command: /sp.plan
labels: ["plan", "chatkit", "mcp", "fastmcp", "openai-agents-sdk", "phase-3"]
links:
  spec: specs/004-frontend-chatkit/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-frontend-chatkit/plan.md
  - specs/004-frontend-chatkit/research.md
  - specs/004-frontend-chatkit/data-model.md
  - specs/004-frontend-chatkit/quickstart.md
  - specs/004-frontend-chatkit/contracts/mcp-tools.md
  - specs/004-frontend-chatkit/contracts/chat-api.md
tests:
  - N/A
---

## Prompt

/sp.plan (Phase-III, Spec 2: AI Chatbot MCP Tools Integration)

Objective:
Generate a detailed step-by-step development plan for Spec 2 of Phase III (AI-powered Todo Chatbot) using existing Phase 2 backend as base.

Requirements:
- Focus on MCP tools + backend agent integration to frontend only (Spec 2).
- Implement MCP tools: add_task, list_tasks, complete_task, delete_task, update_task.
- Integrate backend agent to MCP tools using OpenAI Agents SDK.
- Connect frontend ChatKit to backend chat endpoint.
- Persist conversations and messages in Neon PostgreSQL.
- Steps must be sequential, actionable, and Claude Code-ready.
- Include checkpoints for testing each step (e.g., tool invocation test, chat endpoint test).
- Specify success criteria for each step.

Constraints:
- All backend actions via MCP tools only.
- Stateless FastAPI chat endpoint.
- Agents cannot access database directly.
- Use OpenAI Agents SDK and Official MCP SDK.
- Output plan in Markdown format for repository reference.

## Response snapshot

Created comprehensive implementation plan with 6 phases:

1. **Phase 1: Backend MCP Server Setup** — FastMCP server on FastAPI at `/mcp` with 5 task tools (add, list, complete, delete, update)
2. **Phase 2: Conversation Persistence** — New ConversationSession and ConversationMessage models in Neon PostgreSQL
3. **Phase 3: Frontend ChatKit Integration** — @openai/chatkit-react, session API route, ChatContainer component replacing TaskList
4. **Phase 4: Conversation Sync** — Persist messages to Neon via MCP save_message tool
5. **Phase 5: Error Handling & Polish** — Graceful errors, responsive design, edge cases
6. **Phase 6: End-to-End Validation** — All user stories and success criteria verified

Key architecture: ChatKit → OpenAI Responses API → Agent → MCP tools → FastAPI/FastMCP → Neon PostgreSQL

Generated artifacts: research.md (6 decisions), data-model.md (2 new entities), mcp-tools.md (5 tools), chat-api.md (2 endpoints), quickstart.md

## Outcome

- ✅ Impact: Full implementation plan for Phase-III frontend ChatKit + MCP integration
- 🧪 Tests: N/A (planning document)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/mcp-tools.md, contracts/chat-api.md
- 🔁 Next prompts: /sp.tasks to generate implementation tasks, or /sp.adr for architecture decisions
- 🧠 Reflection: ChatKit's tight coupling to OpenAI API is the primary architectural constraint; documented in research.md R1

## Evaluation notes (flywheel)

- Failure modes observed: ChatKit cannot use custom backend — requires OpenAI sessions
- Graders run and results (PASS/FAIL): Constitution check — ALL PASS (21/21 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify ChatKit session creation with MCP tools in Phase 3 implementation
