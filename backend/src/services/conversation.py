"""Conversation persistence and context management service.

Handles creation, retrieval, and context rebuilding for conversations.
All operations enforce user isolation via user_id parameter.
"""

import logging
from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlmodel import Session, select

from ..models.conversation import ConversationMessage, ConversationSession

logger = logging.getLogger("backend.services.conversation")


def create_conversation(session: Session, user_id: str) -> ConversationSession:
    """Create a new conversation session for the user."""
    conv = ConversationSession(
        user_id=user_id,
        openai_thread_id=f"thread_{uuid4().hex[:24]}",
    )
    session.add(conv)
    session.commit()
    session.refresh(conv)
    logger.info("Conversation created | id=%s | user=%s", conv.id, user_id)
    return conv


def get_or_create_conversation(
    session: Session, user_id: str, conversation_id: str | None
) -> ConversationSession:
    """Get an existing conversation or create a new one.

    Args:
        session: Database session
        user_id: Authenticated user ID (from JWT)
        conversation_id: Optional UUID string of existing conversation

    Returns:
        ConversationSession instance

    Raises:
        HTTPException 400 if conversation_id is invalid UUID format
        HTTPException 404 if conversation not found or belongs to different user
    """
    if conversation_id:
        try:
            conv_uuid = UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation_id format (must be UUID)",
            )
        stmt = select(ConversationSession).where(
            ConversationSession.id == conv_uuid,
            ConversationSession.user_id == user_id,
        )
        conv = session.exec(stmt).first()
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied",
            )
        return conv

    return create_conversation(session, user_id)


def load_conversation_history(
    session: Session, conversation_id: UUID, user_id: str
) -> list[dict]:
    """Load conversation messages formatted for OpenAI agent consumption.

    Messages are ordered chronologically and filtered to user/assistant roles only.

    Args:
        session: Database session
        conversation_id: UUID of the conversation
        user_id: Authenticated user ID for isolation check

    Returns:
        List of message dicts: [{"role": "user"|"assistant", "content": "..."}]
    """
    # Verify conversation belongs to user
    conv_stmt = select(ConversationSession).where(
        ConversationSession.id == conversation_id,
        ConversationSession.user_id == user_id,
    )
    conv = session.exec(conv_stmt).first()
    if not conv:
        logger.warning(
            "Conversation isolation violation | conversation=%s | user=%s",
            conversation_id, user_id,
        )
        return []

    stmt = (
        select(ConversationMessage)
        .where(
            ConversationMessage.session_id == conversation_id,
            ConversationMessage.user_id == user_id,
        )
        .order_by(ConversationMessage.created_at)
    )
    messages = session.exec(stmt).all()

    history = [
        {"role": msg.role, "content": msg.content}
        for msg in messages
        if msg.role in ("user", "assistant")
    ]
    logger.info(
        "Context loaded | conversation=%s | messages=%d", conversation_id, len(history)
    )
    return history


def save_message(
    session: Session,
    conversation_id: UUID,
    user_id: str,
    role: str,
    content: str,
    tool_calls: dict | None = None,
    tool_responses: dict | None = None,
) -> ConversationMessage:
    """Persist a message to the database.

    Args:
        session: Database session
        conversation_id: UUID of the conversation (session_id FK)
        user_id: Authenticated user ID
        role: Message role (user, assistant, system)
        content: Message content text
        tool_calls: Optional dict of MCP tool calls made by agent
        tool_responses: Optional dict of tool call results

    Returns:
        The persisted ConversationMessage instance
    """
    msg = ConversationMessage(
        session_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls,
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)
    logger.info(
        "Message saved | conversation=%s | role=%s | user=%s",
        conversation_id, role, user_id,
    )
    return msg
