from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Column, Field, SQLModel, JSON


class ConversationSession(SQLModel, table=True):
    """Tracks ChatKit sessions linked to users."""

    __tablename__ = "conversation_session"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True, nullable=False, max_length=36)
    openai_thread_id: str = Field(unique=True, nullable=False, max_length=100)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    last_active_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ConversationMessage(SQLModel, table=True):
    """Persists conversation messages."""

    __tablename__ = "conversation_message"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="conversation_session.id", nullable=False)
    user_id: str = Field(index=True, nullable=False, max_length=36)
    role: str = Field(nullable=False, max_length=20)
    content: str = Field(nullable=False)
    tool_calls: dict | None = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
