import importlib
import sys
import inspect
from typing import List

__all__: List[str] = []

CORE_MODULES = [
    "gitlab_api.gitlab_input_models",
    "gitlab_api.gitlab_response_models",
    "gitlab_api.gitlab_api",
]

OPTIONAL_MODULES = {
    "gitlab_api.gitlab_gql": "gql",
    "gitlab_api.agent": "agent",
    "gitlab_api.mcp": "mcp",
}


def _import_module_safely(module_name: str):
    """Try to import a module and return it, or None if not available."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


def _expose_members(module):
    """Expose public classes and functions from a module into globals and __all__."""
    for name, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) or inspect.isfunction(obj)) and not name.startswith(
            "_"
        ):
            globals()[name] = obj
            __all__.append(name)


for module_name in CORE_MODULES:
    module = importlib.import_module(module_name)
    _expose_members(module)

for module_name, extra_name in OPTIONAL_MODULES.items():
    module = _import_module_safely(module_name)
    if module is not None:
        _expose_members(module)
        globals()[f"_{extra_name.upper()}_AVAILABLE"] = True
    else:
        globals()[f"_{extra_name.upper()}_AVAILABLE"] = False

_MCP_AVAILABLE = "gitlab_api.mcp" in globals() or "gitlab_api.mcp" in sys.modules
_AGENT_AVAILABLE = "gitlab_api.agent" in globals()
_GQL_AVAILABLE = "gitlab_api.gitlab_gql" in globals()

__all__.extend(["_MCP_AVAILABLE", "_AGENT_AVAILABLE", "_GQL_AVAILABLE"])

"""
GitLab API - A Python Wrapper for GitLab

Features are conditionally loaded based on installed extras:
- base: core API client and models
- [mcp]: FastMCP server and tools
- [a2a]: Agent-to-Agent multi-agent system with Graphiti knowledge graph
- [gql]: GraphQL support
"""
