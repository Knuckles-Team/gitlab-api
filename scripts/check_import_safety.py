#!/usr/bin/env python3
"""Cross-platform import-safety gate.

Walks every module under a package and imports it, failing on any exception
raised at import time (chiefly ``ImportError``/``ModuleNotFoundError``). This
is the cheapest, highest-yield check available against the entire "works on
Linux, breaks on Windows because it unconditionally imports a POSIX-only
stdlib module" class of defect -- an unguarded top-level ``import fcntl`` (or
``termios``/``pwd``/``resource``/``grp``) blows up the instant the module is
imported, before a single line of the module's own logic runs.

Two modes, one script
----------------------
* Bare invocation -- import every module in the *real* running interpreter.
  Run this on an actual Windows runner and POSIX-only stdlib modules are
  already absent, so this alone reproduces a genuine Windows import failure.
* ``--simulate-windows`` -- additionally poison ``POSIX_ONLY_STDLIB_MODULES``
  in ``sys.modules``/the import machinery *before* touching the target
  package, so a Linux or macOS developer gets the same signal locally,
  before ever touching Windows CI. On a real Windows interpreter this flag
  is a harmless no-op (those modules do not exist there to begin with).

This script is intentionally stdlib-only (no third-party imports of its own)
so it can run in the fast pre-commit tier with no environment sync.

Known blind spot: this only catches imports that happen at *module import
time* (module-level statements, including inside ``__init__.py``/class
bodies/decorators evaluated at import). A guarded-but-still-broken import
performed *lazily inside a function body* (``def f(): import fcntl``) is
invisible to a static import walk -- it only fails when that function is
actually called on the wrong platform. That is a real, separate gap; see
AGENTS.md for which call sites still need runtime (not just import-time)
Windows coverage.

Usage::

    python3 scripts/check_import_safety.py --package agent_utilities
    python3 scripts/check_import_safety.py --package agent_utilities --simulate-windows
    python3 scripts/check_import_safety.py --package agent_utilities --exclude agent_utilities.some.heavy_optional_module
"""

from __future__ import annotations

import argparse
import builtins
import importlib
import pkgutil
import sys
import traceback

# Stdlib modules that exist only on POSIX. An unconditional top-level import
# of any of these is exactly the defect class this gate exists to catch --
# see agent_utilities/knowledge_graph/core/file_lock.py for the guarded
# (sys.platform == "win32" branch) pattern every call site should follow.
POSIX_ONLY_STDLIB_MODULES = ("fcntl", "termios", "pwd", "resource", "grp")


def install_windows_simulation(blocked: tuple[str, ...] = POSIX_ONLY_STDLIB_MODULES) -> None:
    """Make POSIX-only stdlib modules unimportable, as they are on Windows.

    Overrides ``builtins.__import__`` (rather than just deleting cache
    entries) so it also catches ``from fcntl import flock``-style imports,
    not only ``import fcntl``. Must be called before the target package is
    imported at all -- if a POSIX-only module were already cached in
    ``sys.modules`` by something imported earlier in this process, a plain
    cache-delete could race with re-import; evicting it here too closes that
    gap for a process where this is the very first thing that runs.

    Deliberately does NOT flip ``sys.platform``/``os.name`` to the Windows
    values -- that looks like a more complete simulation, but a live
    interpreter's ``pathlib.Path`` factory dispatches to ``WindowsPath`` vs
    ``PosixPath`` off the REAL ``os.name`` at construction time, and
    ``WindowsPath`` refuses to instantiate on an actual POSIX host
    (``UnsupportedOperation: cannot instantiate 'WindowsPath' on your
    system``) -- confirmed by trying it against this exact repo, where it
    broke the editable-install import hook before a single target module was
    even reached. A module-blocking-only shim is a deliberately narrower,
    safe approximation, not full platform emulation.

    Known false-positive class this narrowness produces: a module that
    ALREADY branches correctly on ``sys.platform == "win32"`` (this
    codebase's canonical guard, e.g. ``file_lock.py``) still evaluates that
    check against the REAL (POSIX) platform under this shim, so it still
    takes the POSIX arm and still hits the blocked module -- reported as a
    failure here even though the exact same code imports cleanly on real
    Windows. That is a real, understood limitation of a sys.modules-only
    shim, not a claim that the flagged module is actually broken; verify by
    reading the flagged module for a platform guard before assuming a
    regression. It does not weaken the check for the defect class it exists
    to catch: a module with NO guard at all still fails identically under
    this shim and on real Windows.
    """
    blocked_set = set(blocked)
    real_import = builtins.__import__

    def _blocking_import(name, globals=None, locals=None, fromlist=(), level=0):  # noqa: A002
        top = name.split(".", 1)[0]
        if top in blocked_set:
            raise ModuleNotFoundError(
                f"No module named {top!r} (simulated: POSIX-only, unavailable on Windows)"
            )
        return real_import(name, globals, locals, fromlist, level)

    builtins.__import__ = _blocking_import
    for name in blocked_set:
        sys.modules.pop(name, None)


