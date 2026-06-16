"""Multi-tenant GitLab instance registry + resolution (CONCEPT:KG-2.9g)."""

from types import SimpleNamespace

import pytest

from gitlab_api import instances
from gitlab_api.auth import _resolve_connection


def _patch_config(monkeypatch, gitlab_instances):
    """Point the registry at a fake agent-utilities config singleton."""
    monkeypatch.setattr(
        "agent_utilities.core.config.config",
        SimpleNamespace(gitlab_instances=gitlab_instances),
        raising=False,
    )


def test_list_from_shared_config(monkeypatch):
    _patch_config(
        monkeypatch,
        [
            {"name": "prod", "url": "https://gl.acme.io", "token": "t1", "verify_ssl": False},
            {"url": "https://gitlab.com", "token": "t2"},  # name → host slug
            {"name": "bad"},  # no url → skipped
        ],
    )
    insts = instances.list_configured_instances()
    assert [i.name for i in insts] == ["prod", "gitlab.com"]
    assert insts[0].url == "https://gl.acme.io" and insts[0].verify_ssl is False


def test_single_host_fallback(monkeypatch):
    _patch_config(monkeypatch, None)
    monkeypatch.setenv("GITLAB_URL", "https://gl.x")
    monkeypatch.setenv("GITLAB_TOKEN", "tok")
    insts = instances.list_configured_instances()
    assert len(insts) == 1 and insts[0].name == "gl.x" and insts[0].token == "tok"


def test_get_instance_by_name_and_default(monkeypatch):
    _patch_config(
        monkeypatch,
        [
            {"name": "a", "url": "https://a.io", "token": "ta"},
            {"name": "b", "url": "https://b.io", "token": "tb"},
        ],
    )
    assert instances.get_instance("b").url == "https://b.io"
    assert instances.get_instance(None).name == "a"  # default = first
    assert instances.get_instance("missing") is None


def test_summaries_never_expose_tokens(monkeypatch):
    _patch_config(monkeypatch, [{"name": "a", "url": "https://a.io", "token": "secret"}])
    summary = instances.instance_summaries()[0]
    assert summary == {"name": "a", "url": "https://a.io", "verify_ssl": True, "has_token": True}
    assert "token" not in summary


def test_resolve_connection_by_name(monkeypatch):
    _patch_config(
        monkeypatch, [{"name": "prod", "url": "https://gl.acme.io", "token": "t1", "verify_ssl": False}]
    )
    url, token, verify = _resolve_connection("prod", None, None)
    assert url == "https://gl.acme.io" and token == "t1" and verify is False


def test_resolve_connection_bare_url_passthrough(monkeypatch):
    _patch_config(monkeypatch, None)
    monkeypatch.setenv("GITLAB_TOKEN", "envtok")
    # A bare URL is used as-is and the caller owns the token (no env fallback):
    # explicit None stays None; an explicit token passes through.
    url, token, _ = _resolve_connection("https://explicit.io", None, None)
    assert url == "https://explicit.io" and token is None
    _, token2, _ = _resolve_connection("https://explicit.io", "given", None)
    assert token2 == "given"


def test_resolve_connection_default_uses_env_token(monkeypatch):
    # No instance + no config → legacy single-host env defaults (env token DOES apply).
    _patch_config(monkeypatch, None)
    monkeypatch.setenv("GITLAB_URL", "https://gl.env")
    monkeypatch.setenv("GITLAB_TOKEN", "envtok")
    url, token, _ = _resolve_connection(None, None, None)
    assert url == "https://gl.env" and token == "envtok"


def test_resolve_connection_explicit_token_wins(monkeypatch):
    _patch_config(monkeypatch, [{"name": "prod", "url": "https://gl.io", "token": "stored"}])
    _, token, _ = _resolve_connection("prod", "override", None)
    assert token == "override"


def test_resolve_connection_unknown_name_raises(monkeypatch):
    _patch_config(monkeypatch, [{"name": "prod", "url": "https://gl.io", "token": "t"}])
    with pytest.raises(RuntimeError, match="not configured"):
        _resolve_connection("nope", None, None)
