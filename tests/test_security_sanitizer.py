"""The sanitizer's inline exemption marker is narrow (one justified line)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "security_sanitizer", Path(__file__).parents[1] / "scripts" / "security_sanitizer.py"
)
assert _SPEC is not None and _SPEC.loader is not None
sanitizer = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(sanitizer)

TOKEN = "glpat-" + "abcdefghijklmnopqrst"  # sanitizer:ignore - synthetic test token


def test_unmarked_secret_is_reported() -> None:
    line = f'token = "{TOKEN}"'
    assert sanitizer._secret_violations_in_line(line, Path("x.py"), 1)


def test_justified_marker_exempts_only_its_line() -> None:
    marked = f'token = "{TOKEN}"  # sanitizer:ignore - synthetic fixture'
    assert sanitizer._secret_violations_in_line(marked, Path("x.py"), 1) == []


def test_bare_marker_exempts_nothing() -> None:
    bare = f'token = "{TOKEN}"  # sanitizer:ignore'
    assert sanitizer._secret_violations_in_line(bare, Path("x.py"), 1)
