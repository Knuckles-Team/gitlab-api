"""MCP tools for branches operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_branches_tools(mcp: FastMCP):
    @mcp.tool(tags={"branches"})
    async def gitlab_branches(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'delete', 'delete_merged'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab branches operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "create", "delete", "delete_merged"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "branch" in kwargs:
                return await run_blocking(client.get_branch, **kwargs)
            return await run_blocking(client.get_branches, **kwargs)
        if action == "create":
            return await run_blocking(client.create_branch, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_branch, **kwargs)
        if action == "delete_merged":
            return await run_blocking(client.delete_merged_branches, **kwargs)
        raise ValueError(f"Unknown action: {action}")
