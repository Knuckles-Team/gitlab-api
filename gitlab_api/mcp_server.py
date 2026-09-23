#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

# General urllib3/chardet mismatch warnings
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from collections.abc import Callable
from typing import Any, Literal

from agent_utilities.core.config import load_config, setting
from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface

from gitlab_api.api_client import Api
from gitlab_api.auth import get_client

__version__ = "27.1.0"
print(f"Gitlab MCP v{__version__}", file=sys.stderr)

logger = get_logger(name="mcp_server")
logger.setLevel(logging.DEBUG)

DEFAULT_GITLAB_URL = setting("GITLAB_URL", "https://gitlab.com")
DEFAULT_GITLAB_TOKEN = setting("GITLAB_TOKEN", None)


def _parse_params(params_json: str) -> dict[str, Any] | None:
    """Decode a ``params_json`` payload, dropping null values.

    Returns ``None`` when the payload is not decodable JSON; callers surface
    that as the generic ``{"error": "Operation failed"}`` response.
    """
    import json

    try:
        kwargs = json.loads(params_json)
    except Exception:
        return None
    return {k: v for k, v in kwargs.items() if v is not None}


def _by_keys(
    keys: tuple[str, ...], present: str, absent: str
) -> Callable[[dict[str, Any]], str]:
    """Selector picking ``present`` when any of ``keys`` was supplied."""

    def _select(kwargs: dict[str, Any]) -> str:
        return present if any(k in kwargs for k in keys) else absent

    return _select


def _deploy_token_get(kwargs: dict[str, Any]) -> str:
    """Selector for the deploy-token read that matches the given identifiers."""
    if "token_id" in kwargs and "project_id" in kwargs:
        return "get_project_deploy_token"
    if "token_id" in kwargs and "group_id" in kwargs:
        return "get_group_deploy_token"
    return "get_deploy_tokens"


async def _dispatch_tool_action(
    action: str,
    params_json: str,
    client: Any,
    ctx: Context | None,
    table: dict[str, Any],
) -> Any:
    """Resolve ``action`` against ``table`` and run the matching client method.

    ``table`` maps each canonical action either to an ``Api`` method name or to
    a selector callable that picks one from the decoded parameters. This is the
    single shared body behind every condensed ``gitlab_<domain>`` tool.
    """
    if ctx:
        await ctx.info("Executing tool...")
    kwargs = _parse_params(params_json)
    if kwargs is None:
        return {"error": "Operation failed"}
    resolved = resolve_action(action, set(table), service="gitlab-api")
    if isinstance(resolved, dict):
        return resolved
    target = table.get(resolved)
    if target is None:
        raise ValueError(f"Unknown action: {resolved}")
    method = target(kwargs) if callable(target) else target
    return await run_blocking(getattr(client, method), **kwargs)


def _records_as_dicts(resp: Any) -> list[dict[str, Any]]:
    """Normalize an Api response into a list of plain dicts."""
    data = getattr(resp, "data", resp)
    records = data if isinstance(data, list) else [data]
    return [
        r.model_dump() if hasattr(r, "model_dump") else r
        for r in records
        if r is not None
    ]


async def _fetch_pipeline_jobs(
    client: Any, project_id: str, pipelines: list[dict[str, Any]]
) -> dict[Any, list[dict[str, Any]]]:
    """Fetch each pipeline's jobs, keyed by pipeline id."""
    jobs_by_pipeline: dict[Any, list[dict[str, Any]]] = {}
    for pipe in pipelines:
        pid = pipe.get("id")
        if pid is None:
            continue
        jresp = await run_blocking(
            client.get_pipeline_jobs, project_id=project_id, pipeline_id=pid
        )
        jobs_by_pipeline[pid] = _records_as_dicts(jresp)
    return jobs_by_pipeline


def _sole_model_parameter(method: Any) -> Any:
    """The one required parameter of ``method`` when it is a pydantic model.

    Returns ``None`` unless the operation takes exactly one required argument
    and that argument is annotated with a ``BaseModel`` subclass.
    """
    import inspect

    from pydantic import BaseModel

    required = [
        p
        for p in inspect.signature(method).parameters.values()
        if p.default is inspect.Parameter.empty
        and p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
    ]
    if (
        len(required) == 1
        and isinstance(required[0].annotation, type)
        and issubclass(required[0].annotation, BaseModel)
    ):
        return required[0]
    return None


