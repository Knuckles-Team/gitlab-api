"""CONN-GITLAB-API-R002: the connector is filed under its fleet name, gitlab-mcp."""

from __future__ import annotations

import ast
import json
import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "gitlab_api"
FLEET = "gitlab-mcp"


def _call_connectors(path: Path) -> list[str]:
    names = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Call) and getattr(
            node.func, "id", getattr(node.func, "attr", "")
        ) in {
            "IngestBinding",
            "ConnectorContent",
        }:
            names += [
                str(k.value.value)
                for k in node.keywords
                if k.arg == "connector" and isinstance(k.value, ast.Constant)
            ]
    return names


@pytest.mark.spec("CONN-GITLAB-API-R002")
def test_connector_name_is_the_fleet_name() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["entry-points"]["agent_connector_sdk.connector"] == {
        FLEET: "gitlab_api"
    }
    manifest = (PACKAGE / "connector_manifest.yml").read_text(encoding="utf-8")
    match = re.search(r'^\s*"?connector"?\s*:\s*"?([^"\s,]+)', manifest, re.MULTILINE)
    assert match is not None and match.group(1) == FLEET
    fingerprints = PACKAGE / "connectors" / "tool_schema_fingerprints.json"
    if fingerprints.is_file():
        assert (
            json.loads(fingerprints.read_text(encoding="utf-8"))["connector"] == FLEET
        )
    for module in sorted(PACKAGE.glob("*.py")):
        assert all(name == FLEET for name in _call_connectors(module)), module.name
