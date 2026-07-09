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
from typing import Any

from agent_utilities.core.config import setting
from agent_utilities.mcp_utilities import (
    create_mcp_server,
    load_config,
    register_tool_surface,
    resolve_action,
    run_blocking,
)

from gitlab_api.api_client import Api
from gitlab_api.auth import get_client

__version__ = "26.1.1"
print(f"Gitlab MCP v{__version__}", file=sys.stderr)

logger = get_logger(name="mcp_server")
logger.setLevel(logging.DEBUG)

DEFAULT_GITLAB_SSL_VERIFY = setting("GITLAB_SSL_VERIFY", True)
DEFAULT_GITLAB_URL = setting("GITLAB_URL", "https://gitlab.com")
DEFAULT_GITLAB_TOKEN = setting("GITLAB_TOKEN", None)


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
                "verify_ssl": inst.verify_ssl,
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
        Best-effort: returns ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        import json as _json

        from gitlab_api.kg_ingest import ingest_projects

        kwargs = _json.loads(params_json) if params_json else {}
        resp = await run_blocking(client.get_projects, **kwargs)
        data = getattr(resp, "data", resp)
        records = data if isinstance(data, list) else [data]
        projects = [
            r.model_dump() if hasattr(r, "model_dump") else r
            for r in records
            if r is not None
        ]
        result = ingest_projects(projects)
        return {"listed": len(projects), "ingested": result}

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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "create", "delete", "delete_merged"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "branch" in kwargs:
                return await run_blocking(client.get_branch, **kwargs)
            return await run_blocking(client.get_branches, **kwargs)
        if action == "create":
            return await run_blocking(client.create_branch, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_branch, **kwargs)
        if action == "delete_merged":
            return await run_blocking(client.delete_merged_branches, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {"get", "protect", "unprotect", "require_code_owner_approvals"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "branch" in kwargs:
                return await run_blocking(client.get_protected_branch, **kwargs)
            return await run_blocking(client.get_protected_branches, **kwargs)
        if action == "protect":
            return await run_blocking(client.protect_branch, **kwargs)
        if action == "unprotect":
            return await run_blocking(client.unprotect_branch, **kwargs)
        if action == "require_code_owner_approvals":
            return await run_blocking(
                client.require_code_owner_approvals_single_branch, **kwargs
            )
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get",
                "create",
                "diff",
                "revert",
                "get_comments",
                "create_comment",
                "get_discussions",
                "get_statuses",
                "post_status",
                "get_merge_requests",
                "get_gpg_signature",
                "cherry_pick",
                "get_references",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "commit_sha" in kwargs:
                return await run_blocking(client.get_commit, **kwargs)
            return await run_blocking(client.get_commits, **kwargs)
        if action == "create":
            return await run_blocking(client.create_commit, **kwargs)
        if action == "diff":
            return await run_blocking(client.get_commit_diff, **kwargs)
        if action == "revert":
            return await run_blocking(client.revert_commit, **kwargs)
        if action == "get_comments":
            return await run_blocking(client.get_commit_comments, **kwargs)
        if action == "create_comment":
            return await run_blocking(client.create_commit_comment, **kwargs)
        if action == "get_discussions":
            return await run_blocking(client.get_commit_discussions, **kwargs)
        if action == "get_statuses":
            return await run_blocking(client.get_commit_statuses, **kwargs)
        if action == "post_status":
            return await run_blocking(client.post_build_status_to_commit, **kwargs)
        if action == "get_merge_requests":
            return await run_blocking(client.get_commit_merge_requests, **kwargs)
        if action == "get_gpg_signature":
            return await run_blocking(client.get_commit_gpg_signature, **kwargs)
        if action == "cherry_pick":
            return await run_blocking(client.cherry_pick_commit, **kwargs)
        if action == "get_references":
            return await run_blocking(client.get_commit_references, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get",
                "get_project",
                "create_project",
                "delete_project",
                "get_group",
                "create_group",
                "delete_group",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "token_id" in kwargs and "project_id" in kwargs:
                return await run_blocking(client.get_project_deploy_token, **kwargs)
            elif "token_id" in kwargs and "group_id" in kwargs:
                return await run_blocking(client.get_group_deploy_token, **kwargs)
            return await run_blocking(client.get_deploy_tokens, **kwargs)
        if action == "get_project":
            return await run_blocking(client.get_project_deploy_tokens, **kwargs)
        if action == "create_project":
            return await run_blocking(client.create_project_deploy_token, **kwargs)
        if action == "delete_project":
            return await run_blocking(client.delete_project_deploy_token, **kwargs)
        if action == "get_group":
            return await run_blocking(client.get_group_deploy_tokens, **kwargs)
        if action == "create_group":
            return await run_blocking(client.create_group_deploy_token, **kwargs)
        if action == "delete_group":
            return await run_blocking(client.delete_group_deploy_token, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get",
                "create",
                "update",
                "delete",
                "stop",
                "stop_stale",
                "delete_stopped",
                "get_protected",
                "protect",
                "update_protected",
                "unprotect",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "environment_id" in kwargs:
                return await run_blocking(client.get_environment, **kwargs)
            return await run_blocking(client.get_environments, **kwargs)
        if action == "create":
            return await run_blocking(client.create_environment, **kwargs)
        if action == "update":
            return await run_blocking(client.update_environment, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_environment, **kwargs)
        if action == "stop":
            return await run_blocking(client.stop_environment, **kwargs)
        if action == "stop_stale":
            return await run_blocking(client.stop_stale_environments, **kwargs)
        if action == "delete_stopped":
            return await run_blocking(client.delete_stopped_environments, **kwargs)
        if action == "get_protected":
            if "environment_name" in kwargs:
                return await run_blocking(client.get_protected_environment, **kwargs)
            return await run_blocking(client.get_protected_environments, **kwargs)
        if action == "protect":
            return await run_blocking(client.protect_environment, **kwargs)
        if action == "update_protected":
            return await run_blocking(client.update_protected_environment, **kwargs)
        if action == "unprotect":
            return await run_blocking(client.unprotect_environment, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get",
                "edit",
                "get_subgroups",
                "get_descendants",
                "get_projects",
                "get_merge_requests",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "group_id" in kwargs:
                return await run_blocking(client.get_group, **kwargs)
            return await run_blocking(client.get_groups, **kwargs)
        if action == "edit":
            return await run_blocking(client.edit_group, **kwargs)
        if action == "get_subgroups":
            return await run_blocking(client.get_group_subgroups, **kwargs)
        if action == "get_descendants":
            return await run_blocking(client.get_group_descendant_groups, **kwargs)
        if action == "get_projects":
            return await run_blocking(client.get_group_projects, **kwargs)
        if action == "get_merge_requests":
            return await run_blocking(client.get_group_merge_requests, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get_project_jobs",
                "get_job",
                "get_log",
                "cancel",
                "retry",
                "erase",
                "run",
                "get_pipeline_jobs",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_project_jobs":
            return await run_blocking(client.get_project_jobs, **kwargs)
        if action == "get_job":
            return await run_blocking(client.get_project_job, **kwargs)
        if action == "get_log":
            return await run_blocking(client.get_project_job_log, **kwargs)
        if action == "cancel":
            return await run_blocking(client.cancel_project_job, **kwargs)
        if action == "retry":
            return await run_blocking(client.retry_project_job, **kwargs)
        if action == "erase":
            return await run_blocking(client.erase_project_job, **kwargs)
        if action == "run":
            return await run_blocking(client.run_project_job, **kwargs)
        if action == "get_pipeline_jobs":
            return await run_blocking(client.get_pipeline_jobs, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get_group", "get_project"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_group":
            return await run_blocking(client.get_group_members, **kwargs)
        if action == "get_project":
            return await run_blocking(client.get_project_members, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {"create", "get", "get_project", "accept", "cancel_auto_merge"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "create":
            return await run_blocking(client.create_merge_request, **kwargs)
        if action == "get":
            if "merge_request_iid" in kwargs:
                return await run_blocking(client.get_project_merge_request, **kwargs)
            return await run_blocking(client.get_merge_requests, **kwargs)
        if action == "get_project":
            return await run_blocking(client.get_project_merge_requests, **kwargs)
        if action == "accept":
            return await run_blocking(client.accept_merge_request, **kwargs)
        if action == "cancel_auto_merge":
            return await run_blocking(
                client.cancel_merge_when_pipeline_succeeds, **kwargs
            )
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get_project_level",
                "create_project_level",
                "update_project_level",
                "delete_project_level",
                "get_mr_approvals",
                "get_mr_approval_state",
                "get_mr_level",
                "approve_mr",
                "unapprove_mr",
                "get_group_level",
                "edit_group_level",
                "edit_project_level",
                "set_mr_approvals",
                "get_project_rule",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_project_level":
            if "approval_rule_id" in kwargs:
                return await run_blocking(
                    client.get_project_level_merge_request_rule, **kwargs
                )
            return await run_blocking(
                client.get_project_level_merge_request_rules, **kwargs
            )
        if action == "create_project_level":
            return await run_blocking(client.create_project_level_rule, **kwargs)
        if action == "update_project_level":
            return await run_blocking(client.update_project_level_rule, **kwargs)
        if action == "delete_project_level":
            return await run_blocking(client.delete_project_level_rule, **kwargs)
        if action == "get_mr_approvals" or action == "get_mr_approval_state":
            return await run_blocking(
                client.get_approval_state_merge_requests, **kwargs
            )
        if action == "get_mr_level":
            return await run_blocking(client.get_merge_request_level_rules, **kwargs)
        if action == "approve_mr":
            return await run_blocking(client.approve_merge_request, **kwargs)
        if action == "unapprove_mr":
            return await run_blocking(client.unapprove_merge_request, **kwargs)
        if action == "get_group_level":
            return await run_blocking(client.get_group_level_rule, **kwargs)
        if action == "edit_group_level":
            return await run_blocking(client.edit_group_level_rule, **kwargs)
        if action == "edit_project_level":
            return await run_blocking(client.edit_project_level_rule, **kwargs)
        if action == "set_mr_approvals":
            return await run_blocking(client.merge_request_level_approvals, **kwargs)
        if action == "get_project_rule":
            return await run_blocking(client.get_project_level_rule, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "publish", "download"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            return await run_blocking(client.get_repository_packages, **kwargs)
        if action == "publish":
            return await run_blocking(client.publish_repository_package, **kwargs)
        if action == "download":
            return await run_blocking(client.download_repository_package, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(action, {"get", "run"}, service="gitlab-api")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "pipeline_id" in kwargs:
                return await run_blocking(client.get_pipeline, **kwargs)
            return await run_blocking(client.get_pipelines, **kwargs)
        if action == "run":
            return await run_blocking(client.run_pipeline, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get_all",
                "get",
                "get_triggered",
                "create",
                "edit",
                "take_ownership",
                "delete",
                "run",
                "create_variable",
                "delete_variable",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_all":
            return await run_blocking(client.get_pipeline_schedules, **kwargs)
        if action == "get":
            return await run_blocking(client.get_pipeline_schedule, **kwargs)
        if action == "get_triggered":
            return await run_blocking(
                client.get_pipelines_triggered_from_schedule, **kwargs
            )
        if action == "create":
            return await run_blocking(client.create_pipeline_schedule, **kwargs)
        if action == "edit":
            return await run_blocking(client.edit_pipeline_schedule, **kwargs)
        if action == "take_ownership":
            return await run_blocking(client.take_pipeline_schedule_ownership, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_pipeline_schedule, **kwargs)
        if action == "run":
            return await run_blocking(client.run_pipeline_schedule, **kwargs)
        if action == "create_variable":
            return await run_blocking(
                client.create_pipeline_schedule_variable, **kwargs
            )
        if action == "delete_variable":
            return await run_blocking(
                client.delete_pipeline_schedule_variable, **kwargs
            )
        raise ValueError(f"Unknown action: {action}")


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(tags={"projects"})
    async def gitlab_projects(
        action: str = Field(
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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get",
                "create",
                "delete",
                "get_nested_by_group",
                "get_contributors",
                "get_statistics",
                "edit",
                "share_with_group",
                "unshare_with_group",
                "archive",
                "unarchive",
                "get_project_groups",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "project_id" in kwargs or "id" in kwargs:
                return await run_blocking(client.get_project, **kwargs)
            return await run_blocking(client.get_projects, **kwargs)
        if action == "create":
            return await run_blocking(client.create_project, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_project, **kwargs)
        if action == "get_nested_by_group":
            return await run_blocking(client.get_nested_projects_by_group, **kwargs)
        if action == "get_contributors":
            return await run_blocking(client.get_project_contributors, **kwargs)
        if action == "get_statistics":
            return await run_blocking(client.get_project_statistics, **kwargs)
        if action == "edit":
            return await run_blocking(client.edit_project, **kwargs)
        if action == "share_with_group":
            return await run_blocking(client.share_project, **kwargs)
        if action == "unshare_with_group":
            return await run_blocking(client.delete_shared_project_link, **kwargs)
        if action == "archive":
            return await run_blocking(client.archive_project, **kwargs)
        if action == "unarchive":
            return await run_blocking(client.unarchive_project, **kwargs)
        if action == "get_project_groups":
            return await run_blocking(client.get_project_groups, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get",
                "get_latest",
                "get_latest_evidence",
                "get_latest_asset",
                "get_group_releases",
                "download_asset",
                "get_by_tag",
                "create",
                "create_evidence",
                "update",
                "delete",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "tag_name" in kwargs:
                return await run_blocking(client.get_release_by_tag, **kwargs)
            return await run_blocking(client.get_releases, **kwargs)
        if action == "get_latest":
            return await run_blocking(client.get_latest_release, **kwargs)
        if action == "get_latest_evidence":
            return await run_blocking(client.get_latest_release_evidence, **kwargs)
        if action == "get_latest_asset":
            return await run_blocking(client.get_latest_release_asset, **kwargs)
        if action == "get_group_releases":
            return await run_blocking(client.get_group_releases, **kwargs)
        if action == "download_asset":
            return await run_blocking(client.download_release_asset, **kwargs)
        if action == "get_by_tag":
            return await run_blocking(client.get_release_by_tag, **kwargs)
        if action == "create":
            return await run_blocking(client.create_release, **kwargs)
        if action == "create_evidence":
            return await run_blocking(client.create_release_evidence, **kwargs)
        if action == "update":
            return await run_blocking(client.update_release, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_release, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get_all",
                "get",
                "update_details",
                "pause",
                "get_jobs",
                "get_project",
                "enable_project",
                "delete_project",
                "get_group",
                "register",
                "delete",
                "verify_auth",
                "reset_gitlab_token",
                "reset_project_token",
                "reset_group_token",
                "reset_token",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_all":
            return await run_blocking(client.get_runners, **kwargs)
        if action == "get":
            return await run_blocking(client.get_runner, **kwargs)
        if action == "update_details":
            return await run_blocking(client.update_runner_details, **kwargs)
        if action == "pause":
            return await run_blocking(client.pause_runner, **kwargs)
        if action == "get_jobs":
            return await run_blocking(client.get_runner_jobs, **kwargs)
        if action == "get_project":
            return await run_blocking(client.get_project_runners, **kwargs)
        if action == "enable_project":
            return await run_blocking(client.enable_project_runner, **kwargs)
        if action == "delete_project":
            return await run_blocking(client.delete_project_runner, **kwargs)
        if action == "get_group":
            return await run_blocking(client.get_group_runners, **kwargs)
        if action == "register":
            return await run_blocking(client.register_new_runner, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_runner, **kwargs)
        if action == "verify_auth":
            return await run_blocking(client.verify_runner_authentication, **kwargs)
        if action == "reset_gitlab_token":
            return await run_blocking(client.reset_gitlab_runner_token, **kwargs)
        if action == "reset_project_token":
            return await run_blocking(client.reset_project_runner_token, **kwargs)
        if action == "reset_group_token":
            return await run_blocking(client.reset_group_runner_token, **kwargs)
        if action == "reset_token":
            return await run_blocking(client.reset_token, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {
                "get",
                "create",
                "delete",
                "get_protected",
                "get_protected_tag",
                "protect",
                "unprotect",
            },
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "tag" in kwargs or "tag_name" in kwargs:
                return await run_blocking(client.get_tag, **kwargs)
            return await run_blocking(client.get_tags, **kwargs)
        if action == "create":
            return await run_blocking(client.create_tag, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_tag, **kwargs)
        if action == "get_protected":
            return await run_blocking(client.get_protected_tags, **kwargs)
        if action == "get_protected_tag":
            return await run_blocking(client.get_protected_tag, **kwargs)
        if action == "protect":
            return await run_blocking(client.protect_tag, **kwargs)
        if action == "unprotect":
            return await run_blocking(client.unprotect_tag, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "create", "update", "delete"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "name" in kwargs or "label_id" in kwargs:
                return await run_blocking(client.get_label, **kwargs)
            return await run_blocking(client.get_labels, **kwargs)
        if action == "create":
            return await run_blocking(client.create_label, **kwargs)
        if action == "update":
            return await run_blocking(client.update_label, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_label, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "create", "update", "delete"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "milestone_id" in kwargs:
                return await run_blocking(client.get_milestone, **kwargs)
            return await run_blocking(client.get_milestones, **kwargs)
        if action == "create":
            return await run_blocking(client.create_milestone, **kwargs)
        if action == "update":
            return await run_blocking(client.update_milestone, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_milestone, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "create", "update", "delete"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "snippet_id" in kwargs:
                return await run_blocking(client.get_snippet, **kwargs)
            return await run_blocking(client.get_snippets, **kwargs)
        if action == "create":
            return await run_blocking(client.create_snippet, **kwargs)
        if action == "update":
            return await run_blocking(client.update_snippet, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_snippet, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "create", "update", "delete"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "note_id" in kwargs:
                return await run_blocking(client.get_note, **kwargs)
            return await run_blocking(client.get_notes, **kwargs)
        if action == "create":
            return await run_blocking(client.create_note, **kwargs)
        if action == "update":
            return await run_blocking(client.update_note, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_note, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "create", "update", "delete"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "epic_iid" in kwargs or "epic_id" in kwargs:
                return await run_blocking(client.get_epic, **kwargs)
            return await run_blocking(client.get_epics, **kwargs)
        if action == "create":
            return await run_blocking(client.create_epic, **kwargs)
        if action == "update":
            return await run_blocking(client.update_epic, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_epic, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {"get", "create", "update", "delete", "get_group"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            if "issue_iid" in kwargs or "issue_id" in kwargs:
                return await run_blocking(client.get_issue, **kwargs)
            return await run_blocking(client.get_issues, **kwargs)
        if action == "create":
            return await run_blocking(client.create_issue, **kwargs)
        if action == "update":
            return await run_blocking(client.update_issue, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_issue, **kwargs)
        if action == "get_group":
            return await run_blocking(client.get_group_issues, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {"get", "get_user", "create", "update", "delete"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            return await run_blocking(client.get_users, **kwargs)
        if action == "get_user":
            return await run_blocking(client.get_user, **kwargs)
        if action == "create":
            return await run_blocking(client.create_user, **kwargs)
        if action == "update":
            return await run_blocking(client.update_user, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_user, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {"get_list", "get", "create", "update", "delete", "upload_attachment"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_list":
            return await run_blocking(client.get_wiki_list, **kwargs)
        if action == "get":
            return await run_blocking(client.get_wiki_page, **kwargs)
        if action == "create":
            return await run_blocking(client.create_wiki_page, **kwargs)
        if action == "update":
            return await run_blocking(client.update_wiki_page, **kwargs)
        if action == "delete":
            return await run_blocking(client.delete_wiki_page, **kwargs)
        if action == "upload_attachment":
            return await run_blocking(client.upload_wiki_page_attachment, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, {"get", "get_namespace"}, service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get":
            return await run_blocking(client.get_namespaces, **kwargs)
        if action == "get_namespace":
            return await run_blocking(client.get_namespace, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action,
            {"dependencies", "get_project", "get_group", "get"},
            service="gitlab-api",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "dependencies":
            return await run_blocking(client.get_project_dependencies, **kwargs)
        if action == "get_project":
            return await run_blocking(client.get_project_vulnerabilities, **kwargs)
        if action == "get_group":
            return await run_blocking(client.get_group_vulnerabilities, **kwargs)
        if action == "get":
            return await run_blocking(client.get_vulnerability, **kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        except Exception as e:
            return {"error": f"Invalid variables JSON: {e}"}

        try:
            return await run_blocking(
                client.execute_gql,
                query_str=query,
                variables=vars_dict,
                operation_name=operation_name,
            )
        except Exception as e:
            return {"error": f"GraphQL execution failed: {str(e)}"}

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
        except Exception as e:
            return {"error": f"Failed to discover GitLab GraphQL schema: {str(e)}"}


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
        import inspect
        import json

        from pydantic import BaseModel

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        resolved = resolve_action(
            action, set(_GRAPHQL_OPS_ACTIONS), service="gitlab-api"
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        method = getattr(client, action)
        required = [
            p
            for p in inspect.signature(method).parameters.values()
            if p.default is inspect.Parameter.empty
            and p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
        ]
        try:
            if (
                len(required) == 1
                and isinstance(required[0].annotation, type)
                and issubclass(required[0].annotation, BaseModel)
            ):
                model = required[0].annotation(**kwargs)
                return await run_blocking(method, **{required[0].name: model})
            return await run_blocking(method, **kwargs)
        except Exception as e:
            return {"error": f"GraphQL operation '{action}' failed: {str(e)}"}


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
