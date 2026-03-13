from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Request body for creating or retrieving a conversation session."""

    openai_thread_id: str = Field(
        ...,
        max_length=100,
        description="OpenAI thread ID to associate with this session",
    )


class SessionRead(BaseModel):
    """Response schema for conversation session."""

    id: str = Field(..., description="Session UUID as string")
    user_id: str = Field(..., description="User ID who owns this session")
    openai_thread_id: str = Field(..., description="OpenAI thread ID")
    created_at: str = Field(..., description="ISO 8601 timestamp")
    last_active_at: str = Field(..., description="ISO 8601 timestamp")

    @classmethod
    def from_model(cls, session) -> "SessionRead":
        """Convert SQLModel ConversationSession to response schema."""
        return cls(
            id=str(session.id),
            user_id=session.user_id,
            openai_thread_id=session.openai_thread_id,
            created_at=session.created_at.isoformat(),
            last_active_at=session.last_active_at.isoformat(),
        )


class MessageCreate(BaseModel):
    """Request body for saving a conversation message."""

    session_id: str = Field(..., description="Session UUID as string")
    role: str = Field(..., max_length=20, description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")
    tool_calls: dict | None = Field(
        default=None,
        description="Optional tool calls metadata",
    )


class MessageRead(BaseModel):
    """Response schema for conversation message."""

    id: str = Field(..., description="Message UUID as string")
    session_id: str = Field(..., description="Session UUID as string")
    user_id: str = Field(..., description="User ID")
    role: str = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    tool_calls: dict | None = Field(default=None, description="Tool calls metadata")
    created_at: str = Field(..., description="ISO 8601 timestamp")

    @classmethod
    def from_model(cls, message) -> "MessageRead":
        """Convert SQLModel ConversationMessage to response schema."""
        return cls(
            id=str(message.id),
            session_id=str(message.session_id),
            user_id=message.user_id,
            role=message.role,
            content=message.content,
            tool_calls=message.tool_calls,
            created_at=message.created_at.isoformat(),
        )
