"""MCP tools for notes operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_notes_tools(mcp: FastMCP):
    @mcp.tool(tags={"notes"})
    async def gitlab_notes(
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
        """Manage GitLab notes/comments on issues, merge requests, commits, and epics."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            if "note_id" in kwargs:
                return client.get_note(**kwargs)
            return client.get_notes(**kwargs)
        if action == "create":
            return client.create_note(**kwargs)
        if action == "update":
            return client.update_note(**kwargs)
        if action == "delete":
            return client.delete_note(**kwargs)
        raise ValueError(f"Unknown action: {action}")
