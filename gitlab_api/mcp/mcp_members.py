"""MCP tools for members operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_members_tools(mcp: FastMCP):
    @mcp.tool(tags={"members"})
    async def gitlab_members(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_group', 'get_project'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab members operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_group":
            return client.get_group_members(**kwargs)
        if action == "get_project":
            return client.get_project_members(**kwargs)
        raise ValueError(f"Unknown action: {action}")