#: Action -> Api method for the ``gitlab_branches`` tool.
_BRANCHES_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("branch",), "get_branch", "get_branches"),
    "create": "create_branch",
    "delete": "delete_branch",
    "delete_merged": "delete_merged_branches",
}

#: Action -> Api method for the ``gitlab_protected_branches`` tool.
_PROTECTED_BRANCHES_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("branch",), "get_protected_branch", "get_protected_branches"),
    "protect": "protect_branch",
    "unprotect": "unprotect_branch",
    "require_code_owner_approvals": "require_code_owner_approvals_single_branch",
}

#: Action -> Api method for the ``gitlab_commits`` tool.
_COMMITS_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("commit_sha",), "get_commit", "get_commits"),
    "create": "create_commit",
    "diff": "get_commit_diff",
    "revert": "revert_commit",
    "get_comments": "get_commit_comments",
    "create_comment": "create_commit_comment",
    "get_discussions": "get_commit_discussions",
    "get_statuses": "get_commit_statuses",
    "post_status": "post_build_status_to_commit",
    "get_merge_requests": "get_commit_merge_requests",
    "get_gpg_signature": "get_commit_gpg_signature",
    "cherry_pick": "cherry_pick_commit",
    "get_references": "get_commit_references",
}

#: Action -> Api method for the ``gitlab_deploy_tokens`` tool.
_DEPLOY_TOKENS_ACTIONS: dict[str, Any] = {
    "get": _deploy_token_get,
    "get_project": "get_project_deploy_tokens",
    "create_project": "create_project_deploy_token",
    "delete_project": "delete_project_deploy_token",
    "get_group": "get_group_deploy_tokens",
    "create_group": "create_group_deploy_token",
    "delete_group": "delete_group_deploy_token",
}

#: Action -> Api method for the ``gitlab_environments`` tool.
_ENVIRONMENTS_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("environment_id",), "get_environment", "get_environments"),
    "create": "create_environment",
    "update": "update_environment",
    "delete": "delete_environment",
    "stop": "stop_environment",
    "stop_stale": "stop_stale_environments",
    "delete_stopped": "delete_stopped_environments",
    "get_protected": _by_keys(
        ("environment_name",), "get_protected_environment", "get_protected_environments"
    ),
    "protect": "protect_environment",
    "update_protected": "update_protected_environment",
    "unprotect": "unprotect_environment",
}

#: Action -> Api method for the ``gitlab_groups`` tool.
_GROUPS_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("group_id",), "get_group", "get_groups"),
    "edit": "edit_group",
    "get_subgroups": "get_group_subgroups",
    "get_descendants": "get_group_descendant_groups",
    "get_projects": "get_group_projects",
    "get_merge_requests": "get_group_merge_requests",
}

#: Action -> Api method for the ``gitlab_jobs`` tool.
_JOBS_ACTIONS: dict[str, Any] = {
    "get_project_jobs": "get_project_jobs",
    "get_job": "get_project_job",
    "get_log": "get_project_job_log",
    "cancel": "cancel_project_job",
    "retry": "retry_project_job",
    "erase": "erase_project_job",
    "run": "run_project_job",
    "get_pipeline_jobs": "get_pipeline_jobs",
}

#: Action -> Api method for the ``gitlab_members`` tool.
_MEMBERS_ACTIONS: dict[str, Any] = {
    "get_group": "get_group_members",
    "get_project": "get_project_members",
}

#: Action -> Api method for the ``gitlab_merge_requests`` tool.
_MERGE_REQUESTS_ACTIONS: dict[str, Any] = {
    "create": "create_merge_request",
    "get": _by_keys(
        ("merge_request_iid",), "get_project_merge_request", "get_merge_requests"
    ),
    "get_project": "get_project_merge_requests",
    "accept": "accept_merge_request",
    "cancel_auto_merge": "cancel_merge_when_pipeline_succeeds",
}

