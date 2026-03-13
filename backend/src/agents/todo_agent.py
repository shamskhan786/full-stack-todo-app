"""
AI-powered Todo Chatbot Agent using OpenAI Agents SDK with FastMCP integration.

This module provides an async agent that can manage todo tasks through natural language
conversation, leveraging MCP tools for task operations.
"""

import os
from typing import Any

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

from ..config import settings


async def run_agent(
    user_message: str,
    user_id: str,
    conversation_history: list[dict] | None = None
) -> str:
    """
    Run the Todo Chatbot agent with MCP tool integration.

    Args:
        user_message: The user's current message/query
        user_id: The authenticated user's ID (passed to all MCP tools)
        conversation_history: Optional list of previous messages in format:
                            [{"role": "user"|"assistant", "content": "..."}]

    Returns:
        str: The agent's text response

    Raises:
        Returns friendly error message string if agent execution fails
    """
    try:
        # Set OpenAI API key in environment (required by openai-agents SDK)
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

        # Build the complete message history
        messages: list[dict[str, Any]] | str
        if conversation_history:
            messages = conversation_history + [{"role": "user", "content": user_message}]
        else:
            messages = user_message

        # System instructions for the todo management agent
        system_prompt = f"""You are a helpful AI assistant for managing todo tasks.

Your primary function is to help users manage their tasks through natural language conversation.

CRITICAL: You are currently assisting user with ID: {user_id}
You MUST pass this exact user_id as the first parameter to EVERY MCP tool call you make:
- add_task(user_id="{user_id}", ...)
- list_tasks(user_id="{user_id}", ...)
- complete_task(user_id="{user_id}", ...)
- delete_task(user_id="{user_id}", ...)
- update_task(user_id="{user_id}", ...)

Available operations:
1. Add tasks with titles and optional descriptions
2. List all tasks (with status filters)
3. Mark tasks as complete
4. Delete tasks
5. Update task details

Guidelines:
- Be conversational and friendly
- Confirm actions before executing destructive operations (delete)
- Provide clear feedback after each operation
- When listing tasks, format them clearly with status indicators
- If a user's request is ambiguous, ask clarifying questions
- Always use the user_id provided above in every tool call

Remember: Task IDs are UUIDs. When users refer to tasks by position (e.g., "the first one"),
map that to the actual task_id from the list.
"""

        # Initialize MCP server connection (FastMCP v2 uses streamable HTTP)
        mcp_server = MCPServerStreamableHttp(params={"url": settings.MCP_SERVER_URL})

        # Create and run the agent within the MCP server context
        async with mcp_server:
            # Create the agent with MCP tools
            agent = Agent(
                name="Todo Assistant",
                instructions=system_prompt,
                mcp_servers=[mcp_server]
            )

            # Run the agent with the message(s)
            result = await Runner.run(agent, input=messages)

            # Extract text response from result
            # The result should contain the agent's response text
            if hasattr(result, 'final_output'):
                return str(result.final_output)
            elif hasattr(result, 'text'):
                return str(result.text)
            elif isinstance(result, str):
                return result
            else:
                # Fallback: try to extract text from result object
                return str(result)

    except Exception as e:
        # Return friendly error message instead of raising
        error_msg = str(e)
        return f"I apologize, but I encountered an error while processing your request: {error_msg}. Please try again or contact support if the issue persists."
