"""MCP tools for merge requests operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_merge_requests_tools(mcp: FastMCP):
    @mcp.tool(tags={"merge_requests"})
    async def gitlab_merge_requests(
        action: str = Field(
            description="Action to perform. Must be one of: 'create', 'get', 'get_project', 'accept', 'cancel_auto_merge'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab merge requests operations."""
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
            {"create", "get", "get_project", "accept", "cancel_auto_merge"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "create":
            return await run_blocking(client.create_merge_request, **kwargs)
        if action == "get":
            if "merge_request_iid" in kwargs:
                return await run_blocking(client.get_project_merge_request, **kwargs)
            return await run_blocking(client.get_merge_requests, **kwargs)
        if action == "get_project":
            return await run_blocking(client.get_project_merge_requests, **kwargs)
        if action == "accept":
            return await run_blocking(client.accept_merge_request, **kwargs)
        if action == "cancel_auto_merge":
            return await run_blocking(
                client.cancel_merge_when_pipeline_succeeds, **kwargs
            )
        raise ValueError(f"Unknown action: {action}")
