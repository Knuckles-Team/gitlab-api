"""MCP tools for commits operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_commits_tools(mcp: FastMCP):
    @mcp.tool(tags={"commits"})
    async def gitlab_commits(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'diff', 'revert', 'get_comments', 'create_comment', 'get_discussions', 'get_statuses', 'post_status', 'get_merge_requests', 'get_gpg_signature'"
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

        if action == "get":
            if "commit_sha" in kwargs:
                return client.get_commit(**kwargs)
            return client.get_commits(**kwargs)
        if action == "create":
            return client.create_commit(**kwargs)
        if action == "diff":
            return client.get_commit_diff(**kwargs)
        if action == "revert":
            return client.revert_commit(**kwargs)
        if action == "get_comments":
            return client.get_commit_comments(**kwargs)
        if action == "create_comment":
            return client.create_commit_comment(**kwargs)
        if action == "get_discussions":
            return client.get_commit_discussions(**kwargs)
        if action == "get_statuses":
            return client.get_commit_statuses(**kwargs)
        if action == "post_status":
            return client.post_build_status_to_commit(**kwargs)
        if action == "get_merge_requests":
            return client.get_commit_merge_requests(**kwargs)
        if action == "get_gpg_signature":
            return client.get_commit_gpg_signature(**kwargs)
        raise ValueError(f"Unknown action: {action}")
