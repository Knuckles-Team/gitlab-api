"""Optional kwargs are optional, GraphQL failures explain themselves, calls time out."""

from unittest.mock import patch

import pytest
from pydantic import BaseModel
from scion_sdk.connector import build_server

import gitlab_api.gitlab_input_models as input_models
from gitlab_api.api import api_client_base
from gitlab_api.gitlab_gql import GraphQL
from gitlab_api.mcp_server import _graphql_failure


def _is_optional(schema: dict) -> bool:
    return any(b.get("type") == "null" for b in schema.get("anyOf", []))


def test_no_input_model_requires_an_optional_field():
    bad = [
        f"{cls.__name__}.{name}"
        for cls in vars(input_models).values()
        if isinstance(cls, type)
        and issubclass(cls, BaseModel)
        and cls.__module__ == input_models.__name__
        for name, field in cls.model_fields.items()
        if field.is_required() and "None" in str(field.annotation)
    ]
    assert bad == []


@pytest.mark.asyncio
async def test_no_tool_schema_requires_an_optional_field():
    with patch("sys.argv", ["gitlab-mcp"]):
        _, mcp = build_server("gitlab_api", command_args=[])
        tools = await mcp.list_tools()
    bad = [
        f"{t.name}.{r}"
        for t in tools
        for r in (t.parameters or {}).get("required", [])
        if _is_optional(t.parameters["properties"].get(r, {}))
    ]
    assert bad == []
    mr = next(t for t in tools if t.name == "gitlab_get_project_merge_request")
    assert "title" not in mr.parameters.get("required", [])


def test_graphql_failure_names_message_and_expected_kwargs():
    method = getattr(GraphQL.update_merge_request, "__wrapped__", None)
    try:
        method(None, iid=1, projectId="x")
    except TypeError as exc:
        out = _graphql_failure(
            "update_merge_request",
            method,
            exc,
            type("C", (), {"token": "s3cr3t-token"})(),
        )
    assert "unexpected keyword argument" in out["error"]
    assert "project_id" in out["expected_params"]
    assert "merge_request_iid" in out["expected_params"]


def test_graphql_failure_redacts_the_token():
    out = _graphql_failure(
        "x",
        lambda: None,
        RuntimeError("boom Bearer abcdef0123456789 s3cr3t-token"),
        type("C", (), {"token": "s3cr3t-token"})(),
    )
    assert "s3cr3t-token" not in out["error"]
    assert "boom" in out["error"]


def test_rest_session_applies_a_default_timeout(monkeypatch):
    monkeypatch.setenv("GITLAB_REQUEST_TIMEOUT", "7")
    seen = {}

    def fake(self, *a, **kw):
        seen.update(kw)

    with patch("requests.Session.request", fake):
        api_client_base._TimeoutSession().request("GET", "http://x")
        assert seen["timeout"] == 7.0
        api_client_base._TimeoutSession().request("GET", "http://x", timeout=3)
        assert seen["timeout"] == 3


def test_timeout_falls_back_on_bad_value(monkeypatch):
    monkeypatch.setenv("GITLAB_REQUEST_TIMEOUT", "-1")
    assert api_client_base.request_timeout() == api_client_base.DEFAULT_REQUEST_TIMEOUT
