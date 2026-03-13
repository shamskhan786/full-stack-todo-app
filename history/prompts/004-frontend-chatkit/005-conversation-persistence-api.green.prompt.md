---
id: 005
title: Conversation Persistence API Routes
stage: green
date: 2026-02-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-frontend-chatkit
branch: 004-frontend-chatkit
user: nextjs-frontend-builder
command: /implement
labels: ["chatkit", "api-routes", "persistence", "conversation-history"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/app/api/chatkit/history/route.ts
  - frontend/app/api/chatkit/session/route.ts
tests:
  - None (Next.js API routes - manual testing required)
---

## Prompt

Add conversation persistence to the frontend. This involves creating a history API route and updating the ChatContainer to persist and load messages.

**Context:**
The backend now has these endpoints:
- `POST /api/conversations/sessions` — body: `{ openai_thread_id: string }`, returns `{ success: true, data: { id, user_id, openai_thread_id, ... } }`
- `POST /api/conversations/messages` — body: `{ session_id: string, role: string, content: string, tool_calls?: object }`, returns `{ success: true, data: { id, ... } }`
- `GET /api/conversations/messages?limit=50` — returns `{ success: true, data: [{ id, role, content, created_at, ... }] }`

All backend endpoints require `Authorization: Bearer <token>` header.

Backend URL is `http://localhost:8000` (from `NEXT_PUBLIC_API_URL` env var or default).

**Existing frontend files:**
- `frontend/lib/api.ts` has `getToken()`, `ApiError`, and existing `getChatHistory()` and `createChatSession()` functions
- `frontend/components/chat/chat-container.tsx` uses `useChatKit` from `@openai/chatkit-react`
- `frontend/app/api/chatkit/session/route.ts` creates OpenAI sessions

**Task T021: Create `frontend/app/api/chatkit/history/route.ts`**

Create a GET handler that:
1. Gets JWT from Authorization header
2. Calls the backend `GET /api/conversations/messages?limit=<limit>` with the JWT
3. Returns `{ messages: [...] }` to the client

**Task T020 + T022 + T023: Update session route and ChatContainer for persistence**

In `frontend/app/api/chatkit/session/route.ts`, after creating the OpenAI session, also call the backend to store the session.

For the ChatContainer, ChatKit handles conversation threading internally via OpenAI's API. The persistence layer (storing messages in Neon DB) should happen as a side effect.

Focus on:
1. Creating the history API route (T021)
2. Persisting the session in the session route (T020)
3. The ChatKit component already handles message display/history via OpenAI threads

Write the code files now.

## Response snapshot

I've successfully created the conversation persistence API routes for the frontend. Here's what was implemented:

**1. Created History API Route** (`frontend/app/api/chatkit/history/route.ts`):
- GET handler that retrieves conversation history from the backend
- Validates JWT authentication from Authorization header
- Accepts optional `limit` query parameter (default: 50)
- Calls backend `GET /api/conversations/messages?limit=<limit>` endpoint
- Returns `{ messages: [...] }` format matching frontend expectations
- Proper error handling with authentication and fetch error responses

**2. Updated Session Route** (`frontend/app/api/chatkit/session/route.ts`):
- Added session persistence after OpenAI session creation
- Calls backend `POST /api/conversations/sessions` with `openai_thread_id`
- Non-blocking: session still works even if persistence fails
- Returns `session_id` in response alongside `client_secret` and `thread_id`
- Proper error handling with console warnings for persistence failures

**Architecture Notes:**
- ChatKit manages its own conversation state via OpenAI threads
- Our persistence layer operates as a side effect for analytics/history
- The history API route is available but not actively consumed by ChatContainer yet
- ChatKit's built-in history feature handles conversation display
- Database persistence enables cross-session conversation retrieval if needed later

**Files Modified/Created:**
- Created: `frontend/app/api/chatkit/history/route.ts` (53 lines)
- Modified: `frontend/app/api/chatkit/session/route.ts` (added session persistence)

Both routes follow Next.js App Router conventions, use proper TypeScript typing, and maintain consistent error handling patterns with the existing codebase.

## Outcome

- ✅ Impact: Added conversation persistence infrastructure for ChatKit frontend, enabling backend storage of sessions and message history
- 🧪 Tests: Manual testing required - verify API routes work with authenticated requests
- 📁 Files: 2 files (1 created, 1 modified) - history API route and session persistence
- 🔁 Next prompts: Test the API routes with authenticated requests, implement message persistence hook in ChatKit events
- 🧠 Reflection: Clean separation of concerns - ChatKit handles UI/UX while backend persistence operates as side effect

## Evaluation notes (flywheel)

- Failure modes observed: None - straightforward API route implementation following existing patterns
- Graders run and results (PASS/FAIL): Not applicable - API routes require integration testing
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add ChatKit event listeners to persist messages in real-time as conversations occur
