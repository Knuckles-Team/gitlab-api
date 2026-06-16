"""MCP tools for environments operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_environments_tools(mcp: FastMCP):
    @mcp.tool(tags={"environments"})
    async def gitlab_environments(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete', 'stop', 'stop_stale', 'delete_stopped', 'get_protected', 'protect', 'update_protected', 'unprotect'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab environments operations."""
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
                "create",
                "update",
                "delete",
                "stop",
                "stop_stale",
                "delete_stopped",
                "get_protected",
                "protect",
                "update_protected",
                "unprotect",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "environment_id" in kwargs:
                return client.get_environment(**kwargs)
            return client.get_environments(**kwargs)
        if action == "create":
            return client.create_environment(**kwargs)
        if action == "update":
            return client.update_environment(**kwargs)
        if action == "delete":
            return client.delete_environment(**kwargs)
        if action == "stop":
            return client.stop_environment(**kwargs)
        if action == "stop_stale":
            return client.stop_stale_environments(**kwargs)
        if action == "delete_stopped":
            return client.delete_stopped_environments(**kwargs)
        if action == "get_protected":
            if "environment_name" in kwargs:
                return client.get_protected_environment(**kwargs)
            return client.get_protected_environments(**kwargs)
        if action == "protect":
            return client.protect_environment(**kwargs)
        if action == "update_protected":
            return client.update_protected_environment(**kwargs)
        if action == "unprotect":
            return client.unprotect_environment(**kwargs)
        raise ValueError(f"Unknown action: {action}")
