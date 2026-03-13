# Data Model: Frontend ChatKit Integration

**Feature**: 004-frontend-chatkit
**Date**: 2026-02-15

## Existing Entities (from Phase-II)

### Task (existing, no changes)

| Field         | Type         | Constraints                  |
|---------------|-------------|------------------------------|
| id            | UUID        | PK, auto-generated           |
| user_id       | str(36)     | NOT NULL, indexed            |
| title         | str(500)    | NOT NULL, min 1 char         |
| description   | str | null  | nullable                     |
| is_completed  | bool        | default false                |
| completed_at  | datetime    | nullable                     |
| created_at    | datetime    | NOT NULL, auto UTC           |
| updated_at    | datetime    | NOT NULL, auto UTC           |

**Table**: `task`
**File**: `backend/src/models/task.py`

## New Entities

### ConversationSession

Tracks ChatKit sessions linked to users for persistence and audit.

| Field            | Type         | Constraints                  |
|------------------|-------------|------------------------------|
| id               | UUID        | PK, auto-generated           |
| user_id          | str(36)     | NOT NULL, indexed            |
| openai_thread_id | str(100)    | NOT NULL, unique             |
| created_at       | datetime    | NOT NULL, auto UTC           |
| last_active_at   | datetime    | NOT NULL, auto UTC           |

**Table**: `conversation_session`
**File**: `backend/src/models/conversation.py`

**Rationale**: Links our user_id to OpenAI's thread_id. Enables
querying which thread belongs to which user. Updated on each
interaction for activity tracking.

### ConversationMessage

Persists conversation messages in Neon PostgreSQL per constitution
Principle XIX (Conversation Persistence).

| Field          | Type         | Constraints                  |
|----------------|-------------|------------------------------|
| id             | UUID        | PK, auto-generated           |
| session_id     | UUID        | FK → conversation_session.id |
| user_id        | str(36)     | NOT NULL, indexed            |
| role           | str(20)     | NOT NULL (user | assistant)  |
| content        | text        | NOT NULL                     |
| tool_calls     | JSON | null | nullable, stores MCP calls   |
| created_at     | datetime    | NOT NULL, auto UTC           |

**Table**: `conversation_message`
**File**: `backend/src/models/conversation.py`

**Rationale**: Stores each message exchanged in the chat. The
`tool_calls` JSON field captures which MCP tools the agent invoked
and their results, satisfying Principle XX (Traceability).

## Relationships

```
User (Better Auth)
  └── 1:N → ConversationSession
       └── 1:N → ConversationMessage
  └── 1:N → Task
```

## State Transitions

### ConversationMessage.role
- `user` — message from the human user
- `assistant` — response from the AI agent

### Task.is_completed
- `false` → `true` (via `complete_task` MCP tool)
- No reverse transition (completed tasks cannot be uncompleted)

## Migration Requirements

- New migration: Create `conversation_session` table
- New migration: Create `conversation_message` table
- Existing `task` table: No changes required
