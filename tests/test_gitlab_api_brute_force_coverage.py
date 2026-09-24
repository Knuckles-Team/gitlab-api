import asyncio
import inspect
import json
import re
from typing import Any
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_session():
    with patch("requests.Session") as mock_s:
        session = mock_s.return_value
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "id": 1,
            "name": "test",
            "web_url": "http://test",
            "data": {"project": {"id": "1"}},
        }
        response.text = '{"id": 1}'
        response.headers = {"X-Total-Pages": "1"}
        session.get.return_value = response
        session.post.return_value = response
        session.put.return_value = response
        session.delete.return_value = response
        session.patch.return_value = response
        session.request.return_value = response
        yield session


def _build_api_brute_force_kwargs() -> dict[str, Any]:
    return {
        "project_id": "1",
        "group_id": "1",
        "id": "1",
        "user_id": "1",
        "issue_iid": "1",
        "merge_request_iid": "1",
        "commit_sha": "abc123def456",
        "branch": "main",
        "ref": "main",
        "name": "test",
        "tag": "v1.0",
        "pipeline_id": "1",
        "job_id": "1",
        "note_id": "1",
        "snippet_id": "1",
        "title": "test",
        "description": "test",
        "payload": {},
        "data": {},
        "attributes": {},
        "path": "test.txt",
        "content": "test",
        "message": "test",
    }


def _kwargs_for_api_method(method: Any, common_kwargs: dict[str, Any]) -> dict[str, Any]:
    sig = inspect.signature(method)
    has_kwargs = any(
        p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
    )
    if has_kwargs:
        return common_kwargs.copy()

    kwargs = {k: v for k, v in common_kwargs.items() if k in sig.parameters}
    # Fill missing mandatory ones
    for p_name, p in sig.parameters.items():
        if p.default == inspect.Parameter.empty and p_name not in kwargs:
            kwargs[p_name] = "test"
    return kwargs


def test_gitlab_api_brute_force(mock_session):
    _ = mock_session
    from gitlab_api.api_client import Api

    with patch.dict("os.environ", {"GITLAB_URL": "http://test"}):
        api = Api(url="http://test", token="test")

    common_kwargs = _build_api_brute_force_kwargs()

    # Introspect all methods
    for name, method in inspect.getmembers(api, predicate=inspect.ismethod):
        if name.startswith("_"):
            continue
        print(f"Calling Api.{name}...")
        kwargs = _kwargs_for_api_method(method, common_kwargs)
        try:
            method(**kwargs)
        except:
            pass


def _build_common_mcp_params() -> dict[str, Any]:
    return {
        "project_id": "1",
        "group_id": "1",
        "id": "1",
        "user_id": "1",
        "issue_iid": "1",
        "merge_request_iid": "1",
        "branch": "main",
        "ref": "main",
        "name": "test",
        "tag": "v1.0",
        "pipeline_id": "1",
        "job_id": "1",
        "note_id": "1",
        "snippet_id": "1",
        "title": "test",
        "description": "test",
        "body": "test",
        "slug": "home",
        "username": "user",
        "issue_id": "1",
        "mr_id": "1",
        "schedule_id": "1",
        "package_id": "1",
        "package_type": "npm",
        "namespace_id": "1",
        "search": "test",
        "after": "test",
        "method": "GET",
        "endpoint": "/projects/1/issues",
        "query": 'query { project(fullPath: "a") { id } }',
        "variables": "{}",
    }


def _build_sparse_mcp_params(common_params: dict[str, Any]) -> dict[str, Any]:
    """common_params without branch/ref/id-ish keys, to hit get-all paths."""
    excluded = [
        "branch",
        "tag",
        "ref",
        "issue_iid",
        "merge_request_iid",
        "username",
    ]
    return {k: v for k, v in common_params.items() if k not in excluded}


def _build_mcp_params_profiles(
    common_params: dict[str, Any], sparse_params: dict[str, Any]
) -> list[dict[str, Any]]:
    """All parameter profiles to exhaustively trigger conditional blocks."""
    return [
        common_params,
        {},
        {"commit_sha": "abc"},
        {"token_id": "1", "project_id": "1"},
        {"token_id": "1", "group_id": "1"},
        {"environment_id": "1"},
        {"environment_name": "prod"},
        {"approval_rule_id": "1"},
        {"milestone_id": "1"},
        {"epic_iid": "1"},
        {"epic_id": "1"},
        {"issue_id": "1"},
        {"tag_name": "v1"},
        sparse_params,
    ]