#: Action -> Api method for the ``gitlab_merge_rules`` tool.
_MERGE_RULES_ACTIONS: dict[str, Any] = {
    "get_project_level": _by_keys(
        ("approval_rule_id",),
        "get_project_level_merge_request_rule",
        "get_project_level_merge_request_rules",
    ),
    "create_project_level": "create_project_level_rule",
    "update_project_level": "update_project_level_rule",
    "delete_project_level": "delete_project_level_rule",
    "get_mr_approvals": "get_approval_state_merge_requests",
    "get_mr_approval_state": "get_approval_state_merge_requests",
    "get_mr_level": "get_merge_request_level_rules",
    "approve_mr": "approve_merge_request",
    "unapprove_mr": "unapprove_merge_request",
    "get_group_level": "get_group_level_rule",
    "edit_group_level": "edit_group_level_rule",
    "edit_project_level": "edit_project_level_rule",
    "set_mr_approvals": "merge_request_level_approvals",
    "get_project_rule": "get_project_level_rule",
}

#: Action -> Api method for the ``gitlab_packages`` tool.
_PACKAGES_ACTIONS: dict[str, Any] = {
    "get": "get_repository_packages",
    "publish": "publish_repository_package",
    "download": "download_repository_package",
}

#: Action -> Api method for the ``gitlab_pipelines`` tool.
_PIPELINES_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("pipeline_id",), "get_pipeline", "get_pipelines"),
    "run": "run_pipeline",
}

#: Action -> Api method for the ``gitlab_pipeline_schedules`` tool.
_PIPELINE_SCHEDULES_ACTIONS: dict[str, Any] = {
    "get_all": "get_pipeline_schedules",
    "get": "get_pipeline_schedule",
    "get_triggered": "get_pipelines_triggered_from_schedule",
    "create": "create_pipeline_schedule",
    "edit": "edit_pipeline_schedule",
    "take_ownership": "take_pipeline_schedule_ownership",
    "delete": "delete_pipeline_schedule",
    "run": "run_pipeline_schedule",
    "create_variable": "create_pipeline_schedule_variable",
    "delete_variable": "delete_pipeline_schedule_variable",
}

#: Action -> Api method for the ``gitlab_projects`` tool.
_PROJECTS_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("project_id", "id"), "get_project", "get_projects"),
    "create": "create_project",
    "delete": "delete_project",
    "get_nested_by_group": "get_nested_projects_by_group",
    "get_contributors": "get_project_contributors",
    "get_statistics": "get_project_statistics",
    "edit": "edit_project",
    "share_with_group": "share_project",
    "unshare_with_group": "delete_shared_project_link",
    "archive": "archive_project",
    "unarchive": "unarchive_project",
    "get_project_groups": "get_project_groups",
}

#: Action -> Api method for the ``gitlab_releases`` tool.
_RELEASES_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("tag_name",), "get_release_by_tag", "get_releases"),
    "get_latest": "get_latest_release",
    "get_latest_evidence": "get_latest_release_evidence",
    "get_latest_asset": "get_latest_release_asset",
    "get_group_releases": "get_group_releases",
    "download_asset": "download_release_asset",
    "get_by_tag": "get_release_by_tag",
    "create": "create_release",
    "create_evidence": "create_release_evidence",
    "update": "update_release",
    "delete": "delete_release",
}

#: Action -> Api method for the ``gitlab_runners`` tool.
_RUNNERS_ACTIONS: dict[str, Any] = {
    "get_all": "get_runners",
    "get": "get_runner",
    "update_details": "update_runner_details",
    "pause": "pause_runner",
    "get_jobs": "get_runner_jobs",
    "get_project": "get_project_runners",
    "enable_project": "enable_project_runner",
    "delete_project": "delete_project_runner",
    "get_group": "get_group_runners",
    "register": "register_new_runner",
    "delete": "delete_runner",
    "verify_auth": "verify_runner_authentication",
    "reset_gitlab_token": "reset_gitlab_runner_token",
    "reset_project_token": "reset_project_runner_token",
    "reset_group_token": "reset_group_runner_token",
    "reset_token": "reset_token",
}

#: Action -> Api method for the ``gitlab_tags`` tool.
_TAGS_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("tag", "tag_name"), "get_tag", "get_tags"),
    "create": "create_tag",
    "delete": "delete_tag",
    "get_protected": "get_protected_tags",
    "get_protected_tag": "get_protected_tag",
    "protect": "protect_tag",
    "unprotect": "unprotect_tag",
}

#: Action -> Api method for the ``gitlab_labels`` tool.
_LABELS_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("name", "label_id"), "get_label", "get_labels"),
    "create": "create_label",
    "update": "update_label",
    "delete": "delete_label",
}

