#!/usr/bin/env python3
"""Run a repository tool with its local agent-utilities sibling available.

Real git worktrees live outside the workspace tree, so uv cannot infer the
editable ``agent-utilities`` source declared in ``pyproject.toml``. This
wrapper resolves that source and its certified ``epistemic_graph.numeric``
kernel from the shared git directory (or the explicit ``AGENT_UTILITIES_ROOT``
override), maintains the ignored sibling symlink, and then replaces itself
with the requested command. It never downloads packages or falls back to a
published dependency.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


class WorkspaceDependencyError(RuntimeError):
    """The required local workspace dependency cannot be resolved safely."""


def _git_common_repository() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    common_dir = Path(result.stdout.strip()).resolve()
    if common_dir.name != ".git":
        raise WorkspaceDependencyError("git common directory is not a repository root")
    return common_dir.parent


def _agent_utilities_root() -> Path:
    configured = os.environ.get("AGENT_UTILITIES_ROOT")
    if configured:
        candidate = Path(configured).expanduser().resolve()
        if (candidate / "scripts").is_dir() and (
            candidate / "pyproject.toml"
        ).is_file():
            return candidate
        raise WorkspaceDependencyError("AGENT_UTILITIES_ROOT is not agent-utilities")

    repository = _git_common_repository()
    for parent in (repository, *repository.parents):
        candidate = parent / "agent-utilities"
        if (candidate / "scripts").is_dir() and (
            candidate / "pyproject.toml"
        ).is_file():
            return candidate.resolve()
    raise WorkspaceDependencyError(
        "cannot locate the agent-utilities workspace sibling"
    )


def _epistemic_graph_root(agent_utilities_root: Path) -> Path:
    candidates = [agent_utilities_root.parent / "epistemic-graph"]
    repository = _git_common_repository()
    candidates.extend(parent / "epistemic-graph" for parent in repository.parents)
    for candidate in candidates:
        package = candidate / "epistemic_graph"
        if (package / "__init__.py").is_file() and any(
            package.glob("numeric.*.so")
        ):
            return candidate.resolve()
    raise WorkspaceDependencyError(
        "cannot locate epistemic-graph with the certified numeric kernel"
    )


def _ensure_sibling(repository_root: Path, source: Path) -> None:
    sibling_dir = repository_root / ".uv-workspace-siblings"
    sibling_dir.mkdir(mode=0o755, exist_ok=True)
    link = sibling_dir / "agent-utilities"
    if link.is_symlink():
        if link.resolve() == source:
            return
        link.unlink()
    elif link.exists():
        raise WorkspaceDependencyError(
            ".uv-workspace-siblings/agent-utilities exists and is not a symlink"
        )
    link.symlink_to(source, target_is_directory=True)


def main(argv: list[str] | None = None) -> int:
    command = list(sys.argv[1:] if argv is None else argv)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        raise WorkspaceDependencyError("no command was supplied")

    repository_root = Path.cwd().resolve()
    agent_utilities_root = _agent_utilities_root()
    epistemic_graph_root = _epistemic_graph_root(agent_utilities_root)
    _ensure_sibling(repository_root, agent_utilities_root)
    environment = os.environ.copy()
    existing_pythonpath = environment.get("PYTHONPATH")
    python_paths = list(
        map(str, (repository_root, agent_utilities_root, epistemic_graph_root))
    )
    if existing_pythonpath:
        python_paths.append(existing_pythonpath)
    environment["PYTHONPATH"] = os.pathsep.join(python_paths)
    os.execvpe(command[0], command, environment)
    return 1  # pragma: no cover - os.execvpe either replaces us or raises


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.SubprocessError, WorkspaceDependencyError) as exc:
        print(f"workspace dependency bootstrap failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
