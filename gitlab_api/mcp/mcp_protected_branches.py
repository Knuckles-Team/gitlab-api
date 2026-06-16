"""MCP tools for protected branches operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_protected_branches_tools(mcp: FastMCP):
    @mcp.tool(tags={"protected_branches"})
    async def gitlab_protected_branches(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'protect', 'unprotect'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab protected branches operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "protect", "unprotect"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "branch" in kwargs:
                return client.get_protected_branch(**kwargs)
            return client.get_protected_branches(**kwargs)
        if action == "protect":
            return client.protect_branch(**kwargs)
        if action == "unprotect":
            return client.unprotect_branch(**kwargs)
        raise ValueError(f"Unknown action: {action}")
