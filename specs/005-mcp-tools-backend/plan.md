# Implementation Plan: MCP Tools & Backend Agent Core

**Feature**: MCP Tools & Backend Agent Core
**Branch**: 005-mcp-tools-backend
**Created**: 2026-02-16
**Status**: Draft

## Technical Context

### Known Information
- **Backend Framework**: FastAPI (Python)
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Agent SDK**: OpenAI Agents SDK
- **MCP Tools**: Official MCP SDK
- **Authentication**: JWT tokens from Phase-II implementation
- **Entities**: Task, Conversation, Message (from spec)
- **Endpoint Pattern**: POST /api/{user_id}/chat (stateless chat endpoint)
- **Architecture**: Stateless server with persistent conversation context rebuilt from database

### Unknown Information (NEEDS CLARIFICATION)
- None (all previously unknown items have been researched and resolved)

## Constitution Check

### Gate 1: Agent-First API Design (Section V)
- **Requirement**: All task operations MUST be performed through AI agents that invoke MCP tools
- **Validation**: Plan must ensure task CRUD operations only happen through MCP tools, not direct REST endpoints
- **Status**: VALIDATED - Plan ensures all task operations flow through agent → MCP tools pathway

### Gate 2: MCP Tool Boundary (Section XVIII)
- **Requirement**: MCP tools are the exclusive interface between agents and the database
- **Validation**: Plan must ensure no direct database access from route handlers or services
- **Status**: VALIDATED - Plan ensures all DB access occurs through MCP tools only

### Gate 3: Conversation Persistence (Section XIX)
- **Requirement**: Conversation history MUST be persisted so context can be rebuilt on every request
- **Validation**: Plan must include database persistence for conversations and messages
- **Status**: VALIDATED - Plan includes database persistence and context rebuilding

### Gate 4: User Isolation (Section XIII)
- **Requirement**: User data MUST be properly isolated; one user cannot access another's data
- **Validation**: Plan must ensure user_id from JWT is used to scope all data access
- **Status**: VALIDATED - Plan ensures user_id from JWT is used to scope all operations

### Gate 5: Technology Stack Compliance (Section XLV-XLVII)
- **Requirement**: Must use specified technologies (FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Neon PostgreSQL)
- **Validation**: Plan must align with all stack requirements
- **Status**: VALIDATED - Plan uses all required technologies as specified

---

## Phase 0: Research & Resolution of Unknowns

### Objective
Resolve all NEEDS CLARIFICATION items from Technical Context through research and experimentation.

### Research Tasks

#### R0.1: OpenAI API Configuration Research
- **Task**: Research OpenAI Agents SDK configuration for MCP tools integration
- **Deliverable**: research/openai-config.md with API key handling, model selection, and agent initialization patterns
- **Success Criteria**: Clear understanding of how to initialize agent with MCP tools

#### R0.2: MCP SDK Integration Research
- **Task**: Research official MCP SDK patterns for FastAPI integration
- **Deliverable**: research/mcp-integration.md with tool registration and invocation patterns
- **Success Criteria**: Understanding of how to register and use MCP tools with OpenAI Agents

#### R0.3: Database Schema Research
- **Task**: Research SQLModel patterns for Task, Conversation, Message entities
- **Deliverable**: research/database-schema.md with field types, relationships, and constraints
- **Success Criteria**: Clear schema definitions for all required entities

#### R0.4: JWT Token Processing Research
- **Task**: Research JWT token verification and user_id extraction in FastAPI
- **Deliverable**: research/jwt-processing.md with dependency injection patterns and token validation
- **Success Criteria**: Understanding of how to extract and validate user_id from JWT

#### R0.5: Conversation Context Research
- **Task**: Research conversation history formatting for agent consumption
- **Deliverable**: research/conversation-format.md with message structuring patterns
- **Success Criteria**: Understanding of how to format conversation context for agents

### Validation
- All research deliverables completed
- All NEEDS CLARIFICATION items resolved
- Technical Context updated with research findings

---

## Phase 1: Data Model & API Contracts

### Objective
Design the data model and API contracts that will support the MCP tools and agent integration.

