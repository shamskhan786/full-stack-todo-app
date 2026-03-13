# MCP Tools Contract

**Feature**: 004-frontend-chatkit
**Transport**: Streamable HTTP at `/mcp`

## Tool: add_task

**Description**: Create a new task for the authenticated user.

**Parameters**:
| Name        | Type   | Required | Description              |
|-------------|--------|----------|--------------------------|
| user_id     | string | yes      | Authenticated user's ID  |
| title       | string | yes      | Task title (1-500 chars) |
| description | string | no       | Optional description     |

**Returns**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string|null",
  "is_completed": false,
  "created_at": "ISO datetime"
}
```

**Errors**:
- `VALIDATION_ERROR`: title empty or exceeds 500 chars
- `DATABASE_ERROR`: DB write failure

---

## Tool: list_tasks

**Description**: List all tasks for the authenticated user.

**Parameters**:
| Name    | Type   | Required | Description              |
|---------|--------|----------|--------------------------|
| user_id | string | yes      | Authenticated user's ID  |

**Returns**:
```json
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string|null",
    "is_completed": false,
    "completed_at": "ISO datetime|null",
    "created_at": "ISO datetime",
    "updated_at": "ISO datetime"
  }
]
```

**Returns empty array** if user has no tasks.

---

## Tool: complete_task

**Description**: Mark a specific task as completed.

**Parameters**:
| Name    | Type   | Required | Description              |
|---------|--------|----------|--------------------------|
| user_id | string | yes      | Authenticated user's ID  |
| task_id | string | yes      | UUID of task to complete  |

**Returns**:
```json
{
  "id": "uuid",
  "title": "string",
  "is_completed": true,
  "completed_at": "ISO datetime"
}
```

**Errors**:
- `NOT_FOUND`: task_id not found for this user
- `ALREADY_COMPLETED`: task is already marked complete

---

## Tool: delete_task

**Description**: Permanently delete a task.

**Parameters**:
| Name    | Type   | Required | Description              |
|---------|--------|----------|--------------------------|
| user_id | string | yes      | Authenticated user's ID  |
| task_id | string | yes      | UUID of task to delete   |

**Returns**:
```json
{
  "deleted": true,
  "task_id": "uuid",
  "title": "string"
}
```

**Errors**:
- `NOT_FOUND`: task_id not found for this user

---

## Tool: update_task

**Description**: Update a task's title and/or description.

**Parameters**:
| Name        | Type   | Required | Description                 |
|-------------|--------|----------|-----------------------------|
| user_id     | string | yes      | Authenticated user's ID     |
| task_id     | string | yes      | UUID of task to update      |
| title       | string | no       | New title (1-500 chars)     |
| description | string | no       | New description             |

**Returns**:
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string|null",
  "is_completed": false,
  "updated_at": "ISO datetime"
}
```

**Errors**:
- `NOT_FOUND`: task_id not found for this user
- `VALIDATION_ERROR`: title empty or exceeds 500 chars
- `NO_CHANGES`: neither title nor description provided
