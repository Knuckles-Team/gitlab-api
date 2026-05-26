"""MCP tools for pipelines operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_pipelines_tools(mcp: FastMCP):
    @mcp.tool(tags={"pipelines"})
    async def gitlab_pipelines(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'run'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab pipelines operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get":
            if "pipeline_id" in kwargs:
                return client.get_pipeline(**kwargs)
            return client.get_pipelines(**kwargs)
        if action == "run":
            return client.run_pipeline(**kwargs)
        raise ValueError(f"Unknown action: {action}")