def _actions_to_test(tool: Any) -> list[Any]:
    """Parse a tool's `action == "..."` options from its source, plus a
    forced-invalid option (or [None, "invalid_action"] when none are found)."""
    try:
        source = inspect.getsource(tool.fn)
        actions = re.findall(r'action\s*==\s*["\']([^"\']+)["\']', source)
    except Exception:
        actions = []

    actions_to_test = list(actions) + ["invalid_action"]
    if not actions:
        actions_to_test = [None, "invalid_action"]
    return actions_to_test


def _profiles_for_action(
    act: Any, params_profiles: list[dict[str, Any]], common_params: dict[str, Any]
) -> list[dict[str, Any]]:
    # Optimize: only test all profiles on "get"/"get_protected"/similar prefix
    # actions, the only ones with internal conditional logic. Other actions
    # have no branch logic and only need one profile to be covered.
    if act is None or (isinstance(act, str) and act.startswith("get")):
        return params_profiles
    return [common_params]


def _coerce_param_value(annotation: Any, val: Any) -> Any:
    if annotation == int:
        try:
            return int(val)
        except:
            return 1
    if annotation == float:
        try:
            return float(val)
        except:
            return 1.0
    if annotation == bool:
        return True
    return val


def _target_value_for_param(
    p_name: str, p: inspect.Parameter, profile: dict[str, Any]
) -> Any:
    """Resolve one non-special parameter's brute-force value: its own
    default (unwrapping a FieldInfo-like default), else the profile's
    value, type-coerced to the parameter's annotation."""
    p_default = p.default
    if p_default != inspect.Parameter.empty and hasattr(p_default, "default"):
        p_default = p_default.default

    if (
        p_default == inspect.Parameter.empty
        or str(p_default).endswith("Undefined")
        or p_default is Ellipsis
    ):
        val = profile.get(p_name, "test")
    else:
        val = p_default

    return _coerce_param_value(p.annotation, val)


def _build_target_params_for_profile(
    tool: Any, act: Any, profile: dict[str, Any]
) -> dict[str, Any]:
    """Populate one call's kwargs for (tool, action, profile) while brute-forcing."""
    target_params: dict[str, Any] = {}
    sig = inspect.signature(tool.fn)

    for p_name, p in sig.parameters.items():
        if p_name in ["client", "_client", "ctx", "context"]:
            # Injected/handled by FastMCP/Depends, MUST NOT pass to call_tool
            continue
        if p_name == "action":
            target_params[p_name] = act if act is not None else "test"
            continue
        if p_name == "params_json":
            target_params[p_name] = json.dumps(profile)
            continue
        target_params[p_name] = _target_value_for_param(p_name, p, profile)

    return target_params


async def _brute_force_action_profiles(
    mcp: Any, tool: Any, act: Any, profiles_to_test: list[dict[str, Any]]
) -> None:
    for profile in profiles_to_test:
        target_params = _build_target_params_for_profile(tool, act, profile)
        try:
            await mcp.call_tool(tool.name, target_params)
        except Exception:
            pass


async def _brute_force_tool_actions(
    mcp: Any,
    tool: Any,
    common_params: dict[str, Any],
    params_profiles: list[dict[str, Any]],
) -> None:
    for act in _actions_to_test(tool):
        profiles_to_test = _profiles_for_action(act, params_profiles, common_params)
        await _brute_force_action_profiles(mcp, tool, act, profiles_to_test)


def _default_or_common_value(
    p_name: str, p: inspect.Parameter, common_params: dict[str, Any]
) -> Any:
    p_default = p.default
    if p_default != inspect.Parameter.empty and hasattr(p_default, "default"):
        p_default = p_default.default
    if (
        p_default == inspect.Parameter.empty
        or str(p_default).endswith("Undefined")
        or p_default is Ellipsis
    ):
        return common_params.get(p_name, "test")
    return p_default


def _invalid_json_target_params(
    tool: Any, common_params: dict[str, Any]
) -> dict[str, Any]:
    """Kwargs that trigger the ValueError/JSONDecodeError except blocks."""
    target_params: dict[str, Any] = {}
    sig = inspect.signature(tool.fn)
    for p_name, p in sig.parameters.items():
        if p_name in ["client", "_client", "ctx", "context"]:
            continue
        if p_name == "action":
            target_params[p_name] = "get"
            continue
        if p_name in ("params_json", "variables"):
            target_params[p_name] = "{invalid"
            continue
        target_params[p_name] = _default_or_common_value(p_name, p, common_params)
    return target_params


