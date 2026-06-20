"""MCP_TOOL_MODE: condensed (default) / verbose / both surfaces (ECO-4.82)."""

from unittest.mock import patch

import pytest

from gitlab_api.mcp_server import get_mcp_instance


async def _names(monkeypatch, mode):
    if mode is None:
        monkeypatch.delenv("MCP_TOOL_MODE", raising=False)
    else:
        monkeypatch.setenv("MCP_TOOL_MODE", mode)
    with patch("sys.argv", ["gitlab-mcp"]):
        mcp, *_ = get_mcp_instance()
        return {t.name for t in await mcp.list_tools()}


@pytest.mark.asyncio
async def test_condensed_default(monkeypatch):
    names = await _names(monkeypatch, None)
    assert "gitlab_branches" in names  # action-routed tool
    assert "gitlab_get_branches" not in names  # verbose absent


@pytest.mark.asyncio
async def test_verbose(monkeypatch):
    names = await _names(monkeypatch, "verbose")
    assert "gitlab_branches" not in names
    # one 1:1 tool per public Api method
    from gitlab_api.api_client import Api

    assert callable(getattr(Api, "get_branches", None))
    assert "gitlab_get_branches" in names


@pytest.mark.asyncio
async def test_both_is_union(monkeypatch):
    names = await _names(monkeypatch, "both")
    assert "gitlab_branches" in names
    assert "gitlab_get_branches" in names
