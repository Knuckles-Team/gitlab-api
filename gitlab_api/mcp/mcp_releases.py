"""MCP tools for releases operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_releases_tools(mcp: FastMCP):
    @mcp.tool(tags={"releases"})
    async def gitlab_releases(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_latest', 'get_latest_evidence', 'get_latest_asset', 'get_group_releases', 'download_asset', 'get_by_tag', 'create', 'create_evidence', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab releases operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            if "tag_name" in kwargs:
                return client.get_release_by_tag(**kwargs)
            return client.get_releases(**kwargs)
        if action == "get_latest":
            return client.get_latest_release(**kwargs)
        if action == "get_latest_evidence":
            return client.get_latest_release_evidence(**kwargs)
        if action == "get_latest_asset":
            return client.get_latest_release_asset(**kwargs)
        if action == "get_group_releases":
            return client.get_group_releases(**kwargs)
        if action == "download_asset":
            return client.download_release_asset(**kwargs)
        if action == "get_by_tag":
            return client.get_release_by_tag(**kwargs)
        if action == "create":
            return client.create_release(**kwargs)
        if action == "create_evidence":
            return client.create_release_evidence(**kwargs)
        if action == "update":
            return client.update_release(**kwargs)
        if action == "delete":
            return client.delete_release(**kwargs)
        raise ValueError(f"Unknown action: {action}")
