# Data Model: MCP Tools & Backend Agent Core

**Feature**: MCP Tools & Backend Agent Core
**Created**: 2026-02-16

## Entity Definitions

### Task Entity
**Purpose**: Represents a user's todo item

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `user_id`: UUID (Foreign Key to User, indexed)
- `title`: String (max_length=255, required)
- `description`: Text (optional, nullable)
- `status`: String (choices: "pending", "completed", default: "pending")
- `created_at`: DateTime (auto-generated, indexed)
- `updated_at`: DateTime (auto-generated, updates on change)

**Relationships**:
- Belongs to one User (via user_id foreign key)
- No child relationships

**Indexes**:
- Primary: id
- Foreign key: user_id
- Composite: (user_id, status) for efficient filtering
- Created at: created_at for chronological queries

### Conversation Entity
**Purpose**: Represents a chat session between user and AI agent

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `user_id`: UUID (Foreign Key to User, indexed)
- `title`: String (max_length=255, optional, nullable)
- `created_at`: DateTime (auto-generated, indexed)
- `updated_at`: DateTime (auto-generated, updates on change)

**Relationships**:
- Belongs to one User (via user_id foreign key)
- Has many Messages (via conversation_id foreign key)

**Indexes**:
- Primary: id
- Foreign key: user_id
- Created at: created_at for chronological queries

### Message Entity
**Purpose**: Represents individual messages within a conversation

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `conversation_id`: UUID (Foreign Key to Conversation, indexed)
- `user_id`: UUID (Foreign Key to User, indexed, for authorization)
- `role`: String (choices: "user", "assistant", "system", required)
- `content`: Text (required)
- `timestamp`: DateTime (auto-generated, indexed)
- `tool_calls`: JSON (optional, nullable, for agent tool calls)
- `tool_responses`: JSON (optional, nullable, for tool call results)

**Relationships**:
- Belongs to one Conversation (via conversation_id foreign key)
- Belongs to one User (via user_id foreign key)

**Indexes**:
- Primary: id
- Foreign keys: conversation_id, user_id
- Timestamp: timestamp for chronological ordering
- Role: role for filtering by message type

## Validation Rules

### Task Validation
- Title must not be empty (length > 0)
- Status must be one of: "pending", "completed"
- user_id must reference an existing user
- Cannot modify a task that belongs to a different user

### Conversation Validation
- user_id must reference an existing user
- Title length must be <= 255 characters if provided
- Cannot access a conversation that belongs to a different user

### Message Validation
- conversation_id must reference an existing conversation
- user_id must reference an existing user
- role must be one of: "user", "assistant", "system"
- content must not be empty (length > 0)
- Cannot create/access messages in a conversation belonging to a different user

## State Transitions

### Task State Transitions
- `pending` → `completed`: When complete_task MCP tool is invoked
- `completed` → `pending`: When update_task MCP tool is invoked with status change
- No other state transitions allowed

## Index Recommendations

### Primary Queries
1. **Get user's tasks**: INDEX(user_id, status) - efficient for retrieving all tasks for a user
2. **Get conversation messages**: INDEX(conversation_id, timestamp) - efficient for chronological message retrieval
3. **User access validation**: INDEX(user_id) on all entities - efficient for authorization checks

### Performance Considerations
- UUID primary keys provide global uniqueness for distributed systems
- Indexed foreign keys ensure efficient joins
- Composite indexes optimize common query patterns
- Timestamp indexes enable efficient chronological queries