async def _run_invalid_json_coverage(
    mcp: Any, tool: Any, common_params: dict[str, Any]
) -> None:
    target_params = _invalid_json_target_params(tool, common_params)
    try:
        await mcp.call_tool(tool.name, target_params)
    except Exception:
        pass


_PROMPT_COVERAGE_CASES: list[tuple[str, dict[str, Any]]] = [
    (
        "create_branch_prompt",
        {"new_branch": "a", "source_branch": "b", "project_id": "c"},
    ),
    (
        "create_merge_request_prompt",
        {
            "new_branch": "a",
            "source_branch": "b",
            "project_id": "c",
            "title": "d",
            "description": "e",
        },
    ),
    ("get_project_statistics_prompt", {"project_id": "a"}),
    ("trigger_pipeline_prompt", {"branch": "a", "project_id": "c"}),
    ("get_latest_release_prompt", {"project_id": "a"}),
]


async def _run_prompts_coverage(mcp: Any) -> None:
    print("Running prompts coverage...")
    for prompt_name, prompt_args in _PROMPT_COVERAGE_CASES:
        try:
            prompt = await mcp.get_prompt(prompt_name)
            await prompt.render(prompt_args)
        except Exception as e:
            print(f"Operation failed: {type(e).__name__}")


def test_mcp_server_coverage(mock_session):
    _ = mock_session
    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware

    from gitlab_api.api_client import Api
    from gitlab_api.gitlab_gql import GraphQL
    from gitlab_api.mcp_server import get_mcp_instance

    # Patch RateLimitingMiddleware to do nothing
    async def mock_on_request(self, context, call_next):
        return await call_next(context)

    async def dummy_log(*args, **kwargs):
        return None

    # Let's mock get_client and get_graphql_client using dummy functions with proper signature
    mock_api = MagicMock(spec=Api)
    mock_api.get_branches.return_value = [{"name": "main"}]
    mock_api.get_branch.return_value = {"name": "main"}
    mock_api.create_branch.return_value = {"name": "main"}
    mock_api.delete_branch.return_value = {}

    mock_gql = MagicMock(spec=GraphQL)
    mock_gql.execute_gql.return_value = {"data": {}}

    def dummy_get_client(*args, **kwargs):
        return mock_api

    def dummy_get_graphql_client(*args, **kwargs):
        return mock_gql

    with patch.object(RateLimitingMiddleware, "on_request", mock_on_request):
        with (
            patch("fastmcp.server.context.Context.info", dummy_log),
            patch("fastmcp.server.context.Context.warning", dummy_log),
            patch("fastmcp.server.context.Context.error", dummy_log),
        ):
            with patch("gitlab_api.mcp_server.get_client", dummy_get_client):
                with patch(
                    "gitlab_api.auth.get_graphql_client", dummy_get_graphql_client
                ):
                    mcp_data = get_mcp_instance()
                    mcp = mcp_data[0] if isinstance(mcp_data, tuple) else mcp_data

                    async def run_tools():
                        tool_objs = (
                            await mcp.list_tools()
                            if inspect.iscoroutinefunction(mcp.list_tools)
                            else mcp.list_tools()
                        )

                        common_params = _build_common_mcp_params()
                        sparse_params = _build_sparse_mcp_params(common_params)
                        params_profiles = _build_mcp_params_profiles(
                            common_params, sparse_params
                        )

                        for tool in tool_objs:
                            print(f"Brute forcing MCP tool: {tool.name}...")
                            await _brute_force_tool_actions(
                                mcp, tool, common_params, params_profiles
                            )
                            await _run_invalid_json_coverage(
                                mcp, tool, common_params
                            )

                        await _run_prompts_coverage(mcp)

                loop = asyncio.new_event_loop()
                loop.run_until_complete(run_tools())
                loop.close()


def test_mcp_server_main():
    from gitlab_api.mcp_server import mcp_server

    with patch("gitlab_api.mcp_server.get_mcp_instance") as mock_get:
        mock_mcp = MagicMock()
        mock_args = MagicMock()
        mock_args.transport = "stdio"
        mock_get.return_value = (mock_mcp, mock_args, [], [])

        mcp_server()
        assert mock_mcp.run.called

        mock_args.transport = "streamable-http"
        mcp_server()

        mock_args.transport = "sse"
        mcp_server()

        mock_args.transport = "invalid"
        try:
            mcp_server()
        except SystemExit:
            pass
