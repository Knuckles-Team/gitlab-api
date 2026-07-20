"""MCP tools for graphql operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field


def register_graphql_tools(mcp: FastMCP):
    from gitlab_api.auth import get_graphql_client

    @mcp.tool(tags={"graphql"})
    async def gitlab_graphql(
        query: str = Field(
            description="The raw GraphQL query or mutation string to execute against the GitLab API."
        ),
        variables: str = Field(
            default="{}",
            description="JSON string of variables to pass along with the query.",
        ),
        operation_name: str | None = Field(
            default=None,
            description="Optional operation name if executing a specific query within the document.",
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute raw GraphQL queries and mutations natively on GitLab."""
        if ctx:
            await ctx.info("Executing GitLab GraphQL query...")
        import json

        try:
            vars_dict = json.loads(variables) if variables else None
        except Exception as e:
            return {"error": "Operation failed"}

        try:
            return await run_blocking(
                client.execute_gql,
                query_str=query,
                variables=vars_dict,
                operation_name=operation_name,
            )
        except Exception as e:
            return {"error": f"GraphQL execution failed: {type(e).__name__}"}

    @mcp.tool(tags={"graphql"})
    async def gitlab_discover_graphql_schema(
        type_name: str | None = Field(
            default=None,
            description="Optional specific GraphQL type name to inspect details for (e.g., 'Project', 'Issue'). If omitted, lists all available types in the schema.",
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Discover the dynamic GitLab GraphQL schema including types, fields, and custom attributes in real-time."""
        from agent_utilities.mcp.context_helpers import (
            ctx_graphql_get_type_details,
            ctx_graphql_list_types,
        )

        if ctx:
            await ctx.info("Retrieving dynamic GitLab GraphQL schema...")

        # Safe wrapper to call execute_gql
        async def execute_fn(q, variables=None):
            return await run_blocking(
                client.execute_gql, query_str=q, variables=variables
            )

        try:
            if type_name:
                return await ctx_graphql_get_type_details(execute_fn, type_name)
            return await ctx_graphql_list_types(execute_fn)
        except Exception as e:
            return {"error": "Failed to discover GitLab GraphQL schema"}