#: Action -> Api method for the ``gitlab_milestones`` tool.
_MILESTONES_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("milestone_id",), "get_milestone", "get_milestones"),
    "create": "create_milestone",
    "update": "update_milestone",
    "delete": "delete_milestone",
}

#: Action -> Api method for the ``gitlab_snippets`` tool.
_SNIPPETS_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("snippet_id",), "get_snippet", "get_snippets"),
    "create": "create_snippet",
    "update": "update_snippet",
    "delete": "delete_snippet",
}

#: Action -> Api method for the ``gitlab_notes`` tool.
_NOTES_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("note_id",), "get_note", "get_notes"),
    "create": "create_note",
    "update": "update_note",
    "delete": "delete_note",
}

#: Action -> Api method for the ``gitlab_epics`` tool.
_EPICS_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("epic_iid", "epic_id"), "get_epic", "get_epics"),
    "create": "create_epic",
    "update": "update_epic",
    "delete": "delete_epic",
}

#: Action -> Api method for the ``gitlab_issues`` tool.
_ISSUES_ACTIONS: dict[str, Any] = {
    "get": _by_keys(("issue_iid", "issue_id"), "get_issue", "get_issues"),
    "create": "create_issue",
    "update": "update_issue",
    "delete": "delete_issue",
    "get_group": "get_group_issues",
}

#: Action -> Api method for the ``gitlab_users`` tool.
_USERS_ACTIONS: dict[str, Any] = {
    "get": "get_users",
    "get_user": "get_user",
    "create": "create_user",
    "update": "update_user",
    "delete": "delete_user",
}

#: Action -> Api method for the ``gitlab_wiki`` tool.
_WIKI_ACTIONS: dict[str, Any] = {
    "get_list": "get_wiki_list",
    "get": "get_wiki_page",
    "create": "create_wiki_page",
    "update": "update_wiki_page",
    "delete": "delete_wiki_page",
    "upload_attachment": "upload_wiki_page_attachment",
}

#: Action -> Api method for the ``gitlab_namespaces`` tool.
_NAMESPACES_ACTIONS: dict[str, Any] = {
    "get": "get_namespaces",
    "get_namespace": "get_namespace",
}

#: Action -> Api method for the ``gitlab_vulnerabilities`` tool.
_VULNERABILITIES_ACTIONS: dict[str, Any] = {
    "dependencies": "get_project_dependencies",
    "get_project": "get_project_vulnerabilities",
    "get_group": "get_group_vulnerabilities",
    "get": "get_vulnerability",
}


