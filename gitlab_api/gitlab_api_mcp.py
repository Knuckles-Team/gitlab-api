#!/usr/bin/python
# coding: utf-8

import os
import getopt
import sys
from gitlab_api.gitlab_api import Api
from fastmcp import FastMCP, Context
from typing import Optional, List, Dict, Union
from typing_extensions import Annotated
from pydantic import Field

mcp = FastMCP("GitLab")


def to_boolean(string: str) -> bool:
    normalized = str(string).strip().lower()
    true_values = {"t", "true", "y", "yes", "1"}
    false_values = {"f", "false", "n", "no", "0"}
    if normalized in true_values:
        return True
    elif normalized in false_values:
        return False
    else:
        raise ValueError(f"Cannot convert '{string}' to boolean")


environment_gitlab_instance = os.environ.get("GITLAB_INSTANCE", None)
environment_access_token = os.environ.get("ACCESS_TOKEN", None)
environment_verify = to_boolean(os.environ.get("VERIFY", "True"))


# Branches Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"branches"})
def get_branches(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    search: Annotated[
        Optional[str], Field(description="Filter branches by name containing this term")
    ] = None,
    regex: Annotated[
        Optional[str], Field(description="Filter branches by regex pattern on name")
    ] = None,
    branch: Annotated[Optional[str], Field(description="Branch name")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, Dict]]], dict]:
    """Get branches in a GitLab project, optionally filtered."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    if branch:
        response = client.get_branch(**kwargs)
    else:
        response = client.get_branches(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"branches"})
def create_branch(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    branch: Annotated[str, Field(description="New branch name")] = None,
    ref: Annotated[
        str, Field(description="Reference to create from (branch/tag/commit SHA)")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[str, Dict]]:
    """Create a new branch in a GitLab project from a reference."""
    if not project_id or not branch or not ref:
        raise ValueError("project_id, branch, and ref are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.create_branch(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"branches"})
async def delete_branch(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    branch: Annotated[Optional[str], Field(description="Branch name to delete")] = None,
    delete_merged_branches: Annotated[
        Optional[bool],
        Field(description="Delete all merged branches (excluding protected)"),
    ] = False,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
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
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Deletion complete")
    return response.data


# Commits Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
def get_commits(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[Optional[str], Field(description="Commit SHA")] = None,
    ref_name: Annotated[
        Optional[str], Field(description="Branch, tag, or commit SHA to filter commits")
    ] = None,
    since: Annotated[
        Optional[str],
        Field(description="Only commits after this date (ISO 8601 format)"),
    ] = None,
    until: Annotated[
        Optional[str],
        Field(description="Only commits before this date (ISO 8601 format)"),
    ] = None,
    path: Annotated[
        Optional[str], Field(description="Only commits that include this file path")
    ] = None,
    all: Annotated[
        Optional[bool], Field(description="Include all commits across all branches")
    ] = False,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, Dict]]], Dict]:
    """Get commits in a GitLab project, optionally filtered."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    if commit_hash:
        response = client.get_commit(**kwargs)
    else:
        response = client.get_commits(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
def create_commit(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    branch: Annotated[str, Field(description="Branch name for the commit")] = None,
    commit_message: Annotated[str, Field(description="Commit message")] = None,
    actions: Annotated[
        List[Dict[str, str]],
        Field(description="List of actions (create/update/delete files)"),
    ] = None,
    author_email: Annotated[
        Optional[str], Field(description="Author email for the commit")
    ] = None,
    author_name: Annotated[
        Optional[str], Field(description="Author name for the commit")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[str, Dict]]:
    """Create a new commit in a GitLab project."""
    if not project_id or not branch or not commit_message or not actions:
        raise ValueError("project_id, branch, commit_message, and actions are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.create_commit(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
async def get_commit_diff(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[str, Field(description="Commit SHA")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> List[Dict[str, str]]:
    """Get the diff of a specific commit in a GitLab project."""
    if not project_id or not commit_hash:
        raise ValueError("project_id and commit_hash are required")
    if ctx:
        await ctx.info(
            f"Fetching diff for commit {commit_hash} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.get_commit_diff(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Diff retrieval complete")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
def revert_commit(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[str, Field(description="Commit SHA to revert")] = None,
    branch: Annotated[
        str, Field(description="Target branch to apply the revert")
    ] = None,
    dry_run: Annotated[
        Optional[bool], Field(description="Simulate the revert without applying")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[str, Dict]]:
    """Revert a commit in a target branch in a GitLab project.

    - If dry_run=True, simulates the revert without applying changes.
    - Returns the revert commit details or simulation result.
    """
    if not project_id or not commit_hash or not branch:
        raise ValueError("project_id, commit_hash, and branch are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "commit_hash"]
    }
    response = client.revert_commit(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
async def get_commit_comments(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[str, Field(description="Commit SHA")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve comments on a specific commit in a GitLab project."""
    if not project_id or not commit_hash:
        raise ValueError("project_id and commit_hash are required")
    if ctx:
        await ctx.info(
            f"Fetching comments for commit {commit_hash} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.get_commit_comments(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Comments retrieval complete")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
async def create_commit_comment(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[str, Field(description="Commit SHA")] = None,
    note: Annotated[str, Field(description="Content of the comment")] = None,
    path: Annotated[
        Optional[str], Field(description="File path to associate with the comment")
    ] = None,
    line: Annotated[
        Optional[int], Field(description="Line number in the file for the comment")
    ] = None,
    line_type: Annotated[
        Optional[str], Field(description="Type of line ('new' or 'old')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Create a new comment on a specific commit in a GitLab project."""
    if not project_id or not commit_hash or not note:
        raise ValueError("project_id, commit_hash, and note are required")
    if ctx:
        await ctx.info(
            f"Creating comment on commit {commit_hash} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.create_commit_comment(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Comment creation complete")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
async def get_commit_discussions(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[str, Field(description="Commit SHA")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> List[Dict[str, Union[str, List]]]:
    """Retrieve discussions (threaded comments) on a specific commit in a GitLab project."""
    if not project_id or not commit_hash:
        raise ValueError("project_id and commit_hash are required")
    if ctx:
        await ctx.info(
            f"Fetching discussions for commit {commit_hash} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.get_commit_discussions(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Discussions retrieval complete")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
async def get_commit_statuses(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[str, Field(description="Commit SHA")] = None,
    ref: Annotated[
        Optional[str], Field(description="Filter statuses by reference (branch or tag)")
    ] = None,
    stage: Annotated[
        Optional[str], Field(description="Filter statuses by CI stage")
    ] = None,
    name: Annotated[
        Optional[str], Field(description="Filter statuses by job name")
    ] = None,
    coverage: Annotated[
        Optional[bool], Field(description="Include coverage information")
    ] = None,
    all: Annotated[Optional[bool], Field(description="Include all statuses")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> List[Dict[str, Union[str, bool]]]:
    """Retrieve build/CI statuses for a specific commit in a GitLab project."""
    if not project_id or not commit_hash:
        raise ValueError("project_id and commit_hash are required")
    if ctx:
        await ctx.info(
            f"Fetching statuses for commit {commit_hash} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.get_commit_statuses(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Statuses retrieval complete")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
async def post_build_status_to_commit(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[str, Field(description="Commit SHA")] = None,
    state: Annotated[
        str,
        Field(
            description="State of the build (e.g., 'pending', 'running', 'success', 'failed')"
        ),
    ] = None,
    target_url: Annotated[
        Optional[str], Field(description="URL to link to the build")
    ] = None,
    context: Annotated[
        Optional[str], Field(description="Context of the status (e.g., 'ci/build')")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="Description of the status")
    ] = None,
    coverage: Annotated[
        Optional[float], Field(description="Coverage percentage")
    ] = None,
    pipeline_id: Annotated[
        Optional[int], Field(description="ID of the associated pipeline")
    ] = None,
    ref: Annotated[
        Optional[str], Field(description="Reference (branch or tag) for the status")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, bool]]:
    """Post a build/CI status to a specific commit in a GitLab project."""
    if not project_id or not commit_hash or not state:
        raise ValueError("project_id, commit_hash, and state are required")
    if ctx:
        await ctx.info(
            f"Posting build status for commit {commit_hash} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.post_build_status_to_commit(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Build status posted successfully")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
async def get_commit_merge_requests(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[str, Field(description="Commit SHA")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve merge requests associated with a specific commit in a GitLab project."""
    if not project_id or not commit_hash:
        raise ValueError("project_id and commit_hash are required")
    if ctx:
        await ctx.info(
            f"Fetching merge requests for commit {commit_hash} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.get_commit_merge_requests(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Merge requests retrieval complete")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"commits"})
async def get_commit_gpg_signature(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    commit_hash: Annotated[str, Field(description="Commit SHA")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, bool]]:
    """Retrieve the GPG signature for a specific commit in a GitLab project."""
    if not project_id or not commit_hash:
        raise ValueError("project_id and commit_hash are required")
    if ctx:
        await ctx.info(
            f"Fetching GPG signature for commit {commit_hash} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.get_commit_gpg_signature(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("GPG signature retrieval complete")
    return response.data


# Deploy Tokens Tools
@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"deploy_tokens"}
)
def get_deploy_tokens(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of all deploy tokens for the GitLab instance."""
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_deploy_tokens()
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"deploy_tokens"}
)
def get_project_deploy_tokens(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    token_id: Annotated[Optional[int], Field(description="Deploy token ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], dict]:
    """Retrieve a list of deploy tokens for a specific GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    if token_id:
        response = client.get_project_deploy_token(
            project_id=project_id, token=token_id
        )
    else:
        response = client.get_project_deploy_tokens(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"deploy_tokens"}
)
async def create_project_deploy_token(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[str, Field(description="Name of the deploy token")] = None,
    scopes: Annotated[
        List[str],
        Field(description="Scopes for the deploy token (e.g., ['read_repository'])"),
    ] = None,
    expires_at: Annotated[
        Optional[str], Field(description="Expiration date (ISO 8601 format)")
    ] = None,
    username: Annotated[
        Optional[str], Field(description="Username associated with the token")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Create a deploy token for a GitLab project with specified name and scopes."""
    if not project_id or not name or not scopes:
        raise ValueError("project_id, name, and scopes are required")
    if ctx:
        await ctx.info(f"Creating deploy token '{name}' for project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.create_project_deploy_token(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Deploy token created")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"deploy_tokens"}
)
async def delete_project_deploy_token(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    token_id: Annotated[int, Field(description="Deploy token ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a specific deploy token for a GitLab project."""
    if not project_id or not token_id:
        raise ValueError("project_id and token_id are required")
    if ctx:
        await ctx.info(f"Deleting deploy token {token_id} for project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_project_deploy_token(project_id=project_id, token=token_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Deploy token deleted")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"deploy_tokens"}
)
def get_group_deploy_tokens(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    token_id: Annotated[
        Optional[int], Field(description="Deploy token ID for single retrieval")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]:
    """Retrieve deploy tokens for a GitLab group (list or single by ID)."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    if token_id:
        response = client.get_group_deploy_token(group_id=group_id, token=token_id)
    else:
        response = client.get_group_deploy_tokens(group_id=group_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"deploy_tokens"}
)
async def create_group_deploy_token(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    name: Annotated[str, Field(description="Name of the deploy token")] = None,
    scopes: Annotated[
        List[str],
        Field(description="Scopes for the deploy token (e.g., ['read_repository'])"),
    ] = None,
    expires_at: Annotated[
        Optional[str], Field(description="Expiration date (ISO 8601 format)")
    ] = None,
    username: Annotated[
        Optional[str], Field(description="Username associated with the token")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Create a deploy token for a GitLab group with specified name and scopes."""
    if not group_id or not name or not scopes:
        raise ValueError("group_id, name, and scopes are required")
    if ctx:
        await ctx.info(f"Creating deploy token '{name}' for group {group_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.create_group_deploy_token(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Deploy token created")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"deploy_tokens"}
)
async def delete_group_deploy_token(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    token_id: Annotated[int, Field(description="Deploy token ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a specific deploy token for a GitLab group."""
    if not group_id or not token_id:
        raise ValueError("group_id and token_id are required")
    if ctx:
        await ctx.info(f"Deleting deploy token {token_id} for group {group_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_group_deploy_token(group_id=group_id, token=token_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Deploy token deleted")
    return response.data


# Environments Tools
@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
def get_environments(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    environment_id: Annotated[
        Optional[int], Field(description="Environment ID")
    ] = None,
    name: Annotated[
        Optional[str], Field(description="Filter environments by exact name")
    ] = None,
    search: Annotated[
        Optional[str], Field(description="Filter environments by search term in name")
    ] = None,
    states: Annotated[
        Optional[str],
        Field(
            description="Filter environments by state (e.g., 'available', 'stopped')"
        ),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]:
    """Retrieve a list of environments for a GitLab project, optionally filtered by name, search, or states or a single environment by id."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    else:
        response = client.get_environments(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
async def create_environment(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[str, Field(description="Name of the environment")] = None,
    external_url: Annotated[
        Optional[str], Field(description="External URL for the environment")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Create a new environment in a GitLab project with a specified name and optional external URL."""
    if not project_id or not name:
        raise ValueError("project_id and name are required")
    if ctx:
        await ctx.info(f"Creating environment '{name}' for project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Environment created")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
async def update_environment(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    environment_id: Annotated[int, Field(description="Environment ID")] = None,
    name: Annotated[
        Optional[str], Field(description="New name for the environment")
    ] = None,
    external_url: Annotated[
        Optional[str], Field(description="New external URL for the environment")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Update an existing environment in a GitLab project with new name or external URL."""
    if not project_id or not environment_id:
        raise ValueError("project_id and environment_id are required")
    if not name and not external_url:
        raise ValueError("At least one of name or external_url must be provided")
    if ctx:
        await ctx.info(f"Updating environment {environment_id} in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Environment updated")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
async def delete_environment(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    environment_id: Annotated[int, Field(description="Environment ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a specific environment in a GitLab project."""
    if not project_id or not environment_id:
        raise ValueError("project_id and environment_id are required")
    if ctx:
        await ctx.info(f"Deleting environment {environment_id} in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_environment(
        project_id=project_id, environment_id=environment_id
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Environment deleted")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
async def stop_environment(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    environment_id: Annotated[int, Field(description="Environment ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Stop a specific environment in a GitLab project."""
    if not project_id or not environment_id:
        raise ValueError("project_id and environment_id are required")
    if ctx:
        await ctx.info(f"Stopping environment {environment_id} in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.stop_environment(
        project_id=project_id, environment_id=environment_id
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Environment stopped")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
async def stop_stale_environments(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    older_than: Annotated[
        Optional[str],
        Field(
            description="Filter environments older than this timestamp (ISO 8601 format)"
        ),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, List[str]]:
    """Stop stale environments in a GitLab project, optionally filtered by older_than timestamp."""
    if not project_id:
        raise ValueError("project_id is required")
    if ctx:
        await ctx.info(f"Stopping stale environments in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Stale environments stopped")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
async def delete_stopped_environments(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, List[str]]:
    """Delete stopped review app environments in a GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    if ctx:
        await ctx.info(f"Deleting stopped review apps in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_stopped_environments(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Stopped review apps deleted")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
def get_protected_environments(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[str, Field(description="Name of the protected environment")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]:
    """Retrieve protected environments in a GitLab project (list or single by name)."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    if name:
        response = client.get_protected_environment(project_id=project_id, name=name)
    else:
        response = client.get_protected_environments(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
async def protect_environment(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[
        str, Field(description="Name of the environment to protect")
    ] = None,
    required_approval_count: Annotated[
        Optional[int], Field(description="Number of approvals required for deployment")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Protect an environment in a GitLab project with optional approval count."""
    if not project_id or not name:
        raise ValueError("project_id and name are required")
    if ctx:
        await ctx.info(f"Protecting environment '{name}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Environment protected")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
async def update_protected_environment(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[str, Field(description="Name of the protected environment")] = None,
    required_approval_count: Annotated[
        Optional[int],
        Field(description="New number of approvals required for deployment"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Update a protected environment in a GitLab project with new approval count."""
    if not project_id or not name:
        raise ValueError("project_id and name are required")
    if not required_approval_count:
        raise ValueError("required_approval_count must be provided")
    if ctx:
        await ctx.info(
            f"Updating protected environment '{name}' in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Protected environment updated")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"environments"}
)
async def unprotect_environment(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[
        str, Field(description="Name of the environment to unprotect")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Unprotect a specific environment in a GitLab project."""
    if not project_id or not name:
        raise ValueError("project_id and name are required")
    if ctx:
        await ctx.info(f"Unprotecting environment '{name}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.unprotect_environment(project_id=project_id, name=name)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Environment unprotected")
    return response.data


# Groups Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"})
def get_groups(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[Optional[str], Field(description="Group ID or path")] = None,
    search: Annotated[
        Optional[str], Field(description="Filter groups by search term in name or path")
    ] = None,
    sort: Annotated[
        Optional[str], Field(description="Sort order (e.g., 'asc', 'desc')")
    ] = None,
    order_by: Annotated[
        Optional[str], Field(description="Field to sort by (e.g., 'name', 'path')")
    ] = None,
    owned: Annotated[
        Optional[bool],
        Field(description="Filter groups owned by the authenticated user"),
    ] = None,
    min_access_level: Annotated[
        Optional[int],
        Field(description="Filter groups by minimum access level (e.g., 10 for Guest)"),
    ] = None,
    top_level_only: Annotated[
        Optional[bool],
        Field(description="Include only top-level groups (exclude subgroups)"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int, List]]]:
    """Retrieve a list of groups, optionally filtered by search, sort, ownership, or access level or retrieve a single group by id."""
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    if group_id:
        response = client.get_group(group_id=group_id, **kwargs)
    else:
        response = client.get_groups(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"})
async def edit_group(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    name: Annotated[Optional[str], Field(description="New name for the group")] = None,
    path: Annotated[Optional[str], Field(description="New path for the group")] = None,
    description: Annotated[
        Optional[str], Field(description="New description for the group")
    ] = None,
    visibility: Annotated[
        Optional[str],
        Field(description="New visibility level (e.g., 'public', 'private')"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Edit a specific GitLab group's details (name, path, description, or visibility)."""
    if not group_id:
        raise ValueError("group_id is required")
    if not any([name, path, description, visibility]):
        raise ValueError(
            "At least one of name, path, description, or visibility must be provided"
        )
    if ctx:
        await ctx.info(f"Editing group {group_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Group edited")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"})
def get_group_subgroups(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    search: Annotated[
        Optional[str],
        Field(description="Filter subgroups by search term in name or path"),
    ] = None,
    sort: Annotated[
        Optional[str], Field(description="Sort order (e.g., 'asc', 'desc')")
    ] = None,
    order_by: Annotated[
        Optional[str], Field(description="Field to sort by (e.g., 'name', 'path')")
    ] = None,
    owned: Annotated[
        Optional[bool],
        Field(description="Filter subgroups owned by the authenticated user"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of subgroups for a specific GitLab group, optionally filtered."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_subgroups(group_id=group_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"})
def get_group_descendant_groups(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    search: Annotated[
        Optional[str],
        Field(description="Filter descendant groups by search term in name or path"),
    ] = None,
    sort: Annotated[
        Optional[str], Field(description="Sort order (e.g., 'asc', 'desc')")
    ] = None,
    order_by: Annotated[
        Optional[str], Field(description="Field to sort by (e.g., 'name', 'path')")
    ] = None,
    owned: Annotated[
        Optional[bool],
        Field(description="Filter descendant groups owned by the authenticated user"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of all descendant groups for a specific GitLab group, optionally filtered."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_descendant_groups(group_id=group_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"})
def get_group_projects(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    include_subgroups: Annotated[
        Optional[bool], Field(description="Include projects from subgroups")
    ] = None,
    search: Annotated[
        Optional[str],
        Field(description="Filter projects by search term in name or path"),
    ] = None,
    sort: Annotated[
        Optional[str], Field(description="Sort order (e.g., 'asc', 'desc')")
    ] = None,
    order_by: Annotated[
        Optional[str], Field(description="Field to sort by (e.g., 'name', 'path')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of projects associated with a specific GitLab group, optionally including subgroups."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_projects(group_id=group_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"groups"})
def get_group_merge_requests(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    state: Annotated[
        Optional[str],
        Field(description="Filter merge requests by state (e.g., 'opened', 'closed')"),
    ] = None,
    scope: Annotated[
        Optional[str],
        Field(description="Filter merge requests by scope (e.g., 'created_by_me')"),
    ] = None,
    milestone: Annotated[
        Optional[str], Field(description="Filter merge requests by milestone title")
    ] = None,
    search: Annotated[
        Optional[str],
        Field(
            description="Filter merge requests by search term in title or description"
        ),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of merge requests associated with a specific GitLab group, optionally filtered."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_merge_requests(group_id=group_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


# Jobs Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
def get_project_jobs(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    job_id: Annotated[Optional[int], Field(description="Job ID")] = None,
    scope: Annotated[
        Optional[str],
        Field(description="Filter jobs by scope (e.g., 'success', 'failed')"),
    ] = None,
    include_retried: Annotated[
        Optional[bool], Field(description="Include retried jobs")
    ] = None,
    include_invisible: Annotated[
        Optional[bool],
        Field(description="Include invisible jobs (e.g., from hidden pipelines)"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]:
    """Retrieve a list of jobs for a specific GitLab project, optionally filtered by scope or a single job by id."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    if job_id:
        response = client.get_project_job(project_id=project_id, job_id=job_id)
    else:
        response = client.get_project_jobs(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
def get_project_job_log(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    job_id: Annotated[int, Field(description="Job ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, str]:
    """Retrieve the log (trace) of a specific job in a GitLab project."""
    if not project_id or not job_id:
        raise ValueError("project_id and job_id are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_project_job_log(project_id=project_id, job_id=job_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
async def cancel_project_job(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    job_id: Annotated[int, Field(description="Job ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Cancel a specific job in a GitLab project."""
    if not project_id or not job_id:
        raise ValueError("project_id and job_id are required")
    if ctx:
        await ctx.info(f"Cancelling job {job_id} in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.cancel_project_job(project_id=project_id, job_id=job_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Job cancelled")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
async def retry_project_job(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    job_id: Annotated[int, Field(description="Job ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Retry a specific job in a GitLab project."""
    if not project_id or not job_id:
        raise ValueError("project_id and job_id are required")
    if ctx:
        await ctx.info(f"Retrying job {job_id} in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.retry_project_job(project_id=project_id, job_id=job_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Job retried")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
async def erase_project_job(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    job_id: Annotated[int, Field(description="Job ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Erase (delete artifacts and logs of) a specific job in a GitLab project."""
    if not project_id or not job_id:
        raise ValueError("project_id and job_id are required")
    if ctx:
        await ctx.info(f"Erasing job {job_id} in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.erase_project_job(project_id=project_id, job_id=job_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Job erased")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
async def run_project_job(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    job_id: Annotated[int, Field(description="Job ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Run (play) a specific manual job in a GitLab project."""
    if not project_id or not job_id:
        raise ValueError("project_id and job_id are required")
    if ctx:
        await ctx.info(f"Running job {job_id} in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.run_project_job(project_id=project_id, job_id=job_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Job started")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"jobs"})
def get_pipeline_jobs(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_id: Annotated[int, Field(description="Pipeline ID")] = None,
    scope: Annotated[
        Optional[str],
        Field(description="Filter jobs by scope (e.g., 'success', 'failed')"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of jobs for a specific pipeline in a GitLab project, optionally filtered by scope."""
    if not project_id or not pipeline_id:
        raise ValueError("project_id and pipeline_id are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


# Members Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"members"})
def get_group_members(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    query: Annotated[
        Optional[str],
        Field(description="Filter members by search term in name or username"),
    ] = None,
    user_ids: Annotated[
        Optional[List[int]], Field(description="Filter members by user IDs")
    ] = None,
    skip_users: Annotated[
        Optional[List[int]], Field(description="Exclude specified user IDs")
    ] = None,
    show_seat_info: Annotated[
        Optional[bool], Field(description="Include seat information for members")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of members in a specific GitLab group, optionally filtered by query or user IDs."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_members(group_id=group_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"members"})
def get_project_members(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    query: Annotated[
        Optional[str],
        Field(description="Filter members by search term in name or username"),
    ] = None,
    user_ids: Annotated[
        Optional[List[int]], Field(description="Filter members by user IDs")
    ] = None,
    skip_users: Annotated[
        Optional[List[int]], Field(description="Exclude specified user IDs")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of members in a specific GitLab project, optionally filtered by query or user IDs."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_project_members(project_id=project_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


# Merge Request Tools
@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_requests"}
)
async def create_merge_request(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    source_branch: Annotated[
        str, Field(description="Source branch for the merge request")
    ] = None,
    target_branch: Annotated[
        str, Field(description="Target branch for the merge request")
    ] = None,
    title: Annotated[str, Field(description="Title of the merge request")] = None,
    description: Annotated[
        Optional[str], Field(description="Description of the merge request")
    ] = None,
    assignee_id: Annotated[
        Optional[int],
        Field(description="ID of the user to assign the merge request to"),
    ] = None,
    reviewer_ids: Annotated[
        Optional[List[int]], Field(description="IDs of users to set as reviewers")
    ] = None,
    labels: Annotated[
        Optional[List[str]], Field(description="Labels to apply to the merge request")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Create a new merge request in a GitLab project with specified source and target branches."""
    if not project_id or not source_branch or not target_branch or not title:
        raise ValueError(
            "project_id, source_branch, target_branch, and title are required"
        )
    if ctx:
        await ctx.info(f"Creating merge request '{title}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Merge request created")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_requests"}
)
def get_merge_requests(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    state: Annotated[
        Optional[str],
        Field(description="Filter merge requests by state (e.g., 'opened', 'closed')"),
    ] = None,
    scope: Annotated[
        Optional[str],
        Field(description="Filter merge requests by scope (e.g., 'created_by_me')"),
    ] = None,
    milestone: Annotated[
        Optional[str], Field(description="Filter merge requests by milestone title")
    ] = None,
    view: Annotated[
        Optional[str],
        Field(description="Filter merge requests by view (e.g., 'simple')"),
    ] = None,
    labels: Annotated[
        Optional[List[str]], Field(description="Filter merge requests by labels")
    ] = None,
    author_id: Annotated[
        Optional[int], Field(description="Filter merge requests by author ID")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of merge requests across all projects, optionally filtered by state, scope, or labels."""
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_merge_requests(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_requests"}
)
def get_project_merge_requests(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    merge_id: Annotated[Optional[int], Field(description="Merge request ID")] = None,
    state: Annotated[
        Optional[str],
        Field(description="Filter merge requests by state (e.g., 'opened', 'closed')"),
    ] = None,
    scope: Annotated[
        Optional[str],
        Field(description="Filter merge requests by scope (e.g., 'created_by_me')"),
    ] = None,
    milestone: Annotated[
        Optional[str], Field(description="Filter merge requests by milestone title")
    ] = None,
    labels: Annotated[
        Optional[List[str]], Field(description="Filter merge requests by labels")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]:
    """Retrieve a list of merge requests for a specific GitLab project, optionally filtered or a single merge request or a single merge request by merge id"""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    else:
        response = client.get_project_merge_requests(project_id=project_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
def get_project_level_merge_request_approval_rules(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    approval_rule_id: Annotated[int, Field(description="Approval rule ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]:
    """Retrieve project-level merge request approval rules for a GitLab project details of a specific project-level merge request approval rule."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    if approval_rule_id:
        response = client.get_project_level_rule(
            project_id=project_id, approval_rule_id=approval_rule_id
        )
    else:
        response = client.get_project_level_rule(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
async def create_project_level_rule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[str, Field(description="Name of the approval rule")] = None,
    approvals_required: Annotated[
        Optional[int], Field(description="Number of approvals required")
    ] = None,
    rule_type: Annotated[
        Optional[str], Field(description="Type of rule (e.g., 'regular')")
    ] = None,
    user_ids: Annotated[
        Optional[List[int]], Field(description="List of user IDs required to approve")
    ] = None,
    group_ids: Annotated[
        Optional[List[int]], Field(description="List of group IDs required to approve")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Create a new project-level merge request approval rule."""
    if not project_id or not name:
        raise ValueError("project_id and name are required")
    if ctx:
        await ctx.info(f"Creating approval rule '{name}' for project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Approval rule created")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
async def update_project_level_rule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    approval_rule_id: Annotated[int, Field(description="Approval rule ID")] = None,
    name: Annotated[
        Optional[str], Field(description="New name for the approval rule")
    ] = None,
    approvals_required: Annotated[
        Optional[int], Field(description="New number of approvals required")
    ] = None,
    user_ids: Annotated[
        Optional[List[int]],
        Field(description="Updated list of user IDs required to approve"),
    ] = None,
    group_ids: Annotated[
        Optional[List[int]],
        Field(description="Updated list of group IDs required to approve"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
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
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Approval rule updated")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
async def delete_project_level_rule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    approval_rule_id: Annotated[int, Field(description="Approval rule ID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a project-level merge request approval rule."""
    if not project_id or not approval_rule_id:
        raise ValueError("project_id and approval_rule_id are required")
    if ctx:
        await ctx.info(
            f"Deleting approval rule {approval_rule_id} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_project_level_rule(
        project_id=project_id, approval_rule_id=approval_rule_id
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Approval rule deleted")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
def merge_request_level_approvals(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    merge_request_iid: Annotated[int, Field(description="Merge request IID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[bool, List]]:
    """Retrieve approvals for a specific merge request in a GitLab project."""
    if not project_id or not merge_request_iid:
        raise ValueError("project_id and merge_request_iid are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.merge_request_level_approvals(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
def get_approval_state_merge_requests(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    merge_request_iid: Annotated[int, Field(description="Merge request IID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[bool, int]]:
    """Retrieve the approval state of a specific merge request in a GitLab project."""
    if not project_id or not merge_request_iid:
        raise ValueError("project_id and merge_request_iid are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_approval_state_merge_requests(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
def get_merge_request_level_rules(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    merge_request_iid: Annotated[int, Field(description="Merge request IID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve merge request-level approval rules for a specific merge request in a GitLab project."""
    if not project_id or not merge_request_iid:
        raise ValueError("project_id and merge_request_iid are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_merge_request_level_rules(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
async def approve_merge_request(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    merge_request_iid: Annotated[int, Field(description="Merge request IID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Approve a specific merge request in a GitLab project."""
    if not project_id or not merge_request_iid:
        raise ValueError("project_id and merge_request_iid are required")
    if ctx:
        await ctx.info(
            f"Approving merge request {merge_request_iid} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.approve_merge_request(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Merge request approved")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
async def unapprove_merge_request(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    merge_request_iid: Annotated[int, Field(description="Merge request IID")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Unapprove a specific merge request in a GitLab project."""
    if not project_id or not merge_request_iid:
        raise ValueError("project_id and merge_request_iid are required")
    if ctx:
        await ctx.info(
            f"Unapproving merge request {merge_request_iid} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.unapprove_merge_request(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Merge request unapproved")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
def get_group_level_rule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[bool, int]]:
    """Retrieve merge request approval settings for a specific GitLab group."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_group_level_rule(group_id=group_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
async def edit_group_level_rule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    allow_author_approval: Annotated[
        Optional[bool],
        Field(description="Whether authors can approve their own merge requests"),
    ] = None,
    allow_committer_approval: Annotated[
        Optional[bool],
        Field(description="Whether committers can approve merge requests"),
    ] = None,
    allow_overrides_to_approver_list: Annotated[
        Optional[bool],
        Field(description="Whether overrides to the approver list are allowed"),
    ] = None,
    minimum_approvals: Annotated[
        Optional[int], Field(description="Minimum number of approvals required")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[bool, int]]:
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
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Approval settings edited")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
def get_project_level_rule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[bool, int]]:
    """Retrieve merge request approval settings for a specific GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_project_level_rule(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"merge_rules"}
)
async def edit_project_level_rule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    allow_author_approval: Annotated[
        Optional[bool],
        Field(description="Whether authors can approve their own merge requests"),
    ] = None,
    allow_committer_approval: Annotated[
        Optional[bool],
        Field(description="Whether committers can approve merge requests"),
    ] = None,
    allow_overrides_to_approver_list: Annotated[
        Optional[bool],
        Field(description="Whether overrides to the approver list are allowed"),
    ] = None,
    minimum_approvals: Annotated[
        Optional[int], Field(description="Minimum number of approvals required")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[bool, int]]:
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
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Approval settings edited")
    return response.data


# Packages Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"packages"})
def get_repository_packages(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    package_type: Annotated[
        Optional[str],
        Field(description="Filter packages by type (e.g., 'npm', 'maven')"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of repository packages for a specific GitLab project, optionally filtered by package type."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_repository_packages(project_id=project_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"packages"})
async def publish_repository_package(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    package_name: Annotated[str, Field(description="Name of the package")] = None,
    package_version: Annotated[str, Field(description="Version of the package")] = None,
    file_name: Annotated[str, Field(description="Name of the package file")] = None,
    status: Annotated[
        Optional[str],
        Field(description="Status of the package (e.g., 'default', 'hidden')"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Publish a repository package to a specific GitLab project."""
    if not project_id or not package_name or not package_version or not file_name:
        raise ValueError(
            "project_id, package_name, package_version, and file_name are required"
        )
    if ctx:
        await ctx.info(
            f"Publishing package {package_name}/{package_version} to project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Package published")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"packages"})
def download_repository_package(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    package_name: Annotated[str, Field(description="Name of the package")] = None,
    package_version: Annotated[str, Field(description="Version of the package")] = None,
    file_name: Annotated[
        str, Field(description="Name of the package file to download")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, str]:
    """Download a repository package from a specific GitLab project."""
    if not project_id or not package_name or not package_version or not file_name:
        raise ValueError(
            "project_id, package_name, package_version, and file_name are required"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.download_repository_package(
        project_id=project_id,
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


# Pipeline Tools
@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"pipelines"}
)
def get_pipelines(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_id: Annotated[Optional[int], Field(description="Pipeline ID")] = None,
    scope: Annotated[
        Optional[str],
        Field(description="Filter pipelines by scope (e.g., 'running', 'branches')"),
    ] = None,
    status: Annotated[
        Optional[str],
        Field(description="Filter pipelines by status (e.g., 'success', 'failed')"),
    ] = None,
    ref: Annotated[
        Optional[str],
        Field(description="Filter pipelines by reference (e.g., branch or tag name)"),
    ] = None,
    source: Annotated[
        Optional[str],
        Field(description="Filter pipelines by source (e.g., 'push', 'schedule')"),
    ] = None,
    updated_after: Annotated[
        Optional[str],
        Field(description="Filter pipelines updated after this date (ISO 8601 format)"),
    ] = None,
    updated_before: Annotated[
        Optional[str],
        Field(
            description="Filter pipelines updated before this date (ISO 8601 format)"
        ),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]:
    """Retrieve a list of pipelines for a specific GitLab project, optionally filtered by scope, status, or ref or details of a specific pipeline in a GitLab project.."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    if pipeline_id:
        response = client.get_pipeline(project_id=project_id, pipeline_id=pipeline_id)
    else:
        response = client.get_pipelines(project_id=project_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"], tags={"pipelines"}
)
async def run_pipeline(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    ref: Annotated[
        str, Field(description="Reference (e.g., branch or tag) to run the pipeline on")
    ] = None,
    variables: Annotated[
        Optional[Dict[str, str]], Field(description="Dictionary of pipeline variables")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Run a pipeline for a specific GitLab project with a given reference (e.g., branch or tag)."""
    if not project_id or not ref:
        raise ValueError("project_id and ref are required")
    if ctx:
        await ctx.info(f"Running pipeline for project {project_id} on ref {ref}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.run_pipeline(project_id=project_id, ref=ref, variables=variables)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Pipeline started")
    return response.data


# Pipeline Schedules Tools
@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
def get_pipeline_schedules(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of pipeline schedules for a specific GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_pipeline_schedules(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
def get_pipeline_schedule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_schedule_id: Annotated[
        int, Field(description="Pipeline schedule ID")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[str, int]]:
    """Retrieve details of a specific pipeline schedule in a GitLab project."""
    if not project_id or not pipeline_schedule_id:
        raise ValueError("project_id and pipeline_schedule_id are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_pipeline_schedule(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
def get_pipelines_triggered_from_schedule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_schedule_id: Annotated[
        int, Field(description="Pipeline schedule ID")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve pipelines triggered by a specific pipeline schedule in a GitLab project."""
    if not project_id or not pipeline_schedule_id:
        raise ValueError("project_id and pipeline_schedule_id are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_pipelines_triggered_from_schedule(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
async def create_pipeline_schedule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    description: Annotated[
        Optional[str], Field(description="Description of the pipeline schedule")
    ] = None,
    ref: Annotated[
        str, Field(description="Reference (e.g., branch or tag) for the pipeline")
    ] = None,
    cron: Annotated[
        str,
        Field(description="Cron expression defining the schedule (e.g., '0 0 * * *')"),
    ] = None,
    cron_timezone: Annotated[
        Optional[str], Field(description="Timezone for the cron schedule (e.g., 'UTC')")
    ] = None,
    active: Annotated[
        Optional[bool], Field(description="Whether the schedule is active")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Create a pipeline schedule for a specific GitLab project."""
    if not project_id or not ref or not cron:
        raise ValueError("project_id, ref, and cron are required")
    if ctx:
        await ctx.info(
            f"Creating pipeline schedule '{description or 'no description'}' for project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Pipeline schedule created")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
async def edit_pipeline_schedule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_schedule_id: Annotated[
        int, Field(description="Pipeline schedule ID")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="New description of the pipeline schedule")
    ] = None,
    ref: Annotated[
        Optional[str],
        Field(description="New reference (e.g., branch or tag) for the pipeline"),
    ] = None,
    cron: Annotated[
        Optional[str],
        Field(description="New cron expression for the schedule (e.g., '0 0 * * *')"),
    ] = None,
    cron_timezone: Annotated[
        Optional[str],
        Field(description="New timezone for the cron schedule (e.g., 'UTC')"),
    ] = None,
    active: Annotated[
        Optional[bool], Field(description="Whether the schedule is active")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
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
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Pipeline schedule edited")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
async def take_pipeline_schedule_ownership(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_schedule_id: Annotated[
        int, Field(description="Pipeline schedule ID")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Take ownership of a pipeline schedule in a GitLab project."""
    if not project_id or not pipeline_schedule_id:
        raise ValueError("project_id and pipeline_schedule_id are required")
    if ctx:
        await ctx.info(
            f"Taking ownership of pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.take_pipeline_schedule_ownership(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Ownership taken")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
async def delete_pipeline_schedule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_schedule_id: Annotated[
        int, Field(description="Pipeline schedule ID")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a pipeline schedule in a GitLab project."""
    if not project_id or not pipeline_schedule_id:
        raise ValueError("project_id and pipeline_schedule_id are required")
    if ctx:
        await ctx.info(
            f"Deleting pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_pipeline_schedule(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Pipeline schedule deleted")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
async def run_pipeline_schedule(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_schedule_id: Annotated[
        int, Field(description="Pipeline schedule ID")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Run a pipeline schedule immediately in a GitLab project."""
    if not project_id or not pipeline_schedule_id:
        raise ValueError("project_id and pipeline_schedule_id are required")
    if ctx:
        await ctx.info(
            f"Running pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.run_pipeline_schedule(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Pipeline schedule run started")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
async def create_pipeline_schedule_variable(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_schedule_id: Annotated[
        int, Field(description="Pipeline schedule ID")
    ] = None,
    key: Annotated[str, Field(description="Key of the variable")] = None,
    value: Annotated[str, Field(description="Value of the variable")] = None,
    variable_type: Annotated[
        Optional[str], Field(description="Type of variable (e.g., 'env_var')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Create a variable for a pipeline schedule in a GitLab project."""
    if not project_id or not pipeline_schedule_id or not key or not value:
        raise ValueError(
            "project_id, pipeline_schedule_id, key, and value are required"
        )
    if ctx:
        await ctx.info(
            f"Creating variable '{key}' for pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Variable created")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"pipeline_schedules"},
)
async def delete_pipeline_schedule_variable(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    pipeline_schedule_id: Annotated[
        int, Field(description="Pipeline schedule ID")
    ] = None,
    key: Annotated[str, Field(description="Key of the variable to delete")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a variable from a pipeline schedule in a GitLab project."""
    if not project_id or not pipeline_schedule_id or not key:
        raise ValueError("project_id, pipeline_schedule_id, and key are required")
    if ctx:
        await ctx.info(
            f"Deleting variable '{key}' from pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_pipeline_schedule_variable(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id, key=key
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Variable deleted")
    return response.data


# Projects Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
def get_projects(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[
        Optional[str], Field(description="Project ID or path")
    ] = None,
    owned: Annotated[
        Optional[bool],
        Field(description="Filter projects owned by the authenticated user"),
    ] = None,
    search: Annotated[
        Optional[str],
        Field(description="Filter projects by search term in name or path"),
    ] = None,
    sort: Annotated[
        Optional[str],
        Field(description="Sort projects by criteria (e.g., 'created_at', 'name')"),
    ] = None,
    visibility: Annotated[
        Optional[str],
        Field(description="Filter projects by visibility (e.g., 'public', 'private')"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]:
    """Retrieve a list of projects, optionally filtered by ownership, search, sort, or visibility or Retrieve details of a specific GitLab project.."""
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    if project_id:
        response = client.get_project(project_id=project_id)
    else:
        response = client.get_projects(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
def get_nested_projects_by_group(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    per_page: Annotated[
        Optional[int], Field(description="Number of projects per page")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of nested projects within a GitLab group, including descendant groups."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_nested_projects_by_group(group_id=group_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
def get_project_contributors(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of contributors to a specific GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_project_contributors(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
def get_project_statistics(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, int]:
    """Retrieve statistics for a specific GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_project_statistics(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
async def edit_project(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[Optional[str], Field(description="New name of the project")] = None,
    description: Annotated[
        Optional[str], Field(description="New description of the project")
    ] = None,
    visibility: Annotated[
        Optional[str],
        Field(description="New visibility of the project (e.g., 'public', 'private')"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Edit a specific GitLab project's details (name, description, or visibility)."""
    if not project_id:
        raise ValueError("project_id is required")
    if not any([name, description, visibility]):
        raise ValueError(
            "At least one of name, description, or visibility must be provided"
        )
    if ctx:
        await ctx.info(f"Editing project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Project edited")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
def get_project_groups(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    skip_groups: Annotated[
        Optional[List[int]], Field(description="List of group IDs to exclude")
    ] = None,
    search: Annotated[
        Optional[str], Field(description="Filter groups by search term in name")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of groups associated with a specific GitLab project, optionally filtered."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_project_groups(project_id=project_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
async def archive_project(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Archive a specific GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    if ctx:
        await ctx.info(f"Archiving project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.archive_project(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Project archived")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
async def unarchive_project(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Unarchive a specific GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    if ctx:
        await ctx.info(f"Unarchiving project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.unarchive_project(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Project unarchived")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
async def delete_project(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a specific GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    if ctx:
        await ctx.info(f"Deleting project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_project(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Project deleted")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"projects"})
async def share_project(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    group_id: Annotated[
        str, Field(description="Group ID or path to share with")
    ] = None,
    group_access: Annotated[
        str,
        Field(
            description="Access level for the group (e.g., 'guest', 'developer', 'maintainer')"
        ),
    ] = None,
    expires_at: Annotated[
        Optional[str],
        Field(description="Expiration date for the share in ISO 8601 format"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Share a specific GitLab project with a group, specifying access level."""
    if not project_id or not group_id or not group_access:
        raise ValueError("project_id, group_id, and group_access are required")
    if ctx:
        await ctx.info(f"Sharing project {project_id} with group {group_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Project shared")
    return response.data


# Protected Branches Tools
@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"protected_branches"},
)
def get_protected_branches(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    branch: Annotated[
        str, Field(description="Name of the branch to retrieve (e.g., 'main')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, List]]], Dict[str, Union[str, List]]]:
    """Retrieve a list of protected branches in a specific GitLab project or Retrieve details of a specific protected branch in a GitLab project.."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    if branch:
        response = client.get_protected_branch(project_id=project_id, branch=branch)
    else:
        response = client.get_protected_branches(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"protected_branches"},
)
async def protect_branch(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    branch: Annotated[
        str, Field(description="Name of the branch to protect (e.g., 'main')")
    ] = None,
    push_access_level: Annotated[
        Optional[str],
        Field(description="Access level for pushing (e.g., 'maintainer')"),
    ] = None,
    merge_access_level: Annotated[
        Optional[str], Field(description="Access level for merging (e.g., 'developer')")
    ] = None,
    unprotect_access_level: Annotated[
        Optional[str],
        Field(description="Access level for unprotecting (e.g., 'maintainer')"),
    ] = None,
    allow_force_push: Annotated[
        Optional[bool], Field(description="Whether force pushes are allowed")
    ] = None,
    allowed_to_push: Annotated[
        Optional[List[Dict]],
        Field(description="List of users or groups allowed to push"),
    ] = None,
    allowed_to_merge: Annotated[
        Optional[List[Dict]],
        Field(description="List of users or groups allowed to merge"),
    ] = None,
    allowed_to_unprotect: Annotated[
        Optional[List[Dict]],
        Field(description="List of users or groups allowed to unprotect"),
    ] = None,
    code_owner_approval_required: Annotated[
        Optional[bool], Field(description="Whether code owner approval is required")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, List]]:
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
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Branch protected")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"protected_branches"},
)
async def unprotect_branch(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    branch: Annotated[
        str, Field(description="Name of the branch to unprotect (e.g., 'main')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Unprotect a specific branch in a GitLab project."""
    if not project_id or not branch:
        raise ValueError("project_id and branch are required")
    if ctx:
        await ctx.info(f"Unprotecting branch '{branch}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.unprotect_branch(project_id=project_id, branch=branch)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Branch unprotected")
    return response.data


@mcp.tool(
    exclude_args=["gitlab_instance", "access_token", "verify"],
    tags={"protected_branches"},
)
async def require_code_owner_approvals_single_branch(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    branch: Annotated[
        str,
        Field(
            description="Name of the branch to set approval requirements for (e.g., 'main')"
        ),
    ] = None,
    code_owner_approval_required: Annotated[
        bool, Field(description="Whether code owner approval is required")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, bool]]:
    """Require or disable code owner approvals for a specific branch in a GitLab project."""
    if not project_id or not branch or code_owner_approval_required is None:
        raise ValueError(
            "project_id, branch, and code_owner_approval_required are required"
        )
    if ctx:
        await ctx.info(
            f"Setting code owner approval requirement for branch '{branch}' in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.require_code_owner_approvals_single_branch(
        project_id=project_id,
        branch=branch,
        code_owner_approval_required=code_owner_approval_required,
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Code owner approval setting updated")
    return response.data


# Release Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
def get_releases(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    include_html_description: Annotated[
        Optional[bool], Field(description="Whether to include HTML descriptions")
    ] = None,
    sort: Annotated[
        Optional[str],
        Field(description="Sort releases by criteria (e.g., 'released_at')"),
    ] = None,
    order_by: Annotated[
        Optional[str],
        Field(description="Order releases by criteria (e.g., 'asc', 'desc')"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of releases for a specific GitLab project, optionally filtered."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_releases(project_id=project_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
def get_latest_release(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[str, int]]:
    """Retrieve details of the latest release in a GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_latest_release(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
def get_latest_release_evidence(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[str, int]]:
    """Retrieve evidence for the latest release in a GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_latest_release_evidence(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
def get_latest_release_asset(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    direct_asset_path: Annotated[
        str, Field(description="Path to the asset (e.g., 'assets/file.zip')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, str]:
    """Retrieve a specific asset for the latest release in a GitLab project."""
    if not project_id or not direct_asset_path:
        raise ValueError("project_id and direct_asset_path are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_latest_release_asset(
        project_id=project_id, direct_asset_path=direct_asset_path
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
def get_group_releases(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    include_html_description: Annotated[
        Optional[bool], Field(description="Whether to include HTML descriptions")
    ] = None,
    sort: Annotated[
        Optional[str],
        Field(description="Sort releases by criteria (e.g., 'released_at')"),
    ] = None,
    order_by: Annotated[
        Optional[str],
        Field(description="Order releases by criteria (e.g., 'asc', 'desc')"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of releases for a specific GitLab group, optionally filtered."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_releases(group_id=group_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
def download_release_asset(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    tag_name: Annotated[
        str, Field(description="Tag name of the release (e.g., 'v1.0.0')")
    ] = None,
    direct_asset_path: Annotated[
        str, Field(description="Path to the asset (e.g., 'assets/file.zip')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, str]:
    """Download a release asset from a group's release in GitLab."""
    if not group_id or not tag_name or not direct_asset_path:
        raise ValueError("group_id, tag_name, and direct_asset_path are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.download_release_asset(
        group_id=group_id, tag_name=tag_name, direct_asset_path=direct_asset_path
    )
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
def get_release_by_tag(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    tag_name: Annotated[
        str, Field(description="Tag name of the release (e.g., 'v1.0.0')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[str, int]]:
    """Retrieve details of a release by its tag in a GitLab project."""
    if not project_id or not tag_name:
        raise ValueError("project_id and tag_name are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_release_by_tag(project_id=project_id, tag_name=tag_name)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
async def create_release(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[str, Field(description="Name of the release")] = None,
    tag_name: Annotated[
        str, Field(description="Tag name associated with the release (e.g., 'v1.0.0')")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="Description of the release")
    ] = None,
    released_at: Annotated[
        Optional[str], Field(description="Release date in ISO 8601 format")
    ] = None,
    assets: Annotated[
        Optional[Dict], Field(description="Dictionary of release assets")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Create a new release in a GitLab project."""
    if not project_id or not name or not tag_name:
        raise ValueError("project_id, name, and tag_name are required")
    if ctx:
        await ctx.info(f"Creating release '{name}' for project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Release created")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
async def create_release_evidence(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    tag_name: Annotated[
        str, Field(description="Tag name of the release (e.g., 'v1.0.0')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Create evidence for a release in a GitLab project."""
    if not project_id or not tag_name:
        raise ValueError("project_id and tag_name are required")
    if ctx:
        await ctx.info(
            f"Creating release evidence for tag '{tag_name}' in project {project_id}"
        )
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.create_release_evidence(project_id=project_id, tag_name=tag_name)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Release evidence created")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
async def update_release(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    tag_name: Annotated[
        str, Field(description="Tag name of the release to update (e.g., 'v1.0.0')")
    ] = None,
    name: Annotated[Optional[str], Field(description="New name of the release")] = None,
    description: Annotated[
        Optional[str], Field(description="New description of the release")
    ] = None,
    released_at: Annotated[
        Optional[str], Field(description="New release date in ISO 8601 format")
    ] = None,
    assets: Annotated[
        Optional[Dict], Field(description="Updated dictionary of release assets")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Update a release in a GitLab project."""
    if not project_id or not tag_name:
        raise ValueError("project_id and tag_name are required")
    if not any([name, description, released_at, assets]):
        raise ValueError(
            "At least one of name, description, released_at, or assets must be provided"
        )
    if ctx:
        await ctx.info(f"Updating release for tag '{tag_name}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    response = client.update_release(project_id=project_id, tag_name=tag_name, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Release updated")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"releases"})
async def delete_release(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    tag_name: Annotated[
        str, Field(description="Tag name of the release to delete (e.g., 'v1.0.0')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a release in a GitLab project."""
    if not project_id or not tag_name:
        raise ValueError("project_id and tag_name are required")
    if ctx:
        await ctx.info(f"Deleting release for tag '{tag_name}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_release(project_id=project_id, tag_name=tag_name)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Release deleted")
    return response.data


# Runners Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
def get_runners(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    runner_id: Annotated[
        Optional[int], Field(description="ID of the runner to retrieve")
    ] = None,
    scope: Annotated[
        Optional[str], Field(description="Filter runners by scope (e.g., 'active')")
    ] = None,
    type: Annotated[
        Optional[str],
        Field(description="Filter runners by type (e.g., 'instance_type')"),
    ] = None,
    status: Annotated[
        Optional[str], Field(description="Filter runners by status (e.g., 'online')")
    ] = None,
    tag_list: Annotated[
        Optional[List[str]], Field(description="Filter runners by tags")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, int]]], Dict[str, Union[str, int]]]:
    """Retrieve a list of runners in GitLab, optionally filtered by scope, type, status, or tags or Retrieve details of a specific GitLab runner.."""
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def update_runner_details(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    runner_id: Annotated[int, Field(description="ID of the runner to update")] = None,
    description: Annotated[
        Optional[str], Field(description="New description of the runner")
    ] = None,
    active: Annotated[
        Optional[bool], Field(description="Whether the runner is active")
    ] = None,
    tag_list: Annotated[
        Optional[List[str]], Field(description="List of tags for the runner")
    ] = None,
    run_untagged: Annotated[
        Optional[bool], Field(description="Whether the runner can run untagged jobs")
    ] = None,
    locked: Annotated[
        Optional[bool], Field(description="Whether the runner is locked")
    ] = None,
    access_level: Annotated[
        Optional[str],
        Field(description="Access level of the runner (e.g., 'ref_protected')"),
    ] = None,
    maximum_timeout: Annotated[
        Optional[int], Field(description="Maximum timeout for the runner in seconds")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int, bool]]:
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
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Runner updated")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def pause_runner(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    runner_id: Annotated[
        int, Field(description="ID of the runner to pause or unpause")
    ] = None,
    active: Annotated[
        bool,
        Field(
            description="Whether the runner should be active (True) or paused (False)"
        ),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, bool]]:
    """Pause or unpause a specific GitLab runner."""
    if not runner_id or active is None:
        raise ValueError("runner_id and active are required")
    if ctx:
        await ctx.info(f"Setting runner {runner_id} active status to {active}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.pause_runner(runner_id=runner_id, active=active)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Runner status updated")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
def get_runner_jobs(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    runner_id: Annotated[
        int, Field(description="ID of the runner to retrieve jobs for")
    ] = None,
    status: Annotated[
        Optional[str],
        Field(description="Filter jobs by status (e.g., 'success', 'failed')"),
    ] = None,
    sort: Annotated[
        Optional[str], Field(description="Sort jobs by criteria (e.g., 'created_at')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve jobs for a specific GitLab runner, optionally filtered by status or sorted."""
    if not runner_id:
        raise ValueError("runner_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "runner_id"]
    }
    response = client.get_runner_jobs(runner_id=runner_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
def get_project_runners(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    scope: Annotated[
        Optional[str], Field(description="Filter runners by scope (e.g., 'active')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of runners in a specific GitLab project, optionally filtered by scope."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_project_runners(project_id=project_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def enable_project_runner(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    runner_id: Annotated[int, Field(description="ID of the runner to enable")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Enable a runner in a specific GitLab project."""
    if not project_id or not runner_id:
        raise ValueError("project_id and runner_id are required")
    if ctx:
        await ctx.info(f"Enabling runner {runner_id} for project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.enable_project_runner(project_id=project_id, runner_id=runner_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Runner enabled")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def delete_project_runner(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    runner_id: Annotated[int, Field(description="ID of the runner to delete")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a runner from a specific GitLab project."""
    if not project_id or not runner_id:
        raise ValueError("project_id and runner_id are required")
    if ctx:
        await ctx.info(f"Deleting runner {runner_id} from project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_project_runner(project_id=project_id, runner_id=runner_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Runner deleted")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
def get_group_runners(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    scope: Annotated[
        Optional[str], Field(description="Filter runners by scope (e.g., 'active')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, int]]]:
    """Retrieve a list of runners in a specific GitLab group, optionally filtered by scope."""
    if not group_id:
        raise ValueError("group_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_runners(group_id=group_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def register_new_runner(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    token: Annotated[
        str, Field(description="Registration token for the runner")
    ] = None,
    description: Annotated[
        Optional[str], Field(description="Description of the runner")
    ] = None,
    tag_list: Annotated[
        Optional[List[str]], Field(description="List of tags for the runner")
    ] = None,
    run_untagged: Annotated[
        Optional[bool], Field(description="Whether the runner can run untagged jobs")
    ] = None,
    locked: Annotated[
        Optional[bool], Field(description="Whether the runner is locked")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, int]]:
    """Register a new GitLab runner."""
    if not token:
        raise ValueError("token is required")
    if ctx:
        await ctx.info("Registering new runner with token")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.register_new_runner(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Runner registered")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def delete_runner(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    runner_id: Annotated[
        Optional[int], Field(description="ID of the runner to delete")
    ] = None,
    token: Annotated[
        Optional[str], Field(description="Token of the runner to delete")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a GitLab runner by ID or token."""
    if not runner_id and not token:
        raise ValueError("Either runner_id or token is required")
    if ctx:
        await ctx.info(f"Deleting runner with ID {runner_id or 'token'}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.delete_runner(**kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Runner deleted")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def verify_runner_authentication(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    token: Annotated[str, Field(description="Runner token to verify")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Verify authentication for a GitLab runner using its token."""
    if not token:
        raise ValueError("token is required")
    if ctx:
        await ctx.info("Verifying runner authentication")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.verify_runner_authentication(token=token)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Runner authentication verified")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def reset_gitlab_runner_token(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Reset the GitLab runner registration token."""
    if ctx:
        await ctx.info("Resetting GitLab runner registration token")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.reset_gitlab_runner_token()
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Runner token reset")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def reset_project_runner_token(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Reset the registration token for a project's runner in GitLab."""
    if not project_id:
        raise ValueError("project_id is required")
    if ctx:
        await ctx.info(f"Resetting runner token for project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.reset_project_runner_token(project_id=project_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Project runner token reset")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def reset_group_runner_token(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    group_id: Annotated[str, Field(description="Group ID or path")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Reset the registration token for a group's runner in GitLab."""
    if not group_id:
        raise ValueError("group_id is required")
    if ctx:
        await ctx.info(f"Resetting runner token for group {group_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.reset_group_runner_token(group_id=group_id)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Group runner token reset")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"runners"})
async def reset_token(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    runner_id: Annotated[
        int, Field(description="ID of the runner to reset the token for")
    ] = None,
    token: Annotated[str, Field(description="Current token of the runner")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Reset the authentication token for a specific GitLab runner."""
    if not runner_id or not token:
        raise ValueError("runner_id and token are required")
    if ctx:
        await ctx.info(f"Resetting authentication token for runner {runner_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.reset_token(runner_id=runner_id, token=token)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Runner authentication token reset")
    return response.data


# Tags Tools
@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
def get_tags(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[
        Optional[str], Field(description="Name of the tag to retrieve (e.g., 'v1.0.0')")
    ] = None,
    search: Annotated[
        Optional[str], Field(description="Filter tags by search term in name")
    ] = None,
    sort: Annotated[
        Optional[str],
        Field(description="Sort tags by criteria (e.g., 'name', 'updated')"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Union[List[Dict[str, Union[str, Dict]]], Dict[str, Union[str, Dict]]]:
    """Retrieve a list of tags for a specific GitLab project, optionally filtered or sorted or Retrieve details of a specific tag in a GitLab project."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    if name:
        response = client.get_tag(project_id=project_id, name=name)
    else:
        response = client.get_tags(project_id=project_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
async def create_tag(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[
        str, Field(description="Name of the tag to create (e.g., 'v1.0.0')")
    ] = None,
    ref: Annotated[
        str, Field(description="Reference (e.g., branch or commit SHA) to tag")
    ] = None,
    message: Annotated[Optional[str], Field(description="Tag message")] = None,
    release_description: Annotated[
        Optional[str], Field(description="Release description associated with the tag")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, Dict]]:
    """Create a new tag in a GitLab project."""
    if not project_id or not name or not ref:
        raise ValueError("project_id, name, and ref are required")
    if ctx:
        await ctx.info(f"Creating tag '{name}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Tag created")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
async def delete_tag(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[
        str, Field(description="Name of the tag to delete (e.g., 'v1.0.0')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Delete a specific tag in a GitLab project."""
    if not project_id or not name:
        raise ValueError("project_id and name are required")
    if ctx:
        await ctx.info(f"Deleting tag '{name}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.delete_tag(project_id=project_id, name=name)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Tag deleted")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
def get_protected_tags(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[Optional[str], Field(description="Filter tags by name")] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> List[Dict[str, Union[str, List]]]:
    """Retrieve a list of protected tags in a specific GitLab project, optionally filtered by name."""
    if not project_id:
        raise ValueError("project_id is required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_protected_tags(project_id=project_id, **kwargs)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
def get_protected_tag(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[
        str, Field(description="Name of the protected tag to retrieve (e.g., 'v1.0.0')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
) -> Dict[str, Union[str, List]]:
    """Retrieve details of a specific protected tag in a GitLab project."""
    if not project_id or not name:
        raise ValueError("project_id and name are required")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.get_protected_tag(project_id=project_id, name=name)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
async def protect_tag(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[
        str, Field(description="Name of the tag to protect (e.g., 'v1.0.0')")
    ] = None,
    create_access_level: Annotated[
        Optional[str],
        Field(description="Access level for creating the tag (e.g., 'maintainer')"),
    ] = None,
    allowed_to_create: Annotated[
        Optional[List[Dict]],
        Field(description="List of users or groups allowed to create the tag"),
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, Union[str, List]]:
    """Protect a specific tag in a GitLab project with specified access levels."""
    if not project_id or not name:
        raise ValueError("project_id and name are required")
    if not create_access_level and not allowed_to_create:
        raise ValueError(
            "At least one of create_access_level or allowed_to_create must be provided"
        )
    if ctx:
        await ctx.info(f"Protecting tag '{name}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
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
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Tag protected")
    return response.data


@mcp.tool(exclude_args=["gitlab_instance", "access_token", "verify"], tags={"tags"})
async def unprotect_tag(
    gitlab_instance: Annotated[
        str, Field(description="URL of GitLab instance with /api/v4/ suffix")
    ] = environment_gitlab_instance,
    access_token: Annotated[
        str, Field(description="GitLab access token")
    ] = environment_access_token,
    project_id: Annotated[str, Field(description="Project ID or path")] = None,
    name: Annotated[
        str, Field(description="Name of the tag to unprotect (e.g., 'v1.0.0')")
    ] = None,
    verify: Annotated[
        bool, Field(description="Verify SSL certificate")
    ] = environment_verify,
    ctx: Annotated[
        Optional[Context], Field(description="MCP context for progress")
    ] = None,
) -> Dict[str, str]:
    """Unprotect a specific tag in a GitLab project."""
    if not project_id or not name:
        raise ValueError("project_id and name are required")
    if ctx:
        await ctx.info(f"Unprotecting tag '{name}' in project {project_id}")
    client = Api(url=gitlab_instance, token=access_token, verify=verify)
    response = client.unprotect_tag(project_id=project_id, name=name)
    if "error" in response.data:
        raise RuntimeError(response.data["error"])
    if ctx:
        await ctx.info("Tag unprotected")
    return response.data


def gitlab_api_mcp(argv: List[str]) -> None:
    """Run the GitLab MCP server with specified transport and connection parameters.

    This function parses command-line arguments to configure and start the MCP server for GitLab API interactions.
    It supports stdio or TCP transport modes and exits on invalid arguments or help requests.

    Args:
        argv (List[str]): Command-line arguments passed to the script.

    Command-line Options:
        -h, --help: Display help and exit.
        -t, --transport: Specify transport mode ("stdio" or "tcp"). Defaults to "stdio".
        -h, --host: Specify host for TCP transport (e.g., "localhost"). Required for TCP mode.
        -p, --port: Specify port for TCP transport (e.g., "5000"). Required for TCP mode.

    Raises:
        SystemExit: If invalid arguments are provided or help is requested.

    Example:
        $ python gitlab_api_mcp.py --transport tcp --host localhost --port 5000
    """
    transport = "stdio"
    host = None
    port = None
    try:
        opts, args = getopt.getopt(
            argv,
            "ht:h:p:",
            ["help", "transport=", "host=", "port="],
        )
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            sys.exit()
        elif opt in ("-t", "--transport"):
            transport = arg
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            try:
                port = int(arg)  # Attempt to convert port to integer
                if not (0 <= port <= 65535):  # Valid port range
                    print(f"Error: Port {arg} is out of valid range (0-65535).")
                    sys.exit(1)
            except ValueError:
                print(f"Error: Port {arg} is not a valid integer.")
                sys.exit(1)
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host=host, port=port)


def main() -> None:
    """Entry point for the GitLab MCP script.

    This function serves as the main entry point for the script, passing command-line arguments to the gitlab_api_mcp function.

    Example:
        $ python gitlab_api_mcp.py --transport stdio
    """
    gitlab_api_mcp(sys.argv[1:])


if __name__ == "__main__":
    main()