### Implementation Steps

#### Step 1.1: Design Data Model
- **Action**: Create data-model.md with complete schema for Task, Conversation, Message entities
- **Inputs**: Research findings from Phase 0
- **Outputs**: data-model.md with:
  - Entity definitions with fields, types, constraints
  - Relationships between entities
  - Validation rules
  - Index recommendations
- **Technical Checkpoint**: Schema aligns with SQLModel best practices and Neon PostgreSQL capabilities

#### Step 1.2: Design MCP Tool Contracts
- **Action**: Create MCP tool specifications with input/output schemas
- **Inputs**: Functional requirements from spec, data model
- **Outputs**: contracts/mcp-tools.json with:
  - add_task: {title: string, description?: string} → {task_id: string, title: string, ...}
  - list_tasks: {} → {tasks: [{task_id: string, title: string, status: string, ...}]}
  - complete_task: {task_id: string} → {success: boolean, task: {...}}
  - delete_task: {task_id: string} → {success: boolean}
  - update_task: {task_id: string, title?: string, description?: string, status?: string} → {success: boolean, task: {...}}
- **Technical Checkpoint**: Tool contracts support all functional requirements

#### Step 1.3: Design Chat API Contract
- **Action**: Create chat endpoint specification
- **Inputs**: User scenarios from spec, authentication requirements
- **Outputs**: contracts/chat-api.json with:
  - POST /api/{user_id}/chat
  - Request: {message: string}
  - Response: {response: string, tool_calls?: [...]}
  - Headers: Authorization: Bearer {jwt_token}
- **Technical Checkpoint**: API contract supports stateless operation with JWT authentication

#### Step 1.4: Create Quickstart Guide
- **Action**: Document setup and development workflow
- **Inputs**: All research and design work
- **Outputs**: quickstart.md with:
  - Environment setup instructions
  - Development workflow
  - Testing procedures
- **Technical Checkpoint**: New developer can follow guide to run the system

### Validation
- Data model supports all functional requirements
- MCP tool contracts are complete and well-defined
- API contract enables stateless chat with proper authentication
- Quickstart guide is comprehensive and accurate

### Success Criteria
- Complete data model documented
- MCP tool contracts defined
- Chat API contract defined
- Quickstart guide available

---

## Phase 2: Infrastructure & Setup

### Objective
Set up the foundational infrastructure needed for MCP tools and agent integration.

### Implementation Steps

#### Step 2.1: Database Setup
- **Action**: Create database models and migration scripts
- **Inputs**: Data model from Phase 1
- **Outputs**: backend/src/models/ with Task, Conversation, Message models; alembic migration scripts
- **Technical Checkpoint**: Models properly defined with relationships and constraints

#### Step 2.2: MCP Tools Implementation
- **Action**: Implement MCP tools with database operations
- **Inputs**: MCP tool contracts from Phase 1, database models
- **Outputs**: backend/src/mcp/ with add_task, list_tasks, complete_task, delete_task, update_task implementations
- **Technical Checkpoint**: Tools follow MCP SDK patterns and enforce user isolation

#### Step 2.3: Authentication Integration
- **Action**: Implement JWT verification and user context extraction
- **Inputs**: JWT research from Phase 0, existing Phase-II auth
- **Outputs**: backend/src/auth/ with JWT verification utilities
- **Technical Checkpoint**: Proper user_id extraction and validation

#### Step 2.4: Agent Integration Setup
- **Action**: Set up OpenAI Agent with MCP tools
- **Inputs**: OpenAI research from Phase 0, MCP tools from Step 2.2
- **Outputs**: backend/src/agents/ with agent initialization and configuration
- **Technical Checkpoint**: Agent properly configured with MCP tools

### Validation
- Database models created and migratable
- MCP tools implemented with proper database access
- Authentication integrated with user isolation
- Agent properly configured with tools

### Success Criteria
- Database infrastructure ready
- MCP tools functional
- Authentication working
- Agent configured

---

## Phase 3: Core Implementation

### Objective
Implement the stateless chat endpoint that integrates all components.

