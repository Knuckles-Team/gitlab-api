"""MCP tools for jobs operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_jobs_tools(mcp: FastMCP):
    @mcp.tool(tags={"jobs"})
    async def gitlab_jobs(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_project_jobs', 'get_log', 'cancel', 'retry', 'erase', 'run', 'get_pipeline_jobs'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab jobs operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_project_jobs":
            return client.get_project_jobs(**kwargs)
        if action == "get_log":
            return client.get_project_job_log(**kwargs)
        if action == "cancel":
            return client.cancel_project_job(**kwargs)
        if action == "retry":
            return client.retry_project_job(**kwargs)
        if action == "erase":
            return client.erase_project_job(**kwargs)
        if action == "run":
            return client.run_project_job(**kwargs)
        if action == "get_pipeline_jobs":
            return client.get_pipeline_jobs(**kwargs)
        raise ValueError(f"Unknown action: {action}")
