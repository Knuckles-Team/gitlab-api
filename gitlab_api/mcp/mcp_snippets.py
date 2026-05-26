"""MCP tools for snippets operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_snippets_tools(mcp: FastMCP):
    @mcp.tool(tags={"snippets"})
    async def gitlab_snippets(
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
        """Manage GitLab snippets."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            if "snippet_id" in kwargs:
                return client.get_snippet(**kwargs)
            return client.get_snippets(**kwargs)
        if action == "create":
            return client.create_snippet(**kwargs)
        if action == "update":
            return client.update_snippet(**kwargs)
        if action == "delete":
            return client.delete_snippet(**kwargs)
        raise ValueError(f"Unknown action: {action}")
