"""MCP tools for labels operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_labels_tools(mcp: FastMCP):
    @mcp.tool(tags={"labels"})
    async def gitlab_labels(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage GitLab labels."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "create", "update", "delete"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "name" in kwargs or "label_id" in kwargs:
                return await run_blocking(client.get_label, **kwargs)
            return await run_blocking(client.get_labels, **kwargs)
        if action == "create":
            return await run_blocking(client.create_label, **kwargs)
        if action == "update":
            return await run_blocking(client.update_label, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_label, **kwargs)
        raise ValueError(f"Unknown action: {action}")
