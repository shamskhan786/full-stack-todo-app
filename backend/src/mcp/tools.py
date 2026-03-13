"""MCP Tools for Task Management.

This module implements 5 MCP tools that OpenAI's agent can invoke:
1. add_task - Create a new task
2. list_tasks - Retrieve all tasks for a user
3. complete_task - Mark a task as completed
4. delete_task - Permanently delete a task
5. update_task - Update task title and/or description

All tools enforce user isolation and return error dicts instead of raising exceptions.
"""

import logging
import time
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlmodel import Session, select

from ..database import engine
from ..models.task import Task
from . import mcp

logger = logging.getLogger("backend.mcp.tools")


def _validate_user_id(user_id: str) -> dict[str, str] | None:
    """Validate user_id is non-empty string. Returns error dict or None."""
    if not user_id or not user_id.strip():
        return {
            "error": "VALIDATION_ERROR",
            "message": "user_id is required and cannot be empty"
        }
    return None


def _task_to_dict(task: Task) -> dict[str, Any]:
    """Convert a Task model to a JSON-serializable dictionary.

    Args:
        task: The Task SQLModel instance

    Returns:
        Dictionary with string-serialized UUIDs and ISO datetime strings
    """
    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "is_completed": task.is_completed,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


@mcp.tool()
def add_task(user_id: str, title: str, description: str = "") -> dict[str, Any]:
    """Create a new task for a user.

    Args:
        user_id: The user's unique identifier
        title: Task title (required, max 500 characters)
        description: Optional task description

    Returns:
        Dictionary containing task details (id, title, description, is_completed, created_at)
        OR error dict with error code and message

    Error Codes:
        VALIDATION_ERROR: Title is empty or exceeds 500 characters
    """
    start = time.time()
    logger.info("add_task | user=%s | title=%s", user_id, title[:50] if title else "")

    # Validate user_id
    if err := _validate_user_id(user_id):
        return err

    # Validate title
    if not title or not title.strip():
        return {
            "error": "VALIDATION_ERROR",
            "message": "Title cannot be empty"
        }

    if len(title) > 500:
        return {
            "error": "VALIDATION_ERROR",
            "message": "Title cannot exceed 500 characters"
        }

    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info("add_task OK | user=%s | task=%s | %.3fs", user_id, task.id, time.time() - start)
        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "is_completed": task.is_completed,
            "created_at": task.created_at.isoformat(),
        }


@mcp.tool()
def list_tasks(user_id: str) -> list[dict[str, Any]]:
    """Retrieve all tasks for a user.

    Args:
        user_id: The user's unique identifier

    Returns:
        List of task dictionaries, each containing:
        - id, title, description, is_completed, completed_at, created_at, updated_at
        Returns empty list if user has no tasks
    """
    start = time.time()
    logger.info("list_tasks | user=%s", user_id)

    if err := _validate_user_id(user_id):
        return [err]

    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at)
        tasks = session.exec(statement).all()
        logger.info("list_tasks OK | user=%s | count=%d | %.3fs", user_id, len(tasks), time.time() - start)
        return [_task_to_dict(task) for task in tasks]


@mcp.tool()
def complete_task(user_id: str, task_id: str) -> dict[str, Any]:
    """Mark a task as completed with a timestamp.

    Args:
        user_id: The user's unique identifier
        task_id: The UUID of the task to complete

    Returns:
        Updated task dictionary
        OR error dict with error code and message

    Error Codes:
        NOT_FOUND: Task ID not found for this user
        ALREADY_COMPLETED: Task is already marked as completed
    """
    start = time.time()
    logger.info("complete_task | user=%s | task=%s", user_id, task_id)

    if err := _validate_user_id(user_id):
        return err

    with Session(engine) as session:
        try:
            task_uuid = UUID(task_id)
        except (ValueError, AttributeError):
            return {
                "error": "NOT_FOUND",
                "message": f"Task with ID {task_id} not found"
            }

        statement = select(Task).where(
            Task.id == task_uuid,
            Task.user_id == user_id
        )
        task = session.exec(statement).first()

        if not task:
            return {
                "error": "NOT_FOUND",
                "message": f"Task with ID {task_id} not found"
            }

        if task.is_completed:
            return {
                "error": "ALREADY_COMPLETED",
                "message": f"Task '{task.title}' is already completed"
            }

        task.is_completed = True
        task.completed_at = datetime.now(timezone.utc)
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info("complete_task OK | user=%s | task=%s | %.3fs", user_id, task_id, time.time() - start)
        return _task_to_dict(task)


