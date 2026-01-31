#!/usr/bin/python
# coding: utf-8

import os
import argparse
import sys
import logging
from typing import Optional, List, Dict, Union, Any

import requests
from pydantic import Field
from eunomia_mcp.middleware import EunomiaMcpMiddleware
from fastmcp import FastMCP, Context
from fastmcp.server.auth.oidc_proxy import OIDCProxy
from fastmcp.server.auth import OAuthProxy, RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier, StaticTokenVerifier
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.utilities.logging import get_logger
from gitlab_api.gitlab_response_models import Response
from gitlab_api.utils import to_boolean, to_integer
from gitlab_api.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
    get_client,
)
from starlette.requests import Request
from starlette.responses import JSONResponse

__version__ = "25.14.16"
print(f"Gitlab MCP v{__version__}")

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)

config = {
    "enable_delegation": to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
    "audience": os.environ.get("AUDIENCE", None),
    "delegated_scopes": os.environ.get("DELEGATED_SCOPES", "api"),
    "token_endpoint": None,  # Will be fetched dynamically from OIDC config
    "oidc_client_id": os.environ.get("OIDC_CLIENT_ID", None),
    "oidc_client_secret": os.environ.get("OIDC_CLIENT_SECRET", None),
    "oidc_config_url": os.environ.get("OIDC_CONFIG_URL", None),
    "jwt_jwks_uri": os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI", None),
    "jwt_issuer": os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER", None),
    "jwt_audience": os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE", None),
    "jwt_algorithm": os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM", None),
    "jwt_secret": os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY", None),
    "jwt_required_scopes": os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES", None),
}

