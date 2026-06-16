"""MCP tools for epics operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_epics_tools(mcp: FastMCP):
    @mcp.tool(tags={"epics"})
    async def gitlab_epics(
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
        """Manage GitLab epics."""
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
            if "epic_iid" in kwargs or "epic_id" in kwargs:
                return await run_blocking(client.get_epic, **kwargs)
            return await run_blocking(client.get_epics, **kwargs)
        if action == "create":
            return await run_blocking(client.create_epic, **kwargs)
        if action == "update":
            return await run_blocking(client.update_epic, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_epic, **kwargs)
        raise ValueError(f"Unknown action: {action}")
