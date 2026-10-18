"""The packaged ingestible-source declaration (CONN-GITLAB-API-R001)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from agent_connector_sdk.ingest.sources import load_ingest_sources
from agent_connector_sdk.mcp.method_tools import operation_annotations, operation_verb
from agent_connector_sdk.mcp.tool_surface import operation_prefix

import gitlab_api
from gitlab_api.api_client import Api


@pytest.mark.spec("CONN-GITLAB-API-R001")
def test_declares_ingestible_sources() -> None:
    declaration = load_ingest_sources(Path(gitlab_api.__file__).parent)
    assert declaration is not None
    assert declaration.connector == "gitlab-api"
    source = declaration.source("projects")
    assert source is not None and source.record_type == "Project"
    prefix = operation_prefix("gitlab-api")
    assert source.tools == (f"{prefix}_get_projects",)
    # The engine admits a record only under the pack mapping of its type.
    manifest = yaml.safe_load(
        (Path(gitlab_api.__file__).parent / "connector_manifest.yml").read_text(
            "utf-8"
        )
    )
    assert source.record_type in manifest["schema_mappings"]
    method = getattr(Api, "get_projects")
    annotations = operation_annotations("get_projects", operation_verb(method))
    assert annotations.read_only_hint is True
