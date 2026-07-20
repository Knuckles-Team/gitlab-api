"""Multi-tenant GitLab instance registry.

The single source of truth for *which* GitLab instances exist is the
agent-utilities XDG config (`~/.config/agent-utilities/config.json`,
`gitlab_instances`) — the same list the KG GitLab indexer reads — so one config
drives both code/metadata indexing AND every `gitlab-api` client/MCP call. When
no instances are configured it falls back to the single-host `GITLAB_URL` /
`GITLAB_TOKEN` env the connector has always used.

`get_client(instance="<name>")` (auth.py) resolves a configured instance by
name; a bare URL is also accepted, and an unset instance resolves to
the default (first configured, else `GITLAB_URL`).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse

from agent_utilities.base_utilities import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class GitLabInstance:
    """Connection facts for one GitLab tenant."""

    name: str
    url: str
    token: str = ""
    tls_profile_name: str | None = None


def _host_slug(url: str) -> str:
    return (urlparse(url).netloc or url).lower()


def _from_shared_config() -> list[GitLabInstance]:
    """Read the structured `gitlab_instances` list from the agent-utilities config."""
    try:
        from agent_utilities.core.config import config

        raw = getattr(config, "gitlab_instances", None) or []
    except Exception:  # noqa: BLE001 - config optional; fall back to env
        return []
    out: list[GitLabInstance] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        url = str(item.get("url", "")).strip()
        if not url:
            continue
        out.append(
            GitLabInstance(
                name=str(item.get("name") or _host_slug(url)),
                url=url,
                token=str(item.get("token", "")),
                tls_profile_name=(
                    str(item["tls_profile"]).strip()
                    if item.get("tls_profile")
                    else None
                ),
            )
        )
    return out


def _single_host_fallback() -> list[GitLabInstance]:
    """The legacy single-host instance from GITLAB_URL / GITLAB_TOKEN, if a token is set."""
    url = os.getenv("GITLAB_URL", "https://gitlab.com")
    token = os.getenv("GITLAB_TOKEN")
    if not token:
        return []
    return [
        GitLabInstance(
            name=_host_slug(url),
            url=url,
            token=token,
            tls_profile_name=os.getenv("GITLAB_TLS_PROFILE") or None,
        )
    ]


def list_configured_instances() -> list[GitLabInstance]:
    """Every configured GitLab instance (shared config first, else single-host env)."""
    return _from_shared_config() or _single_host_fallback()


def get_instance(name: str | None = None) -> GitLabInstance | None:
    """Resolve one instance by name, or the default (first configured) when ``name`` is None."""
    instances = list_configured_instances()
    if not instances:
        return None
    if name is None:
        return instances[0]
    for inst in instances:
        if inst.name == name:
            return inst
    return None


def instance_summaries() -> list[dict[str, object]]:
    """Tenant list for discovery — names/URLs/profile state only, never tokens."""
    return [
        {
            "name": i.name,
            "url": i.url,
            "tls_profile_configured": bool(i.tls_profile_name),
            "has_token": bool(i.token),
        }
        for i in list_configured_instances()
    ]
