"""MCP tools for graphql ops operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field


def register_graphql_ops_tools(mcp: FastMCP):
    from gitlab_api.auth import get_graphql_client
    from gitlab_api.gitlab_gql import GraphQL as _GitlabGraphQL

    #: Every typed operation on the GraphQL client (all methods except the raw
    #: execute_gql passthrough, which the gitlab_graphql tool already exposes).
    _GRAPHQL_OPS_ACTIONS = tuple(
        sorted(
            name
            for name, attr in vars(_GitlabGraphQL).items()
            if not name.startswith("_") and callable(attr) and name != "execute_gql"
        )
    )

    @mcp.tool(tags={"graphql_ops"})
    async def gitlab_graphql_ops(
        action: str = Field(
            description=(
                "Typed GraphQL operation to run (a method on the GitLab GraphQL "
                "client), e.g. 'get_merge_requests', 'update_merge_request', "
                "'delete_merge_request', 'accept_merge_request', 'retry_pipeline', "
                "'cancel_pipeline', 'create_pipeline', 'get_projects', 'get_job'."
            )
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Run a typed GitLab GraphQL operation by name.

        The GraphQL-native counterpart to the REST gitlab_<domain> tools — prefer it
        for GraphQL-only capabilities (merge-request update/delete, pipeline
        retry/cancel, member add/update/delete) and rich nested reads. Parameters in
        params_json are passed as keyword arguments to the named operation; a few
        operations that take a single typed model (e.g. get_project) build it from
        those same kwargs automatically.
        """
        if ctx:
            await ctx.info("Executing GitLab GraphQL operation...")
        import inspect
        import json

        from pydantic import BaseModel

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, set(_GRAPHQL_OPS_ACTIONS), service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        method = getattr(client, action)
        required = [
            p
            for p in inspect.signature(method).parameters.values()
            if p.default is inspect.Parameter.empty
            and p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
        ]
        try:
            if (
                len(required) == 1
                and isinstance(required[0].annotation, type)
                and issubclass(required[0].annotation, BaseModel)
            ):
                model = required[0].annotation(**kwargs)
                return await run_blocking(method, **{required[0].name: model})
            return await run_blocking(method, **kwargs)
        except Exception as e:
            return {"error": f"GraphQL operation '{action}' failed: {str(e)}"}
