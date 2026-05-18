#!/usr/bin/python
import warnings

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

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    config,
    create_mcp_server,
    ctx_confirm_destructive,
    ctx_progress,
)
from dotenv import find_dotenv, load_dotenv
from fastmcp import Context, FastMCP
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from gitlab_api.auth import get_client
from gitlab_api.gitlab_response_models import Response

__version__ = "25.24.0"
print(f"Gitlab MCP v{__version__}", file=sys.stderr)

logger = get_logger(name="mcp_server")
logger.setLevel(logging.DEBUG)


DEFAULT_GITLAB_SSL_VERIFY = to_boolean(string=os.getenv("GITLAB_SSL_VERIFY", "True"))
DEFAULT_GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
DEFAULT_GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", None)


def register_misc_tools(mcp: FastMCP):
    pass
    pass

    def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})


def register_branches_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"branches"}
    )
    async def gitlab_branches(
        action: str = Field(description="Action: 'get', 'create', 'delete'"),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Optional ID or path"
        ),  # type: ignore
        search: str | None = Field(
            default=None,
            description="Filter branches by name containing this term (for 'get')",
        ),
        regex: str | None = Field(
            default=None,
            description="Filter branches by regex pattern on name (for 'get')",
        ),
        branch: str | None = Field(
            default=None, description="Branch name (for 'get', 'create', 'delete')"
        ),
        ref: str | None = Field(
            default=None,
            description="Reference to create from (branch/tag/commit SHA) (for 'create')",
        ),
        delete_merged_branches: bool | None = Field(
            default=False,
            description="Delete all merged branches (excluding protected) (for 'delete')",
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage branches in a GitLab project (get, create, delete)."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "search": search,
            "regex": regex,
            "branch": branch,
            "ref": ref,
            "delete_merged_branches": delete_merged_branches,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            if branch:
                return client.get_branch(**kwargs)
            else:
                response = client.get_branches(**kwargs)
                return {"branches": response.data}  # type: ignore

        elif action == "create":
            if not branch or not ref:
                raise ValueError("branch and ref are required for 'create'")
            return client.create_branch(**kwargs)

        elif action == "delete":
            if not await ctx_confirm_destructive(ctx, "delete branch"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}  # type: ignore
            if ctx:
                await ctx_progress(ctx, 0, 100)
                await ctx.info(
                    f"Deleting {'merged branches' if delete_merged_branches else f'branch {branch}'} in project {project_id}"
                )
            if delete_merged_branches:
                response = client.delete_merged_branches(**kwargs)
            else:
                if not branch:
                    raise ValueError(
                        "branch is required when delete_merged_branches=False"
                    )
                response = client.delete_branch(**kwargs)
            if ctx:
                await ctx.info("Deletion complete")
                await ctx_progress(ctx, 100, 100)
            return response

        else:
            raise ValueError(f"Unknown action: {action}")


def register_protected_branches_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"protected_branches"},
    )
    async def gitlab_protected_branches(
        action: str = Field(description="Action: 'get', 'protect', 'unprotect'"),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        branch: str | None = Field(
            default=None,
            description="Name of the branch or wildcard (e.g., 'main' or '*-stable')",
        ),
        push_access_level: int | None = Field(
            default=None, description="Access level allowed to push"
        ),
        merge_access_level: int | None = Field(
            default=None, description="Access level allowed to merge"
        ),
        unprotect_access_level: int | None = Field(
            default=None, description="Access level allowed to unprotect"
        ),
        allow_force_push: bool | None = Field(
            default=None, description="Allow force push"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage protected branches in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "branch": branch,
            "push_access_level": push_access_level,
            "merge_access_level": merge_access_level,
            "unprotect_access_level": unprotect_access_level,
            "allow_force_push": allow_force_push,
            "name": branch,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            if not project_id:
                raise ValueError("project_id required")
            if branch:
                return client.get_protected_branch(project_id=project_id, branch=branch)
            return client.get_protected_branches(project_id=project_id)
        elif action == "protect":
            if not project_id or not branch:
                raise ValueError("project_id, branch required")
            return client.protect_branch(**kwargs)
        elif action == "unprotect":
            if not project_id or not branch:
                raise ValueError("project_id, branch required")
            if not await ctx_confirm_destructive(ctx, "unprotect_branch"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.unprotect_branch(project_id=project_id, name=branch)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_commits_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def gitlab_commits(
        action: str = Field(
            description="Action: 'get', 'create', 'diff', 'revert', 'get_comments', 'create_comment', 'get_discussions', 'get_statuses', 'post_status', 'get_merge_requests', 'get_gpg_signature'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Optional ID or path"
        ),
        commit_hash: str | None = Field(default=None, description="Commit SHA"),
        ref_name: str | None = Field(
            default=None, description="Branch, tag, or commit SHA to filter commits"
        ),
        since: str | None = Field(
            default=None, description="Only commits after this date (ISO 8601 format)"
        ),
        until: str | None = Field(
            default=None, description="Only commits before this date (ISO 8601 format)"
        ),
        path: str | None = Field(
            default=None, description="Only commits that include this file path"
        ),
        all: bool | None = Field(
            default=False, description="Include all commits across all branches"
        ),
        branch: str | None = Field(
            default=None, description="Branch name for the commit"
        ),
        commit_message: str | None = Field(default=None, description="Commit message"),
        actions: list[dict[str, str]] | None = Field(
            default=None, description="List of actions (create/update/delete files)"
        ),
        author_email: str | None = Field(
            default=None, description="Author email for the commit"
        ),
        author_name: str | None = Field(
            default=None, description="Author name for the commit"
        ),
        dry_run: bool | None = Field(
            default=None, description="Simulate the revert without applying"
        ),
        note: str | None = Field(default=None, description="Content of the comment"),
        line: int | None = Field(
            default=None, description="Line number in the file for the comment"
        ),
        line_type: str | None = Field(
            default=None, description="Type of line ('new' or 'old')"
        ),
        ref: str | None = Field(
            default=None, description="Filter statuses by reference (branch or tag)"
        ),
        stage: str | None = Field(
            default=None, description="Filter statuses by CI stage"
        ),
        name: str | None = Field(
            default=None, description="Filter statuses by job name"
        ),
        coverage: float | None = Field(default=None, description="Coverage percentage"),
        state: str | None = Field(
            default=None,
            description="State of the build (e.g., 'pending', 'running', 'success', 'failed')",
        ),
        target_url: str | None = Field(
            default=None, description="URL to link to the build"
        ),
        context: str | None = Field(
            default=None, description="Context of the status (e.g., 'ci/build')"
        ),
        description: str | None = Field(
            default=None, description="Description of the status"
        ),
        pipeline_id: int | None = Field(
            default=None, description="ID of the associated pipeline"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage commits in a GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "commit_hash": commit_hash,
            "ref_name": ref_name,
            "since": since,
            "until": until,
            "path": path,
            "all": all,
            "branch": branch,
            "commit_message": commit_message,
            "actions": actions,
            "author_email": author_email,
            "author_name": author_name,
            "dry_run": dry_run,
            "note": note,
            "line": line,
            "line_type": line_type,
            "ref": ref,
            "stage": stage,
            "name": name,
            "coverage": coverage,
            "state": state,
            "target_url": target_url,
            "context": context,
            "description": description,
            "pipeline_id": pipeline_id,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            if commit_hash:
                return client.get_commit(**kwargs)
            else:
                response = client.get_commits(**kwargs)
                return {"commits": response.data}
        elif action == "create":
            if not branch or not commit_message or not actions:
                raise ValueError(
                    "branch, commit_message, and actions are required for 'create'"
                )
            return client.create_commit(**kwargs)
        elif action == "diff":
            if not commit_hash:
                raise ValueError("commit_hash is required")
            return client.get_commit_diff(**kwargs)
        elif action == "revert":
            if not commit_hash or not branch:
                raise ValueError("commit_hash and branch are required")
            if not dry_run and ctx:
                if not await ctx_confirm_destructive(
                    ctx, f"revert commit {commit_hash}"
                ):
                    return {
                        "status": "cancelled",
                        "message": "Operation cancelled by user",
                    }
            return client.revert_commit(**kwargs)
        elif action == "get_comments":
            if not commit_hash:
                raise ValueError("commit_hash is required")
            return client.get_commit_comments(**kwargs)
        elif action == "create_comment":
            if not commit_hash or not note:
                raise ValueError("commit_hash and note are required")
            return client.create_commit_comment(**kwargs)
        elif action == "get_discussions":
            if not commit_hash:
                raise ValueError("commit_hash is required")
            return client.get_commit_discussions(**kwargs)
        elif action == "get_statuses":
            if not commit_hash:
                raise ValueError("commit_hash is required")
            return client.get_commit_statuses(**kwargs)
        elif action == "post_status":
            if not commit_hash or not state:
                raise ValueError("commit_hash and state are required")
            return client.post_build_status_to_commit(**kwargs)
        elif action == "get_merge_requests":
            if not commit_hash:
                raise ValueError("commit_hash is required")
            return client.get_commit_merge_requests(**kwargs)
        elif action == "get_gpg_signature":
            if not commit_hash:
                raise ValueError("commit_hash is required")
            return client.get_commit_gpg_signature(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_deploy_tokens_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"deploy_tokens"},
    )
    async def gitlab_deploy_tokens(
        action: str = Field(
            description="Action: 'get', 'get_project', 'create_project', 'delete_project', 'get_group', 'create_group', 'delete_group'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        group_id: int | str | None = Field(
            default=None, description="Group ID or path"
        ),
        token_id: int | None = Field(default=None, description="Deploy token ID"),
        name: str | None = Field(default=None, description="Name of the deploy token"),
        scopes: list[str] | None = Field(
            default=None,
            description="Scopes for the deploy token (e.g., ['read_repository'])",
        ),
        expires_at: str | None = Field(
            default=None, description="Expiration date (ISO 8601 format)"
        ),
        username: str | None = Field(
            default=None, description="Username associated with the token"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage deploy tokens in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "group_id": group_id,
            "token_id": token_id,
            "name": name,
            "scopes": scopes,
            "expires_at": expires_at,
            "username": username,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            return client.get_deploy_tokens(**kwargs)
        elif action == "get_project":
            if not project_id:
                raise ValueError("project_id is required")
            return client.get_project_deploy_tokens(**kwargs)
        elif action == "create_project":
            if not project_id or not name or not scopes:
                raise ValueError("project_id, name, and scopes are required")
            return client.create_project_deploy_token(**kwargs)
        elif action == "delete_project":
            if not project_id or not token_id:
                raise ValueError("project_id and token_id are required")
            if not await ctx_confirm_destructive(
                ctx, f"delete project deploy token {token_id}"
            ):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_project_deploy_token(**kwargs)
        elif action == "get_group":
            if not group_id:
                raise ValueError("group_id is required")
            return client.get_group_deploy_tokens(**kwargs)
        elif action == "create_group":
            if not group_id or not name or not scopes:
                raise ValueError("group_id, name, and scopes are required")
            return client.create_group_deploy_token(**kwargs)
        elif action == "delete_group":
            if not group_id or not token_id:
                raise ValueError("group_id and token_id are required")
            if not await ctx_confirm_destructive(
                ctx, f"delete group deploy token {token_id}"
            ):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_group_deploy_token(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_environments_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def gitlab_environments(
        action: str = Field(
            description="Action: 'get', 'create', 'update', 'delete', 'stop', 'stop_stale', 'delete_stopped', 'get_protected', 'protect', 'update_protected', 'unprotect'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        environment_id: int | None = Field(default=None, description="Environment ID"),
        name: str | None = Field(default=None, description="Name of the environment"),
        search: str | None = Field(
            default=None, description="Filter environments by search term in name"
        ),
        states: str | None = Field(
            default=None,
            description="Filter environments by state (e.g., 'available', 'stopped')",
        ),
        external_url: str | None = Field(
            default=None, description="External URL for the environment"
        ),
        older_than: str | None = Field(
            default=None,
            description="Filter environments older than this timestamp (ISO 8601 format)",
        ),
        required_approval_count: int | None = Field(
            default=None, description="Number of approvals required for deployment"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage environments in GitLab."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "environment_id": environment_id,
            "name": name,
            "search": search,
            "states": states,
            "external_url": external_url,
            "older_than": older_than,
            "required_approval_count": required_approval_count,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            return client.get_environments(**kwargs)
        elif action == "create":
            if not name:
                raise ValueError("name is required for 'create'")
            return client.create_environment(**kwargs)
        elif action == "update":
            if not environment_id:
                raise ValueError("environment_id is required")
            return client.update_environment(**kwargs)
        elif action == "delete":
            if not environment_id:
                raise ValueError("environment_id is required")
            if not await ctx_confirm_destructive(
                ctx, f"delete environment {environment_id}"
            ):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_environment(**kwargs)
        elif action == "stop":
            if not environment_id:
                raise ValueError("environment_id is required")
            return client.stop_environment(**kwargs)
        elif action == "stop_stale":
            if not older_than:
                raise ValueError("older_than is required")
            return client.stop_stale_environments(**kwargs)
        elif action == "delete_stopped":
            if not await ctx_confirm_destructive(ctx, "delete stopped environments"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_stopped_environments(**kwargs)
        elif action == "get_protected":
            return client.get_protected_environments(**kwargs)
        elif action == "protect":
            if not name:
                raise ValueError("name is required")
            return client.protect_environment(**kwargs)
        elif action == "update_protected":
            if not name:
                raise ValueError("name is required")
            return client.update_protected_environment(**kwargs)
        elif action == "unprotect":
            if not name:
                raise ValueError("name is required")
            if not await ctx_confirm_destructive(ctx, f"unprotect environment {name}"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.unprotect_environment(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_groups_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"}
    )
    async def gitlab_groups(
        action: str = Field(
            description="Action: 'get', 'edit', 'get_subgroups', 'get_descendants', 'get_projects', 'get_merge_requests'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        group_id: int | str | None = Field(
            default=None, description="Group ID or path"
        ),
        search: str | None = Field(
            default=None, description="Filter groups by search term in name or path"
        ),
        sort: str | None = Field(
            default=None, description="Sort order (e.g., 'asc', 'desc')"
        ),
        order_by: str | None = Field(
            default=None, description="Field to sort by (e.g., 'name', 'path')"
        ),
        owned: bool | None = Field(
            default=None, description="Filter groups owned by the authenticated user"
        ),
        min_access_level: int | None = Field(
            default=None,
            description="Filter groups by minimum access level (e.g., 10 for Guest)",
        ),
        top_level_only: bool | None = Field(
            default=None,
            description="Include only top-level groups (exclude subgroups)",
        ),
        name: str | None = Field(default=None, description="New name for the group"),
        path: str | None = Field(default=None, description="New path for the group"),
        description: str | None = Field(
            default=None, description="New description for the group"
        ),
        visibility: str | None = Field(
            default=None, description="New visibility level (e.g., 'public', 'private')"
        ),
        include_subgroups: bool | None = Field(
            default=None, description="Include projects from subgroups"
        ),
        state: str | None = Field(
            default=None,
            description="Filter merge requests by state (e.g., 'opened', 'closed')",
        ),
        scope: str | None = Field(
            default=None,
            description="Filter merge requests by scope (e.g., 'created_by_me')",
        ),
        milestone: str | None = Field(
            default=None, description="Filter merge requests by milestone title"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage groups in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "group_id": group_id,
            "search": search,
            "sort": sort,
            "order_by": order_by,
            "owned": owned,
            "min_access_level": min_access_level,
            "top_level_only": top_level_only,
            "name": name,
            "path": path,
            "description": description,
            "visibility": visibility,
            "include_subgroups": include_subgroups,
            "state": state,
            "scope": scope,
            "milestone": milestone,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            return client.get_groups(**kwargs)
        elif action == "edit":
            if not group_id:
                raise ValueError("group_id is required")
            return client.edit_group(**kwargs)
        elif action == "get_subgroups":
            if not group_id:
                raise ValueError("group_id is required")
            return client.get_group_subgroups(**kwargs)
        elif action == "get_descendants":
            if not group_id:
                raise ValueError("group_id is required")
            return client.get_group_descendant_groups(**kwargs)
        elif action == "get_projects":
            if not group_id:
                raise ValueError("group_id is required")
            return client.get_group_projects(**kwargs)
        elif action == "get_merge_requests":
            if not group_id:
                raise ValueError("group_id is required")
            return client.get_group_merge_requests(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_jobs_tools(mcp: FastMCP):
    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
    async def gitlab_jobs(
        action: str = Field(
            description="Action: 'get_project_jobs', 'get_log', 'cancel', 'retry', 'erase', 'run', 'get_pipeline_jobs'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        job_id: int | None = Field(default=None, description="Job ID"),
        scope: str | None = Field(
            default=None, description="Filter jobs by scope (e.g., 'success', 'failed')"
        ),
        include_retried: bool | None = Field(
            default=None, description="Include retried jobs"
        ),
        include_invisible: bool | None = Field(
            default=None,
            description="Include invisible jobs (e.g., from hidden pipelines)",
        ),
        pipeline_id: int | None = Field(default=None, description="Pipeline ID"),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage CI/CD jobs in GitLab."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "job_id": job_id,
            "scope": scope,
            "include_retried": include_retried,
            "include_invisible": include_invisible,
            "pipeline_id": pipeline_id,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get_project_jobs":
            return client.get_project_jobs(**kwargs)
        elif action == "get_log":
            if not job_id:
                raise ValueError("job_id is required")
            return client.get_project_job_log(**kwargs)
        elif action == "cancel":
            if not job_id:
                raise ValueError("job_id is required")
            return client.cancel_project_job(**kwargs)
        elif action == "retry":
            if not job_id:
                raise ValueError("job_id is required")
            return client.retry_project_job(**kwargs)
        elif action == "erase":
            if not job_id:
                raise ValueError("job_id is required")
            if not await ctx_confirm_destructive(ctx, f"erase job {job_id}"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.erase_project_job(**kwargs)
        elif action == "run":
            if not job_id:
                raise ValueError("job_id is required")
            return client.run_project_job(**kwargs)
        elif action == "get_pipeline_jobs":
            if not pipeline_id:
                raise ValueError("pipeline_id is required")
            return client.get_pipeline_jobs(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_members_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"members"}
    )
    async def gitlab_members(
        action: str = Field(description="Action: 'get_group', 'get_project'"),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        group_id: int | str | None = Field(
            default=None, description="Group ID or path"
        ),
        query: str | None = Field(
            default=None,
            description="Filter members by search term in name or username",
        ),
        user_ids: list[int] | None = Field(
            default=None, description="Filter members by user IDs"
        ),
        skip_users: list[int] | None = Field(
            default=None, description="Exclude specified user IDs"
        ),
        show_seat_info: bool | None = Field(
            default=None, description="Include seat information for members"
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage members in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "group_id": group_id,
            "query": query,
            "user_ids": user_ids,
            "skip_users": skip_users,
            "show_seat_info": show_seat_info,
            "project_id": project_id,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get_group":
            if not group_id:
                raise ValueError("group_id required")
            return client.get_group_members(**kwargs)
        elif action == "get_project":
            if not project_id:
                raise ValueError("project_id required")
            return client.get_project_members(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_merge_requests_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"merge_requests"},
    )
    async def gitlab_merge_requests(
        action: str = Field(description="Action: 'create', 'get', 'get_project'"),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        merge_id: int | None = Field(default=None, description="Merge request ID"),
        source_branch: str | None = Field(
            default=None, description="Source branch for the merge request"
        ),
        target_branch: str | None = Field(
            default=None, description="Target branch for the merge request"
        ),
        title: str | None = Field(
            default=None, description="Title of the merge request"
        ),
        description: str | None = Field(
            default=None, description="Description of the merge request"
        ),
        assignee_id: int | None = Field(
            default=None, description="ID of the user to assign the merge request to"
        ),
        reviewer_ids: list[int] | None = Field(
            default=None, description="IDs of users to set as reviewers"
        ),
        labels: list[str] | None = Field(
            default=None, description="Labels to apply to the merge request"
        ),
        state: str | None = Field(
            default=None,
            description="Filter merge requests by state (e.g., 'opened', 'closed')",
        ),
        scope: str | None = Field(
            default=None,
            description="Filter merge requests by scope (e.g., 'created_by_me')",
        ),
        milestone: str | None = Field(
            default=None, description="Filter merge requests by milestone title"
        ),
        view: str | None = Field(
            default=None, description="Filter merge requests by view (e.g., 'simple')"
        ),
        author_id: int | None = Field(
            default=None, description="Filter merge requests by author ID"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage merge requests in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "merge_id": merge_id,
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title,
            "description": description,
            "assignee_id": assignee_id,
            "reviewer_ids": reviewer_ids,
            "labels": labels,
            "state": state,
            "scope": scope,
            "milestone": milestone,
            "view": view,
            "author_id": author_id,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "create":
            if not project_id or not source_branch or not target_branch or not title:
                raise ValueError(
                    "project_id, source_branch, target_branch, title required"
                )
            return client.create_merge_request(**kwargs)
        elif action == "get":
            return client.get_merge_requests(**kwargs)
        elif action == "get_project":
            if not project_id:
                raise ValueError("project_id required")
            if merge_id:
                return client.get_project_merge_request(
                    project_id=project_id, merge_id=merge_id
                )
            else:
                response = client.get_project_merge_requests(**kwargs)
                return {"merge_requests": response.data}
        else:
            raise ValueError(f"Unknown action: {action}")


def register_merge_rules_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def gitlab_merge_rules(
        action: str = Field(
            description="Action: 'get_project_level', 'create_project_level', 'update_project_level', 'delete_project_level', 'get_mr_approvals', 'get_mr_approval_state', 'get_mr_level', 'approve_mr', 'unapprove_mr', 'get_group_level', 'edit_group_level', 'edit_project_level'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        approval_rule_id: int | None = Field(
            default=None, description="Approval rule ID"
        ),
        name: str | None = Field(default=None, description="Name of the approval rule"),
        approvals_required: int | None = Field(
            default=None, description="Number of approvals required"
        ),
        rule_type: str | None = Field(
            default=None, description="Type of rule (e.g., 'regular')"
        ),
        user_ids: list[int] | None = Field(
            default=None, description="List of user IDs required to approve"
        ),
        group_ids: list[int] | None = Field(
            default=None, description="List of group IDs required to approve"
        ),
        merge_request_iid: int | None = Field(
            default=None, description="Merge request IID"
        ),
        group_id: int | str | None = Field(
            default=None, description="Group ID or path"
        ),
        allow_author_approval: bool | None = Field(
            default=None,
            description="Whether authors can approve their own merge requests",
        ),
        allow_committer_approval: bool | None = Field(
            default=None, description="Whether committers can approve merge requests"
        ),
        allow_overrides_to_approver_list: bool | None = Field(
            default=None,
            description="Whether overrides to the approver list are allowed",
        ),
        minimum_approvals: int | None = Field(
            default=None, description="Minimum number of approvals required"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage merge rules in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "approval_rule_id": approval_rule_id,
            "name": name,
            "approvals_required": approvals_required,
            "rule_type": rule_type,
            "user_ids": user_ids,
            "group_ids": group_ids,
            "merge_request_iid": merge_request_iid,
            "group_id": group_id,
            "allow_author_approval": allow_author_approval,
            "allow_committer_approval": allow_committer_approval,
            "allow_overrides_to_approver_list": allow_overrides_to_approver_list,
            "minimum_approvals": minimum_approvals,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get_project_level":
            if not project_id:
                raise ValueError("project_id required")
            return client.get_project_level_merge_request_rules(**kwargs)
        elif action == "create_project_level":
            if not project_id or not name or approvals_required is None:
                raise ValueError("project_id, name, approvals_required required")
            return client.create_project_level_rule(**kwargs)
        elif action == "update_project_level":
            if (
                not project_id
                or not approval_rule_id
                or not name
                or approvals_required is None
            ):
                raise ValueError(
                    "project_id, approval_rule_id, name, approvals_required required"
                )
            return client.update_project_level_rule(**kwargs)
        elif action == "delete_project_level":
            if not project_id or not approval_rule_id:
                raise ValueError("project_id, approval_rule_id required")
            if not await ctx_confirm_destructive(ctx, "delete_project_level_rule"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_project_level_rule(**kwargs)
        elif action == "get_mr_approvals":
            if not project_id or not merge_request_iid:
                raise ValueError("project_id, merge_request_iid required")
            return client.merge_request_level_approvals(**kwargs)
        elif action == "get_mr_approval_state":
            if not project_id or not merge_request_iid:
                raise ValueError("project_id, merge_request_iid required")
            return client.get_approval_state_merge_requests(**kwargs)
        elif action == "get_mr_level":
            if not project_id or not merge_request_iid:
                raise ValueError("project_id, merge_request_iid required")
            return client.get_merge_request_level_rules(**kwargs)
        elif action == "approve_mr":
            if not project_id or not merge_request_iid:
                raise ValueError("project_id, merge_request_iid required")
            return client.approve_merge_request(**kwargs)
        elif action == "unapprove_mr":
            if not project_id or not merge_request_iid:
                raise ValueError("project_id, merge_request_iid required")
            return client.unapprove_merge_request(**kwargs)
        elif action == "get_group_level":
            if not group_id:
                raise ValueError("group_id required")
            return client.get_group_level_rule(**kwargs)
        elif action == "edit_group_level":
            if not group_id:
                raise ValueError("group_id required")
            return client.edit_group_level_rule(**kwargs)
        elif action == "edit_project_level":
            if not project_id:
                raise ValueError("project_id required")
            return client.edit_project_level_rule(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_packages_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"packages"}
    )
    async def gitlab_packages(
        action: str = Field(description="Action: 'get', 'publish', 'download'"),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        package_type: str | None = Field(
            default=None, description="Filter packages by type (e.g., 'npm', 'maven')"
        ),
        package_name: str | None = Field(
            default=None, description="Name of the package"
        ),
        package_version: str | None = Field(
            default=None, description="Version of the package"
        ),
        file_name: str | None = Field(
            default=None, description="Name of the package file"
        ),
        status: str | None = Field(
            default=None,
            description="Status of the package (e.g., 'default', 'hidden')",
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage packages in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "package_type": package_type,
            "package_name": package_name,
            "package_version": package_version,
            "file_name": file_name,
            "status": status,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            if not project_id:
                raise ValueError("project_id required")
            return client.get_repository_packages(**kwargs)
        elif action == "publish":
            if (
                not project_id
                or not package_name
                or not package_version
                or not file_name
            ):
                raise ValueError(
                    "project_id, package_name, package_version, file_name required"
                )
            return client.publish_repository_package(**kwargs)
        elif action == "download":
            if (
                not project_id
                or not package_name
                or not package_version
                or not file_name
            ):
                raise ValueError(
                    "project_id, package_name, package_version, file_name required"
                )
            return client.download_repository_package(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_pipelines_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"pipelines"}
    )
    async def gitlab_pipelines(
        action: str = Field(description="Action: 'get', 'run'"),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        pipeline_id: int | None = Field(default=None, description="Pipeline ID"),
        scope: str | None = Field(
            default=None,
            description="Filter pipelines by scope (e.g., 'running', 'branches')",
        ),
        status: str | None = Field(
            default=None,
            description="Filter pipelines by status (e.g., 'success', 'failed')",
        ),
        ref: str | None = Field(
            default=None,
            description="Filter pipelines by reference (e.g., branch or tag name)",
        ),
        source: str | None = Field(
            default=None,
            description="Filter pipelines by source (e.g., 'push', 'schedule')",
        ),
        updated_after: str | None = Field(
            default=None,
            description="Filter pipelines updated after this date (ISO 8601 format)",
        ),
        updated_before: str | None = Field(
            default=None,
            description="Filter pipelines updated before this date (ISO 8601 format)",
        ),
        variables: dict[str, str] | None = Field(
            default=None, description="Dictionary of pipeline variables"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage pipelines in GitLab."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "pipeline_id": pipeline_id,
            "scope": scope,
            "status": status,
            "ref": ref,
            "source": source,
            "updated_after": updated_after,
            "updated_before": updated_before,
            "variables": variables,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            if pipeline_id:
                return client.get_pipeline(
                    project_id=project_id, pipeline_id=pipeline_id
                )
            else:
                return client.get_pipelines(**kwargs)
        elif action == "run":
            if not ref:
                raise ValueError("ref is required for 'run'")
            return client.run_pipeline(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_pipeline_schedules_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def gitlab_pipeline_schedules(
        action: str = Field(
            description="Action: 'get_all', 'get', 'get_triggered', 'create', 'edit', 'take_ownership', 'delete', 'run', 'create_variable', 'delete_variable'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        pipeline_schedule_id: int | None = Field(
            default=None, description="Pipeline schedule ID"
        ),
        description: str | None = Field(
            default=None, description="Description of the pipeline schedule"
        ),
        ref: str | None = Field(
            default=None, description="Reference (e.g., branch or tag) for the pipeline"
        ),
        cron: str | None = Field(
            default=None,
            description="Cron expression defining the schedule (e.g., '0 0 * * *')",
        ),
        cron_timezone: str | None = Field(
            default=None, description="Timezone for the cron schedule (e.g., 'UTC')"
        ),
        active: bool | None = Field(
            default=None, description="Whether the schedule is active"
        ),
        key: str | None = Field(default=None, description="Key of the variable"),
        value: str | None = Field(default=None, description="Value of the variable"),
        variable_type: str | None = Field(
            default=None, description="Type of variable (e.g., 'env_var')"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage pipeline schedules in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "pipeline_schedule_id": pipeline_schedule_id,
            "description": description,
            "ref": ref,
            "cron": cron,
            "cron_timezone": cron_timezone,
            "active": active,
            "key": key,
            "value": value,
            "variable_type": variable_type,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get_all":
            if not project_id:
                raise ValueError("project_id required")
            return client.get_pipeline_schedules(**kwargs)
        elif action == "get":
            if not project_id or not pipeline_schedule_id:
                raise ValueError("project_id, pipeline_schedule_id required")
            return client.get_pipeline_schedule(**kwargs)
        elif action == "get_triggered":
            if not project_id or not pipeline_schedule_id:
                raise ValueError("project_id, pipeline_schedule_id required")
            return client.get_pipelines_triggered_from_schedule(**kwargs)
        elif action == "create":
            if not project_id or not description or not ref or not cron:
                raise ValueError("project_id, description, ref, cron required")
            return client.create_pipeline_schedule(**kwargs)
        elif action == "edit":
            if not project_id or not pipeline_schedule_id:
                raise ValueError("project_id, pipeline_schedule_id required")
            return client.edit_pipeline_schedule(**kwargs)
        elif action == "take_ownership":
            if not project_id or not pipeline_schedule_id:
                raise ValueError("project_id, pipeline_schedule_id required")
            return client.take_pipeline_schedule_ownership(**kwargs)
        elif action == "delete":
            if not project_id or not pipeline_schedule_id:
                raise ValueError("project_id, pipeline_schedule_id required")
            if not await ctx_confirm_destructive(ctx, "delete_pipeline_schedule"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_pipeline_schedule(**kwargs)
        elif action == "run":
            if not project_id or not pipeline_schedule_id:
                raise ValueError("project_id, pipeline_schedule_id required")
            return client.run_pipeline_schedule(**kwargs)
        elif action == "create_variable":
            if not project_id or not pipeline_schedule_id or not key or not value:
                raise ValueError(
                    "project_id, pipeline_schedule_id, key, value required"
                )
            return client.create_pipeline_schedule_variable(**kwargs)
        elif action == "delete_variable":
            if not project_id or not pipeline_schedule_id or not key:
                raise ValueError("project_id, pipeline_schedule_id, key required")
            if not await ctx_confirm_destructive(
                ctx, "delete_pipeline_schedule_variable"
            ):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_pipeline_schedule_variable(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def gitlab_projects(
        action: str = Field(
            description="Action: 'get', 'get_nested_by_group', 'get_contributors', 'get_statistics', 'edit', 'share_with_group', 'unshare_with_group'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        owned: bool | None = Field(
            default=None, description="Filter projects owned by the authenticated user"
        ),
        search: str | None = Field(
            default=None, description="Filter projects by search term in name or path"
        ),
        sort: str | None = Field(
            default=None,
            description="Sort projects by criteria (e.g., 'created_at', 'name')",
        ),
        visibility: str | None = Field(
            default=None,
            description="Filter projects by visibility (e.g., 'public', 'private')",
        ),
        group_id: int | str | None = Field(
            default=None, description="Group ID or path"
        ),
        name: str | None = Field(default=None, description="New name of the project"),
        description: str | None = Field(
            default=None, description="New description of the project"
        ),
        skip_groups: list[int] | None = Field(
            default=None, description="List of group IDs to exclude"
        ),
        group_access: str | None = Field(
            default=None,
            description="Access level for the group (e.g., 'guest', 'developer', 'maintainer')",
        ),
        expires_at: str | None = Field(
            default=None, description="Expiration date for the share in ISO 8601 format"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage projects in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "owned": owned,
            "search": search,
            "sort": sort,
            "visibility": visibility,
            "group_id": group_id,
            "name": name,
            "description": description,
            "skip_groups": skip_groups,
            "group_access": group_access,
            "expires_at": expires_at,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            if project_id:
                return client.get_project(project_id=project_id)
            else:
                response = client.get_projects(**kwargs)
                return response
        elif action == "get_nested_by_group":
            if not group_id:
                raise ValueError("group_id is required")
            return client.get_nested_projects_by_group(**kwargs)
        elif action == "get_contributors":
            if not project_id:
                raise ValueError("project_id is required")
            return client.get_project_contributors(**kwargs)
        elif action == "get_statistics":
            if not project_id:
                raise ValueError("project_id is required")
            return client.get_project_statistics(**kwargs)
        elif action == "edit":
            if not project_id:
                raise ValueError("project_id is required")
            return client.edit_project(**kwargs)
        elif action == "share_with_group":
            if not project_id or not group_id or not group_access:
                raise ValueError("project_id, group_id, group_access are required")
            return client.share_project(**kwargs)
        elif action == "unshare_with_group":
            if not project_id or not group_id:
                raise ValueError("project_id, group_id are required")
            if not await ctx_confirm_destructive(
                ctx, f"unshare project {project_id} with group {group_id}"
            ):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_shared_project_link(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_releases_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def gitlab_releases(
        action: str = Field(
            description="Action: 'get', 'get_latest', 'get_latest_evidence', 'get_latest_asset', 'get_group_releases', 'download_asset', 'get_by_tag', 'create', 'create_evidence', 'update', 'delete'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        group_id: int | str | None = Field(
            default=None, description="Group ID or path (for group releases)"
        ),
        tag_name: str | None = Field(
            default=None, description="Tag name of the release"
        ),
        name: str | None = Field(default=None, description="Release name"),
        description: str | None = Field(
            default=None, description="Release description"
        ),
        ref: str | None = Field(
            default=None, description="Commit SHA or branch name (for create)"
        ),
        link_id: int | None = Field(default=None, description="ID of the asset link"),
        filepath: str | None = Field(
            default=None, description="Filepath for downloaded asset"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage releases in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "group_id": group_id,
            "tag_name": tag_name,
            "name": name,
            "description": description,
            "ref": ref,
            "link_id": link_id,
            "filepath": filepath,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            if not project_id:
                raise ValueError("project_id required")
            return client.get_releases(project_id=project_id)
        elif action == "get_latest":
            if not project_id:
                raise ValueError("project_id required")
            return client.get_latest_release(project_id=project_id)
        elif action == "get_latest_evidence":
            if not project_id:
                raise ValueError("project_id required")
            return client.get_latest_release_evidence(project_id=project_id)
        elif action == "get_latest_asset":
            if not project_id or not link_id or not filepath:
                raise ValueError("project_id, link_id, filepath required")
            return client.get_latest_release_asset(
                project_id=project_id, link_id=link_id, filepath=filepath
            )
        elif action == "get_group_releases":
            if not group_id:
                raise ValueError("group_id required")
            return client.get_group_releases(group_id=group_id)
        elif action == "download_asset":
            if not group_id or not tag_name or not link_id or not filepath:
                raise ValueError("group_id, tag_name, link_id, filepath required")
            return client.download_release_asset(
                group_id=group_id, tag_name=tag_name, link_id=link_id, filepath=filepath
            )
        elif action == "get_by_tag":
            if not project_id or not tag_name:
                raise ValueError("project_id, tag_name required")
            return client.get_release_by_tag(project_id=project_id, tag_name=tag_name)
        elif action == "create":
            if not project_id or not name or not tag_name or not description:
                raise ValueError("project_id, name, tag_name, description required")
            return client.create_release(**kwargs)
        elif action == "create_evidence":
            if not project_id or not tag_name:
                raise ValueError("project_id, tag_name required")
            return client.create_release_evidence(
                project_id=project_id, tag_name=tag_name
            )
        elif action == "update":
            if not project_id or not tag_name:
                raise ValueError("project_id, tag_name required")
            return client.update_release(**kwargs)
        elif action == "delete":
            if not project_id or not tag_name:
                raise ValueError("project_id, tag_name required")
            if not await ctx_confirm_destructive(ctx, "delete_release"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_release(project_id=project_id, tag_name=tag_name)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_runners_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def gitlab_runners(
        action: str = Field(
            description="Action: 'get_all', 'update_details', 'pause', 'get_jobs', 'get_project', 'enable_project', 'delete_project', 'get_group', 'register', 'delete', 'verify_auth', 'reset_gitlab_token', 'reset_project_token', 'reset_group_token', 'reset_token'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        runner_id: int | None = Field(
            default=None, description="ID of the runner to retrieve"
        ),
        scope: str | None = Field(
            default=None, description="Filter runners by scope (e.g., 'active')"
        ),
        type: str | None = Field(
            default=None, description="Filter runners by type (e.g., 'instance_type')"
        ),
        status: str | None = Field(
            default=None, description="Filter runners by status (e.g., 'online')"
        ),
        tag_list: list[str] | None = Field(
            default=None, description="Filter runners by tags"
        ),
        description: str | None = Field(
            default=None, description="New description of the runner"
        ),
        active: bool | None = Field(
            default=None, description="Whether the runner is active"
        ),
        run_untagged: bool | None = Field(
            default=None, description="Whether the runner can run untagged jobs"
        ),
        locked: bool | None = Field(
            default=None, description="Whether the runner is locked"
        ),
        access_level: str | None = Field(
            default=None,
            description="Access level of the runner (e.g., 'ref_protected')",
        ),
        maximum_timeout: int | None = Field(
            default=None, description="Maximum timeout for the runner in seconds"
        ),
        sort: str | None = Field(
            default=None, description="Sort jobs by criteria (e.g., 'created_at')"
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        group_id: int | str | None = Field(
            default=None, description="Group ID or path"
        ),
        token: str | None = Field(
            default=None, description="Registration token for the runner"
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage runners in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "runner_id": runner_id,
            "scope": scope,
            "type": type,
            "status": status,
            "tag_list": tag_list,
            "description": description,
            "active": active,
            "run_untagged": run_untagged,
            "locked": locked,
            "access_level": access_level,
            "maximum_timeout": maximum_timeout,
            "sort": sort,
            "project_id": project_id,
            "group_id": group_id,
            "token": token,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get_all":
            return client.get_runners(**kwargs)
        elif action == "update_details":
            if not runner_id:
                raise ValueError("runner_id required")
            return client.update_runner_details(**kwargs)
        elif action == "pause":
            if not runner_id:
                raise ValueError("runner_id required")
            return client.pause_runner(**kwargs)
        elif action == "get_jobs":
            if not runner_id:
                raise ValueError("runner_id required")
            return client.get_runner_jobs(**kwargs)
        elif action == "get_project":
            if not project_id:
                raise ValueError("project_id required")
            return client.get_project_runners(**kwargs)
        elif action == "enable_project":
            if not project_id or not runner_id:
                raise ValueError("project_id, runner_id required")
            return client.enable_project_runner(**kwargs)
        elif action == "delete_project":
            if not project_id or not runner_id:
                raise ValueError("project_id, runner_id required")
            if not await ctx_confirm_destructive(ctx, "delete_project_runner"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_project_runner(**kwargs)
        elif action == "get_group":
            if not group_id:
                raise ValueError("group_id required")
            return client.get_group_runners(**kwargs)
        elif action == "register":
            if not token:
                raise ValueError("token required")
            return client.register_new_runner(**kwargs)
        elif action == "delete":
            if not runner_id:
                raise ValueError("runner_id required")
            if not await ctx_confirm_destructive(ctx, "delete_runner"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_runner(**kwargs)
        elif action == "verify_auth":
            if not token:
                raise ValueError("token required")
            return client.verify_runner_authentication(**kwargs)
        elif action == "reset_gitlab_token":
            if not await ctx_confirm_destructive(ctx, "reset_gitlab_runner_token"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.reset_gitlab_runner_token(**kwargs)
        elif action == "reset_project_token":
            if not project_id:
                raise ValueError("project_id required")
            if not await ctx_confirm_destructive(ctx, "reset_project_runner_token"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.reset_project_runner_token(**kwargs)
        elif action == "reset_group_token":
            if not group_id:
                raise ValueError("group_id required")
            if not await ctx_confirm_destructive(ctx, "reset_group_runner_token"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.reset_group_runner_token(**kwargs)
        elif action == "reset_token":
            if not runner_id:
                raise ValueError("runner_id required")
            if not await ctx_confirm_destructive(ctx, "reset_token"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.reset_token(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_tags_tools(mcp: FastMCP):
    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
    async def gitlab_tags(
        action: str = Field(
            description="Action: 'get', 'create', 'delete', 'get_protected', 'get_protected_tag', 'protect', 'unprotect'"
        ),
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        project_id: int | str | None = Field(
            default=None, description="Project ID or path"
        ),
        name: str | None = Field(
            default=None, description="Name of the tag to retrieve (e.g., 'v1.0.0')"
        ),
        search: str | None = Field(
            default=None, description="Filter tags by search term in name"
        ),
        sort: str | None = Field(
            default=None, description="Sort tags by criteria (e.g., 'name', 'updated')"
        ),
        ref: str | None = Field(
            default=None, description="Reference (e.g., branch or commit SHA) to tag"
        ),
        message: str | None = Field(default=None, description="Tag message"),
        release_description: str | None = Field(
            default=None, description="Release description associated with the tag"
        ),
        create_access_level: str | None = Field(
            default=None,
            description="Access level for creating the tag (e.g., 'maintainer')",
        ),
        allowed_to_create: list[dict] | None = Field(
            default=None,
            description="List of users or groups allowed to create the tag",
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        ctx: Context | None = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response | dict[str, Any]:
        """Manage tags in GitLab."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )

        args_dict = {
            "project_id": project_id,
            "name": name,
            "search": search,
            "sort": sort,
            "ref": ref,
            "message": message,
            "release_description": release_description,
            "create_access_level": create_access_level,
            "allowed_to_create": allowed_to_create,
        }
        kwargs = {k: v for k, v in args_dict.items() if v is not None}

        if action == "get":
            if not project_id:
                raise ValueError("project_id required")
            if name:
                return client.get_tag(project_id=project_id, name=name)
            return client.get_tags(**kwargs)
        elif action == "create":
            if not project_id or not name or not ref:
                raise ValueError("project_id, name, ref required")
            return client.create_tag(**kwargs)
        elif action == "delete":
            if not project_id or not name:
                raise ValueError("project_id, name required")
            if not await ctx_confirm_destructive(ctx, "delete_tag"):
                return {"status": "cancelled", "message": "Operation cancelled by user"}
            return client.delete_tag(**kwargs)
        elif action == "get_protected":
            if not project_id:
                raise ValueError("project_id required")
            return client.get_protected_tags(**kwargs)
        elif action == "get_protected_tag":
            if not project_id or not name:
                raise ValueError("project_id, name required")
            return client.get_protected_tag(**kwargs)
        elif action == "protect":
            if not project_id or not name:
                raise ValueError("project_id, name required")
            return client.protect_tag(**kwargs)
        elif action == "unprotect":
            if not project_id or not name:
                raise ValueError("project_id, name required")
            return client.unprotect_tag(**kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")


def register_custom_api_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"custom-api"},
    )
    async def api_request(
        gitlab_instance: str | None = Field(
            default=os.environ.get("GITLAB_URL", DEFAULT_GITLAB_URL),
            description="URL of GitLab instance with /api/v4/ suffix",
        ),
        access_token: str | None = Field(
            default=os.environ.get("GITLAB_TOKEN", DEFAULT_GITLAB_TOKEN),
            description="GitLab access token",
        ),
        verify: bool | None = Field(
            default=to_boolean(
                os.environ.get("GITLAB_VERIFY", DEFAULT_GITLAB_SSL_VERIFY)
            ),
            description="Verify SSL certificate",
        ),
        method: str | None = Field(
            description="The HTTP method to use ('GET', 'POST', 'PUT', 'DELETE')"
        ),
        endpoint: str | None = Field(
            description="The API endpoint to send the request to"
        ),
        data: dict[str, Any] | None = Field(
            default=None,
            description="Data to include in the request body (for non-JSON payloads)",
        ),
        json: dict[str, Any] | None = Field(
            default=None, description="JSON data to include in the request body"
        ),
        ctx: Context | None = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response | dict[str, Any]:
        """
        Make a custom API request to a GitLab instance.
        """
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_TOKEN] Access Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance or DEFAULT_GITLAB_URL,
            token=access_token,
            verify=bool(verify),
            config=config,
        )
        response = client.api_request(
            method=method, endpoint=endpoint, data=data, json=json
        )
        if ctx:
            await ctx.info("API Complete")
        return response


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


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the GitLab MCP instance, args, and middlewares."""
    load_dotenv(find_dotenv())
    os.environ["FASTMCP_LOG_LEVEL"] = "ERROR"
    os.environ["TERM"] = "dumb"
    os.environ["NO_COLOR"] = "1"

    args, mcp, middlewares = create_mcp_server(
        name="GitLab",
        version=__version__,
        instructions="GitLab API MCP Server - Manage projects, issues, merge requests, branches, and more.",
    )

    DEFAULT_MISCTOOL = to_boolean(os.getenv("MISCTOOL", "True"))
    if DEFAULT_MISCTOOL:
        register_misc_tools(mcp)
    DEFAULT_BRANCHESTOOL = to_boolean(os.getenv("BRANCHESTOOL", "True"))
    if DEFAULT_BRANCHESTOOL:
        register_branches_tools(mcp)
    DEFAULT_COMMITSTOOL = to_boolean(os.getenv("COMMITSTOOL", "True"))
    if DEFAULT_COMMITSTOOL:
        register_commits_tools(mcp)
    DEFAULT_DEPLOY_TOKENSTOOL = to_boolean(os.getenv("DEPLOY_TOKENSTOOL", "True"))
    if DEFAULT_DEPLOY_TOKENSTOOL:
        register_deploy_tokens_tools(mcp)
    DEFAULT_ENVIRONMENTSTOOL = to_boolean(os.getenv("ENVIRONMENTSTOOL", "True"))
    if DEFAULT_ENVIRONMENTSTOOL:
        register_environments_tools(mcp)
    DEFAULT_GROUPSTOOL = to_boolean(os.getenv("GROUPSTOOL", "True"))
    if DEFAULT_GROUPSTOOL:
        register_groups_tools(mcp)
    DEFAULT_JOBSTOOL = to_boolean(os.getenv("JOBSTOOL", "True"))
    if DEFAULT_JOBSTOOL:
        register_jobs_tools(mcp)
    DEFAULT_MEMBERSTOOL = to_boolean(os.getenv("MEMBERSTOOL", "True"))
    if DEFAULT_MEMBERSTOOL:
        register_members_tools(mcp)
    DEFAULT_MERGE_REQUESTSTOOL = to_boolean(os.getenv("MERGE_REQUESTSTOOL", "True"))
    if DEFAULT_MERGE_REQUESTSTOOL:
        register_merge_requests_tools(mcp)
    DEFAULT_MERGE_RULESTOOL = to_boolean(os.getenv("MERGE_RULESTOOL", "True"))
    if DEFAULT_MERGE_RULESTOOL:
        register_merge_rules_tools(mcp)
    DEFAULT_PACKAGESTOOL = to_boolean(os.getenv("PACKAGESTOOL", "True"))
    if DEFAULT_PACKAGESTOOL:
        register_packages_tools(mcp)
    DEFAULT_PIPELINESTOOL = to_boolean(os.getenv("PIPELINESTOOL", "True"))
    if DEFAULT_PIPELINESTOOL:
        register_pipelines_tools(mcp)
    DEFAULT_PIPELINE_SCHEDULESTOOL = to_boolean(
        os.getenv("PIPELINE_SCHEDULESTOOL", "True")
    )
    if DEFAULT_PIPELINE_SCHEDULESTOOL:
        register_pipeline_schedules_tools(mcp)
    DEFAULT_PROJECTSTOOL = to_boolean(os.getenv("PROJECTSTOOL", "True"))
    if DEFAULT_PROJECTSTOOL:
        register_projects_tools(mcp)
    DEFAULT_PROTECTED_BRANCHESTOOL = to_boolean(
        os.getenv("PROTECTED_BRANCHESTOOL", "True")
    )
    if DEFAULT_PROTECTED_BRANCHESTOOL:
        register_protected_branches_tools(mcp)
    DEFAULT_RELEASESTOOL = to_boolean(os.getenv("RELEASESTOOL", "True"))
    if DEFAULT_RELEASESTOOL:
        register_releases_tools(mcp)
    DEFAULT_RUNNERSTOOL = to_boolean(os.getenv("RUNNERSTOOL", "True"))
    if DEFAULT_RUNNERSTOOL:
        register_runners_tools(mcp)  # type: ignore
    DEFAULT_TAGSTOOL = to_boolean(os.getenv("TAGSTOOL", "True"))
    if DEFAULT_TAGSTOOL:
        register_tags_tools(mcp)
    DEFAULT_CUSTOM_APITOOL = to_boolean(os.getenv("CUSTOM_APITOOL", "True"))
    if DEFAULT_CUSTOM_APITOOL:
        register_custom_api_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    registered_tags: list[str] = []
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
