"""MCP tools for projects operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(tags={"projects"})
    async def gitlab_projects(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'delete', 'archive', 'unarchive', 'get_nested_by_group', 'get_contributors', 'get_statistics', 'edit', 'share_with_group', 'unshare_with_group', 'get_project_groups'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab projects operations."""
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
                "delete",
                "archive",
                "unarchive",
                "get_nested_by_group",
                "get_contributors",
                "get_statistics",
                "edit",
                "share_with_group",
                "unshare_with_group",
                "get_project_groups",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "project_id" in kwargs or "id" in kwargs:
                return await run_blocking(client.get_project, **kwargs)
            return await run_blocking(client.get_projects, **kwargs)
        if action == "create":
            return await run_blocking(client.create_project, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_project, **kwargs)
        if action == "archive":
            return await run_blocking(client.archive_project, **kwargs)
        if action == "unarchive":
            return await run_blocking(client.unarchive_project, **kwargs)
        if action == "get_nested_by_group":
            return await run_blocking(client.get_nested_projects_by_group, **kwargs)
        if action == "get_contributors":
            return await run_blocking(client.get_project_contributors, **kwargs)
        if action == "get_statistics":
            return await run_blocking(client.get_project_statistics, **kwargs)
        if action == "edit":
            return await run_blocking(client.edit_project, **kwargs)
        if action == "share_with_group":
            return await run_blocking(client.share_project, **kwargs)
        if action == "unshare_with_group":
            return await run_blocking(client.delete_shared_project_link, **kwargs)
        if action == "get_project_groups":
            return await run_blocking(client.get_project_groups, **kwargs)
        raise ValueError(f"Unknown action: {action}")
