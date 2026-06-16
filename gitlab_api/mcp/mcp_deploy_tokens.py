"""MCP tools for deploy tokens operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_deploy_tokens_tools(mcp: FastMCP):
    @mcp.tool(tags={"deploy_tokens"})
    async def gitlab_deploy_tokens(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_project', 'create_project', 'delete_project', 'get_group', 'create_group', 'delete_group'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab deploy tokens operations."""
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
                "get_project",
                "create_project",
                "delete_project",
                "get_group",
                "create_group",
                "delete_group",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "token_id" in kwargs and "project_id" in kwargs:
                return client.get_project_deploy_token(**kwargs)
            elif "token_id" in kwargs and "group_id" in kwargs:
                return client.get_group_deploy_token(**kwargs)
            return client.get_deploy_tokens(**kwargs)
        if action == "get_project":
            return client.get_project_deploy_tokens(**kwargs)
        if action == "create_project":
            return client.create_project_deploy_token(**kwargs)
        if action == "delete_project":
            return client.delete_project_deploy_token(**kwargs)
        if action == "get_group":
            return client.get_group_deploy_tokens(**kwargs)
        if action == "create_group":
            return client.create_group_deploy_token(**kwargs)
        if action == "delete_group":
            return client.delete_group_deploy_token(**kwargs)
        raise ValueError(f"Unknown action: {action}")
