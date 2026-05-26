"""MCP tools for pipeline schedules operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_pipeline_schedules_tools(mcp: FastMCP):
    @mcp.tool(tags={"pipeline_schedules"})
    async def gitlab_pipeline_schedules(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_all', 'get', 'get_triggered', 'create', 'edit', 'take_ownership', 'delete', 'run', 'create_variable', 'delete_variable'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab pipeline schedules operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_all":
            return client.get_pipeline_schedules(**kwargs)
        if action == "get":
            return client.get_pipeline_schedule(**kwargs)
        if action == "get_triggered":
            return client.get_pipelines_triggered_from_schedule(**kwargs)
        if action == "create":
            return client.create_pipeline_schedule(**kwargs)
        if action == "edit":
            return client.edit_pipeline_schedule(**kwargs)
        if action == "take_ownership":
            return client.take_pipeline_schedule_ownership(**kwargs)
        if action == "delete":
            return client.delete_pipeline_schedule(**kwargs)
        if action == "run":
            return client.run_pipeline_schedule(**kwargs)
        if action == "create_variable":
            return client.create_pipeline_schedule_variable(**kwargs)
        if action == "delete_variable":
            return client.delete_pipeline_schedule_variable(**kwargs)
        raise ValueError(f"Unknown action: {action}")
