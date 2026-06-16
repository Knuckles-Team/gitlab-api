"""MCP tools for merge rules operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gitlab_api.auth import get_client


def register_merge_rules_tools(mcp: FastMCP):
    @mcp.tool(tags={"merge_rules"})
    async def gitlab_merge_rules(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_project_level', 'create_project_level', 'update_project_level', 'delete_project_level', 'get_mr_approvals', 'get_mr_approval_state', 'get_mr_level', 'approve_mr', 'unapprove_mr', 'get_group_level', 'edit_group_level', 'edit_project_level'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab merge rules operations."""
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
                "get_project_level",
                "create_project_level",
                "update_project_level",
                "delete_project_level",
                "get_mr_approvals",
                "get_mr_approval_state",
                "get_mr_level",
                "approve_mr",
                "unapprove_mr",
                "get_group_level",
                "edit_group_level",
                "edit_project_level",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_project_level":
            if "approval_rule_id" in kwargs:
                return client.get_project_level_merge_request_rule(**kwargs)
            return client.get_project_level_merge_request_rules(**kwargs)
        if action == "create_project_level":
            return client.create_project_level_rule(**kwargs)
        if action == "update_project_level":
            return client.update_project_level_rule(**kwargs)
        if action == "delete_project_level":
            return client.delete_project_level_rule(**kwargs)
        if action == "get_mr_approvals" or action == "get_mr_approval_state":
            return client.get_approval_state_merge_requests(**kwargs)
        if action == "get_mr_level":
            return client.get_merge_request_level_rules(**kwargs)
        if action == "approve_mr":
            return client.approve_merge_request(**kwargs)
        if action == "unapprove_mr":
            return client.unapprove_merge_request(**kwargs)
        if action == "get_group_level":
            return client.get_group_level_rule(**kwargs)
        if action == "edit_group_level":
            return client.edit_group_level_rule(**kwargs)
        if action == "edit_project_level":
            return client.edit_project_level_rule(**kwargs)
        raise ValueError(f"Unknown action: {action}")
