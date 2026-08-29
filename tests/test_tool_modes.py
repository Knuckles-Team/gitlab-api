"""MCP_TOOL_MODE registration and visibility-gating surfaces (ECO-4.82)."""

from unittest.mock import patch

import pytest

from gitlab_api.mcp_server import get_mcp_instance


async def _tools(monkeypatch, mode):
    if mode is None:
        monkeypatch.delenv("MCP_TOOL_MODE", raising=False)
    else:
        monkeypatch.setenv("MCP_TOOL_MODE", mode)
    with patch("sys.argv", ["gitlab-mcp"]):
        mcp, *_ = get_mcp_instance()
        return {tool.name: tool for tool in await mcp.list_tools()}


@pytest.mark.asyncio
async def test_intent_registers_and_gates_condensed_dispatch(monkeypatch):
    tools = await _tools(monkeypatch, "intent")
    assert "gitlab_branches" in tools
    assert "gated" in tools["gitlab_branches"].tags
    assert "gitlab_get_branches" not in tools


@pytest.mark.asyncio
async def test_verbose(monkeypatch):
    tools = await _tools(monkeypatch, "verbose")
    assert "gitlab_branches" in tools
    assert "gated" in tools["gitlab_branches"].tags
    # one 1:1 tool per public Api method
    from gitlab_api.api_client import Api

    assert callable(getattr(Api, "get_branches", None))
    assert "gitlab_get_branches" in tools


@pytest.mark.asyncio
async def test_both_is_union(monkeypatch):
    tools = await _tools(monkeypatch, "both")
    assert "gitlab_branches" in tools
    assert "gated" not in tools["gitlab_branches"].tags
    assert "gitlab_get_branches" in tools
