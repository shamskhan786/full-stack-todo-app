# Feature Specification: Frontend ChatKit Integration

**Feature Branch**: `004-frontend-chatkit`
**Created**: 2026-02-15
**Status**: Draft
**Input**: User description: "Phase-III Frontend ChatKit Integration — Build a ChatKit-based conversational UI for the Todo AI Chatbot, integrating with backend MCP tools via a chat endpoint."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Send Chat Messages to Manage Tasks (Priority: P1)

As a signed-in user, I want to type natural-language messages in a chat interface and have an AI agent manage my tasks (create, list, complete, update, delete) based on what I say, so I can manage todos conversationally without navigating forms or buttons.

**Why this priority**: This is the core interaction model for Phase-III. Without chat-based task management, the feature has no value. Every other story depends on this working.

**Independent Test**: A signed-in user types "Add a task called Buy groceries" in the chat input, presses send, and sees a friendly confirmation from the AI agent (e.g., "Done! I've added 'Buy groceries' to your list."). The task is persisted in the database.

**Acceptance Scenarios**:

1. **Given** a signed-in user on the chat page, **When** they type "Add a task: Buy groceries" and press send, **Then** the AI responds with a confirmation that the task was created.
2. **Given** a signed-in user with existing tasks, **When** they type "Show my tasks", **Then** the AI responds with a formatted list of their tasks.
3. **Given** a signed-in user with a task "Buy groceries", **When** they type "Mark Buy groceries as done", **Then** the AI responds confirming the task is complete.
4. **Given** a signed-in user with a task "Buy groceries", **When** they type "Delete Buy groceries", **Then** the AI responds confirming the task was deleted.
5. **Given** a signed-in user with a task "Buy groceries", **When** they type "Update Buy groceries to Buy organic groceries", **Then** the AI responds confirming the update.
6. **Given** a signed-in user who sends a message, **When** the AI is processing, **Then** a typing/loading indicator is visible until the response arrives.

---

### User Story 2 - Conversation Persistence and Context Resumption (Priority: P2)

As a signed-in user, I want my conversation history to be preserved so that when I refresh the page or return later, I can see my previous messages and AI responses, and the AI remembers what we discussed.

**Why this priority**: Without persistence, every page load starts fresh, losing context and degrading user experience. This is critical for the "stateful context, stateless server" constitution principle.

**Independent Test**: A user sends several messages, refreshes the browser, and sees all previous messages in the chat window. They type a follow-up referencing a prior conversation, and the AI responds with context awareness.

**Acceptance Scenarios**:

1. **Given** a user who sent 5 messages in a conversation, **When** they refresh the page, **Then** all 5 messages and their AI responses are visible in the chat window.
2. **Given** a user with conversation history, **When** the page loads, **Then** the conversation history loads and the user can scroll through past messages.
3. **Given** a new user with no conversation history, **When** they open the chat page for the first time, **Then** a welcome message is displayed with example commands they can try.

---

### User Story 3 - Graceful Error Handling in Chat (Priority: P3)

As a user, when something goes wrong (network error, invalid request, task not found), I want the chat to show a friendly error message so I understand what happened and know what to do next.

**Why this priority**: Error handling ensures the experience is robust and users are never confused by silent failures or technical error messages.

**Independent Test**: Disconnect the network while sending a message; verify the chat displays a user-friendly error with a retry suggestion.

**Acceptance Scenarios**:

1. **Given** a user sends a message and the backend is unreachable, **When** the request fails, **Then** the chat displays a friendly error message with a retry option.
2. **Given** a user asks to complete a task that doesn't exist, **When** the agent returns a not-found response, **Then** the AI responds with a helpful suggestion (e.g., "I couldn't find that task. Try saying 'Show my tasks' to see your current list.").
3. **Given** a user's JWT token expires mid-conversation, **When** they send a message and receive a 401, **Then** they are redirected to the sign-in page.
4. **Given** a user sends an ambiguous message, **When** the agent cannot determine intent, **Then** the AI responds with a helpful prompt listing available actions.

---

### User Story 4 - Responsive Chat UI Across Devices (Priority: P4)

As a user on a mobile phone, tablet, or desktop, I want the chat interface to adapt to my screen size so I can manage tasks comfortably on any device.

