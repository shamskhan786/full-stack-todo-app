"""Chat endpoint for AI-powered Todo Chatbot.

Stateless chat endpoint that verifies JWT, rebuilds conversation context
from database, invokes the AI agent with MCP tools, persists the exchange,
and returns the agent response.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session

from ..agents.todo_agent import run_agent
from ..dependencies import get_session, verify_jwt
from ..services.conversation import (
    get_or_create_conversation,
    load_conversation_history,
    save_message,
)

logger = logging.getLogger("backend.api.chat")

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    message: str = Field(..., min_length=1, description="User's chat message")
    conversation_id: str | None = Field(
        default=None, description="Optional conversation ID to continue"
    )


class ChatResponse(BaseModel):
    """Response from the chat endpoint."""

    response: str = Field(..., description="Agent's natural-language response")
    conversation_id: str = Field(
        ..., description="Conversation ID for subsequent messages"
    )


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    summary="Send a message to the AI agent",
    description="Stateless chat endpoint: verifies JWT, rebuilds context, invokes agent, persists exchange.",
)
async def chat(
    user_id: str,
    body: ChatRequest,
    session: Session = Depends(get_session),
    jwt_payload: dict = Depends(verify_jwt),
) -> ChatResponse:
    """Process a chat message through the AI agent."""
    # 1. Verify user_id matches JWT sub claim
    jwt_user_id = jwt_payload.get("sub")
    if not jwt_user_id or user_id != jwt_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch: you can only access your own resources",
        )
    logger.info(
        "Chat request | user=%s | conversation=%s", jwt_user_id, body.conversation_id
    )

    # 2. Get or create conversation
    conversation = get_or_create_conversation(
        session, jwt_user_id, body.conversation_id
    )

    # 3. Load conversation history from DB (context rebuild)
    history = load_conversation_history(session, conversation.id, jwt_user_id)
    logger.info(
        "Context rebuilt | messages=%d | conversation=%s",
        len(history),
        conversation.id,
    )

    # 4. Save user message
    save_message(session, conversation.id, jwt_user_id, "user", body.message)

    # 5. Invoke agent with full context
    try:
        agent_response = await run_agent(
            user_message=body.message,
            user_id=jwt_user_id,
            conversation_history=history if history else None,
        )
    except Exception:
        logger.exception("Agent invocation failed | user=%s", jwt_user_id)
        agent_response = (
            "I'm sorry, I encountered an issue processing your request. "
            "Please try again. You can ask me to add, list, complete, update, or delete tasks."
        )

    # 6. Save agent response
    save_message(session, conversation.id, jwt_user_id, "assistant", agent_response)
    logger.info(
        "Chat complete | user=%s | conversation=%s", jwt_user_id, conversation.id
    )

    # 7. Return response
    return ChatResponse(
        response=agent_response,
        conversation_id=str(conversation.id),
    )
