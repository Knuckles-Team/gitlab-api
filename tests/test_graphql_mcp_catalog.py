import inspect
from unittest.mock import MagicMock

import pytest

from gitlab_api.gitlab_gql import GraphQL
from gitlab_api.mcp_server import (
    _GRAPHQL_OPS_EXCLUSION_CATEGORIES,
    _graphql_operation_names,
    get_mcp_instance,
)


def test_graphql_operation_exclusion_contract_is_applied():
    excluded = set().union(*_GRAPHQL_OPS_EXCLUSION_CATEGORIES.values())
    operations = set(_graphql_operation_names(GraphQL))

    assert excluded == {
        "get_deploy_tokens",
        "create_deploy_token",
        "delete_deploy_token",
        "upload_wiki_page_attachment",
        "close",
    }
    assert operations.isdisjoint(excluded)
    assert "execute_gql" not in operations
    assert {"get_projects", "get_merge_requests"}.issubset(operations)


@pytest.mark.asyncio
async def test_graphql_ops_tool_uses_filtered_catalog(monkeypatch):
    monkeypatch.setenv("MCP_TOOL_MODE", "condensed")
    monkeypatch.setenv("GRAPHQL_OPSTOOL", "true")
    mcp, *_ = get_mcp_instance()
    tools = (
        await mcp.list_tools()
        if inspect.iscoroutinefunction(mcp.list_tools)
        else mcp.list_tools()
    )
    tool = next(tool for tool in tools if tool.name == "gitlab_graphql_ops")
    client = MagicMock(spec=GraphQL)

    discovery = await tool.fn(
        action="list_actions", params_json="{}", client=client, ctx=None
    )

    assert discovery["actions"] == sorted(_graphql_operation_names(GraphQL))
    for excluded in set().union(*_GRAPHQL_OPS_EXCLUSION_CATEGORIES.values()):
        with pytest.raises(ValueError, match="Unknown action"):
            await tool.fn(action=excluded, params_json="{}", client=client, ctx=None)


@pytest.mark.asyncio
async def test_graphql_ops_preserves_typed_rest_fallback_guidance(monkeypatch):
    monkeypatch.setenv("MCP_TOOL_MODE", "condensed")
    monkeypatch.setenv("GRAPHQL_OPSTOOL", "true")
    mcp, *_ = get_mcp_instance()
    tools = await mcp.list_tools()
    tool = next(tool for tool in tools if tool.name == "gitlab_graphql_ops")
    client = object.__new__(GraphQL)
    client.headers = {"Authorization": "Bearer test"}

    result = await tool.fn(
        action="get_commits",
        params_json='{"project_id":"group/project","path":"src/app.py"}',
        client=client,
        ctx=None,
    )

    assert result == {
        "error": "GitLab GraphQL does not support `path`; use the GitLab REST API instead."
    }
