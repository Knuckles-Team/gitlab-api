"""The packaged ingestible-source declaration (CONN-GITLAB-API-R001)."""

from __future__ import annotations


import pytest
from agent_connector_sdk.ingest import load_declaration
from agent_connector_sdk.mcp.method_tools import operation_annotations, operation_verb
from agent_connector_sdk.mcp.tool_surface import operation_prefix

from gitlab_api.api_client import Api


@pytest.mark.spec("CONN-GITLAB-API-R001")
def test_declares_ingestible_sources() -> None:
    declaration = load_declaration("gitlab_api")
    assert declaration is not None
    assert declaration.connector == "gitlab-mcp"
    source = declaration.source("projects")
    assert source is not None and source.record_type == "Project"
    prefix = operation_prefix("gitlab-api")
    assert source.tools == (f"{prefix}_get_projects",)
    # The engine admits a record only under the pack mapping of its type.
    assert source.record_type in load_declaration("gitlab_api").schema_mappings
    method = getattr(Api, "get_projects")
    annotations = operation_annotations("get_projects", operation_verb(method))
    assert annotations.read_only_hint is True


@pytest.mark.spec("CONN-GITLAB-API-R001")
def test_declares_issues_source() -> None:
    declaration = load_declaration("gitlab_api")
    assert declaration is not None
    assert declaration.connector == "gitlab-mcp"
    source = declaration.source("issues")
    assert source is not None and source.record_type == "Issue"
    prefix = operation_prefix("gitlab-api")
    assert source.tools == (f"{prefix}_get_issues",)
    assert source.record_type in load_declaration("gitlab_api").schema_mappings
    method = getattr(Api, "get_issues")
    annotations = operation_annotations("get_issues", operation_verb(method))
    assert annotations.read_only_hint is True
