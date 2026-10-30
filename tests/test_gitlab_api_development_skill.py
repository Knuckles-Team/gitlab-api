"""PIPE-CONNSPEC-R125.4: the GitLab API development skill is packaged."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "gitlab_api" / "skills" / "gitlab-api-development" / "SKILL.md"

pytestmark = pytest.mark.spec("PIPE-CONNSPEC-R125.4")


def test_development_skill_has_rapid_contract_and_package_binding() -> None:
    text = SKILL.read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert SKILL.is_file()
    assert re.search(r"^name:\s*gitlab-api-development\s*$", frontmatter, re.M)
    assert re.search(r"^skill_type:\s*skill\s*$", frontmatter, re.M)
    assert "## Rapid delivery: the 5-minute contract" in text
    for term in (
        "gitlab_api/__init__.py",
        "gitlab_api/api_client.py",
        "gitlab_api/api/",
        "gitlab_api/auth.py",
        "gitlab_api/instances.py",
        "gitlab_api/mcp_server.py",
        "gitlab_api/gitlab_gql.py",
        "gitlab_api/kg_ingest.py",
        "gitlab_api/connector_sources.py",
        "GITLAB_URL",
        "GITLAB_TOKEN",
        "GITLAB_TLS_PROFILE",
        "GITLAB_INSTANCES",
        "ENABLE_DELEGATION",
        "MCP_TOOL_MODE",
        "skills/**",
        "ontology/**",
        "uv run --locked --extra test pytest",
    ):
        assert term in text

    assert "verify=False" not in text
    assert "--no-verify" not in text
    package_data = project["tool"]["setuptools"]["package-data"]["gitlab_api"]
    assert "skills/**" in package_data
    assert project["project"]["entry-points"]["scion_sdk.connector"] == {
        "gitlab-mcp": "gitlab_api:connector"
    }