@mcp.tool()
def delete_task(user_id: str, task_id: str) -> dict[str, Any]:
    """Permanently delete a task.

    Args:
        user_id: The user's unique identifier
        task_id: The UUID of the task to delete

    Returns:
        Dictionary with deleted: true, task_id, and title
        OR error dict with error code and message

    Error Codes:
        NOT_FOUND: Task ID not found for this user
    """
    start = time.time()
    logger.info("delete_task | user=%s | task=%s", user_id, task_id)

    if err := _validate_user_id(user_id):
        return err

    with Session(engine) as session:
        try:
            task_uuid = UUID(task_id)
        except (ValueError, AttributeError):
            return {
                "error": "NOT_FOUND",
                "message": f"Task with ID {task_id} not found"
            }

        statement = select(Task).where(
            Task.id == task_uuid,
            Task.user_id == user_id
        )
        task = session.exec(statement).first()

        if not task:
            return {
                "error": "NOT_FOUND",
                "message": f"Task with ID {task_id} not found"
            }

        task_title = task.title
        session.delete(task)
        session.commit()

        logger.info("delete_task OK | user=%s | task=%s | %.3fs", user_id, task_id, time.time() - start)
        return {
            "deleted": True,
            "task_id": task_id,
            "title": task_title
        }


@mcp.tool()
def update_task(
    user_id: str,
    task_id: str,
    title: str = "",
    description: str = ""
) -> dict[str, Any]:
    """Update a task's title and/or description.

    Args:
        user_id: The user's unique identifier
        task_id: The UUID of the task to update
        title: New title (optional, max 500 characters)
        description: New description (optional)

    Returns:
        Updated task dictionary
        OR error dict with error code and message

    Error Codes:
        NOT_FOUND: Task ID not found for this user
        NO_CHANGES: Neither title nor description provided
        VALIDATION_ERROR: Title is empty or exceeds 500 characters
    """
    start = time.time()
    logger.info("update_task | user=%s | task=%s", user_id, task_id)

    if err := _validate_user_id(user_id):
        return err

    # Validate that at least one field is being updated
    if not title and not description:
        return {
            "error": "NO_CHANGES",
            "message": "Must provide either title or description to update"
        }

    # Validate title if provided
    if title:
        if not title.strip():
            return {
                "error": "VALIDATION_ERROR",
                "message": "Title cannot be empty"
            }
        if len(title) > 500:
            return {
                "error": "VALIDATION_ERROR",
                "message": "Title cannot exceed 500 characters"
            }

    with Session(engine) as session:
        try:
            task_uuid = UUID(task_id)
        except (ValueError, AttributeError):
            return {
                "error": "NOT_FOUND",
                "message": f"Task with ID {task_id} not found"
            }

        statement = select(Task).where(
            Task.id == task_uuid,
            Task.user_id == user_id
        )
        task = session.exec(statement).first()

        if not task:
            return {
                "error": "NOT_FOUND",
                "message": f"Task with ID {task_id} not found"
            }

        # Update fields
        if title:
            task.title = title.strip()
        if description:
            task.description = description.strip()

        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info("update_task OK | user=%s | task=%s | %.3fs", user_id, task_id, time.time() - start)
        return _task_to_dict(task)
