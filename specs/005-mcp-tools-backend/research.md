# Research Findings: MCP Tools & Backend Agent Core

**Feature**: MCP Tools & Backend Agent Core
**Created**: 2026-02-16

## R0.1: OpenAI API Configuration Research

### Decision: OpenAI Agent Configuration Pattern
**Rationale**: Need to properly initialize the OpenAI Agent with MCP tools for task management operations.
**Details**:
- Use OpenAI client to create assistant with specified tools
- Register MCP tools as function definitions in the assistant
- Use thread-based conversation management for context persistence
- Include user_id in thread metadata for user isolation

**Alternatives considered**:
- Direct function calling without MCP SDK: Rejected as it violates MCP Tool Boundary principle
- Custom tool protocol: Rejected as it violates MCP SDK requirement

## R0.2: MCP SDK Integration Research

### Decision: MCP Tool Registration Pattern
**Rationale**: MCP tools must be properly registered with the OpenAI Agent to enable task operations.
**Details**:
- Implement each MCP tool as a Python function with proper type hints
- Use official MCP SDK decorators to register tools
- Ensure tools receive user_id parameter for proper authorization
- Return structured data that agents can interpret

**Alternatives considered**:
- Direct database access from agent: Rejected as it violates MCP Tool Boundary principle
- Custom API calls from agent: Rejected as it violates MCP SDK requirement

## R0.3: Database Schema Research

### Decision: SQLModel Entity Definitions
**Rationale**: Need proper database schema that supports task management and conversation persistence.
**Details**:
- Task entity: id, user_id, title, description, status (pending/completed), created_at, updated_at
- Conversation entity: id, user_id, created_at, updated_at
- Message entity: id, conversation_id, user_id, role (user/assistant), content, timestamp
- Proper foreign key relationships and indexes for performance
- SQLModel inheritance for common fields (id, created_at, updated_at)

**Alternatives considered**:
- Separate databases for tasks vs conversations: Rejected for simplicity
- Different field types: Rejected in favor of standard SQLModel patterns

## R0.4: JWT Token Processing Research

### Decision: FastAPI JWT Dependency Pattern
**Rationale**: Need to extract and validate user_id from JWT tokens in all protected endpoints.
**Details**:
- Create FastAPI dependency function to verify JWT token
- Extract user_id from the 'sub' claim of the verified token
- Return user_id for use in downstream functions
- Raise HTTPException(401) if token is invalid/expired

**Alternatives considered**:
- Manual token parsing: Rejected as it's less secure
- Different claim for user_id: Rejected as 'sub' is the standard for user identification

## R0.5: Conversation Context Research

### Decision: Thread-Based Context Management
**Rationale**: Need to structure conversation history for agent consumption while maintaining persistence.
**Details**:
- Use OpenAI Threads API to maintain conversation state
- Store messages in both OpenAI thread and local database for redundancy
- Include user_id in thread metadata for user isolation
- Rebuild thread context from database on each request if needed
- Synchronize local messages with OpenAI thread state

**Alternatives considered**:
- Pure database-based context: Rejected as it doesn't leverage OpenAI's conversation management
- Pure OpenAI-based context: Rejected as it doesn't meet persistence requirements