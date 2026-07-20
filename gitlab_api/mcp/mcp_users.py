"""MCP tools for users operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_users_tools(mcp: FastMCP):
    @mcp.tool(tags={"users"})
    async def gitlab_users(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_user', 'create', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab users operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {"get", "get_user", "create", "update", "delete"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            return await run_blocking(client.get_users, **kwargs)
        if action == "get_user":
            return await run_blocking(client.get_user, **kwargs)
        if action == "create":
            return await run_blocking(client.create_user, **kwargs)
        if action == "update":
            return await run_blocking(client.update_user, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_user, **kwargs)
        raise ValueError(f"Unknown action: {action}")