def register_misc_tools(mcp: FastMCP):
    @mcp.tool(tags={"misc", "multitenant"})
    async def gitlab_instances(
        action: str = Field(
            default="list",
            description="'list' all configured GitLab tenants, or 'get' one by name.",
        ),
        name: str = Field(default="", description="Instance name for action='get'."),
        ctx: Context | None = None,
    ) -> Any:
        """List the configured GitLab tenants (CONCEPT:AU-KG.backend.declared-columns-so-schema).

        Multi-tenancy is driven by the shared agent-utilities XDG config
        (``gitlab_instances`` in ~/.config/agent-utilities/config.json). Every
        gitlab-api tool targets a tenant by passing that instance NAME to the
        client factory; this tool surfaces the available names (tokens are never
        returned). Falls back to the single-host GITLAB_URL/GITLAB_TOKEN.
        """
        from gitlab_api.instances import get_instance, instance_summaries

        if action == "get":
            inst = get_instance(name or None)
            if inst is None:
                return {"error": f"instance '{name}' not configured"}
            return {
                "name": inst.name,
                "url": inst.url,
                "tls_profile_configured": bool(inst.tls_profile_name),
                "has_token": bool(inst.token),
            }
        return {"instances": instance_summaries()}

    @mcp.tool(tags={"misc", "kg"})
    async def gitlab_ingest_projects(
        params_json: str = Field(
            default="{}",
            description="JSON string of get_projects filters (e.g. membership, per_page).",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Natively ingest GitLab projects into epistemic-graph as typed :Project nodes.

        Lists projects via the GitLab API and pushes them (with their :GitLabGroup +
        :partOfGroup links) into the knowledge graph via the fast engine client.
        Native-ingestion failures propagate to the caller.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json as _json

        from gitlab_api.kg_ingest import ingest_projects

        kwargs = _json.loads(params_json) if params_json else {}
        resp = await run_blocking(client.get_projects, **kwargs)
        projects = _records_as_dicts(resp)
        result = ingest_projects(projects)
        return {"listed": len(projects), "ingested": result}

    @mcp.tool(tags={"misc", "kg"})
    async def gitlab_ingest_pipelines(
        project_id: str = Field(
            description="GitLab project id or URL-encoded path to ingest recent pipeline runs for."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of get_pipelines filters (e.g. status, ref, per_page).",
        ),
        include_jobs: bool = Field(
            default=True,
            description="Also fetch + ingest each pipeline's jobs as :Job/:CheckRun nodes.",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Natively ingest GitLab CI pipeline runs (+ jobs) into epistemic-graph.

        Lists recent pipelines for ``project_id`` via the GitLab API (optionally each
        pipeline's jobs) and pushes them as typed ``:PipelineRun``/``:CheckRun`` nodes
        (the SAME classes + ``ranFor``/``hasJob`` edges github-agent uses, so GitLab
        CI/CD and GitHub Actions unify) — ``ranFor`` the ``:Project``, the ``:Commit``,
        and any triggering ``:MergeRequest`` — into the knowledge graph via the fast
        engine client. This is the substrate the autonomous-SDLC loop needs to observe
        CI. Best-effort: returns ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json as _json

        from gitlab_api.kg_ingest import ingest_pipeline_runs

        kwargs = _json.loads(params_json) if params_json else {}
        kwargs["project_id"] = project_id
        resp = await run_blocking(client.get_pipelines, **kwargs)
        pipelines = _records_as_dicts(resp)

        jobs_by_pipeline: dict[Any, list[dict[str, Any]]] = {}
        if include_jobs:
            jobs_by_pipeline = await _fetch_pipeline_jobs(client, project_id, pipelines)

        result = ingest_pipeline_runs(
            project_id, pipelines, jobs_by_pipeline=jobs_by_pipeline
        )
        return {"listed": len(pipelines), "ingested": result}

    return None


def register_branches_tools(mcp: FastMCP):
    @mcp.tool(tags={"branches"})
    async def gitlab_branches(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'delete', 'delete_merged'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab branches operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _BRANCHES_ACTIONS
        )


def register_protected_branches_tools(mcp: FastMCP):
    @mcp.tool(tags={"protected_branches"})
    async def gitlab_protected_branches(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'protect', 'unprotect', 'require_code_owner_approvals'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab protected branches operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _PROTECTED_BRANCHES_ACTIONS
        )


def register_commits_tools(mcp: FastMCP):
    @mcp.tool(tags={"commits"})
    async def gitlab_commits(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'diff', 'revert', 'get_comments', 'create_comment', 'get_discussions', 'get_statuses', 'post_status', 'get_merge_requests', 'get_gpg_signature', 'cherry_pick', 'get_references'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab commits operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _COMMITS_ACTIONS
        )


def register_deploy_tokens_tools(mcp: FastMCP):
    @mcp.tool(tags={"deploy_tokens"})
    async def gitlab_deploy_tokens(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_project', 'create_project', 'delete_project', 'get_group', 'create_group', 'delete_group'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab deploy tokens operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _DEPLOY_TOKENS_ACTIONS
        )


def register_environments_tools(mcp: FastMCP):
    @mcp.tool(tags={"environments"})
    async def gitlab_environments(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete', 'stop', 'stop_stale', 'delete_stopped', 'get_protected', 'protect', 'update_protected', 'unprotect'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab environments operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _ENVIRONMENTS_ACTIONS
        )


def register_groups_tools(mcp: FastMCP):
    @mcp.tool(tags={"groups"})
    async def gitlab_groups(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'edit', 'get_subgroups', 'get_descendants', 'get_projects', 'get_merge_requests'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab groups operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _GROUPS_ACTIONS
        )


def register_jobs_tools(mcp: FastMCP):
    @mcp.tool(tags={"jobs"})
    async def gitlab_jobs(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_project_jobs', 'get_job', 'get_log', 'cancel', 'retry', 'erase', 'run', 'get_pipeline_jobs'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab jobs operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _JOBS_ACTIONS
        )


def register_members_tools(mcp: FastMCP):
    @mcp.tool(tags={"members"})
    async def gitlab_members(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_group', 'get_project'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab members operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _MEMBERS_ACTIONS
        )


def register_merge_requests_tools(mcp: FastMCP):
    @mcp.tool(tags={"merge_requests"})
    async def gitlab_merge_requests(
        action: str = Field(
            description="Action to perform. Must be one of: 'create', 'get', 'get_project', 'accept', 'cancel_auto_merge'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab merge requests operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _MERGE_REQUESTS_ACTIONS
        )


def register_merge_rules_tools(mcp: FastMCP):
    @mcp.tool(tags={"merge_rules"})
    async def gitlab_merge_rules(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_project_level', 'create_project_level', 'update_project_level', 'delete_project_level', 'get_mr_approvals', 'get_mr_approval_state', 'get_mr_level', 'approve_mr', 'unapprove_mr', 'get_group_level', 'edit_group_level', 'edit_project_level', 'set_mr_approvals', 'get_project_rule'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab merge rules operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _MERGE_RULES_ACTIONS
        )


def register_packages_tools(mcp: FastMCP):
    @mcp.tool(tags={"packages"})
    async def gitlab_packages(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'publish', 'download'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab packages operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _PACKAGES_ACTIONS
        )


def register_pipelines_tools(mcp: FastMCP):
    @mcp.tool(tags={"pipelines"})
    async def gitlab_pipelines(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'run'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab pipelines operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _PIPELINES_ACTIONS
        )


def register_pipeline_schedules_tools(mcp: FastMCP):
    @mcp.tool(tags={"pipeline_schedules"})
    async def gitlab_pipeline_schedules(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_all', 'get', 'get_triggered', 'create', 'edit', 'take_ownership', 'delete', 'run', 'create_variable', 'delete_variable'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab pipeline schedules operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _PIPELINE_SCHEDULES_ACTIONS
        )


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(
        tags={"projects"},
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": True,
        },
        meta={
            "eg.annotations": {"modalities_in": ["text"], "modalities_out": ["text"]}
        },
    )
    async def gitlab_projects(
        action: Literal[
            "archive",
            "create",
            "delete",
            "edit",
            "get",
            "get_contributors",
            "get_nested_by_group",
            "get_project_groups",
            "get_statistics",
            "share_with_group",
            "unarchive",
            "unshare_with_group",
        ] = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'delete', 'get_nested_by_group', 'get_contributors', 'get_statistics', 'edit', 'share_with_group', 'unshare_with_group', 'archive', 'unarchive', 'get_project_groups'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab projects operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _PROJECTS_ACTIONS
        )


def register_releases_tools(mcp: FastMCP):
    @mcp.tool(tags={"releases"})
    async def gitlab_releases(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_latest', 'get_latest_evidence', 'get_latest_asset', 'get_group_releases', 'download_asset', 'get_by_tag', 'create', 'create_evidence', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab releases operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _RELEASES_ACTIONS
        )


def register_runners_tools(mcp: FastMCP):
    @mcp.tool(tags={"runners"})
    async def gitlab_runners(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_all', 'get', 'update_details', 'pause', 'get_jobs', 'get_project', 'enable_project', 'delete_project', 'get_group', 'register', 'delete', 'verify_auth', 'reset_gitlab_token', 'reset_project_token', 'reset_group_token', 'reset_token'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab runners operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _RUNNERS_ACTIONS
        )


def register_tags_tools(mcp: FastMCP):
    @mcp.tool(tags={"tags"})
    async def gitlab_tags(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'delete', 'get_protected', 'get_protected_tag', 'protect', 'unprotect'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab tags operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _TAGS_ACTIONS
        )


def register_labels_tools(mcp: FastMCP):
    @mcp.tool(tags={"labels"})
    async def gitlab_labels(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage GitLab labels."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _LABELS_ACTIONS
        )


def register_milestones_tools(mcp: FastMCP):
    @mcp.tool(tags={"milestones"})
    async def gitlab_milestones(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage GitLab milestones."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _MILESTONES_ACTIONS
        )


def register_snippets_tools(mcp: FastMCP):
    @mcp.tool(tags={"snippets"})
    async def gitlab_snippets(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage GitLab snippets."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _SNIPPETS_ACTIONS
        )


def register_notes_tools(mcp: FastMCP):
    @mcp.tool(tags={"notes"})
    async def gitlab_notes(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage GitLab notes/comments on issues, merge requests, commits, and epics."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _NOTES_ACTIONS
        )


def register_epics_tools(mcp: FastMCP):
    @mcp.tool(tags={"epics"})
    async def gitlab_epics(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage GitLab epics."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _EPICS_ACTIONS
        )


def register_issues_tools(mcp: FastMCP):
    @mcp.tool(tags={"issues"})
    async def gitlab_issues(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'create', 'update', 'delete', 'get_group'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage GitLab issues."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _ISSUES_ACTIONS
        )


def register_custom_api_tools(mcp: FastMCP):
    @mcp.tool(tags={"custom-api"})
    async def api_request(
        method: str = Field(
            description="HTTP method to use (e.g. GET, POST, PUT, DELETE, PATCH)"
        ),
        endpoint: str = Field(
            description="The API endpoint path (e.g., /projects/1/issues)"
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of query parameters or body payload to pass to the request.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute arbitrary GitLab REST API requests directly."""
        if ctx:
            await ctx.info("Executing custom API request...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return await run_blocking(
            client.api_request, method=method, endpoint=endpoint, **kwargs
        )


def register_users_tools(mcp: FastMCP):
    @mcp.tool(tags={"users"})
    async def gitlab_users(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_user', 'create', 'update', 'delete'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab users operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _USERS_ACTIONS
        )


def register_wiki_tools(mcp: FastMCP):
    @mcp.tool(tags={"wiki"})
    async def gitlab_wiki(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_list', 'get', 'create', 'update', 'delete', 'upload_attachment'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab wiki operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _WIKI_ACTIONS
        )


def register_namespaces_tools(mcp: FastMCP):
    @mcp.tool(tags={"namespaces"})
    async def gitlab_namespaces(
        action: str = Field(
            description="Action to perform. Must be one of: 'get', 'get_namespace'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage gitlab namespaces operations."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _NAMESPACES_ACTIONS
        )


def register_vulnerabilities_tools(mcp: FastMCP):
    @mcp.tool(tags={"vulnerabilities"})
    async def gitlab_vulnerabilities(
        action: str = Field(
            description="Action to perform. Must be one of: 'dependencies', 'get_project', 'get_group', 'get'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Review a project's dependency list and security vulnerabilities (the GitLab counterpart to GitHub Dependabot)."""
        return await _dispatch_tool_action(
            action, params_json, client, ctx, _VULNERABILITIES_ACTIONS
        )


def register_prompts(mcp: FastMCP):
    @mcp.prompt
    def create_branch_prompt(
        new_branch: str,
        source_branch: str,
        project_id: str | int,
    ) -> str:
        """
        Generates a prompt for creating a branch
        """
        return f"Create a branch called '{new_branch}' from the '{source_branch}' for project id {project_id}"

    @mcp.prompt
    def create_merge_request_prompt(
        new_branch: str,
        source_branch: str,
        project_id: str | int,
        title: str,
        description: str,
    ) -> str:
        """
        Generates a prompt for creating a merge request
        """
        return (
            f"Create a new merge request for project id {project_id} from the '{new_branch}' to the '{source_branch}' "
            f"with a title: '{title}' and a description: '{description}'"
        )

    @mcp.prompt
    def get_project_statistics_prompt(
        project_id: str | int,
    ) -> str:
        """
        Generates a prompt for getting project statistics
        """
        return f"What are the details for project id: {project_id}"

    @mcp.prompt
    def trigger_pipeline_prompt(
        branch: str,
        project_id: str | int,
    ) -> str:
        """
        Generates a prompt for triggering a pipeline
        """
        return f"Run the pipeline for project: '{project_id}' on the '{branch}' branch"

    @mcp.prompt
    def get_latest_release_prompt(
        project_id: str | int,
    ) -> str:
        """
        Generates a prompt for getting the latest gitlab release.
        """
        return f"What is the latest release for project id: {project_id}"


def register_graphql_tools(mcp: FastMCP):
    from gitlab_api.auth import get_graphql_client

    @mcp.tool(tags={"graphql"})
    async def gitlab_graphql(
        query: str = Field(
            description="The raw GraphQL query or mutation string to execute against the GitLab API."
        ),
        variables: str = Field(
            default="{}",
            description="JSON string of variables to pass along with the query.",
        ),
        operation_name: str | None = Field(
            default=None,
            description="Optional operation name if executing a specific query within the document.",
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Execute raw GraphQL queries and mutations natively on GitLab."""
        if ctx:
            await ctx.info("Executing GitLab GraphQL query...")
        import json

        try:
            vars_dict = json.loads(variables) if variables else None
        except Exception:
            return {"error": "Operation failed"}

        try:
            return await run_blocking(
                client.execute_gql,
                query_str=query,
                variables=vars_dict,
                operation_name=operation_name,
            )
        except Exception as e:
            return {"error": f"GraphQL execution failed: {type(e).__name__}"}

    @mcp.tool(tags={"graphql"})
    async def gitlab_discover_graphql_schema(
        type_name: str | None = Field(
            default=None,
            description="Optional specific GraphQL type name to inspect details for (e.g., 'Project', 'Issue'). If omitted, lists all available types in the schema.",
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Discover the dynamic GitLab GraphQL schema including types, fields, and custom attributes in real-time."""
        from agent_utilities.mcp.context_helpers import (
            ctx_graphql_get_type_details,
            ctx_graphql_list_types,
        )

        if ctx:
            await ctx.info("Retrieving dynamic GitLab GraphQL schema...")

        # Safe wrapper to call execute_gql
        async def execute_fn(q, variables=None):
            return await run_blocking(
                client.execute_gql, query_str=q, variables=variables
            )

        try:
            if type_name:
                return await ctx_graphql_get_type_details(execute_fn, type_name)
            return await ctx_graphql_list_types(execute_fn)
        except Exception:
            return {"error": "Failed to discover GitLab GraphQL schema"}


def register_graphql_ops_tools(mcp: FastMCP):
    from gitlab_api.auth import get_graphql_client
    from gitlab_api.gitlab_gql import GraphQL as _GitlabGraphQL

    #: Every typed operation on the GraphQL client (all methods except the raw
    #: execute_gql passthrough, which the gitlab_graphql tool already exposes).
    _GRAPHQL_OPS_ACTIONS = tuple(
        sorted(
            name
            for name, attr in vars(_GitlabGraphQL).items()
            if not name.startswith("_") and callable(attr) and name != "execute_gql"
        )
    )

    @mcp.tool(tags={"graphql_ops"})
    async def gitlab_graphql_ops(
        action: str = Field(
            description=(
                "Typed GraphQL operation to run (a method on the GitLab GraphQL "
                "client), e.g. 'get_merge_requests', 'update_merge_request', "
                "'delete_merge_request', 'accept_merge_request', 'retry_pipeline', "
                "'cancel_pipeline', 'create_pipeline', 'get_projects', 'get_job'."
            )
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_graphql_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Run a typed GitLab GraphQL operation by name.

        The GraphQL-native counterpart to the REST gitlab_<domain> tools — prefer it
        for GraphQL-only capabilities (merge-request update/delete, pipeline
        retry/cancel, member add/update/delete) and rich nested reads. Parameters in
        params_json are passed as keyword arguments to the named operation; a few
        operations that take a single typed model (e.g. get_project) build it from
        those same kwargs automatically.
        """
        if ctx:
            await ctx.info("Executing GitLab GraphQL operation...")
        kwargs = _parse_params(params_json)
        if kwargs is None:
            return {"error": "Operation failed"}

        resolved = resolve_action(
            action, set(_GRAPHQL_OPS_ACTIONS), service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        method = getattr(client, action)
        sole_model = _sole_model_parameter(method)
        try:
            if sole_model is not None:
                model = sole_model.annotation(**kwargs)
                return await run_blocking(method, **{sole_model.name: model})
            return await run_blocking(method, **kwargs)
        except Exception as e:
            return {"error": f"GraphQL operation '{action}' failed: {type(e).__name__}"}


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the GitLab MCP instance, args, and middlewares."""
    load_config()
    os.environ["FASTMCP_LOG_LEVEL"] = "ERROR"
    os.environ["TERM"] = "dumb"
    os.environ["NO_COLOR"] = "1"

    args, mcp, middlewares = create_mcp_server(
        name="GitLab",
        version=__version__,
        instructions="GitLab API MCP Server - Manage projects, issues, merge requests, branches, and more.",
    )

    registered_tags = register_tool_surface(
        mcp,
        client_cls=Api,
        get_client=get_client,
        service="gitlab-api",
        tools_module=sys.modules[__name__],
    )
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server() -> None:
    mcp, args, middlewares, registered_tags = get_mcp_instance()
    print(f"{'gitlab-api'} MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {len(set(registered_tags))}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
