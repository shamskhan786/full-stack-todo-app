"""MCP Server for Todo AI Chatbot.

This module initializes the FastMCP server instance that will be used
to register MCP tools for task management operations.
"""

from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Todo MCP Server")

__all__ = ["mcp"]
