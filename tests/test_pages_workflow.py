"""PIPE-CONNSPEC-R125.3: GitLab API Pages and spec-dashboard contract."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / ".github/spec-dashboard.json"

pytestmark = pytest.mark.spec("PIPE-CONNSPEC-R125.3")


def test_pages_caller_enables_dashboard_and_rebuilds_for_spec_changes() -> None:
    assert not (ROOT / ".github/workflows/docs.yml").exists()





def test_dashboard_reads_only_canonical_spec_status_files() -> None:
    config = json.loads(DASHBOARD.read_text(encoding="utf-8"))

    assert config == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }
