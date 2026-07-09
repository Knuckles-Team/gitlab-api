"""MCP tools for commits operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_commits_tools(mcp: FastMCP):
    @mcp.tool(tags={"commits"})
    async def gitlab_commits(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'diff', 'revert', 'get_comments', 'create_comment', 'get_discussions', 'get_statuses', 'post_status', 'get_merge_requests', 'get_gpg_signature', 'cherry_pick', 'get_references'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab commits operations."""
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
                "diff",
                "revert",
                "get_comments",
                "create_comment",
                "get_discussions",
                "get_statuses",
                "post_status",
                "get_merge_requests",
                "get_gpg_signature",
                "cherry_pick",
                "get_references",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "commit_sha" in kwargs:
                return await run_blocking(client.get_commit, **kwargs)
            return await run_blocking(client.get_commits, **kwargs)
        if action == "create":
            return await run_blocking(client.create_commit, **kwargs)
        if action == "diff":
            return await run_blocking(client.get_commit_diff, **kwargs)
        if action == "revert":
            return await run_blocking(client.revert_commit, **kwargs)
        if action == "get_comments":
            return await run_blocking(client.get_commit_comments, **kwargs)
        if action == "create_comment":
            return await run_blocking(client.create_commit_comment, **kwargs)
        if action == "get_discussions":
            return await run_blocking(client.get_commit_discussions, **kwargs)
        if action == "get_statuses":
            return await run_blocking(client.get_commit_statuses, **kwargs)
        if action == "post_status":
            return await run_blocking(client.post_build_status_to_commit, **kwargs)
        if action == "get_merge_requests":
            return await run_blocking(client.get_commit_merge_requests, **kwargs)
        if action == "get_gpg_signature":
            return await run_blocking(client.get_commit_gpg_signature, **kwargs)
        if action == "cherry_pick":
            return await run_blocking(client.cherry_pick_commit, **kwargs)
        if action == "get_references":
            return await run_blocking(client.get_commit_references, **kwargs)
        raise ValueError(f"Unknown action: {action}")
