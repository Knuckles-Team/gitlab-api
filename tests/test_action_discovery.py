"""Action-discovery standardization tests.

Verifies that action-routed tools expose `list_actions` discovery and raise a
rich did-you-mean error on unknown actions, via the shared agent-utilities
`resolve_action` helper wired into `mcp_server.py`.
"""

import inspect
from unittest.mock import MagicMock

import pytest

from gitlab_api.mcp_server import get_mcp_instance


async def _get_tool(name: str):
    mcp, _args, _mw, _tags = get_mcp_instance()
    tool_objs = (
        await mcp.list_tools()
        if inspect.iscoroutinefunction(mcp.list_tools)
        else mcp.list_tools()
    )
    for tool in tool_objs:
        if tool.name == name:
            return tool
    raise AssertionError(f"tool {name} not registered")


@pytest.mark.asyncio
async def test_list_actions_returns_names():
    tool = await _get_tool("gitlab_branches")
    result = await tool.fn(
        action="list_actions",
        params_json="{}",
        client=MagicMock(),
        ctx=None,
    )
    assert isinstance(result, dict)
    assert result["service"] == "gitlab-api"
    assert set(result["actions"]) == {"get", "create", "delete"}


@pytest.mark.asyncio
async def test_unknown_action_raises_with_list_actions_hint():
    tool = await _get_tool("gitlab_branches")
    with pytest.raises(ValueError) as excinfo:
        await tool.fn(
            action="creat",
            params_json="{}",
            client=MagicMock(),
            ctx=None,
        )
    message = str(excinfo.value)
    assert "list_actions" in message
    assert "create" in message  # did-you-mean suggestion


@pytest.mark.asyncio
async def test_canonical_action_still_dispatches():
    tool = await _get_tool("gitlab_branches")
    client = MagicMock()
    client.get_branches.return_value = {"ok": True}
    result = await tool.fn(
        action="get",
        params_json="{}",
        client=client,
        ctx=None,
    )
    assert result == {"ok": True}
    client.get_branches.assert_called_once()
