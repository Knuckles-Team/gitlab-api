"""MCP tools for tags operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_tags_tools(mcp: FastMCP):
    @mcp.tool(tags={"tags"})
    async def gitlab_tags(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'delete', 'get_protected', 'get_protected_tag', 'protect', 'unprotect'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab tags operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            if "tag" in kwargs or "tag_name" in kwargs:
                return client.get_tag(**kwargs)
            return client.get_tags(**kwargs)
        if action == "create":
            return client.create_tag(**kwargs)
        if action == "delete":
            return client.delete_tag(**kwargs)
        if action == "get_protected":
            return client.get_protected_tags(**kwargs)
        if action == "get_protected_tag":
            return client.get_protected_tag(**kwargs)
        if action == "protect":
            return client.protect_tag(**kwargs)
        if action == "unprotect":
            return client.unprotect_tag(**kwargs)
        raise ValueError(f"Unknown action: {action}")
