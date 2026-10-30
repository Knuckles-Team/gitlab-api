"""MCP_TOOL_MODE: condensed surface (ECO-4.82)."""

from unittest.mock import patch

import pytest

from scion_sdk.connector import build_server


async def _names(monkeypatch, mode):
    if mode is None:
        monkeypatch.delenv("MCP_TOOL_MODE", raising=False)
    else:
        monkeypatch.setenv("MCP_TOOL_MODE", mode)
    with patch("sys.argv", ["gitlab-mcp"]):
        _, mcp = build_server("gitlab_api", command_args=[])
        return {t.name for t in await mcp.list_tools()}


@pytest.mark.asyncio
async def test_condensed_default(monkeypatch):
    names = await _names(monkeypatch, None)
    assert "gitlab_get_branches" in names  # one tool per operation
    assert "gitlab_branches" not in names  # action-routed tool retired
