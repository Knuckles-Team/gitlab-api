"""Identity-scoped GitLab tenant auto-load (CONCEPT:AU-OS.identity.identity-scoped-resource-autoload).

The caller's entitled GitLab instances auto-load; a non-entitled named instance
is denied; the default falls to the first entitled when the first-configured
instance is off-limits. Tests the resolution/enforcement logic with the
entitlement source mocked (the resolver itself is tested in agent-utilities).
"""

from types import SimpleNamespace

import pytest

from gitlab_api import instances


def _setup(monkeypatch, entitled):
    monkeypatch.setattr(
        "agent_utilities.core.config.config",
        SimpleNamespace(
            gitlab_instances=[
                {"name": "prod", "url": "https://gl.acme.io", "token": "t1"},
                {"name": "dev", "url": "https://gl-dev.acme.io", "token": "t2"},
            ]
        ),
        raising=False,
    )
    monkeypatch.setattr(
        instances, "_entitled", lambda namespace, names: [n for n in names if n in entitled]
    )


def test_instance_summaries_filters_to_entitled(monkeypatch):
    _setup(monkeypatch, {"prod"})
    names = {s["name"] for s in instances.instance_summaries()}
    assert names == {"prod"}


def test_auto_selects_entitled_default(monkeypatch):
    # default = first configured ("prod")
    _setup(monkeypatch, {"prod"})
    assert instances.get_instance(None).name == "prod"


def test_default_not_entitled_falls_to_first_entitled(monkeypatch):
    _setup(monkeypatch, {"dev"})
    assert instances.get_instance(None).name == "dev"


def test_named_instance_not_entitled_is_denied(monkeypatch):
    _setup(monkeypatch, {"prod"})
    with pytest.raises(PermissionError):
        instances.get_instance("dev")


def test_named_entitled_instance_allowed(monkeypatch):
    _setup(monkeypatch, {"prod", "dev"})
    assert instances.get_instance("dev").name == "dev"


def test_no_entitled_instances_returns_none(monkeypatch):
    _setup(monkeypatch, set())
    assert instances.get_instance(None) is None


def test_unknown_instance_name_returns_none(monkeypatch):
    _setup(monkeypatch, {"prod"})
    assert instances.get_instance("ghost") is None
