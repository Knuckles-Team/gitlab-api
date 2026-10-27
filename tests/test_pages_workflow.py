"""PIPE-CONNSPEC-R125.3: GitLab API Pages and spec-dashboard contract."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/pages.yml"
DASHBOARD = ROOT / ".github/spec-dashboard.json"

pytestmark = pytest.mark.spec("PIPE-CONNSPEC-R125.3")


def test_pages_caller_enables_dashboard_and_rebuilds_for_spec_changes() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "uses: Knuckles-Team/pipelines/.github/workflows/pages_pipeline.yml@main" in workflow
    assert re.search(r"^      content_source: docs$", workflow, re.MULTILINE)
    assert re.search(r"^      spec_dashboard_enabled: true$", workflow, re.MULTILINE)
    assert re.search(
        r"^      spec_dashboard_config: \.github/spec-dashboard\.json$",
        workflow,
        re.MULTILINE,
    )
    assert re.search(r"^  workflow_dispatch: \{\}$", workflow, re.MULTILINE)
    for path in (
        "'docs/**'",
        "'mkdocs.yml'",
        "'README.md'",
        "'specs/**'",
        "'.github/spec-dashboard.json'",
        "'.github/workflows/pages.yml'",
    ):
        assert path in workflow

    assert re.search(r"(?m)^      pages: write$", workflow)
    assert re.search(r"(?m)^      id-token: write$", workflow)


def test_dashboard_reads_only_canonical_spec_status_files() -> None:
    config = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert config == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }
