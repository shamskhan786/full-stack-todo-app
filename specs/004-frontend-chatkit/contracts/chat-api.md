# Chat API Contract

**Feature**: 004-frontend-chatkit

## Endpoint: Create ChatKit Session

**Path**: `POST /api/chatkit/session`
**Location**: Next.js API Route (`frontend/app/api/chatkit/session/route.ts`)

**Purpose**: Creates an OpenAI ChatKit session for the authenticated
user and returns the client_secret needed by the ChatKit React
component.

### Request

**Headers**:
| Name          | Value                | Required |
|---------------|----------------------|----------|
| Authorization | Bearer `<jwt_token>` | yes      |
| Content-Type  | application/json     | yes      |

**Body**: None required (user identity from JWT).

### Response (200 OK)

```json
{
  "client_secret": "string",
  "thread_id": "string"
}
```

### Error Responses

| Status | Body                                       |
|--------|--------------------------------------------|
| 401    | `{ "error": "Authentication required" }`   |
| 500    | `{ "error": "Failed to create session" }`  |

---

## Endpoint: Get Conversation History

**Path**: `GET /api/chatkit/history`
**Location**: Next.js API Route (`frontend/app/api/chatkit/history/route.ts`)

**Purpose**: Returns conversation history from Neon PostgreSQL for
the authenticated user. Used when ChatKit thread state needs to be
reconciled with our database.

### Request

**Headers**:
| Name          | Value                | Required |
|---------------|----------------------|----------|
| Authorization | Bearer `<jwt_token>` | yes      |

**Query Parameters**:
| Name  | Type   | Required | Description         |
|-------|--------|----------|---------------------|
| limit | number | no       | Max messages (50)   |

### Response (200 OK)

```json
{
  "messages": [
    {
      "id": "uuid",
      "role": "user|assistant",
      "content": "string",
      "created_at": "ISO datetime"
    }
  ]
}
```

---

## MCP Server Endpoint

**Path**: `/mcp` (mounted on FastAPI backend)
**Transport**: Streamable HTTP (MCP protocol)

**Purpose**: Serves MCP tools to the OpenAI agent. Not called by
the frontend directly — called by OpenAI's infrastructure when the
agent invokes tools.

**Tools exposed**: See `mcp-tools.md` for full contract.

**CORS**: Must allow requests from OpenAI's infrastructure.
**Authentication**: User identity is passed as tool parameters
(injected by the agent from system instructions).