### Implementation Steps

#### Step 3.1: Chat Endpoint Implementation
- **Action**: Create POST /api/{user_id}/chat endpoint
- **Inputs**: API contract from Phase 1, all components from Phase 2
- **Outputs**: backend/src/api/chat.py with complete chat endpoint
- **Technical Checkpoint**: Endpoint verifies JWT, rebuilds context, invokes agent, persists results

#### Step 3.2: Conversation Context Rebuilding
- **Action**: Implement conversation history loading and formatting
- **Inputs**: Message/Conversation models, database access
- **Outputs**: backend/src/services/conversation.py with context rebuilding logic
- **Technical Checkpoint**: Efficient loading of conversation history for agent context

#### Step 3.3: Error Handling Implementation
- **Action**: Add comprehensive error handling throughout
- **Inputs**: Error scenarios from spec, graceful degradation principle
- **Outputs**: Updated services/endpoints with proper error responses
- **Technical Checkpoint**: All error paths result in user-friendly responses

#### Step 3.4: Logging Implementation
- **Action**: Add logging for traceability
- **Inputs**: Traceability requirements from constitution
- **Outputs**: Logging configuration and implementation in all layers
- **Technical Checkpoint**: All agent actions and tool calls are traceable

### Validation
- Chat endpoint properly integrates all components
- Conversation context is rebuilt from database
- Error handling covers all scenarios
- Logging enables traceability

### Success Criteria
- Fully functional chat endpoint
- Proper conversation persistence
- Comprehensive error handling
- Adequate logging

---

## Phase 4: Testing & Validation

### Objective
Validate that the implementation meets all functional and non-functional requirements.

### Implementation Steps

#### Step 4.1: Unit Testing
- **Action**: Create unit tests for all components
- **Inputs**: All implemented code
- **Outputs**: test/ directory with comprehensive unit tests
- **Technical Checkpoint**: All units tested with high coverage

#### Step 4.2: Integration Testing
- **Action**: Create integration tests for end-to-end flows
- **Inputs**: Complete system implementation
- **Outputs**: Integration tests covering all user scenarios
- **Technical Checkpoint**: End-to-end functionality validated

#### Step 4.3: Security Testing
- **Action**: Validate user isolation and authentication
- **Inputs**: Authentication and authorization components
- **Outputs**: Security tests confirming user data isolation
- **Technical Checkpoint**: Cross-user data access prevented

#### Step 4.4: Performance Testing
- **Action**: Validate performance against success criteria
- **Inputs**: Complete implementation
- **Outputs**: Performance benchmarks and validation
- **Technical Checkpoint**: Performance meets success criteria

### Validation
- All unit tests pass
- Integration tests validate complete flows
- Security tests confirm proper isolation
- Performance meets requirements

### Success Criteria
- High test coverage achieved
- All tests pass
- Security validated
- Performance requirements met

---

## Post-Implementation Constitution Check

### Gate 1: Agent Sovereignty (Section XVII)
- **Requirement**: All task operations MUST be performed by AI agents using OpenAI Agents SDK
- **Validation**: Confirm all task operations flow through agent → MCP tools
- **Status**: [TO BE VALIDATED]

### Gate 2: MCP Tool Boundary (Section XVIII)
- **Requirement**: MCP tools are the exclusive interface between agents and the database
- **Validation**: Confirm no direct database access outside MCP tools
- **Status**: [TO BE VALIDATED]

### Gate 3: Conversation Persistence (Section XIX)
- **Requirement**: Conversation history MUST be persisted and rebuilt from database
- **Validation**: Confirm conversations survive server restarts
- **Status**: [TO BE VALIDATED]

### Gate 4: Traceability (Section XX)
- **Requirement**: Every agent action and MCP tool invocation MUST be traceable
- **Validation**: Confirm adequate logging for debugging and audit
- **Status**: [TO BE VALIDATED]

### Gate 5: Graceful Degradation (Section XXI)
- **Requirement**: System MUST respond with friendly messages on errors
- **Validation**: Confirm error paths provide user-friendly responses
- **Status**: [TO BE VALIDATED]