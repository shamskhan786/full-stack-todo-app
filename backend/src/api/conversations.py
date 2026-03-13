from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from ..dependencies import get_session, verify_jwt
from ..models.conversation import ConversationMessage, ConversationSession
from ..schemas.conversation import (
    MessageCreate,
    MessageRead,
    SessionCreate,
    SessionRead,
)
from ..schemas.responses import SuccessResponse

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post(
    "/sessions",
    response_model=SuccessResponse[SessionRead],
    status_code=status.HTTP_201_CREATED,
    summary="Create or retrieve conversation session",
    description="Creates a new session or retrieves existing one by OpenAI thread ID. Updates last_active_at on retrieval.",
)
def create_or_get_session(
    body: SessionCreate,
    session: Session = Depends(get_session),
    jwt_payload: dict = Depends(verify_jwt),
) -> SuccessResponse[SessionRead]:
    """
    Create or retrieve a conversation session.

    If a session with the given openai_thread_id exists, it is returned with
    updated last_active_at timestamp. Otherwise, a new session is created.
    """
    user_id = jwt_payload["sub"]

    # Check if session exists for this thread
    statement = select(ConversationSession).where(
        ConversationSession.openai_thread_id == body.openai_thread_id
    )
    existing = session.exec(statement).first()

    if existing:
        # Update last active timestamp and return existing session
        existing.last_active_at = datetime.now(timezone.utc)
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return SuccessResponse(
            data=SessionRead.from_model(existing),
            message="Session retrieved successfully",
        )

    # Create new session
    new_session = ConversationSession(
        user_id=user_id,
        openai_thread_id=body.openai_thread_id,
    )
    session.add(new_session)
    session.commit()
    session.refresh(new_session)

    return SuccessResponse(
        data=SessionRead.from_model(new_session),
        message="Session created successfully",
    )


@router.post(
    "/messages",
    response_model=SuccessResponse[MessageRead],
    status_code=status.HTTP_201_CREATED,
    summary="Save conversation message",
    description="Persists a message in the conversation. Validates session existence and user ownership.",
)
def save_message(
    body: MessageCreate,
    session: Session = Depends(get_session),
    jwt_payload: dict = Depends(verify_jwt),
) -> SuccessResponse[MessageRead]:
    """
    Save a message in the conversation.

    Validates that:
    - The session_id is a valid UUID
    - The referenced session exists
    - The user owns the session (security check)
    """
    user_id = jwt_payload["sub"]

    # Validate UUID format
    try:
        session_uuid = UUID(body.session_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid session_id format (must be UUID)",
        )

    # Validate session exists and belongs to user
    statement = select(ConversationSession).where(
        ConversationSession.id == session_uuid,
        ConversationSession.user_id == user_id,
    )
    conv_session = session.exec(statement).first()

    if not conv_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or access denied",
        )

    # Create message
    msg = ConversationMessage(
        session_id=session_uuid,
        user_id=user_id,
        role=body.role,
        content=body.content,
        tool_calls=body.tool_calls,
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)

    return SuccessResponse(
        data=MessageRead.from_model(msg),
        message="Message saved successfully",
    )


@router.get(
    "/messages",
    response_model=SuccessResponse[list[MessageRead]],
    summary="Get conversation messages",
    description="Retrieves messages for the authenticated user, ordered by creation time. Supports pagination via limit.",
)
def get_messages(
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
        description="Maximum number of messages to retrieve (1-500)",
    ),
    session: Session = Depends(get_session),
    jwt_payload: dict = Depends(verify_jwt),
) -> SuccessResponse[list[MessageRead]]:
    """
    Get conversation messages for the authenticated user.

    Returns messages ordered chronologically (oldest first).
    Limit is enforced between 1 and 500 messages.
    """
    user_id = jwt_payload["sub"]

    statement = (
        select(ConversationMessage)
        .where(ConversationMessage.user_id == user_id)
        .order_by(ConversationMessage.created_at)
        .limit(limit)
    )
    messages = session.exec(statement).all()

    return SuccessResponse(
        data=[MessageRead.from_model(m) for m in messages],
        message=f"Retrieved {len(messages)} message(s)",
    )
