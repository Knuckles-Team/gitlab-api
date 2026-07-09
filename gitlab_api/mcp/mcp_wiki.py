"""MCP tools for wiki operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_wiki_tools(mcp: FastMCP):
    @mcp.tool(tags={"wiki"})
    async def gitlab_wiki(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_list', 'get', 'create', 'update', 'delete', 'upload_attachment'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab wiki operations."""
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
            {"get_list", "get", "create", "update", "delete", "upload_attachment"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_list":
            return await run_blocking(client.get_wiki_list, **kwargs)
        if action == "get":
            return await run_blocking(client.get_wiki_page, **kwargs)
        if action == "create":
            return await run_blocking(client.create_wiki_page, **kwargs)
        if action == "update":
            return await run_blocking(client.update_wiki_page, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_wiki_page, **kwargs)
        if action == "upload_attachment":
            return await run_blocking(client.upload_wiki_page_attachment, **kwargs)
        raise ValueError(f"Unknown action: {action}")
