"""MCP tools for runners operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_runners_tools(mcp: FastMCP):
    @mcp.tool(tags={"runners"})
    async def gitlab_runners(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_all', 'update_details', 'pause', 'get_jobs', 'get_project', 'enable_project', 'delete_project', 'get_group', 'register', 'delete', 'verify_auth', 'reset_gitlab_token', 'reset_project_token', 'reset_group_token', 'reset_token'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab runners operations."""
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
                "get_all",
                "update_details",
                "pause",
                "get_jobs",
                "get_project",
                "enable_project",
                "delete_project",
                "get_group",
                "register",
                "delete",
                "verify_auth",
                "reset_gitlab_token",
                "reset_project_token",
                "reset_group_token",
                "reset_token",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_all":
            return client.get_runners(**kwargs)
        if action == "update_details":
            return client.update_runner_details(**kwargs)
        if action == "pause":
            return client.pause_runner(**kwargs)
        if action == "get_jobs":
            return client.get_runner_jobs(**kwargs)
        if action == "get_project":
            return client.get_project_runners(**kwargs)
        if action == "enable_project":
            return client.enable_project_runner(**kwargs)
        if action == "delete_project":
            return client.delete_project_runner(**kwargs)
        if action == "get_group":
            return client.get_group_runners(**kwargs)
        if action == "register":
            return client.register_new_runner(**kwargs)
        if action == "delete":
            return client.delete_runner(**kwargs)
        if action == "verify_auth":
            return client.verify_runner_authentication(**kwargs)
        if action == "reset_gitlab_token":
            return client.reset_gitlab_runner_token(**kwargs)
        if action == "reset_project_token":
            return client.reset_project_runner_token(**kwargs)
        if action == "reset_group_token":
            return client.reset_group_runner_token(**kwargs)
        if action == "reset_token":
            return client.reset_token(**kwargs)
        raise ValueError(f"Unknown action: {action}")