**Why this priority**: Responsiveness expands usability across devices beyond desktop.

**Independent Test**: Open the chat page on a 375px-wide mobile viewport; verify the chat fills the screen, input is reachable, and messages are readable without horizontal scrolling.

**Acceptance Scenarios**:

1. **Given** a user on a mobile device (375px width), **When** they view the chat page, **Then** the chat fills the viewport, messages are readable, and the input field is fixed at the bottom.
2. **Given** a user on a tablet (768px width), **When** they view the chat page, **Then** the layout uses appropriate proportions with comfortable spacing.
3. **Given** a user on a desktop (1920px width), **When** they view the chat page, **Then** the chat area is centered with a maximum width and messages are well-spaced.

---

### Edge Cases

- What happens when a user sends a very long message (>5000 characters)? The system truncates to a safe limit and informs the user.
- What happens when the AI agent response takes longer than 30 seconds? A timeout message is shown with a retry option.
- What happens when the conversation history is very large (>500 messages)? The UI loads the most recent messages first and supports scrolling to load older messages.
- What happens when two browser tabs are open with the same user? Both tabs show consistent conversation state on refresh.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST render a chat interface using ChatKit as the primary UI component on the dashboard page, replacing the existing task list UI.
- **FR-002**: System MUST send user messages to `POST /api/{user_id}/chat` with the message content and JWT Bearer token in the Authorization header.
- **FR-003**: System MUST display AI agent responses in the chat window as they are received from the backend.
- **FR-004**: System MUST load and display the user's conversation history from the backend when the chat page loads.
- **FR-005**: System MUST show a loading/typing indicator while waiting for the AI agent's response.
- **FR-006**: System MUST extract the authenticated user's ID from the Better Auth session and use it for all API calls.
- **FR-007**: System MUST redirect unauthenticated users to `/signin` before rendering the chat page.
- **FR-008**: System MUST display user-friendly error messages when API calls fail, with specific guidance for common errors (not found, network error, expired session).
- **FR-009**: System MUST support all five task operations via natural-language chat messages: add, list, complete, delete, update.
- **FR-010**: System MUST be fully responsive across mobile (375px), tablet (768px), and desktop (1920px) viewports with no horizontal scrolling.
- **FR-011**: System MUST use the centralized API client (`frontend/lib/api.ts`) for all backend communication, attaching JWT tokens automatically.
- **FR-012**: System MUST display a helpful prompt when the agent cannot determine user intent from an ambiguous message.
- **FR-013**: System MUST display a welcome message with example commands when a new user opens the chat page for the first time (empty conversation history).

### Key Entities

- **ChatMessage**: Represents a single message in the conversation. Key attributes: sender (user or assistant), content (text), timestamp, status (sending, sent, error).
- **Conversation**: Represents the full conversation history for a user. Loaded from the backend on page mount, appended with each new message exchange.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task via chat within 5 seconds of sending the message (end-to-end, from message sent to confirmation displayed).
- **SC-002**: Conversation history loads within 2 seconds on page refresh for conversations with up to 100 messages.
- **SC-003**: All five task operations (add, list, complete, delete, update) are executable through natural-language chat messages.
- **SC-004**: Error states display user-friendly messages within 3 seconds of failure detection; no raw error codes or stack traces are ever shown to the user.
- **SC-005**: Chat interface is fully functional and readable on viewports from 375px to 1920px wide without horizontal scrolling.
- **SC-006**: Users who refresh the page see their full conversation history preserved, including both their messages and AI responses.
- **SC-007**: Unauthenticated users are redirected to the sign-in page within 1 second of attempting to access the chat page.

### Assumptions

- The backend `POST /api/{user_id}/chat` endpoint exists or will be built as part of the Phase-III backend feature (separate spec, 001-backend-self-healing or a new backend-agents spec).
- The backend provides conversation history either via a dedicated `GET /api/{user_id}/chat/history` endpoint or includes prior messages in the chat endpoint response.
- ChatKit is available as an npm package compatible with Next.js 16+ App Router.
- The existing Better Auth setup (`frontend/lib/auth-client.ts`, JWT plugin) remains unchanged from Phase-II.
- The existing centralized API client (`frontend/lib/api.ts`) will be extended to support the chat endpoint, not replaced.