DEFAULT_TRANSPORT = os.getenv("TRANSPORT", "stdio")
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "8000"))


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    # Branches Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"branches"}
    )
    async def get_branches(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        search: Optional[str] = Field(
            description="Filter branches by name containing this term", default=None
        ),
        regex: Optional[str] = Field(
            description="Filter branches by regex pattern on name", default=None
        ),
        branch: Optional[str] = Field(description="Branch name", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Get branches in a GitLab project, optionally filtered."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify"]
        }
        if branch:
            response = client.get_branch(**kwargs)
            return response.data
        else:
            response = client.get_branches(**kwargs)
            return {"branches": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"branches"}
    )
    async def create_branch(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        branch: str = Field(description="New branch name", default=None),
        ref: str = Field(
            description="Reference to create from (branch/tag/commit SHA)", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Create a new branch in a GitLab project from a reference."""
        if not project_id or not branch or not ref:
            raise ValueError("project_id, branch, and ref are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify"]
        }
        response = client.create_branch(**kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"branches"}
    )
    async def delete_branch(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        branch: Optional[str] = Field(
            description="Branch name to delete", default=None
        ),
        delete_merged_branches: Optional[bool] = Field(
            description="Delete all merged branches (excluding protected)",
            default=False,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a branch or all merged branches in a GitLab project.

        - If delete_merged_branches=True, deletes all merged branches (excluding protected).
        - Otherwise, deletes the specified branch.
        """
        if not project_id:
            raise ValueError("project_id is required")
        if not delete_merged_branches and not branch:
            raise ValueError("branch is required when delete_merged_branches=False")
        if ctx:
            await ctx.info(
                f"Deleting {'merged branches' if delete_merged_branches else f'branch {branch}'} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        if delete_merged_branches:
            response = client.delete_merged_branches(**kwargs)
        else:
            response = client.delete_branch(**kwargs)
        if ctx:
            await ctx.info("Deletion complete")
        return response.data

    # Commits Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def get_commits(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: Optional[str] = Field(description="Commit SHA", default=None),
        ref_name: Optional[str] = Field(
            description="Branch, tag, or commit SHA to filter commits", default=None
        ),
        since: Optional[str] = Field(
            description="Only commits after this date (ISO 8601 format)", default=None
        ),
        until: Optional[str] = Field(
            description="Only commits before this date (ISO 8601 format)", default=None
        ),
        path: Optional[str] = Field(
            description="Only commits that include this file path", default=None
        ),
        all: Optional[bool] = Field(
            description="Include all commits across all branches", default=False
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Get commits in a GitLab project, optionally filtered."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify"]
        }
        if commit_hash:
            response = client.get_commit(**kwargs)
            return response.data
        else:
            response = client.get_commits(**kwargs)
            return {"commits": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def create_commit(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        branch: str = Field(description="Branch name for the commit", default=None),
        commit_message: str = Field(description="Commit message", default=None),
        actions: List[Dict[str, str]] = Field(
            description="List of actions (create/update/delete files)", default=None
        ),
        author_email: Optional[str] = Field(
            description="Author email for the commit", default=None
        ),
        author_name: Optional[str] = Field(
            description="Author name for the commit", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Create a new commit in a GitLab project."""
        if not project_id or not branch or not commit_message or not actions:
            raise ValueError(
                "project_id, branch, commit_message, and actions are required"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify"]
        }
        response = client.create_commit(**kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def get_commit_diff(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: str = Field(description="Commit SHA", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Get the diff of a specific commit in a GitLab project."""
        if not project_id or not commit_hash:
            raise ValueError("project_id and commit_hash are required")
        if ctx:
            await ctx.info(
                f"Fetching diff for commit {commit_hash} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.get_commit_diff(**kwargs)
        if ctx:
            await ctx.info("Diff retrieval complete")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def revert_commit(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: str = Field(description="Commit SHA to revert", default=None),
        branch: str = Field(
            description="Target branch to apply the revert", default=None
        ),
        dry_run: Optional[bool] = Field(
            description="Simulate the revert without applying", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Revert a commit in a target branch in a GitLab project.

        - If dry_run=True, simulates the revert without applying changes.
        - Returns the revert commit details or simulation result.
        """
        if not project_id or not commit_hash or not branch:
            raise ValueError("project_id, commit_hash, and branch are required")

        if not dry_run and ctx:
            message = f"Are you sure you want to REVERT commit {commit_hash} in branch {branch} of project {project_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return "Operation cancelled by user."

        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "commit_hash",
                "ctx",
            ]
        }
        response = client.revert_commit(
            project_id=project_id, commit_hash=commit_hash, **kwargs
        )
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def get_commit_comments(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: str = Field(description="Commit SHA", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Retrieve comments on a specific commit in a GitLab project."""
        if not project_id or not commit_hash:
            raise ValueError("project_id and commit_hash are required")
        if ctx:
            await ctx.info(
                f"Fetching comments for commit {commit_hash} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.get_commit_comments(**kwargs)
        if ctx:
            await ctx.info("Comments retrieval complete")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def create_commit_comment(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: str = Field(description="Commit SHA", default=None),
        note: str = Field(description="Content of the comment", default=None),
        path: Optional[str] = Field(
            description="File path to associate with the comment", default=None
        ),
        line: Optional[int] = Field(
            description="Line number in the file for the comment", default=None
        ),
        line_type: Optional[str] = Field(
            description="Type of line ('new' or 'old')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a new comment on a specific commit in a GitLab project."""
        if not project_id or not commit_hash or not note:
            raise ValueError("project_id, commit_hash, and note are required")
        if ctx:
            await ctx.info(
                f"Creating comment on commit {commit_hash} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.create_commit_comment(
            project_id=project_id, commit_hash=commit_hash, **kwargs
        )
        if ctx:
            await ctx.info("Comment creation complete")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def get_commit_discussions(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: str = Field(description="Commit SHA", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Retrieve discussions (threaded comments) on a specific commit in a GitLab project."""
        if not project_id or not commit_hash:
            raise ValueError("project_id and commit_hash are required")
        if ctx:
            await ctx.info(
                f"Fetching discussions for commit {commit_hash} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.get_commit_discussions(**kwargs)
        if ctx:
            await ctx.info("Discussions retrieval complete")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def get_commit_statuses(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: str = Field(description="Commit SHA", default=None),
        ref: Optional[str] = Field(
            description="Filter statuses by reference (branch or tag)", default=None
        ),
        stage: Optional[str] = Field(
            description="Filter statuses by CI stage", default=None
        ),
        name: Optional[str] = Field(
            description="Filter statuses by job name", default=None
        ),
        coverage: Optional[bool] = Field(
            description="Include coverage information", default=None
        ),
        all: Optional[bool] = Field(description="Include all statuses", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Retrieve build/CI statuses for a specific commit in a GitLab project."""
        if not project_id or not commit_hash:
            raise ValueError("project_id and commit_hash are required")
        if ctx:
            await ctx.info(
                f"Fetching statuses for commit {commit_hash} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.get_commit_statuses(
            project_id=project_id, commit_hash=commit_hash, **kwargs
        )
        if ctx:
            await ctx.info("Statuses retrieval complete")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def post_build_status_to_commit(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: str = Field(description="Commit SHA", default=None),
        state: str = Field(
            description="State of the build (e.g., 'pending', 'running', 'success', 'failed')",
            default=None,
        ),
        target_url: Optional[str] = Field(
            description="URL to link to the build", default=None
        ),
        context: Optional[str] = Field(
            description="Context of the status (e.g., 'ci/build')", default=None
        ),
        description: Optional[str] = Field(
            description="Description of the status", default=None
        ),
        coverage: Optional[float] = Field(
            description="Coverage percentage", default=None
        ),
        pipeline_id: Optional[int] = Field(
            description="ID of the associated pipeline", default=None
        ),
        ref: Optional[str] = Field(
            description="Reference (branch or tag) for the status", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Post a build/CI status to a specific commit in a GitLab project."""
        if not project_id or not commit_hash or not state:
            raise ValueError("project_id, commit_hash, and state are required")
        if ctx:
            await ctx.info(
                f"Posting build status for commit {commit_hash} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.post_build_status_to_commit(
            project_id=project_id, commit_hash=commit_hash, **kwargs
        )
        if ctx:
            await ctx.info("Build status posted successfully")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def get_commit_merge_requests(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: str = Field(description="Commit SHA", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Retrieve merge requests associated with a specific commit in a GitLab project."""
        if not project_id or not commit_hash:
            raise ValueError("project_id and commit_hash are required")
        if ctx:
            await ctx.info(
                f"Fetching merge requests for commit {commit_hash} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.get_commit_merge_requests(**kwargs)
        if ctx:
            await ctx.info("Merge requests retrieval complete")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"}
    )
    async def get_commit_gpg_signature(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        commit_hash: str = Field(description="Commit SHA", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Retrieve the GPG signature for a specific commit in a GitLab project."""
        if not project_id or not commit_hash:
            raise ValueError("project_id and commit_hash are required")
        if ctx:
            await ctx.info(
                f"Fetching GPG signature for commit {commit_hash} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.get_commit_gpg_signature(**kwargs)
        if ctx:
            await ctx.info("GPG signature retrieval complete")
        return response.data

    # Deploy Tokens Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"deploy_tokens"},
    )
    async def get_deploy_tokens(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of all deploy tokens for the GitLab instance."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_deploy_tokens()
        return {"deploy_tokens": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"deploy_tokens"},
    )
    async def get_project_deploy_tokens(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        token_id: Optional[int] = Field(description="Deploy token ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of deploy tokens for a specific GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        if token_id:
            response = client.get_project_deploy_token(
                project_id=project_id, token=token_id
            )
            return response.data
        else:
            response = client.get_project_deploy_tokens(project_id=project_id)
            return {"deploy_tokens": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"deploy_tokens"},
    )
    async def create_project_deploy_token(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(description="Name of the deploy token", default=None),
        scopes: List[str] = Field(
            description="Scopes for the deploy token (e.g., ['read_repository'])",
            default=None,
        ),
        expires_at: Optional[str] = Field(
            description="Expiration date (ISO 8601 format)", default=None
        ),
        username: Optional[str] = Field(
            description="Username associated with the token", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a deploy token for a GitLab project with specified name and scopes."""
        if not project_id or not name or not scopes:
            raise ValueError("project_id, name, and scopes are required")
        if ctx:
            await ctx.info(f"Creating deploy token '{name}' for project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.create_project_deploy_token(**kwargs)
        if ctx:
            await ctx.info("Deploy token created")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"deploy_tokens"},
    )
    async def delete_project_deploy_token(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        token_id: int = Field(description="Deploy token ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a specific deploy token for a GitLab project."""
        if not project_id or not token_id:
            raise ValueError("project_id and token_id are required")
        if ctx:
            await ctx.info(f"Deleting deploy token {token_id} for project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_project_deploy_token(
            project_id=project_id, token=token_id
        )
        if ctx:
            await ctx.info("Deploy token deleted")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"deploy_tokens"},
    )
    async def get_group_deploy_tokens(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        token_id: Optional[int] = Field(
            description="Deploy token ID for single retrieval", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve deploy tokens for a GitLab group (list or single by ID)."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        if token_id:
            response = client.get_group_deploy_token(group_id=group_id, token=token_id)
            return response.data
        else:
            response = client.get_group_deploy_tokens(group_id=group_id)
            return {"deploy_tokens": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"deploy_tokens"},
    )
    async def create_group_deploy_token(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        name: str = Field(description="Name of the deploy token", default=None),
        scopes: List[str] = Field(
            description="Scopes for the deploy token (e.g., ['read_repository'])",
            default=None,
        ),
        expires_at: Optional[str] = Field(
            description="Expiration date (ISO 8601 format)", default=None
        ),
        username: Optional[str] = Field(
            description="Username associated with the token", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a deploy token for a GitLab group with specified name and scopes."""
        if not group_id or not name or not scopes:
            raise ValueError("group_id, name, and scopes are required")
        if ctx:
            await ctx.info(f"Creating deploy token '{name}' for group {group_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.create_group_deploy_token(**kwargs)
        if ctx:
            await ctx.info("Deploy token created")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"deploy_tokens"},
    )
    async def delete_group_deploy_token(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        token_id: int = Field(description="Deploy token ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a specific deploy token for a GitLab group."""
        if not group_id or not token_id:
            raise ValueError("group_id and token_id are required")
        if ctx:
            await ctx.info(f"Deleting deploy token {token_id} for group {group_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_group_deploy_token(group_id=group_id, token=token_id)
        if ctx:
            await ctx.info("Deploy token deleted")
        return response.data

    # Environments Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def get_environments(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        environment_id: Optional[int] = Field(
            description="Environment ID", default=None
        ),
        name: Optional[str] = Field(
            description="Filter environments by exact name", default=None
        ),
        search: Optional[str] = Field(
            description="Filter environments by search term in name", default=None
        ),
        states: Optional[str] = Field(
            description="Filter environments by state (e.g., 'available', 'stopped')",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of environments for a GitLab project, optionally filtered by name, search, or states or a single environment by id."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify"]
        }
        if environment_id:
            response = client.get_environment(
                project_id=project_id, environment_id=environment_id
            )
            return response.data
        else:
            response = client.get_environments(**kwargs)
            return {"environments": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def create_environment(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(description="Name of the environment", default=None),
        external_url: Optional[str] = Field(
            description="External URL for the environment", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a new environment in a GitLab project with a specified name and optional external URL."""
        if not project_id or not name:
            raise ValueError("project_id and name are required")
        if ctx:
            await ctx.info(f"Creating environment '{name}' for project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.create_environment(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Environment created")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def update_environment(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        environment_id: int = Field(description="Environment ID", default=None),
        name: Optional[str] = Field(
            description="New name for the environment", default=None
        ),
        external_url: Optional[str] = Field(
            description="New external URL for the environment", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Update an existing environment in a GitLab project with new name or external URL."""
        if not project_id or not environment_id:
            raise ValueError("project_id and environment_id are required")
        if not name and not external_url:
            raise ValueError("At least one of name or external_url must be provided")
        if ctx:
            await ctx.info(
                f"Updating environment {environment_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
                "environment_id",
            ]
        }
        response = client.update_environment(
            project_id=project_id, environment_id=environment_id, **kwargs
        )
        if ctx:
            await ctx.info("Environment updated")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def delete_environment(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        environment_id: int = Field(description="Environment ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a specific environment in a GitLab project."""
        if not project_id or not environment_id:
            raise ValueError("project_id and environment_id are required")
        if ctx:
            await ctx.info(
                f"Deleting environment {environment_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_environment(
            project_id=project_id, environment_id=environment_id
        )
        if ctx:
            await ctx.info("Environment deleted")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def stop_environment(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        environment_id: int = Field(description="Environment ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Stop a specific environment in a GitLab project."""
        if not project_id or not environment_id:
            raise ValueError("project_id and environment_id are required")
        if ctx:
            await ctx.info(
                f"Stopping environment {environment_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.stop_environment(
            project_id=project_id, environment_id=environment_id
        )
        if ctx:
            await ctx.info("Environment stopped")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def stop_stale_environments(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        older_than: Optional[str] = Field(
            description="Filter environments older than this timestamp (ISO 8601 format)",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Stop stale environments in a GitLab project, optionally filtered by older_than timestamp."""
        if not project_id:
            raise ValueError("project_id is required")
        if ctx:
            await ctx.info(f"Stopping stale environments in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.stop_stale_environments(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Stale environments stopped")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def delete_stopped_environments(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete stopped review app environments in a GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if ctx:
            await ctx.info(f"Deleting stopped review apps in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_stopped_environments(project_id=project_id)
        if ctx:
            await ctx.info("Stopped review apps deleted")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def get_protected_environments(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(
            description="Name of the protected environment", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve protected environments in a GitLab project (list or single by name)."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        if name:
            response = client.get_protected_environment(
                project_id=project_id, name=name
            )
            return response.data
        else:
            response = client.get_protected_environments(project_id=project_id)
            return {"protected_environments": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def protect_environment(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(
            description="Name of the environment to protect", default=None
        ),
        required_approval_count: Optional[int] = Field(
            description="Number of approvals required for deployment", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Protect an environment in a GitLab project with optional approval count."""
        if not project_id or not name:
            raise ValueError("project_id and name are required")
        if ctx:
            await ctx.info(f"Protecting environment '{name}' in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.protect_environment(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Environment protected")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def update_protected_environment(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(
            description="Name of the protected environment", default=None
        ),
        required_approval_count: Optional[int] = Field(
            description="New number of approvals required for deployment", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Update a protected environment in a GitLab project with new approval count."""
        if not project_id or not name:
            raise ValueError("project_id and name are required")
        if not required_approval_count:
            raise ValueError("required_approval_count must be provided")
        if ctx:
            await ctx.info(
                f"Updating protected environment '{name}' in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.update_protected_environment(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Protected environment updated")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"environments"},
    )
    async def unprotect_environment(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(
            description="Name of the environment to unprotect", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Unprotect a specific environment in a GitLab project."""
        if not project_id or not name:
            raise ValueError("project_id and name are required")
        if ctx:
            await ctx.info(f"Unprotecting environment '{name}' in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.unprotect_environment(project_id=project_id, name=name)
        if ctx:
            await ctx.info("Environment unprotected")
        return response.data

    # Groups Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"}
    )
    async def get_groups(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: Optional[str] = Field(description="Group ID or path", default=None),
        search: Optional[str] = Field(
            description="Filter groups by search term in name or path", default=None
        ),
        sort: Optional[str] = Field(
            description="Sort order (e.g., 'asc', 'desc')", default=None
        ),
        order_by: Optional[str] = Field(
            description="Field to sort by (e.g., 'name', 'path')", default=None
        ),
        owned: Optional[bool] = Field(
            description="Filter groups owned by the authenticated user", default=None
        ),
        min_access_level: Optional[int] = Field(
            description="Filter groups by minimum access level (e.g., 10 for Guest)",
            default=None,
        ),
        top_level_only: Optional[bool] = Field(
            description="Include only top-level groups (exclude subgroups)",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of groups, optionally filtered by search, sort, ownership, or access level or retrieve a single group by id."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
        }
        if group_id:
            response = client.get_group(group_id=group_id, **kwargs)
            return response.data
        else:
            response = client.get_groups(**kwargs)
            return {"groups": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"}
    )
    async def edit_group(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        name: Optional[str] = Field(description="New name for the group", default=None),
        path: Optional[str] = Field(description="New path for the group", default=None),
        description: Optional[str] = Field(
            description="New description for the group", default=None
        ),
        visibility: Optional[str] = Field(
            description="New visibility level (e.g., 'public', 'private')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Edit a specific GitLab group's details (name, path, description, or visibility)."""
        if not group_id:
            raise ValueError("group_id is required")
        if not any([name, path, description, visibility]):
            raise ValueError(
                "At least one of name, path, description, or visibility must be provided"
            )
        if ctx:
            await ctx.info(f"Editing group {group_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "group_id",
            ]
        }
        response = client.edit_group(group_id=group_id, **kwargs)
        if ctx:
            await ctx.info("Group edited")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"}
    )
    async def get_group_subgroups(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        search: Optional[str] = Field(
            description="Filter subgroups by search term in name or path", default=None
        ),
        sort: Optional[str] = Field(
            description="Sort order (e.g., 'asc', 'desc')", default=None
        ),
        order_by: Optional[str] = Field(
            description="Field to sort by (e.g., 'name', 'path')", default=None
        ),
        owned: Optional[bool] = Field(
            description="Filter subgroups owned by the authenticated user", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of subgroups for a specific GitLab group, optionally filtered."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
        }
        response = client.get_group_subgroups(group_id=group_id, **kwargs)
        return {"subgroups": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"}
    )
    async def get_group_descendant_groups(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        search: Optional[str] = Field(
            description="Filter descendant groups by search term in name or path",
            default=None,
        ),
        sort: Optional[str] = Field(
            description="Sort order (e.g., 'asc', 'desc')", default=None
        ),
        order_by: Optional[str] = Field(
            description="Field to sort by (e.g., 'name', 'path')", default=None
        ),
        owned: Optional[bool] = Field(
            description="Filter descendant groups owned by the authenticated user",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of all descendant groups for a specific GitLab group, optionally filtered."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
        }
        response = client.get_group_descendant_groups(group_id=group_id, **kwargs)
        return {"descendant_groups": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"}
    )
    async def get_group_projects(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        include_subgroups: Optional[bool] = Field(
            description="Include projects from subgroups", default=None
        ),
        search: Optional[str] = Field(
            description="Filter projects by search term in name or path", default=None
        ),
        sort: Optional[str] = Field(
            description="Sort order (e.g., 'asc', 'desc')", default=None
        ),
        order_by: Optional[str] = Field(
            description="Field to sort by (e.g., 'name', 'path')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of projects associated with a specific GitLab group, optionally including subgroups."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
        }
        response = client.get_group_projects(group_id=group_id, **kwargs)
        return {"projects": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"}
    )
    async def get_group_merge_requests(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        state: Optional[str] = Field(
            description="Filter merge requests by state (e.g., 'opened', 'closed')",
            default=None,
        ),
        scope: Optional[str] = Field(
            description="Filter merge requests by scope (e.g., 'created_by_me')",
            default=None,
        ),
        milestone: Optional[str] = Field(
            description="Filter merge requests by milestone title", default=None
        ),
        search: Optional[str] = Field(
            description="Filter merge requests by search term in title or description",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of merge requests associated with a specific GitLab group, optionally filtered."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
        }
        response = client.get_group_merge_requests(group_id=group_id, **kwargs)
        return {"merge_requests": response.data}

    # Jobs Tools
    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
    async def get_project_jobs(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        job_id: Optional[int] = Field(description="Job ID", default=None),
        scope: Optional[str] = Field(
            description="Filter jobs by scope (e.g., 'success', 'failed')", default=None
        ),
        include_retried: Optional[bool] = Field(
            description="Include retried jobs", default=None
        ),
        include_invisible: Optional[bool] = Field(
            description="Include invisible jobs (e.g., from hidden pipelines)",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of jobs for a specific GitLab project, optionally filtered by scope or a single job by id."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify"]
        }
        if job_id:
            response = client.get_project_job(project_id=project_id, job_id=job_id)
            return response.data
        else:
            response = client.get_project_jobs(**kwargs)
            return {"jobs": response.data}

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
    async def get_project_job_log(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        job_id: int = Field(description="Job ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve the log (trace) of a specific job in a GitLab project."""
        if not project_id or not job_id:
            raise ValueError("project_id and job_id are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_project_job_log(project_id=project_id, job_id=job_id)
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
    async def cancel_project_job(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        job_id: int = Field(description="Job ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Cancel a specific job in a GitLab project."""
        if not project_id or not job_id:
            raise ValueError("project_id and job_id are required")
        if ctx:
            await ctx.info(f"Cancelling job {job_id} in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.cancel_project_job(project_id=project_id, job_id=job_id)
        if ctx:
            await ctx.info("Job cancelled")
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
    async def retry_project_job(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        job_id: int = Field(description="Job ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Retry a specific job in a GitLab project."""
        if not project_id or not job_id:
            raise ValueError("project_id and job_id are required")
        if ctx:
            await ctx.info(f"Retrying job {job_id} in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.retry_project_job(project_id=project_id, job_id=job_id)
        if ctx:
            await ctx.info("Job retried")
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
    async def erase_project_job(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        job_id: int = Field(description="Job ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Erase (delete artifacts and logs of) a specific job in a GitLab project."""
        if not project_id or not job_id:
            raise ValueError("project_id and job_id are required")
        if ctx:
            await ctx.info(f"Erasing job {job_id} in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.erase_project_job(project_id=project_id, job_id=job_id)
        if ctx:
            await ctx.info("Job erased")
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
    async def run_project_job(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        job_id: int = Field(description="Job ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Run (play) a specific manual job in a GitLab project."""
        if not project_id or not job_id:
            raise ValueError("project_id and job_id are required")
        if ctx:
            await ctx.info(f"Running job {job_id} in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.run_project_job(project_id=project_id, job_id=job_id)
        if ctx:
            await ctx.info("Job started")
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
    async def get_pipeline_jobs(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_id: int = Field(description="Pipeline ID", default=None),
        scope: Optional[str] = Field(
            description="Filter jobs by scope (e.g., 'success', 'failed')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of jobs for a specific pipeline in a GitLab project, optionally filtered by scope."""
        if not project_id or not pipeline_id:
            raise ValueError("project_id and pipeline_id are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "project_id",
                "pipeline_id",
            ]
        }
        response = client.get_pipeline_jobs(
            project_id=project_id, pipeline_id=pipeline_id, **kwargs
        )
        return {"jobs": response.data}

    # Members Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"members"}
    )
    async def get_group_members(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        query: Optional[str] = Field(
            description="Filter members by search term in name or username",
            default=None,
        ),
        user_ids: Optional[List[int]] = Field(
            description="Filter members by user IDs", default=None
        ),
        skip_users: Optional[List[int]] = Field(
            description="Exclude specified user IDs", default=None
        ),
        show_seat_info: Optional[bool] = Field(
            description="Include seat information for members", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of members in a specific GitLab group, optionally filtered by query or user IDs."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
        }
        response = client.get_group_members(group_id=group_id, **kwargs)
        return {"members": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"members"}
    )
    async def get_project_members(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        query: Optional[str] = Field(
            description="Filter members by search term in name or username",
            default=None,
        ),
        user_ids: Optional[List[int]] = Field(
            description="Filter members by user IDs", default=None
        ),
        skip_users: Optional[List[int]] = Field(
            description="Exclude specified user IDs", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of members in a specific GitLab project, optionally filtered by query or user IDs."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
        }
        response = client.get_project_members(project_id=project_id, **kwargs)
        return {"members": response.data}

    # Merge Request Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"merge_requests"},
    )
    async def create_merge_request(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        source_branch: str = Field(
            description="Source branch for the merge request", default=None
        ),
        target_branch: str = Field(
            description="Target branch for the merge request", default=None
        ),
        title: str = Field(description="Title of the merge request", default=None),
        description: Optional[str] = Field(
            description="Description of the merge request", default=None
        ),
        assignee_id: Optional[int] = Field(
            description="ID of the user to assign the merge request to", default=None
        ),
        reviewer_ids: Optional[List[int]] = Field(
            description="IDs of users to set as reviewers", default=None
        ),
        labels: Optional[List[str]] = Field(
            description="Labels to apply to the merge request", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a new merge request in a GitLab project with specified source and target branches."""
        if not project_id or not source_branch or not target_branch or not title:
            raise ValueError(
                "project_id, source_branch, target_branch, and title are required"
            )
        if ctx:
            await ctx.info(f"Creating merge request '{title}' in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.create_merge_request(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Merge request created")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"merge_requests"},
    )
    async def get_merge_requests(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        state: Optional[str] = Field(
            description="Filter merge requests by state (e.g., 'opened', 'closed')",
            default=None,
        ),
        scope: Optional[str] = Field(
            description="Filter merge requests by scope (e.g., 'created_by_me')",
            default=None,
        ),
        milestone: Optional[str] = Field(
            description="Filter merge requests by milestone title", default=None
        ),
        view: Optional[str] = Field(
            description="Filter merge requests by view (e.g., 'simple')", default=None
        ),
        labels: Optional[List[str]] = Field(
            description="Filter merge requests by labels", default=None
        ),
        author_id: Optional[int] = Field(
            description="Filter merge requests by author ID", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of merge requests across all projects, optionally filtered by state, scope, or labels."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify"]
        }
        response = client.get_merge_requests(**kwargs)
        return {"merge_requests": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"merge_requests"},
    )
    async def get_project_merge_requests(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        merge_id: Optional[int] = Field(description="Merge request ID", default=None),
        state: Optional[str] = Field(
            description="Filter merge requests by state (e.g., 'opened', 'closed')",
            default=None,
        ),
        scope: Optional[str] = Field(
            description="Filter merge requests by scope (e.g., 'created_by_me')",
            default=None,
        ),
        milestone: Optional[str] = Field(
            description="Filter merge requests by milestone title", default=None
        ),
        labels: Optional[List[str]] = Field(
            description="Filter merge requests by labels", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of merge requests for a specific GitLab project, optionally filtered or a single merge request or a single merge request by merge id"""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
        }
        if merge_id:
            response = client.get_project_merge_request(
                project_id=project_id, merge_id=merge_id
            )
            return response.data
        else:
            response = client.get_project_merge_requests(
                project_id=project_id, **kwargs
            )
            return {"merge_requests": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def get_project_level_merge_request_approval_rules(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        approval_rule_id: int = Field(description="Approval rule ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve project-level merge request approval rules for a GitLab project details of a specific project-level merge request approval rule."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        if approval_rule_id:
            response = client.get_project_level_merge_request_rule(
                project_id=project_id, approval_rule_id=approval_rule_id
            )
            return response.data
        else:
            response = client.get_project_level_merge_request_rules(
                project_id=project_id
            )
            return {"approval_rules": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def create_project_level_rule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(description="Name of the approval rule", default=None),
        approvals_required: Optional[int] = Field(
            description="Number of approvals required", default=None
        ),
        rule_type: Optional[str] = Field(
            description="Type of rule (e.g., 'regular')", default=None
        ),
        user_ids: Optional[List[int]] = Field(
            description="List of user IDs required to approve", default=None
        ),
        group_ids: Optional[List[int]] = Field(
            description="List of group IDs required to approve", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a new project-level merge request approval rule."""
        if not project_id or not name:
            raise ValueError("project_id and name are required")
        if ctx:
            await ctx.info(f"Creating approval rule '{name}' for project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.create_project_level_rule(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Approval rule created")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def update_project_level_rule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        approval_rule_id: int = Field(description="Approval rule ID", default=None),
        name: Optional[str] = Field(
            description="New name for the approval rule", default=None
        ),
        approvals_required: Optional[int] = Field(
            description="New number of approvals required", default=None
        ),
        user_ids: Optional[List[int]] = Field(
            description="Updated list of user IDs required to approve", default=None
        ),
        group_ids: Optional[List[int]] = Field(
            description="Updated list of group IDs required to approve", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Update an existing project-level merge request approval rule."""
        if not project_id or not approval_rule_id:
            raise ValueError("project_id and approval_rule_id are required")
        if not any([name, approvals_required, user_ids, group_ids]):
            raise ValueError(
                "At least one of name, approvals_required, user_ids, or group_ids must be provided"
            )
        if ctx:
            await ctx.info(
                f"Updating approval rule {approval_rule_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
                "approval_rule_id",
            ]
        }
        response = client.update_project_level_rule(
            project_id=project_id, approval_rule_id=approval_rule_id, **kwargs
        )
        if ctx:
            await ctx.info("Approval rule updated")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def delete_project_level_rule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        approval_rule_id: int = Field(description="Approval rule ID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a project-level merge request approval rule."""
        if not project_id or not approval_rule_id:
            raise ValueError("project_id and approval_rule_id are required")
        if ctx:
            await ctx.info(
                f"Deleting approval rule {approval_rule_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_project_level_rule(
            project_id=project_id, approval_rule_id=approval_rule_id
        )
        if ctx:
            await ctx.info("Approval rule deleted")
        return response.data

    # Merge Rules Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def merge_request_level_approvals(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        merge_request_iid: int = Field(description="Merge request IID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve approvals for a specific merge request in a GitLab project."""
        if not project_id or not merge_request_iid:
            raise ValueError("project_id and merge_request_iid are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.merge_request_level_approvals(
            project_id=project_id, merge_request_iid=merge_request_iid
        )
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def get_approval_state_merge_requests(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        merge_request_iid: int = Field(description="Merge request IID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve the approval state of a specific merge request in a GitLab project."""
        if not project_id or not merge_request_iid:
            raise ValueError("project_id and merge_request_iid are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_approval_state_merge_requests(
            project_id=project_id, merge_request_iid=merge_request_iid
        )
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def get_merge_request_level_rules(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        merge_request_iid: int = Field(description="Merge request IID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve merge request-level approval rules for a specific merge request in a GitLab project."""
        if not project_id or not merge_request_iid:
            raise ValueError("project_id and merge_request_iid are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_merge_request_level_rules(
            project_id=project_id, merge_request_iid=merge_request_iid
        )
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def approve_merge_request(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        merge_request_iid: int = Field(description="Merge request IID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Approve a specific merge request in a GitLab project."""
        if not project_id or not merge_request_iid:
            raise ValueError("project_id and merge_request_iid are required")
        if ctx:
            await ctx.info(
                f"Approving merge request {merge_request_iid} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.approve_merge_request(
            project_id=project_id, merge_request_iid=merge_request_iid
        )
        if ctx:
            await ctx.info("Merge request approved")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def unapprove_merge_request(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        merge_request_iid: int = Field(description="Merge request IID", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Unapprove a specific merge request in a GitLab project."""
        if not project_id or not merge_request_iid:
            raise ValueError("project_id and merge_request_iid are required")
        if ctx:
            await ctx.info(
                f"Unapproving merge request {merge_request_iid} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.unapprove_merge_request(
            project_id=project_id, merge_request_iid=merge_request_iid
        )
        if ctx:
            await ctx.info("Merge request unapproved")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def get_group_level_rule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve merge request approval settings for a specific GitLab group."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_group_level_rule(group_id=group_id)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def edit_group_level_rule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        allow_author_approval: Optional[bool] = Field(
            description="Whether authors can approve their own merge requests",
            default=None,
        ),
        allow_committer_approval: Optional[bool] = Field(
            description="Whether committers can approve merge requests", default=None
        ),
        allow_overrides_to_approver_list: Optional[bool] = Field(
            description="Whether overrides to the approver list are allowed",
            default=None,
        ),
        minimum_approvals: Optional[int] = Field(
            description="Minimum number of approvals required", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Edit merge request approval settings for a specific GitLab group."""
        if not group_id:
            raise ValueError("group_id is required")
        if not any(
            [
                allow_author_approval,
                allow_committer_approval,
                allow_overrides_to_approver_list,
                minimum_approvals,
            ]
        ):
            raise ValueError(
                "At least one of allow_author_approval, allow_committer_approval, allow_overrides_to_approver_list, or minimum_approvals must be provided"
            )
        if ctx:
            await ctx.info(f"Editing approval settings for group {group_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "group_id",
            ]
        }
        response = client.edit_group_level_rule(group_id=group_id, **kwargs)
        if ctx:
            await ctx.info("Approval settings edited")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def get_project_level_rule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve merge request approval settings for a specific GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_project_level_rule(project_id=project_id)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
    )
    async def edit_project_level_rule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        allow_author_approval: Optional[bool] = Field(
            description="Whether authors can approve their own merge requests",
            default=None,
        ),
        allow_committer_approval: Optional[bool] = Field(
            description="Whether committers can approve merge requests", default=None
        ),
        allow_overrides_to_approver_list: Optional[bool] = Field(
            description="Whether overrides to the approver list are allowed",
            default=None,
        ),
        minimum_approvals: Optional[int] = Field(
            description="Minimum number of approvals required", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Edit merge request approval settings for a specific GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not any(
            [
                allow_author_approval,
                allow_committer_approval,
                allow_overrides_to_approver_list,
                minimum_approvals,
            ]
        ):
            raise ValueError(
                "At least one of allow_author_approval, allow_committer_approval, allow_overrides_to_approver_list, or minimum_approvals must be provided"
            )
        if ctx:
            await ctx.info(f"Editing approval settings for project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.edit_project_level_rule(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Approval settings edited")
        return response.data

    # Packages Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"packages"}
    )
    async def get_repository_packages(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        package_type: Optional[str] = Field(
            description="Filter packages by type (e.g., 'npm', 'maven')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of repository packages for a specific GitLab project, optionally filtered by package type."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
        }
        response = client.get_repository_packages(project_id=project_id, **kwargs)
        return {"packages": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"packages"}
    )
    async def publish_repository_package(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        package_name: str = Field(description="Name of the package", default=None),
        package_version: str = Field(
            description="Version of the package", default=None
        ),
        file_name: str = Field(description="Name of the package file", default=None),
        status: Optional[str] = Field(
            description="Status of the package (e.g., 'default', 'hidden')",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Publish a repository package to a specific GitLab project."""
        if not project_id or not package_name or not package_version or not file_name:
            raise ValueError(
                "project_id, package_name, package_version, and file_name are required"
            )
        if ctx:
            await ctx.info(
                f"Publishing package {package_name}/{package_version} to project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.publish_repository_package(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Package published")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"packages"}
    )
    async def download_repository_package(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        package_name: str = Field(description="Name of the package", default=None),
        package_version: str = Field(
            description="Version of the package", default=None
        ),
        file_name: str = Field(
            description="Name of the package file to download", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Download a repository package from a specific GitLab project."""
        if not project_id or not package_name or not package_version or not file_name:
            raise ValueError(
                "project_id, package_name, package_version, and file_name are required"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.download_repository_package(
            project_id=project_id,
            package_name=package_name,
            package_version=package_version,
            file_name=file_name,
        )
        return response.data

    # Pipeline Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"pipelines"}
    )
    async def get_pipelines(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_id: Optional[int] = Field(description="Pipeline ID", default=None),
        scope: Optional[str] = Field(
            description="Filter pipelines by scope (e.g., 'running', 'branches')",
            default=None,
        ),
        status: Optional[str] = Field(
            description="Filter pipelines by status (e.g., 'success', 'failed')",
            default=None,
        ),
        ref: Optional[str] = Field(
            description="Filter pipelines by reference (e.g., branch or tag name)",
            default=None,
        ),
        source: Optional[str] = Field(
            description="Filter pipelines by source (e.g., 'push', 'schedule')",
            default=None,
        ),
        updated_after: Optional[str] = Field(
            description="Filter pipelines updated after this date (ISO 8601 format)",
            default=None,
        ),
        updated_before: Optional[str] = Field(
            description="Filter pipelines updated before this date (ISO 8601 format)",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of pipelines for a specific GitLab project, optionally filtered by scope, status, or ref or details of a specific pipeline in a GitLab project.."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
        }
        if pipeline_id:
            response = client.get_pipeline(
                project_id=project_id, pipeline_id=pipeline_id
            )
        else:
            response = client.get_pipelines(project_id=project_id, **kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"pipelines"}
    )
    async def run_pipeline(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        ref: str = Field(
            description="Reference (e.g., branch or tag) to run the pipeline on",
            default=None,
        ),
        variables: Optional[Dict[str, str]] = Field(
            description="Dictionary of pipeline variables", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Run a pipeline for a specific GitLab project with a given reference (e.g., branch or tag)."""
        if not project_id or not ref:
            raise ValueError("project_id and ref are required")
        if ctx:
            await ctx.info(f"Running pipeline for project {project_id} on ref {ref}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.run_pipeline(
            project_id=project_id, ref=ref, variables=variables
        )
        if ctx:
            await ctx.info("Pipeline started")
        return response.data

    # Pipeline Schedules Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def get_pipeline_schedules(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of pipeline schedules for a specific GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_pipeline_schedules(project_id=project_id)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def get_pipeline_schedule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_schedule_id: int = Field(
            description="Pipeline schedule ID", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve details of a specific pipeline schedule in a GitLab project."""
        if not project_id or not pipeline_schedule_id:
            raise ValueError("project_id and pipeline_schedule_id are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_pipeline_schedule(
            project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
        )
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def get_pipelines_triggered_from_schedule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_schedule_id: int = Field(
            description="Pipeline schedule ID", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve pipelines triggered by a specific pipeline schedule in a GitLab project."""
        if not project_id or not pipeline_schedule_id:
            raise ValueError("project_id and pipeline_schedule_id are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_pipelines_triggered_from_schedule(
            project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
        )
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def create_pipeline_schedule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        description: Optional[str] = Field(
            description="Description of the pipeline schedule", default=None
        ),
        ref: str = Field(
            description="Reference (e.g., branch or tag) for the pipeline", default=None
        ),
        cron: str = Field(
            description="Cron expression defining the schedule (e.g., '0 0 * * *')",
            default=None,
        ),
        cron_timezone: Optional[str] = Field(
            description="Timezone for the cron schedule (e.g., 'UTC')", default=None
        ),
        active: Optional[bool] = Field(
            description="Whether the schedule is active", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a pipeline schedule for a specific GitLab project."""
        if not project_id or not ref or not cron:
            raise ValueError("project_id, ref, and cron are required")
        if ctx:
            await ctx.info(
                f"Creating pipeline schedule '{description or 'no description'}' for project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.create_pipeline_schedule(
            project_id=project_id,
            description=description,
            ref=ref,
            cron=cron,
            cron_timezone=cron_timezone,
            active=active,
        )
        if ctx:
            await ctx.info("Pipeline schedule created")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def edit_pipeline_schedule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_schedule_id: int = Field(
            description="Pipeline schedule ID", default=None
        ),
        description: Optional[str] = Field(
            description="New description of the pipeline schedule", default=None
        ),
        ref: Optional[str] = Field(
            description="New reference (e.g., branch or tag) for the pipeline",
            default=None,
        ),
        cron: Optional[str] = Field(
            description="New cron expression for the schedule (e.g., '0 0 * * *')",
            default=None,
        ),
        cron_timezone: Optional[str] = Field(
            description="New timezone for the cron schedule (e.g., 'UTC')", default=None
        ),
        active: Optional[bool] = Field(
            description="Whether the schedule is active", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Edit a pipeline schedule in a GitLab project."""
        if not project_id or not pipeline_schedule_id:
            raise ValueError("project_id and pipeline_schedule_id are required")
        if not any([description, ref, cron, cron_timezone, active]):
            raise ValueError(
                "At least one of description, ref, cron, cron_timezone, or active must be provided"
            )
        if ctx:
            await ctx.info(
                f"Editing pipeline schedule {pipeline_schedule_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.edit_pipeline_schedule(
            project_id=project_id,
            pipeline_schedule_id=pipeline_schedule_id,
            description=description,
            ref=ref,
            cron=cron,
            cron_timezone=cron_timezone,
            active=active,
        )
        if ctx:
            await ctx.info("Pipeline schedule edited")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def take_pipeline_schedule_ownership(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_schedule_id: int = Field(
            description="Pipeline schedule ID", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Take ownership of a pipeline schedule in a GitLab project."""
        if not project_id or not pipeline_schedule_id:
            raise ValueError("project_id and pipeline_schedule_id are required")
        if ctx:
            await ctx.info(
                f"Taking ownership of pipeline schedule {pipeline_schedule_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.take_pipeline_schedule_ownership(
            project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
        )
        if ctx:
            await ctx.info("Ownership taken")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def delete_pipeline_schedule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_schedule_id: int = Field(
            description="Pipeline schedule ID", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a pipeline schedule in a GitLab project."""
        if not project_id or not pipeline_schedule_id:
            raise ValueError("project_id and pipeline_schedule_id are required")
        if ctx:
            await ctx.info(
                f"Deleting pipeline schedule {pipeline_schedule_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_pipeline_schedule(
            project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
        )
        if ctx:
            await ctx.info("Pipeline schedule deleted")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def run_pipeline_schedule(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_schedule_id: int = Field(
            description="Pipeline schedule ID", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Run a pipeline schedule immediately in a GitLab project."""
        if not project_id or not pipeline_schedule_id:
            raise ValueError("project_id and pipeline_schedule_id are required")
        if ctx:
            await ctx.info(
                f"Running pipeline schedule {pipeline_schedule_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.run_pipeline_schedule(
            project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
        )
        if ctx:
            await ctx.info("Pipeline schedule run started")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def create_pipeline_schedule_variable(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_schedule_id: int = Field(
            description="Pipeline schedule ID", default=None
        ),
        key: str = Field(description="Key of the variable", default=None),
        value: str = Field(description="Value of the variable", default=None),
        variable_type: Optional[str] = Field(
            description="Type of variable (e.g., 'env_var')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a variable for a pipeline schedule in a GitLab project."""
        if not project_id or not pipeline_schedule_id or not key or not value:
            raise ValueError(
                "project_id, pipeline_schedule_id, key, and value are required"
            )
        if ctx:
            await ctx.info(
                f"Creating variable '{key}' for pipeline schedule {pipeline_schedule_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.create_pipeline_schedule_variable(
            project_id=project_id,
            pipeline_schedule_id=pipeline_schedule_id,
            key=key,
            value=value,
            variable_type=variable_type,
        )
        if ctx:
            await ctx.info("Variable created")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"pipeline_schedules"},
    )
    async def delete_pipeline_schedule_variable(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        pipeline_schedule_id: int = Field(
            description="Pipeline schedule ID", default=None
        ),
        key: str = Field(description="Key of the variable to delete", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a variable from a pipeline schedule in a GitLab project."""
        if not project_id or not pipeline_schedule_id or not key:
            raise ValueError("project_id, pipeline_schedule_id, and key are required")
        if ctx:
            await ctx.info(
                f"Deleting variable '{key}' from pipeline schedule {pipeline_schedule_id} in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_pipeline_schedule_variable(
            project_id=project_id, pipeline_schedule_id=pipeline_schedule_id, key=key
        )
        if ctx:
            await ctx.info("Variable deleted")
        return response.data

    # Projects Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def get_projects(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: Optional[str] = Field(
            description="Project ID or path", default=None
        ),
        owned: Optional[bool] = Field(
            description="Filter projects owned by the authenticated user", default=None
        ),
        search: Optional[str] = Field(
            description="Filter projects by search term in name or path", default=None
        ),
        sort: Optional[str] = Field(
            description="Sort projects by criteria (e.g., 'created_at', 'name')",
            default=None,
        ),
        visibility: Optional[str] = Field(
            description="Filter projects by visibility (e.g., 'public', 'private')",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of projects, optionally filtered by ownership, search, sort, or visibility or Retrieve details of a specific GitLab project."""

        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify"]
        }
        if project_id:
            response = client.get_project(project_id=project_id)
            return response.data
        else:
            response = client.get_projects(**kwargs)
            return {"projects": response.data}

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def get_nested_projects_by_group(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of nested projects within a GitLab group, including descendant groups."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_nested_projects_by_group(group_id=group_id)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def get_project_contributors(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of contributors to a specific GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_project_contributors(project_id=project_id)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def get_project_statistics(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve statistics for a specific GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_project_statistics(project_id=project_id)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def edit_project(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: Optional[str] = Field(
            description="New name of the project", default=None
        ),
        description: Optional[str] = Field(
            description="New description of the project", default=None
        ),
        visibility: Optional[str] = Field(
            description="New visibility of the project (e.g., 'public', 'private')",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Edit a specific GitLab project's details (name, description, or visibility)."""
        if not project_id:
            raise ValueError("project_id is required")
        if not any([name, description, visibility]):
            raise ValueError(
                "At least one of name, description, or visibility must be provided"
            )
        if ctx:
            await ctx.info(f"Editing project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.edit_project(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Project edited")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def get_project_groups(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        skip_groups: Optional[List[int]] = Field(
            description="List of group IDs to exclude", default=None
        ),
        search: Optional[str] = Field(
            description="Filter groups by search term in name", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of groups associated with a specific GitLab project, optionally filtered."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
        }
        response = client.get_project_groups(project_id=project_id, **kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def archive_project(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Archive a specific GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if ctx:
            await ctx.info(f"Archiving project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.archive_project(project_id=project_id)
        if ctx:
            await ctx.info("Project archived")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def unarchive_project(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Unarchive a specific GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if ctx:
            await ctx.info(f"Unarchiving project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.unarchive_project(project_id=project_id)
        if ctx:
            await ctx.info("Project unarchived")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def delete_project(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a specific GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if ctx:
            await ctx.info(f"Deleting project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_project(project_id=project_id)
        if ctx:
            await ctx.info("Project deleted")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"}
    )
    async def share_project(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        group_id: str = Field(
            description="Group ID or path to share with", default=None
        ),
        group_access: str = Field(
            description="Access level for the group (e.g., 'guest', 'developer', 'maintainer')",
            default=None,
        ),
        expires_at: Optional[str] = Field(
            description="Expiration date for the share in ISO 8601 format", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Share a specific GitLab project with a group, specifying access level."""
        if not project_id or not group_id or not group_access:
            raise ValueError("project_id, group_id, and group_access are required")
        if ctx:
            await ctx.info(f"Sharing project {project_id} with group {group_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.share_project(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Project shared")
        return response.data

    # Protected Branches Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"protected_branches"},
    )
    async def get_protected_branches(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        branch: Optional[str] = Field(
            description="Name of the branch to retrieve (e.g., 'main')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of protected branches in a specific GitLab project or Retrieve details of a specific protected branch in a GitLab project.."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        if branch:
            response = client.get_protected_branch(project_id=project_id, branch=branch)
        else:
            response = client.get_protected_branches(project_id=project_id)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"protected_branches"},
    )
    async def protect_branch(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        branch: str = Field(
            description="Name of the branch to protect (e.g., 'main')", default=None
        ),
        push_access_level: Optional[str] = Field(
            description="Access level for pushing (e.g., 'maintainer')", default=None
        ),
        merge_access_level: Optional[str] = Field(
            description="Access level for merging (e.g., 'developer')", default=None
        ),
        unprotect_access_level: Optional[str] = Field(
            description="Access level for unprotecting (e.g., 'maintainer')",
            default=None,
        ),
        allow_force_push: Optional[bool] = Field(
            description="Whether force pushes are allowed", default=None
        ),
        allowed_to_push: Optional[List[Dict]] = Field(
            description="List of users or groups allowed to push", default=None
        ),
        allowed_to_merge: Optional[List[Dict]] = Field(
            description="List of users or groups allowed to merge", default=None
        ),
        allowed_to_unprotect: Optional[List[Dict]] = Field(
            description="List of users or groups allowed to unprotect", default=None
        ),
        code_owner_approval_required: Optional[bool] = Field(
            description="Whether code owner approval is required", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Protect a specific branch in a GitLab project with specified access levels."""
        if not project_id or not branch:
            raise ValueError("project_id and branch are required")
        if not any(
            [
                push_access_level,
                merge_access_level,
                unprotect_access_level,
                allow_force_push,
                allowed_to_push,
                allowed_to_merge,
                allowed_to_unprotect,
                code_owner_approval_required,
            ]
        ):
            raise ValueError("At least one protection parameter must be provided")
        if ctx:
            await ctx.info(f"Protecting branch '{branch}' in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.protect_branch(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Branch protected")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"protected_branches"},
    )
    async def unprotect_branch(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        branch: str = Field(
            description="Name of the branch to unprotect (e.g., 'main')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Unprotect a specific branch in a GitLab project."""
        if not project_id or not branch:
            raise ValueError("project_id and branch are required")
        if ctx:
            await ctx.info(f"Unprotecting branch '{branch}' in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.unprotect_branch(project_id=project_id, branch=branch)
        if ctx:
            await ctx.info("Branch unprotected")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"protected_branches"},
    )
    async def require_code_owner_approvals_single_branch(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        branch: str = Field(
            description="Name of the branch to set approval requirements for (e.g., 'main')",
            default=None,
        ),
        code_owner_approval_required: bool = Field(
            description="Whether code owner approval is required", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Require or disable code owner approvals for a specific branch in a GitLab project."""
        if not project_id or not branch or code_owner_approval_required is None:
            raise ValueError(
                "project_id, branch, and code_owner_approval_required are required"
            )
        if ctx:
            await ctx.info(
                f"Setting code owner approval requirement for branch '{branch}' in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.require_code_owner_approvals_single_branch(
            project_id=project_id,
            branch=branch,
            code_owner_approval_required=code_owner_approval_required,
        )
        if ctx:
            await ctx.info("Code owner approval setting updated")
        return response.data

    # Release Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def get_releases(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        include_html_description: Optional[bool] = Field(
            description="Whether to include HTML descriptions", default=None
        ),
        sort: Optional[str] = Field(
            description="Sort releases by criteria (e.g., 'released_at')", default=None
        ),
        order_by: Optional[str] = Field(
            description="Order releases by criteria (e.g., 'asc', 'desc')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of releases for a specific GitLab project, optionally filtered."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
        }
        response = client.get_releases(project_id=project_id, **kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def get_latest_release(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve details of the latest release in a GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_latest_release(project_id=project_id)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def get_latest_release_evidence(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve evidence for the latest release in a GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_latest_release_evidence(project_id=project_id)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def get_latest_release_asset(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        direct_asset_path: str = Field(
            description="Path to the asset (e.g., 'assets/file.zip')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a specific asset for the latest release in a GitLab project."""
        if not project_id or not direct_asset_path:
            raise ValueError("project_id and direct_asset_path are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_latest_release_asset(
            project_id=project_id, direct_asset_path=direct_asset_path
        )
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def get_group_releases(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        include_html_description: Optional[bool] = Field(
            description="Whether to include HTML descriptions", default=None
        ),
        sort: Optional[str] = Field(
            description="Sort releases by criteria (e.g., 'released_at')", default=None
        ),
        order_by: Optional[str] = Field(
            description="Order releases by criteria (e.g., 'asc', 'desc')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of releases for a specific GitLab group, optionally filtered."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
        }
        response = client.get_group_releases(group_id=group_id, **kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def download_release_asset(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        tag_name: str = Field(
            description="Tag name of the release (e.g., 'v1.0.0')", default=None
        ),
        direct_asset_path: str = Field(
            description="Path to the asset (e.g., 'assets/file.zip')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Download a release asset from a group's release in GitLab."""
        if not group_id or not tag_name or not direct_asset_path:
            raise ValueError("group_id, tag_name, and direct_asset_path are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.download_release_asset(
            group_id=group_id, tag_name=tag_name, direct_asset_path=direct_asset_path
        )
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def get_release_by_tag(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        tag_name: str = Field(
            description="Tag name of the release (e.g., 'v1.0.0')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve details of a release by its tag in a GitLab project."""
        if not project_id or not tag_name:
            raise ValueError("project_id and tag_name are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_release_by_tag(project_id=project_id, tag_name=tag_name)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def create_release(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(description="Name of the release", default=None),
        tag_name: str = Field(
            description="Tag name associated with the release (e.g., 'v1.0.0')",
            default=None,
        ),
        description: Optional[str] = Field(
            description="Description of the release", default=None
        ),
        released_at: Optional[str] = Field(
            description="Release date in ISO 8601 format", default=None
        ),
        assets: Optional[Dict] = Field(
            description="Dictionary of release assets", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a new release in a GitLab project."""
        if not project_id or not name or not tag_name:
            raise ValueError("project_id, name, and tag_name are required")
        if ctx:
            await ctx.info(f"Creating release '{name}' for project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.create_release(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Release created")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def create_release_evidence(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        tag_name: str = Field(
            description="Tag name of the release (e.g., 'v1.0.0')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create evidence for a release in a GitLab project."""
        if not project_id or not tag_name:
            raise ValueError("project_id and tag_name are required")
        if ctx:
            await ctx.info(
                f"Creating release evidence for tag '{tag_name}' in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.create_release_evidence(
            project_id=project_id, tag_name=tag_name
        )
        if ctx:
            await ctx.info("Release evidence created")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def update_release(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        tag_name: str = Field(
            description="Tag name of the release to update (e.g., 'v1.0.0')",
            default=None,
        ),
        name: Optional[str] = Field(
            description="New name of the release", default=None
        ),
        description: Optional[str] = Field(
            description="New description of the release", default=None
        ),
        released_at: Optional[str] = Field(
            description="New release date in ISO 8601 format", default=None
        ),
        assets: Optional[Dict] = Field(
            description="Updated dictionary of release assets", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Update a release in a GitLab project."""
        if not project_id or not tag_name:
            raise ValueError("project_id and tag_name are required")
        if not any([name, description, released_at, assets]):
            raise ValueError(
                "At least one of name, description, released_at, or assets must be provided"
            )
        if ctx:
            await ctx.info(
                f"Updating release for tag '{tag_name}' in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
                "tag_name",
            ]
        }
        response = client.update_release(
            project_id=project_id, tag_name=tag_name, **kwargs
        )
        if ctx:
            await ctx.info("Release updated")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"}
    )
    async def delete_release(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        tag_name: str = Field(
            description="Tag name of the release to delete (e.g., 'v1.0.0')",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a release in a GitLab project."""
        if not project_id or not tag_name:
            raise ValueError("project_id and tag_name are required")
        if ctx:
            await ctx.info(
                f"Deleting release for tag '{tag_name}' in project {project_id}"
            )
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_release(project_id=project_id, tag_name=tag_name)
        if ctx:
            await ctx.info("Release deleted")
        return response.data

    # Runners Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def get_runners(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        runner_id: Optional[int] = Field(
            description="ID of the runner to retrieve", default=None
        ),
        scope: Optional[str] = Field(
            description="Filter runners by scope (e.g., 'active')", default=None
        ),
        type: Optional[str] = Field(
            description="Filter runners by type (e.g., 'instance_type')", default=None
        ),
        status: Optional[str] = Field(
            description="Filter runners by status (e.g., 'online')", default=None
        ),
        tag_list: Optional[List[str]] = Field(
            description="Filter runners by tags", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of runners in GitLab, optionally filtered by scope, type, status, or tags or Retrieve details of a specific GitLab runner.."""
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify"]
        }
        if runner_id:
            response = client.get_runner(runner_id=runner_id)
        else:
            response = client.get_runners(**kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def update_runner_details(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        runner_id: int = Field(description="ID of the runner to update", default=None),
        description: Optional[str] = Field(
            description="New description of the runner", default=None
        ),
        active: Optional[bool] = Field(
            description="Whether the runner is active", default=None
        ),
        tag_list: Optional[List[str]] = Field(
            description="List of tags for the runner", default=None
        ),
        run_untagged: Optional[bool] = Field(
            description="Whether the runner can run untagged jobs", default=None
        ),
        locked: Optional[bool] = Field(
            description="Whether the runner is locked", default=None
        ),
        access_level: Optional[str] = Field(
            description="Access level of the runner (e.g., 'ref_protected')",
            default=None,
        ),
        maximum_timeout: Optional[int] = Field(
            description="Maximum timeout for the runner in seconds", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Update details for a specific GitLab runner."""
        if not runner_id:
            raise ValueError("runner_id is required")
        if not any(
            [
                description,
                active,
                tag_list,
                run_untagged,
                locked,
                access_level,
                maximum_timeout,
            ]
        ):
            raise ValueError("At least one update parameter must be provided")
        if ctx:
            await ctx.info(f"Updating runner {runner_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "runner_id",
            ]
        }
        response = client.update_runner_details(runner_id=runner_id, **kwargs)
        if ctx:
            await ctx.info("Runner updated")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def pause_runner(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        runner_id: int = Field(
            description="ID of the runner to pause or unpause", default=None
        ),
        active: bool = Field(
            description="Whether the runner should be active (True) or paused (False)",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Pause or unpause a specific GitLab runner."""
        if not runner_id or active is None:
            raise ValueError("runner_id and active are required")
        if ctx:
            await ctx.info(f"Setting runner {runner_id} active status to {active}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.pause_runner(runner_id=runner_id, active=active)
        if ctx:
            await ctx.info("Runner status updated")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def get_runner_jobs(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        runner_id: int = Field(
            description="ID of the runner to retrieve jobs for", default=None
        ),
        status: Optional[str] = Field(
            description="Filter jobs by status (e.g., 'success', 'failed')",
            default=None,
        ),
        sort: Optional[str] = Field(
            description="Sort jobs by criteria (e.g., 'created_at')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve jobs for a specific GitLab runner, optionally filtered by status or sorted."""
        if not runner_id:
            raise ValueError("runner_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "runner_id"]
        }
        response = client.get_runner_jobs(runner_id=runner_id, **kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def get_project_runners(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        scope: Optional[str] = Field(
            description="Filter runners by scope (e.g., 'active')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of runners in a specific GitLab project, optionally filtered by scope."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
        }
        response = client.get_project_runners(project_id=project_id, **kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def enable_project_runner(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        runner_id: int = Field(description="ID of the runner to enable", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Enable a runner in a specific GitLab project."""
        if not project_id or not runner_id:
            raise ValueError("project_id and runner_id are required")
        if ctx:
            await ctx.info(f"Enabling runner {runner_id} for project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.enable_project_runner(
            project_id=project_id, runner_id=runner_id
        )
        if ctx:
            await ctx.info("Runner enabled")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def delete_project_runner(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        runner_id: int = Field(description="ID of the runner to delete", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a runner from a specific GitLab project."""
        if not project_id or not runner_id:
            raise ValueError("project_id and runner_id are required")
        if ctx:
            await ctx.info(f"Deleting runner {runner_id} from project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_project_runner(
            project_id=project_id, runner_id=runner_id
        )
        if ctx:
            await ctx.info("Runner deleted")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def get_group_runners(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        scope: Optional[str] = Field(
            description="Filter runners by scope (e.g., 'active')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of runners in a specific GitLab group, optionally filtered by scope."""
        if not group_id:
            raise ValueError("group_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
        }
        response = client.get_group_runners(group_id=group_id, **kwargs)
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def register_new_runner(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        token: str = Field(
            description="Registration token for the runner", default=None
        ),
        description: Optional[str] = Field(
            description="Description of the runner", default=None
        ),
        tag_list: Optional[List[str]] = Field(
            description="List of tags for the runner", default=None
        ),
        run_untagged: Optional[bool] = Field(
            description="Whether the runner can run untagged jobs", default=None
        ),
        locked: Optional[bool] = Field(
            description="Whether the runner is locked", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Register a new GitLab runner."""
        if not token:
            raise ValueError("token is required")
        if ctx:
            await ctx.info("Registering new runner with token")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.register_new_runner(**kwargs)
        if ctx:
            await ctx.info("Runner registered")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def delete_runner(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        runner_id: Optional[int] = Field(
            description="ID of the runner to delete", default=None
        ),
        token: Optional[str] = Field(
            description="Token of the runner to delete", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a GitLab runner by ID or token."""
        if not runner_id and not token:
            raise ValueError("Either runner_id or token is required")
        if ctx:
            await ctx.info(f"Deleting runner with ID {runner_id or 'token'}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
        }
        response = client.delete_runner(**kwargs)
        if ctx:
            await ctx.info("Runner deleted")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def verify_runner_authentication(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        token: str = Field(description="Runner token to verify", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Verify authentication for a GitLab runner using its token."""
        if not token:
            raise ValueError("token is required")
        if ctx:
            await ctx.info("Verifying runner authentication")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.verify_runner_authentication(token=token)
        if ctx:
            await ctx.info("Runner authentication verified")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def reset_gitlab_runner_token(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Reset the GitLab runner registration token."""
        if ctx:
            await ctx.info("Resetting GitLab runner registration token")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.reset_gitlab_runner_token()
        if ctx:
            await ctx.info("Runner token reset")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def reset_project_runner_token(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Reset the registration token for a project's runner in GitLab."""
        if not project_id:
            raise ValueError("project_id is required")
        if ctx:
            await ctx.info(f"Resetting runner token for project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.reset_project_runner_token(project_id=project_id)
        if ctx:
            await ctx.info("Project runner token reset")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def reset_group_runner_token(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        group_id: str = Field(description="Group ID or path", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Reset the registration token for a group's runner in GitLab."""
        if not group_id:
            raise ValueError("group_id is required")
        if ctx:
            await ctx.info(f"Resetting runner token for group {group_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.reset_group_runner_token(group_id=group_id)
        if ctx:
            await ctx.info("Group runner token reset")
        return response.data

    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"}
    )
    async def reset_token(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        runner_id: int = Field(
            description="ID of the runner to reset the token for", default=None
        ),
        token: str = Field(description="Current token of the runner", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Reset the authentication token for a specific GitLab runner."""
        if not runner_id or not token:
            raise ValueError("runner_id and token are required")
        if ctx:
            await ctx.info(f"Resetting authentication token for runner {runner_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.reset_token(runner_id=runner_id, token=token)
        if ctx:
            await ctx.info("Runner authentication token reset")
        return response.data

    # Tags Tools
    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
    async def get_tags(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: Optional[str] = Field(
            description="Name of the tag to retrieve (e.g., 'v1.0.0')", default=None
        ),
        search: Optional[str] = Field(
            description="Filter tags by search term in name", default=None
        ),
        sort: Optional[str] = Field(
            description="Sort tags by criteria (e.g., 'name', 'updated')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of tags for a specific GitLab project, optionally filtered or sorted or Retrieve details of a specific tag in a GitLab project."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
        }
        if name:
            response = client.get_tag(project_id=project_id, name=name)
            return response.data
        else:
            response = client.get_tags(project_id=project_id, **kwargs)
            return {"tags": response.data}

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
    async def create_tag(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(
            description="Name of the tag to create (e.g., 'v1.0.0')", default=None
        ),
        ref: str = Field(
            description="Reference (e.g., branch or commit SHA) to tag", default=None
        ),
        message: Optional[str] = Field(description="Tag message", default=None),
        release_description: Optional[str] = Field(
            description="Release description associated with the tag", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Create a new tag in a GitLab project."""
        if not project_id or not name or not ref:
            raise ValueError("project_id, name, and ref are required")
        if ctx:
            await ctx.info(f"Creating tag '{name}' in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.create_tag(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Tag created")
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
    async def delete_tag(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(
            description="Name of the tag to delete (e.g., 'v1.0.0')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Delete a specific tag in a GitLab project."""
        if not project_id or not name:
            raise ValueError("project_id and name are required")
        if ctx:
            await ctx.info(f"Deleting tag '{name}' in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.delete_tag(project_id=project_id, name=name)
        if ctx:
            await ctx.info("Tag deleted")
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
    async def get_protected_tags(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: Optional[str] = Field(description="Filter tags by name", default=None),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve a list of protected tags in a specific GitLab project, optionally filtered by name."""
        if not project_id:
            raise ValueError("project_id is required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
        }
        response = client.get_protected_tags(project_id=project_id, **kwargs)
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
    async def get_protected_tag(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(
            description="Name of the protected tag to retrieve (e.g., 'v1.0.0')",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
    ) -> Response:
        """Retrieve details of a specific protected tag in a GitLab project."""
        if not project_id or not name:
            raise ValueError("project_id and name are required")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.get_protected_tag(project_id=project_id, name=name)
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
    async def protect_tag(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(
            description="Name of the tag to protect (e.g., 'v1.0.0')", default=None
        ),
        create_access_level: Optional[str] = Field(
            description="Access level for creating the tag (e.g., 'maintainer')",
            default=None,
        ),
        allowed_to_create: Optional[List[Dict]] = Field(
            description="List of users or groups allowed to create the tag",
            default=None,
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Protect a specific tag in a GitLab project with specified access levels."""
        if not project_id or not name:
            raise ValueError("project_id and name are required")
        if not create_access_level and not allowed_to_create:
            raise ValueError(
                "At least one of create_access_level or allowed_to_create must be provided"
            )
        if ctx:
            await ctx.info(f"Protecting tag '{name}' in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        kwargs = {
            k: v
            for k, v in locals().items()
            if v is not None
            and k
            not in [
                "client",
                "gitlab_instance",
                "access_token",
                "verify",
                "ctx",
                "project_id",
            ]
        }
        response = client.protect_tag(project_id=project_id, **kwargs)
        if ctx:
            await ctx.info("Tag protected")
        return response.data

    @mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
    async def unprotect_tag(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        project_id: str = Field(description="Project ID or path", default=None),
        name: str = Field(
            description="Name of the tag to unprotect (e.g., 'v1.0.0')", default=None
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """Unprotect a specific tag in a GitLab project."""
        if not project_id or not name:
            raise ValueError("project_id and name are required")
        if ctx:
            await ctx.info(f"Unprotecting tag '{name}' in project {project_id}")
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.unprotect_tag(project_id=project_id, name=name)
        if ctx:
            await ctx.info("Tag unprotected")
        return response.data

    # Custom API Tools
    @mcp.tool(
        exclude_args=["gitlab_instance", "access_token", "verify"],
        tags={"custom_api"},
    )
    async def api_request(
        gitlab_instance: Optional[str] = Field(
            description="URL of GitLab instance with /api/v4/ suffix",
            default=os.environ.get("GITLAB_INSTANCE", None),
        ),
        access_token: Optional[str] = Field(
            description="GitLab access token",
            default=os.environ.get("GITLAB_ACCESS_TOKEN", None),
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=to_boolean(os.environ.get("GITLAB_VERIFY", "True")),
        ),
        method: str = Field(
            description="The HTTP method to use ('GET', 'POST', 'PUT', 'DELETE')"
        ),
        endpoint: str = Field(description="The API endpoint to send the request to"),
        data: Optional[Dict[str, Any]] = Field(
            default=None,
            description="Data to include in the request body (for non-JSON payloads)",
        ),
        json: Optional[Dict[str, Any]] = Field(
            default=None, description="JSON data to include in the request body"
        ),
        ctx: Optional[Context] = Field(
            description="MCP context for progress", default=None
        ),
    ) -> Response:
        """
        Make a custom API request to a GitLab instance.
        """
        if not access_token:
            raise RuntimeError(
                f"No Access Token supplied as function parameters or as the environment variables [GITLAB_ACCESS_TOKEN]\nAccess Token Supplied: {access_token}"
            )
        client = get_client(
            instance=gitlab_instance, token=access_token, verify=verify, config=config
        )
        response = client.api_request(
            method=method, endpoint=endpoint, data=data, json=json
        )
        if ctx:
            await ctx.info("API Complete")
        return response


def register_prompts(mcp: FastMCP):
    # Prompts
    @mcp.prompt
    def create_branch_prompt(
        new_branch: str,
        source_branch: str,
        project_id: Union[str, int],
    ) -> str:
        """
        Generates a prompt for creating a branch
        """
        return f"Create a branch called '{new_branch}' from the '{source_branch}' for project id {project_id}"

    @mcp.prompt
    def create_merge_request_prompt(
        new_branch: str,
        source_branch: str,
        project_id: Union[str, int],
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
        project_id: Union[str, int],
    ) -> str:
        """
        Generates a prompt for getting project statistics
        """
        return f"What are the details for project id: {project_id}"

    @mcp.prompt
    def trigger_pipeline_prompt(
        branch: str,
        project_id: Union[str, int],
    ) -> str:
        """
        Generates a prompt for triggering a pipeline
        """
        return f"Run the pipeline for project: '{project_id}' on the '{branch}' branch"

    @mcp.prompt
    def get_latest_release_prompt(
        project_id: Union[str, int],
    ) -> str:
        """
        Generates a prompt for getting the latest gitlab release.
        """
        return f"What is the latest release for project id: {project_id}"


def gitlab_mcp() -> None:
    """Run the GitLab MCP server with specified transport and connection parameters.

    This function parses command-line arguments to configure and start the MCP server for GitLab API interactions.
    It supports stdio or TCP transport modes and exits on invalid arguments or help requests.

    Example:
        $ python gitlab_api_mcp.py --transport streamable-http --host localhost --port 5000
    """
    parser = argparse.ArgumentParser(description="GitLab MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        default=DEFAULT_TRANSPORT,
        choices=["stdio", "streamable-http", "sse"],
        help="Transport method: 'stdio', 'streamable-http', or 'sse' [legacy] (default: stdio)",
    )
    parser.add_argument(
        "-s",
        "--host",
        default=DEFAULT_HOST,
        help="Host address for HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port number for HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--auth-type",
        default="none",
        choices=["none", "static", "jwt", "oauth-proxy", "oidc-proxy", "remote-oauth"],
        help="Authentication type for MCP server: 'none' (disabled), 'static' (internal), 'jwt' (external token verification), 'oauth-proxy', 'oidc-proxy', 'remote-oauth' (external) (default: none)",
    )
    # JWT/Token params
    parser.add_argument(
        "--token-jwks-uri", default=None, help="JWKS URI for JWT verification"
    )
    parser.add_argument(
        "--token-issuer", default=None, help="Issuer for JWT verification"
    )
    parser.add_argument(
        "--token-audience", default=None, help="Audience for JWT verification"
    )
    parser.add_argument(
        "--token-algorithm",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM"),
        choices=[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
        ],
        help="JWT signing algorithm (required for HMAC or static key). Auto-detected for JWKS.",
    )
    parser.add_argument(
        "--token-secret",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Shared secret for HMAC (HS*) or PEM public key for static asymmetric verification.",
    )
    parser.add_argument(
        "--token-public-key",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Path to PEM public key file or inline PEM string (for static asymmetric keys).",
    )
    parser.add_argument(
        "--required-scopes",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES"),
        help="Comma-separated list of required scopes (e.g., gitlab.read,gitlab.write).",
    )
    # OAuth Proxy params
    parser.add_argument(
        "--oauth-upstream-auth-endpoint",
        default=None,
        help="Upstream authorization endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-token-endpoint",
        default=None,
        help="Upstream token endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-id",
        default=None,
        help="Upstream client ID for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-secret",
        default=None,
        help="Upstream client secret for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-base-url", default=None, help="Base URL for OAuth Proxy"
    )
    # OIDC Proxy params
    parser.add_argument(
        "--oidc-config-url", default=None, help="OIDC configuration URL"
    )
    parser.add_argument("--oidc-client-id", default=None, help="OIDC client ID")
    parser.add_argument("--oidc-client-secret", default=None, help="OIDC client secret")
    parser.add_argument("--oidc-base-url", default=None, help="Base URL for OIDC Proxy")
    # Remote OAuth params
    parser.add_argument(
        "--remote-auth-servers",
        default=None,
        help="Comma-separated list of authorization servers for Remote OAuth",
    )
    parser.add_argument(
        "--remote-base-url", default=None, help="Base URL for Remote OAuth"
    )
    # Common
    parser.add_argument(
        "--allowed-client-redirect-uris",
        default=None,
        help="Comma-separated list of allowed client redirect URIs",
    )
    # Eunomia params
    parser.add_argument(
        "--eunomia-type",
        default="none",
        choices=["none", "embedded", "remote"],
        help="Eunomia authorization type: 'none' (disabled), 'embedded' (built-in), 'remote' (external) (default: none)",
    )
    parser.add_argument(
        "--eunomia-policy-file",
        default="mcp_policies.json",
        help="Policy file for embedded Eunomia (default: mcp_policies.json)",
    )
    parser.add_argument(
        "--eunomia-remote-url", default=None, help="URL for remote Eunomia server"
    )
    # Delegation params
    parser.add_argument(
        "--enable-delegation",
        action="store_true",
        default=to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
        help="Enable OIDC token delegation",
    )
    parser.add_argument(
        "--audience",
        default=os.environ.get("AUDIENCE", None),
        help="Audience for the delegated token",
    )
    parser.add_argument(
        "--delegated-scopes",
        default=os.environ.get("DELEGATED_SCOPES", "api"),
        help="Scopes for the delegated token (space-separated)",
    )
    parser.add_argument(
        "--openapi-file",
        default=None,
        help="Path to the OpenAPI JSON file to import additional tools from",
    )
    parser.add_argument(
        "--openapi-base-url",
        default=None,
        help="Base URL for the OpenAPI client (overrides instance URL)",
    )
    parser.add_argument(
        "--openapi-use-token",
        action="store_true",
        help="Use the incoming Bearer token (from MCP request) to authenticate OpenAPI import",
    )

    parser.add_argument(
        "--openapi-username",
        default=os.getenv("OPENAPI_USERNAME"),
        help="Username for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-password",
        default=os.getenv("OPENAPI_PASSWORD"),
        help="Password for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-id",
        default=os.getenv("OPENAPI_CLIENT_ID"),
        help="OAuth client ID for OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-secret",
        default=os.getenv("OPENAPI_CLIENT_SECRET"),
        help="OAuth client secret for OpenAPI import",
    )

    args = parser.parse_args()

    if args.port < 0 or args.port > 65535:
        print(f"Error: Port {args.port} is out of valid range (0-65535).")
        sys.exit(1)

    # Update config with CLI arguments
    config["enable_delegation"] = args.enable_delegation
    config["audience"] = args.audience or config["audience"]
    config["delegated_scopes"] = args.delegated_scopes or config["delegated_scopes"]
    config["oidc_config_url"] = args.oidc_config_url or config["oidc_config_url"]
    config["oidc_client_id"] = args.oidc_client_id or config["oidc_client_id"]
    config["oidc_client_secret"] = (
        args.oidc_client_secret or config["oidc_client_secret"]
    )

    # Configure delegation if enabled
    if config["enable_delegation"]:
        if args.auth_type != "oidc-proxy":
            logger.error("Token delegation requires auth-type=oidc-proxy")
            sys.exit(1)
        if not config["audience"]:
            logger.error("audience is required for delegation")
            sys.exit(1)
        if not all(
            [
                config["oidc_config_url"],
                config["oidc_client_id"],
                config["oidc_client_secret"],
            ]
        ):
            logger.error(
                "Delegation requires complete OIDC configuration (oidc-config-url, oidc-client-id, oidc-client-secret)"
            )
            sys.exit(1)

        # Fetch OIDC configuration to get token_endpoint
        try:
            logger.info(
                "Fetching OIDC configuration",
                extra={"oidc_config_url": config["oidc_config_url"]},
            )
            oidc_config_resp = requests.get(config["oidc_config_url"])
            oidc_config_resp.raise_for_status()
            oidc_config = oidc_config_resp.json()
            config["token_endpoint"] = oidc_config.get("token_endpoint")
            if not config["token_endpoint"]:
                logger.error("No token_endpoint found in OIDC configuration")
                raise ValueError("No token_endpoint found in OIDC configuration")
            logger.info(
                "OIDC configuration fetched successfully",
                extra={"token_endpoint": config["token_endpoint"]},
            )
        except Exception as e:
            print(f"Failed to fetch OIDC configuration: {e}")
            logger.error(
                "Failed to fetch OIDC configuration",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            sys.exit(1)

    # Set auth based on type
    auth = None
    allowed_uris = (
        args.allowed_client_redirect_uris.split(",")
        if args.allowed_client_redirect_uris
        else None
    )

    if args.auth_type == "none":
        auth = None
    elif args.auth_type == "static":
        auth = StaticTokenVerifier(
            tokens={
                "test-token": {"client_id": "test-user", "scopes": ["read", "write"]},
                "admin-token": {"client_id": "admin", "scopes": ["admin"]},
            }
        )
    elif args.auth_type == "jwt":
        # Fallback to env vars if not provided via CLI
        jwks_uri = args.token_jwks_uri or os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI")
        issuer = args.token_issuer or os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER")
        audience = args.token_audience or os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE")
        algorithm = args.token_algorithm
        secret_or_key = args.token_secret or args.token_public_key
        public_key_pem = None

        if not (jwks_uri or secret_or_key):
            logger.error(
                "JWT auth requires either --token-jwks-uri or --token-secret/--token-public-key"
            )
            sys.exit(1)
        if not (issuer and audience):
            logger.error("JWT requires --token-issuer and --token-audience")
            sys.exit(1)

        # Load static public key from file if path is given
        if args.token_public_key and os.path.isfile(args.token_public_key):
            try:
                with open(args.token_public_key, "r") as f:
                    public_key_pem = f.read()
                logger.info(f"Loaded static public key from {args.token_public_key}")
            except Exception as e:
                print(f"Failed to read public key file: {e}")
                logger.error(f"Failed to read public key file: {e}")
                sys.exit(1)
        elif args.token_public_key:
            public_key_pem = args.token_public_key  # Inline PEM

        # Validation: Conflicting options
        if jwks_uri and (algorithm or secret_or_key):
            logger.warning(
                "JWKS mode ignores --token-algorithm and --token-secret/--token-public-key"
            )

        # HMAC mode
        if algorithm and algorithm.startswith("HS"):
            if not secret_or_key:
                logger.error(f"HMAC algorithm {algorithm} requires --token-secret")
                sys.exit(1)
            if jwks_uri:
                logger.error("Cannot use --token-jwks-uri with HMAC")
                sys.exit(1)
            public_key = secret_or_key
        else:
            public_key = public_key_pem

        # Required scopes
        required_scopes = None
        if args.required_scopes:
            required_scopes = [
                s.strip() for s in args.required_scopes.split(",") if s.strip()
            ]

        try:
            auth = JWTVerifier(
                jwks_uri=jwks_uri,
                public_key=public_key,
                issuer=issuer,
                audience=audience,
                algorithm=(
                    algorithm if algorithm and algorithm.startswith("HS") else None
                ),
                required_scopes=required_scopes,
            )
            logger.info(
                "JWTVerifier configured",
                extra={
                    "mode": (
                        "JWKS"
                        if jwks_uri
                        else (
                            "HMAC"
                            if algorithm and algorithm.startswith("HS")
                            else "Static Key"
                        )
                    ),
                    "algorithm": algorithm,
                    "required_scopes": required_scopes,
                },
            )
        except Exception as e:
            print(f"Failed to initialize JWTVerifier: {e}")
            logger.error(f"Failed to initialize JWTVerifier: {e}")
            sys.exit(1)
    elif args.auth_type == "oauth-proxy":
        if not (
            args.oauth_upstream_auth_endpoint
            and args.oauth_upstream_token_endpoint
            and args.oauth_upstream_client_id
            and args.oauth_upstream_client_secret
            and args.oauth_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            print(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience"
            )
            logger.error(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience",
                extra={
                    "auth_endpoint": args.oauth_upstream_auth_endpoint,
                    "token_endpoint": args.oauth_upstream_token_endpoint,
                    "client_id": args.oauth_upstream_client_id,
                    "base_url": args.oauth_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = OAuthProxy(
            upstream_authorization_endpoint=args.oauth_upstream_auth_endpoint,
            upstream_token_endpoint=args.oauth_upstream_token_endpoint,
            upstream_client_id=args.oauth_upstream_client_id,
            upstream_client_secret=args.oauth_upstream_client_secret,
            token_verifier=token_verifier,
            base_url=args.oauth_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "oidc-proxy":
        if not (
            args.oidc_config_url
            and args.oidc_client_id
            and args.oidc_client_secret
            and args.oidc_base_url
        ):
            logger.error(
                "oidc-proxy requires oidc-config-url, oidc-client-id, oidc-client-secret, oidc-base-url",
                extra={
                    "config_url": args.oidc_config_url,
                    "client_id": args.oidc_client_id,
                    "base_url": args.oidc_base_url,
                },
            )
            sys.exit(1)
        auth = OIDCProxy(
            config_url=args.oidc_config_url,
            client_id=args.oidc_client_id,
            client_secret=args.oidc_client_secret,
            base_url=args.oidc_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "remote-oauth":
        if not (
            args.remote_auth_servers
            and args.remote_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            logger.error(
                "remote-oauth requires remote-auth-servers, remote-base-url, token-jwks-uri, token-issuer, token-audience",
                extra={
                    "auth_servers": args.remote_auth_servers,
                    "base_url": args.remote_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        auth_servers = [url.strip() for url in args.remote_auth_servers.split(",")]
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = RemoteAuthProvider(
            token_verifier=token_verifier,
            authorization_servers=auth_servers,
            base_url=args.remote_base_url,
        )

    # === 2. Build Middleware List ===
    middlewares: List[
        Union[
            UserTokenMiddleware,
            ErrorHandlingMiddleware,
            RateLimitingMiddleware,
            TimingMiddleware,
            LoggingMiddleware,
            JWTClaimsLoggingMiddleware,
            EunomiaMcpMiddleware,
        ]
    ] = [
        ErrorHandlingMiddleware(include_traceback=True, transform_errors=True),
        RateLimitingMiddleware(max_requests_per_second=10.0, burst_capacity=20),
        TimingMiddleware(),
        LoggingMiddleware(),
        JWTClaimsLoggingMiddleware(),
    ]
    if config["enable_delegation"] or args.auth_type == "jwt":
        middlewares.insert(0, UserTokenMiddleware(config=config))  # Must be first

    if args.eunomia_type in ["embedded", "remote"]:
        try:
            from eunomia_mcp import create_eunomia_middleware

            policy_file = args.eunomia_policy_file or "mcp_policies.json"
            eunomia_endpoint = (
                args.eunomia_remote_url if args.eunomia_type == "remote" else None
            )
            eunomia_mw = create_eunomia_middleware(
                policy_file=policy_file, eunomia_endpoint=eunomia_endpoint
            )
            middlewares.append(eunomia_mw)
            logger.info(f"Eunomia middleware enabled ({args.eunomia_type})")
        except Exception as e:
            print(f"Failed to load Eunomia middleware: {e}")
            logger.error("Failed to load Eunomia middleware", extra={"error": str(e)})
            sys.exit(1)

    mcp = FastMCP("GitLab", auth=auth)
    register_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print("\nStarting GitLab MCP Server")
    print(f"  Transport: {args.transport.upper()}")
    print(f"  Auth: {args.auth_type}")
    print(f"  Delegation: {'ON' if config['enable_delegation'] else 'OFF'}")
    print(f"  Eunomia: {args.eunomia_type}")

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
    gitlab_mcp()
