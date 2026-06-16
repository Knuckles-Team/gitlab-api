"""MCP tools for custom api operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_custom_api_tools(mcp: FastMCP):
    @mcp.tool(tags={"custom-api"})
    async def api_request(
        method: str = Field(
            description="HTTP method to use (e.g. GET, POST, PUT, DELETE, PATCH)"
        ),
        endpoint: str = Field(
            description="The API endpoint path (e.g., /projects/1/issues)"
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of query parameters or body payload to pass to the request.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute arbitrary GitLab REST API requests directly."""
        if ctx:
            await ctx.info("Executing custom API request...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return await run_blocking(
            client.api_request, method=method, endpoint=endpoint, **kwargs
        )
