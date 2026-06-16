"""MCP tools for milestones operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_milestones_tools(mcp: FastMCP):
    @mcp.tool(tags={"milestones"})
    async def gitlab_milestones(
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
        """Manage GitLab milestones."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "create", "update", "delete"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "milestone_id" in kwargs:
                return client.get_milestone(**kwargs)
            return client.get_milestones(**kwargs)
        if action == "create":
            return client.create_milestone(**kwargs)
        if action == "update":
            return client.update_milestone(**kwargs)
        if action == "delete":
            return client.delete_milestone(**kwargs)
        raise ValueError(f"Unknown action: {action}")
