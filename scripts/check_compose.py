#!/usr/bin/env python3
"""Validate Compose files without weakening required production image pins."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


_IMAGE_SENTINEL = (
    "registry.example.invalid/gitlab-api@sha256:"
    "0000000000000000000000000000000000000000000000000000000000000000"
)
_IMMUTABLE_IMAGE = re.compile(r"^[^\s@]+@sha256:[0-9a-f]{64}$")


def _compose_command() -> list[str]:
    if shutil.which("docker"):
        probe = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            check=False,
            timeout=15,
        )
        if probe.returncode == 0:
            return ["docker", "compose"]
    if shutil.which("docker-compose"):
        return ["docker-compose"]
    raise RuntimeError("neither docker compose nor docker-compose is available")


def _validation_target(
    path: Path, *, repository_root: Path, validation_root: Path
) -> Path:
    source = path.resolve()
    try:
        relative = source.relative_to(repository_root)
    except ValueError as exc:
        raise RuntimeError("Compose files must be inside the repository") from exc
    target = validation_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    (validation_root / ".env").touch(mode=0o600, exist_ok=True)
    return target


def _has_only_immutable_images(
    compose: list[str], target: Path, environment: dict[str, str]
) -> bool:
    result = subprocess.run(
        [*compose, "--file", str(target), "config", "--images"],
        capture_output=True,
        check=False,
        env=environment,
        text=True,
        timeout=60,
    )
    if result.returncode:
        return False
    images = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return bool(images) and all(_IMMUTABLE_IMAGE.fullmatch(image) for image in images)


def main(argv: list[str] | None = None) -> int:
    paths = [Path(item) for item in (sys.argv[1:] if argv is None else argv)]
    if not paths:
        raise RuntimeError("no Compose files were supplied")

    environment = os.environ.copy()
    environment.setdefault("GITLAB_API_MCP_IMAGE", _IMAGE_SENTINEL)
    environment.setdefault("GITLAB_API_AGENT_IMAGE", _IMAGE_SENTINEL)
    compose = _compose_command()
    failures = 0
    repository_root = Path.cwd().resolve()
    with tempfile.TemporaryDirectory(prefix="gitlab-api-compose-") as temp_name:
        validation_root = Path(temp_name)
        for path in paths:
            target = _validation_target(
                path,
                repository_root=repository_root,
                validation_root=validation_root,
            )
            if not _has_only_immutable_images(compose, target, environment):
                print(f"ERROR: {path} contains a mutable or missing image", file=sys.stderr)
                failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
        print(f"compose validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
