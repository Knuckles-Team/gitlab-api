"""MCP tools for issues operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_issues_tools(mcp: FastMCP):
    @mcp.tool(tags={"issues"})
    async def gitlab_issues(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete', 'get_group'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage GitLab issues."""
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
            {"get", "create", "update", "delete", "get_group"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "issue_iid" in kwargs or "issue_id" in kwargs:
                return await run_blocking(client.get_issue, **kwargs)
            return await run_blocking(client.get_issues, **kwargs)
        if action == "create":
            return await run_blocking(client.create_issue, **kwargs)
        if action == "update":
            return await run_blocking(client.update_issue, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_issue, **kwargs)
        if action == "get_group":
            return await run_blocking(client.get_group_issues, **kwargs)
        raise ValueError(f"Unknown action: {action}")
