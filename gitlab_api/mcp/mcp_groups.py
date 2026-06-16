"""MCP tools for groups operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_groups_tools(mcp: FastMCP):
    @mcp.tool(tags={"groups"})
    async def gitlab_groups(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'edit', 'get_subgroups', 'get_descendants', 'get_projects', 'get_merge_requests'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab groups operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get",
                "edit",
                "get_subgroups",
                "get_descendants",
                "get_projects",
                "get_merge_requests",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "group_id" in kwargs:
                return client.get_group(**kwargs)
            return client.get_groups(**kwargs)
        if action == "edit":
            return client.edit_group(**kwargs)
        if action == "get_subgroups":
            return client.get_group_subgroups(**kwargs)
        if action == "get_descendants":
            return client.get_group_descendant_groups(**kwargs)
        if action == "get_projects":
            return client.get_group_projects(**kwargs)
        if action == "get_merge_requests":
            return client.get_group_merge_requests(**kwargs)
        raise ValueError(f"Unknown action: {action}")
