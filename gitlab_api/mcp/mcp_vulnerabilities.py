"""MCP tools for vulnerabilities operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_vulnerabilities_tools(mcp: FastMCP):
    @mcp.tool(tags={"vulnerabilities"})
    async def gitlab_vulnerabilities(
        action: str = Field(
            description="Action to perform. Must be one of: 'dependencies', 'get_project', 'get_group', 'get'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Review a project's dependency list and security vulnerabilities (the GitLab counterpart to GitHub Dependabot)."""
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
            {"dependencies", "get_project", "get_group", "get"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "dependencies":
            return await run_blocking(client.get_project_dependencies, **kwargs)
        if action == "get_project":
            return await run_blocking(client.get_project_vulnerabilities, **kwargs)
        if action == "get_group":
            return await run_blocking(client.get_group_vulnerabilities, **kwargs)
        if action == "get":
            return await run_blocking(client.get_vulnerability, **kwargs)
        raise ValueError(f"Unknown action: {action}")
