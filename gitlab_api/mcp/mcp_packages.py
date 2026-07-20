"""MCP tools for packages operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_packages_tools(mcp: FastMCP):
    @mcp.tool(tags={"packages"})
    async def gitlab_packages(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'publish', 'download'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab packages operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "publish", "download"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            return await run_blocking(client.get_repository_packages, **kwargs)
        if action == "publish":
            return await run_blocking(client.publish_repository_package, **kwargs)
        if action == "download":
            return await run_blocking(client.download_repository_package, **kwargs)
        raise ValueError(f"Unknown action: {action}")
