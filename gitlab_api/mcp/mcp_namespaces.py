"""MCP tools for namespaces operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_namespaces_tools(mcp: FastMCP):
    @mcp.tool(tags={"namespaces"})
    async def gitlab_namespaces(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_namespace'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab namespaces operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "get_namespace"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            return await run_blocking(client.get_namespaces, **kwargs)
        if action == "get_namespace":
            return await run_blocking(client.get_namespace, **kwargs)
        raise ValueError(f"Unknown action: {action}")
