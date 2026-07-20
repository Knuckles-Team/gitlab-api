"""MCP tools for environments operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
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
            return {"error": "Operation failed"}

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
                return await run_blocking(client.get_environment, **kwargs)
            return await run_blocking(client.get_environments, **kwargs)
        if action == "create":
            return await run_blocking(client.create_environment, **kwargs)
        if action == "update":
            return await run_blocking(client.update_environment, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_environment, **kwargs)
        if action == "stop":
            return await run_blocking(client.stop_environment, **kwargs)
        if action == "stop_stale":
            return await run_blocking(client.stop_stale_environments, **kwargs)
        if action == "delete_stopped":
            return await run_blocking(client.delete_stopped_environments, **kwargs)
        if action == "get_protected":
            if "environment_name" in kwargs:
                return await run_blocking(client.get_protected_environment, **kwargs)
            return await run_blocking(client.get_protected_environments, **kwargs)
        if action == "protect":
            return await run_blocking(client.protect_environment, **kwargs)
        if action == "update_protected":
            return await run_blocking(client.update_protected_environment, **kwargs)
        if action == "unprotect":
            return await run_blocking(client.unprotect_environment, **kwargs)
        raise ValueError(f"Unknown action: {action}")