def discover_modules(package_name: str) -> tuple[list[str], list[tuple[str, str]]]:
    """Return (discovered module names, walk-time failures).

    ``pkgutil.walk_packages`` must itself IMPORT every subpackage (not leaf
    module) to read its ``__path__`` and keep descending. With the default
    ``onerror=None`` it catches ``ImportError`` raised during that walk-time
    import and silently ignores it -- it does NOT re-raise, does NOT record
    it anywhere, and (critically) cannot descend into that subpackage's own
    children, so an ENTIRE subtree below a broken subpackage vanishes from
    the discovered list with no trace. Left unhandled, that would make this
    gate systematically UNDER-count exactly the blast radius it exists to
    measure -- confirmed empirically against this repo: a naive walk found
    51 fewer modules under Windows simulation (1478) than natively (1529),
    not because 51 modules became fine, but because whole subtrees under a
    failing subpackage went dark. An explicit ``onerror`` callback below
    records the failing subpackage name and its error instead of discarding
    it, so the caller can still report it as a failure even though nothing
    beneath it could be enumerated.
    """
    package = importlib.import_module(package_name)
    names = [package_name]
    walk_failures: list[tuple[str, str]] = []

    def _on_walk_error(broken_name: str) -> None:
        exc = sys.exc_info()[1]
        walk_failures.append((broken_name, f"{type(exc).__name__}: {exc}" if exc else "import failed while walking"))

    walkable_path = getattr(package, "__path__", None)
    if walkable_path is not None:
        for info in pkgutil.walk_packages(walkable_path, prefix=f"{package_name}.", onerror=_on_walk_error):
            names.append(info.name)
    return sorted(names), walk_failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--package",
        required=True,
        help="top-level package/module name to walk, e.g. agent_utilities",
    )
    parser.add_argument(
        "--simulate-windows",
        action="store_true",
        help="poison POSIX-only stdlib modules first, to reproduce a Windows import failure on a POSIX host (no-op on real Windows)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="DOTTED_PREFIX",
        help="dotted module name/prefix to skip (repeatable) -- for modules with legitimately environment-gated import-time side effects, not for hiding real breakage",
    )
    args = parser.parse_args()

    if args.simulate_windows:
        install_windows_simulation()

    try:
        module_names, walk_failures = discover_modules(args.package)
    except Exception as exc:  # the package itself failed to import -- fatal
        print(f"FATAL: could not import {args.package!r} at all: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    excluded = tuple(args.exclude)

    def is_excluded(name: str) -> bool:
        return any(name == prefix or name.startswith(prefix + ".") for prefix in excluded)

    mode = "simulated-windows" if args.simulate_windows else ("windows" if sys.platform == "win32" else "native")

    # Walk-time failures (subpackages pkgutil could not descend into at all)
    # are real findings, not a footnote -- everything beneath them was never
    # enumerable, so report them as failures even though we cannot name what
    # (if anything) they were individually hiding.
    failures: list[tuple[str, str]] = [
        (name, f"{err} (package failed to import WHILE WALKING -- its children could not be enumerated at all)")
        for name, err in walk_failures
        if not is_excluded(name)
    ]
    already_recorded = {name for name, _ in failures}
    checked = 0
    for name in module_names:
        if is_excluded(name) or name in already_recorded:
            # walk_failures already proved this exact name fails to import;
            # re-importing it here would only duplicate the same finding.
            continue
        checked += 1
        try:
            importlib.import_module(name)
        except Exception as exc:  # ImportError/ModuleNotFoundError and anything else raised at import time
            failures.append((name, f"{type(exc).__name__}: {exc}"))
    checked += len(already_recorded)

    print(f"import-safety[{mode}]: checked {checked} modules under {args.package!r}")

    if failures:
        print(f"import-safety[{mode}]: {len(failures)} module(s) FAILED to import:")
        for name, err in failures:
            print(f"  {name}: {err}")
        return 1

    print(f"import-safety[{mode}]: all {checked} modules imported cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
