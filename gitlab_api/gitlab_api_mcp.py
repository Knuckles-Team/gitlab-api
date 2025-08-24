#!/usr/bin/python
# coding: utf-8

import getopt
import sys
from gitlab_api.gitlab_api import Api
from gitlab_api.gitlab_response_models import Response
from fastmcp import FastMCP, Context
from typing import Optional, List, Dict

mcp = FastMCP("GitLab")


# Branches Tools
@mcp.tool()
def get_branches(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    search: Optional[str] = None,
    regex: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of branches in a GitLab project, optionally filtered by search string or regex.

    This function queries the GitLab API to fetch branches for a specified project. It supports
    filtering branches by a search string (exact or partial match) or a regular expression pattern.
    The function returns a dictionary containing the list of branches or an error message if the
    request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str, optional): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
            If None, the default project configured in gitlab_api is used.
        search (Optional[str], optional): A string to filter branches by name (case-sensitive).
            Matches branches containing the search term. Defaults to None (no filtering).
        regex (Optional[str], optional): A regular expression pattern to filter branches by name.
            Applied after the search filter, if both are provided. Defaults to None (no regex filtering).
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of branch details (e.g., [{"name": "main", "commit": {   }},    ]).
            - If failed, contains an error message (e.g., {"error": "Invalid project ID"}).

    Raises:
        ValueError: If required parameters (e.g., project_id, when not configured in gitlab_api) are missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_branches(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                search="feature",
                regex="^feature/.*"
            )
        print(response)
        {"branches": [{"name": "feature/abc", "commit": {   }}, {"name": "feature/xyz", "commit": {   }}]}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_branches(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    branch: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve details about a specific branch in a GitLab project.

    This function queries the GitLab API to fetch details for a specified branch in a project.
    It returns a dictionary containing the branch details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The name of the branch to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains branch details (e.g., {"name": "main", "commit": {   }}).
            - If failed, contains an error message (e.g., {"error": "Branch not found"}).

    Raises:
        ValueError: If project_id or branch is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_branch(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                branch="main"
            )
        print(response)
        {"name": "main", "commit": {   }}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_branch(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def create_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    branch: str = None,
    ref: str = None,
    verify: bool = False,
) -> dict:
    """Create a new branch in a GitLab project from a reference (branch name, tag, or commit SHA).

    This function creates a new branch in the specified project using the provided reference.
    It returns a dictionary containing the branch details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The name of the branch to create.
        ref (str): The reference (branch name, tag, or commit SHA) to create the branch from.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains branch details (e.g., {"name": "new-branch", "commit": {   }}).
            - If failed, contains an error message (e.g., {"error": "Reference not found"}).

    Raises:
        ValueError: If project_id, branch, or ref is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = create_branch(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                branch="feature/new",
                ref="main"
            )
        print(response)
        {"name": "feature/new", "commit": {   }}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.create_branch(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    branch: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a specific branch in a GitLab project.

    This function deletes the specified branch from the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The name of the branch to delete.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Branch not found"}).

    Raises:
        ValueError: If project_id or branch is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_branch(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                branch="feature/old"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting branch '{branch}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.delete_branch(**kwargs)
    if ctx:
        await ctx.info("Deletion complete")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_merged_branches(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete all merged branches in a GitLab project (excluding protected branches).

    This function deletes all branches that have been merged into the project's default branch,
    excluding protected branches, and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletions (e.g., {"deleted": ["branch1", "branch2"]}).
            - If failed, contains an error message (e.g., {"error": "Failed to delete branches"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_merged_branches(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"deleted": ["feature/old", "bugfix/123"]}
    """
    if ctx:
        await ctx.info(f"Deleting merged branches in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]
    }
    response = client.delete_merged_branches(**kwargs)
    if ctx:
        await ctx.info("Deletion complete")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Commits Tools
@mcp.tool()
def get_commits(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    ref_name: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    path: Optional[str] = None,
    author: Optional[str] = None,
    all: Optional[bool] = None,
    with_stats: Optional[bool] = None,
    first_parent: Optional[bool] = None,
    order: Optional[str] = None,
    trailers: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of commits in a GitLab project, optionally filtered by ref, dates, path, author, etc.

    This function queries the GitLab API to fetch commits for a specified project with optional filters.
    It returns a dictionary containing the commit list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        ref_name (Optional[str], optional): The branch, tag, or commit SHA to filter commits. Defaults to None.
        since (Optional[str], optional): Only commits after this date (ISO 8601 format). Defaults to None.
        until (Optional[str], optional): Only commits before this date (ISO 8601 format). Defaults to None.
        path (Optional[str], optional): Only commits modifying this file path. Defaults to None.
        author (Optional[str], optional): Only commits by this author. Defaults to None.
        all (Optional[bool], optional): Include all commits across all branches. Defaults to None.
        with_stats (Optional[bool], optional): Include commit statistics. Defaults to None.
        first_parent (Optional[bool], optional): Follow only the first parent of merge commits. Defaults to None.
        order (Optional[str], optional): Order of commits (e.g., "default", "topo"). Defaults to None.
        trailers (Optional[bool], optional): Parse and include Git trailers. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of commit details (e.g., [{"id": "abc123", "message": "   "},    ]).
            - If failed, contains an error message (e.g., {"error": "Invalid project ID"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_commits(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                ref_name="main",
                since="2023-01-01T00:00:00Z"
            )
        print(response)
        [{"id": "abc123", "message": "Initial commit",    },    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_commits(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    stats: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve details about a specific commit in a GitLab project.

    This function queries the GitLab API to fetch details for a specified commit.
    It returns a dictionary containing the commit details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve.
        stats (Optional[bool], optional): Include commit statistics. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains commit details (e.g., {"id": "abc123", "message": "   "}).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_commit(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123",
                stats=True
            )
        print(response)
        {"id": "abc123", "message": "Fix bug", "stats": {   }}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "commit_hash",
        ]
    }
    response = client.get_commit(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_commit_references(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    type: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve references (branches/tags) where a commit is pushed in a GitLab project.

    This function queries the GitLab API to fetch references (branches or tags) containing the specified commit.
    The type parameter can filter to 'branch', 'tag', or 'all'.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to query.
        type (Optional[str], optional): Filter references by type ('branch', 'tag', or 'all'). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of references (e.g., [{"name": "main", "type": "branch"},    ]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_commit_references(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123",
                type="branch"
            )
        print(response)
        [{"name": "main", "type": "branch"}, {"name": "feature/abc", "type": "branch"}]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "commit_hash",
        ]
    }
    response = client.get_commit_references(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def cherry_pick_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    branch: str = None,
    dry_run: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Cherry-pick a commit into a target branch in a GitLab project.

    This function cherry-picks a specified commit into the target branch.
    Use dry_run to simulate the operation without applying changes.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to cherry-pick.
        branch (str): The target branch to apply the commit to.
        dry_run (Optional[bool], optional): If True, simulate the cherry-pick without applying. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the cherry-pick result (e.g., {"commit_id": "xyz789", "branch": "main"}).
            - If failed, contains an error message (e.g., {"error": "Cannot cherry-pick commit"}).

    Raises:
        ValueError: If project_id, commit_hash, or branch is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = cherry_pick_commit(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123",
                branch="main",
                dry_run=True
            )
        print(response)
        {"commit_id": "abc123", "branch": "main", "status": "simulated"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "commit_hash",
        ]
    }
    response = client.cherry_pick_commit(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def create_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    branch: str = None,
    commit_message: str = None,
    actions: list = None,
    start_branch: Optional[str] = None,
    start_sha: Optional[str] = None,
    start_project: Optional[str] = None,
    author_email: Optional[str] = None,
    author_name: Optional[str] = None,
    stats: Optional[bool] = None,
    force: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Create a new commit with multiple file actions (create/update/delete/move/chmod) in a GitLab project.

    This function creates a new commit with the specified actions on the given branch.
    It returns a dictionary containing the commit details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The branch to commit to.
        commit_message (str): The message for the commit.
        actions (list): A list of file actions (e.g., [{"action": "create", "file_path": "file.txt", "content": "   "}]).
        start_branch (Optional[str], optional): The starting branch for the commit. Defaults to None.
        start_sha (Optional[str], optional): The starting commit SHA. Defaults to None.
        start_project (Optional[str], optional): The starting project ID or path. Defaults to None.
        author_email (Optional[str], optional): The email of the commit author. Defaults to None.
        author_name (Optional[str], optional): The name of the commit author. Defaults to None.
        stats (Optional[bool], optional): Include commit statistics. Defaults to None.
        force (Optional[bool], optional): Force the commit, overwriting existing changes. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains commit details (e.g., {"id": "xyz789", "message": "   "}).
            - If failed, contains an error message (e.g., {"error": "Invalid actions"}).

    Raises:
        ValueError: If project_id, branch, commit_message, or actions is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = create_commit(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                branch="main",
                commit_message="Add new file",
                actions=[{"action": "create", "file_path": "file.txt", "content": "Hello"}]
            )
        print(response)
        {"id": "xyz789", "message": "Add new file"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.create_commit(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def revert_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    branch: str = None,
    dry_run: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Revert a commit in a target branch in a GitLab project.

    This function reverts a specified commit on the target branch.
    Use dry_run to simulate the operation without applying changes.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to revert.
        branch (str): The target branch to apply the revert to.
        dry_run (Optional[bool], optional): If True, simulate the revert without applying. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the revert result (e.g., {"commit_id": "xyz789", "branch": "main"}).
            - If failed, contains an error message (e.g., {"error": "Cannot revert commit"}).

    Raises:
        ValueError: If project_id, commit_hash, or branch is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = revert_commit(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123",
                branch="main",
                dry_run=True
            )
        print(response)
        {"commit_id": "abc123", "branch": "main", "status": "simulated"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "commit_hash",
        ]
    }
    response = client.revert_commit(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_commit_diff(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    unidiff: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve the diff for a specific commit in a GitLab project.

    This function queries the GitLab API to fetch the diff for a specified commit.
    Use unidiff for unified diff format.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve the diff for.
        unidiff (Optional[bool], optional): If True, return the diff in unified format. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the diff details (e.g., [{"diff": "   ", "new_path": "file.txt"},    ]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_commit_diff(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123",
                unidiff=True
            )
        print(response)
        [{"diff": "   ", "new_path": "file.txt"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "commit_hash",
        ]
    }
    response = client.get_commit_diff(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_commit_comments(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve comments on a specific commit in a GitLab project.

    This function queries the GitLab API to fetch comments on a specified commit.
    Note: This endpoint is deprecated in GitLab; consider using get_commit_discussions.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve comments for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of comments (e.g., [{"id": 1, "note": "Great change"},    ]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_commit_comments(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123"
            )
        print(response)
        [{"id": 1, "note": "Great change"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_commit_comments(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def create_commit_comment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    note: str = None,
    path: Optional[str] = None,
    line: Optional[int] = None,
    line_type: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Create a new comment on a specific commit in a GitLab project.

    This function creates a comment on a specified commit, optionally tied to a file path and line.
    It returns a dictionary containing the comment details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to comment on.
        note (str): The content of the comment.
        path (Optional[str], optional): The file path to associate with the comment. Defaults to None.
        line (Optional[int], optional): The line number in the file to associate with the comment. Defaults to None.
        line_type (Optional[str], optional): The type of line ('new' or 'old'). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains comment details (e.g., {"id": 1, "note": "Great change"}).
            - If failed, contains an error message (e.g., {"error": "Invalid commit"}).

    Raises:
        ValueError: If project_id, commit_hash, or note is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = create_commit_comment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123",
                note="Looks good!"
            )
        print(response)
        {"id": 1, "note": "Looks good!"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "commit_hash",
        ]
    }
    response = client.create_commit_comment(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_commit_discussions(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve discussions (threaded comments) on a specific commit in a GitLab project.

    This function queries the GitLab API to fetch threaded discussions for a specified commit.
    It returns a dictionary containing the discussion details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve discussions for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of discussions (e.g., [{"id": "disc1", "notes": [   ]},    ]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_commit_discussions(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123"
            )
        print(response)
        [{"id": "disc1", "notes": [{"note": "Great change"},    ]},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_commit_discussions(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_commit_statuses(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    ref: Optional[str] = None,
    stage: Optional[str] = None,
    name: Optional[str] = None,
    coverage: Optional[bool] = None,
    all: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve build/CI statuses for a specific commit in a GitLab project.

    This function queries the GitLab API to fetch CI statuses for a specified commit, optionally filtered.
    It returns a dictionary containing the status details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve statuses for.
        ref (Optional[str], optional): Filter statuses by reference (branch or tag). Defaults to None.
        stage (Optional[str], optional): Filter statuses by CI stage. Defaults to None.
        name (Optional[str], optional): Filter statuses by job name. Defaults to None.
        coverage (Optional[bool], optional): Include coverage information. Defaults to None.
        all (Optional[bool], optional): Include all statuses. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of statuses (e.g., [{"name": "test", "status": "success"},    ]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_commit_statuses(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123",
                name="test"
            )
        print(response)
        [{"name": "test", "status": "success"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "commit_hash",
        ]
    }
    response = client.get_commit_statuses(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def post_build_status_to_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    state: str = None,
    target_url: Optional[str] = None,
    context: Optional[str] = None,
    description: Optional[str] = None,
    coverage: Optional[float] = None,
    pipeline_id: Optional[int] = None,
    ref: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Post a build/CI status to a specific commit in a GitLab project.

    This function posts a CI status update for a specified commit.
    It returns a dictionary containing the status details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to post the status for.
        state (str): The state of the build (e.g., "pending", "running", "success", "failed").
        target_url (Optional[str], optional): URL to link to the build. Defaults to None.
        context (Optional[str], optional): Context of the status (e.g., "ci/build"). Defaults to None.
        description (Optional[str], optional): Description of the status. Defaults to None.
        coverage (Optional[float], optional): Coverage percentage. Defaults to None.
        pipeline_id (Optional[int], optional): ID of the associated pipeline. Defaults to None.
        ref (Optional[str], optional): Reference (branch or tag) for the status. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the status details (e.g., {"name": "ci/build", "status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Invalid state"}).

    Raises:
        ValueError: If project_id, commit_hash, or state is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = post_build_status_to_commit(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123",
                state="success",
                context="ci/build"
            )
        print(response)
        {"name": "ci/build", "status": "success"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "commit_hash",
        ]
    }
    response = client.post_build_status_to_commit(
        project_id=project_id, commit_hash=commit_hash, **kwargs
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_commit_merge_requests(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve merge requests associated with a specific commit in a GitLab project.

    This function queries the GitLab API to fetch merge requests that include the specified commit.
    It returns a dictionary containing the merge request details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to query.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of merge requests (e.g., [{"iid": 1, "title": "   "},    ]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_commit_merge_requests(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123"
            )
        print(response)
        [{"iid": 1, "title": "Add feature"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_commit_merge_requests(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_commit_gpg_signature(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    commit_hash: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve the GPG signature for a specific commit in a GitLab project.

    This function queries the GitLab API to fetch the GPG signature for a specified commit.
    It returns a dictionary containing the signature details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve the signature for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains signature details (e.g., {"signature": "   ", "verified": true}).
            - If failed, contains an error message (e.g., {"error": "No GPG signature"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_commit_gpg_signature(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                commit_hash="abc123"
            )
        print(response)
        {"signature": "   ", "verified": true}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_commit_gpg_signature(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Deploy Tokens Tools
@mcp.tool()
def get_deploy_tokens(
    gitlab_instance: str = None,
    access_token: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of all deploy tokens for the GitLab instance.

    This function queries the GitLab API to fetch all deploy tokens for the authenticated instance.
    It returns a dictionary containing the token list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of deploy tokens (e.g., [{"id": 1, "name": "token1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Authentication failed"}).

    Raises:
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_deploy_tokens(
                gitlab_instance="https://gitlab.com",
                access_token="your_token"
            )
        print(response)
        [{"id": 1, "name": "token1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_deploy_tokens()
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_deploy_tokens(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of deploy tokens for a specific GitLab project.

    This function queries the GitLab API to fetch deploy tokens for a specified project.
    It returns a dictionary containing the token list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of deploy tokens (e.g., [{"id": 1, "name": "token1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_deploy_tokens(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        [{"id": 1, "name": "token1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_project_deploy_tokens(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    token_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific deploy token for a GitLab project.

    This function queries the GitLab API to fetch details for a specified deploy token in a project.
    It returns a dictionary containing the token details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        token_id (int): The ID of the deploy token to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains token details (e.g., {"id": 1, "name": "token1"}).
            - If failed, contains an error message (e.g., {"error": "Token not found"}).

    Raises:
        ValueError: If project_id or token_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_deploy_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                token_id=1
            )
        print(response)
        {"id": 1, "name": "token1"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_project_deploy_token(project_id=project_id, token=token_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def create_project_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    scopes: List[str] = None,
    expires_at: Optional[str] = None,
    username: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a deploy token for a GitLab project with specified name and scopes.

    This function creates a new deploy token for the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the token details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the deploy token.
        scopes (List[str]): The scopes for the deploy token (e.g., ["read_repository", "read_registry"]).
        expires_at (Optional[str], optional): The expiration date of the token (ISO 8601 format). Defaults to None.
        username (Optional[str], optional): The username associated with the token. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains token details (e.g., {"id": 1, "name": "token1", "token": "   "}).
            - If failed, contains an error message (e.g., {"error": "Invalid scopes"}).

    Raises:
        ValueError: If project_id, name, or scopes is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_project_deploy_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="deploy-token",
                scopes=["read_repository"]
            )
        print(response)
        {"id": 1, "name": "deploy-token", "token": "   "}
    """
    if ctx:
        await ctx.info(f"Creating deploy token '{name}' for project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.create_project_deploy_token(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Deploy token created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_project_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    token_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a specific deploy token for a GitLab project.

    This function deletes a specified deploy token from a project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        token_id (int): The ID of the deploy token to delete.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Token not found"}).

    Raises:
        ValueError: If project_id or token_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_project_deploy_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                token_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting deploy token {token_id} for project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.delete_project_deploy_token(project_id=project_id, token=token_id)
    if ctx:
        await ctx.info("Deploy token deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_group_deploy_tokens(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of deploy tokens for a specific GitLab group.

    This function queries the GitLab API to fetch deploy tokens for a specified group.
    It returns a dictionary containing the token list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of deploy tokens (e.g., [{"id": 1, "name": "token1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_deploy_tokens(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234"
            )
        print(response)
        [{"id": 1, "name": "token1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_group_deploy_tokens(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_group_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    token_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific deploy token for a GitLab group.

    This function queries the GitLab API to fetch details for a specified deploy token in a group.
    It returns a dictionary containing the token details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        token_id (int): The ID of the deploy token to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains token details (e.g., {"id": 1, "name": "token1"}).
            - If failed, contains an error message (e.g., {"error": "Token not found"}).

    Raises:
        ValueError: If group_id or token_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_deploy_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                token_id=1
            )
        print(response)
        {"id": 1, "name": "token1"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_group_deploy_token(group_id=group_id, token=token_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Deploy Tokens Tools
@mcp.tool()
async def create_group_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    name: str = None,
    scopes: List[str] = None,
    expires_at: Optional[str] = None,
    username: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a deploy token for a GitLab group with specified name and scopes.

    This function creates a new deploy token for the specified group and provides progress updates via ctx if available.
    It returns a dictionary containing the token details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        name (str): The name of the deploy token.
        scopes (List[str]): The scopes for the deploy token (e.g., ["read_repository", "read_registry"]).
        expires_at (Optional[str], optional): The expiration date of the token (ISO 8601 format). Defaults to None.
        username (Optional[str], optional): The username associated with the token. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains token details (e.g., {"id": 1, "name": "token1", "token": "   "}).
            - If failed, contains an error message (e.g., {"error": "Invalid scopes"}).

    Raises:
        ValueError: If group_id, name, or scopes is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_group_deploy_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                name="group-token",
                scopes=["read_repository"]
            )
        print(response)
        {"id": 1, "name": "group-token", "token": "   "}
    """
    if ctx:
        await ctx.info(f"Creating deploy token '{name}' for group {group_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "group_id",
            "ctx",
        ]
    }
    response = client.create_group_deploy_token(group_id=group_id, **kwargs)
    if ctx:
        await ctx.info("Deploy token created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_group_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    token_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a specific deploy token for a GitLab group.

    This function deletes a specified deploy token from a group and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        token_id (int): The ID of the deploy token to delete.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Token not found"}).

    Raises:
        ValueError: If group_id or token_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_group_deploy_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                token_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting deploy token {token_id} for group {group_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_group_deploy_token(group_id=group_id, token=token_id)
    if ctx:
        await ctx.info("Deploy token deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Environments Tools
@mcp.tool()
def get_environments(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: Optional[str] = None,
    search: Optional[str] = None,
    states: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of environments for a GitLab project, optionally filtered by name, search, or states.

    This function queries the GitLab API to fetch environments for a specified project.
    It returns a dictionary containing the environment list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (Optional[str], optional): Filter environments by exact name. Defaults to None.
        search (Optional[str], optional): Filter environments by search term in name. Defaults to None.
        states (Optional[str], optional): Filter environments by state (e.g., "available", "stopped"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of environment details (e.g., [{"id": 1, "name": "prod"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_environments(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="prod"
            )
        print(response)
        [{"id": 1, "name": "prod", "state": "available"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_environments(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_environment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    environment_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific environment in a GitLab project.

    This function queries the GitLab API to fetch details for a specified environment.
    It returns a dictionary containing the environment details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        environment_id (int): The ID of the environment to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains environment details (e.g., {"id": 1, "name": "prod"}).
            - If failed, contains an error message (e.g., {"error": "Environment not found"}).

    Raises:
        ValueError: If project_id or environment_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_environment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                environment_id=1
            )
        print(response)
        {"id": 1, "name": "prod", "state": "available"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_environment(
        project_id=project_id, environment_id=environment_id
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def create_environment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    external_url: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a new environment in a GitLab project with a specified name and optional external URL.

    This function creates a new environment in the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the environment details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the environment to create.
        external_url (Optional[str], optional): The external URL associated with the environment. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains environment details (e.g., {"id": 1, "name": "prod"}).
            - If failed, contains an error message (e.g., {"error": "Invalid environment name"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_environment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="prod",
                external_url="https://prod.example.com"
            )
        print(response)
        {"id": 1, "name": "prod", "external_url": "https://prod.example.com"}
    """
    if ctx:
        await ctx.info(f"Creating environment '{name}' for project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.create_environment(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Environment created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def update_environment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    environment_id: int = None,
    name: Optional[str] = None,
    external_url: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Update an existing environment in a GitLab project with new name or external URL.

    This function updates the specified environment in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the updated environment details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        environment_id (int): The ID of the environment to update.
        name (Optional[str], optional): The new name for the environment. Defaults to None.
        external_url (Optional[str], optional): The new external URL for the environment. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated environment details (e.g., {"id": 1, "name": "prod"}).
            - If failed, contains an error message (e.g., {"error": "Environment not found"}).

    Raises:
        ValueError: If project_id or environment_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await update_environment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                environment_id=1,
                name="production"
            )
        print(response)
        {"id": 1, "name": "production"}
    """
    if ctx:
        await ctx.info(f"Updating environment {environment_id} in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "environment_id",
            "ctx",
        ]
    }
    response = client.update_environment(
        project_id=project_id, environment_id=environment_id, **kwargs
    )
    if ctx:
        await ctx.info("Environment updated")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_environment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    environment_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a specific environment in a GitLab project.

    This function deletes the specified environment from the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        environment_id (int): The ID of the environment to delete.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Environment not found"}).

    Raises:
        ValueError: If project_id or environment_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_environment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                environment_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting environment {environment_id} in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_environment(
        project_id=project_id, environment_id=environment_id
    )
    if ctx:
        await ctx.info("Environment deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def stop_environment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    environment_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Stop a specific environment in a GitLab project.

    This function stops the specified environment in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        environment_id (int): The ID of the environment to stop.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of stopping (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Environment not found"}).

    Raises:
        ValueError: If project_id or environment_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await stop_environment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                environment_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Stopping environment {environment_id} in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.stop_environment(
        project_id=project_id, environment_id=environment_id
    )
    if ctx:
        await ctx.info("Environment stopped")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def stop_stale_environments(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    older_than: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Stop stale environments in a GitLab project, optionally filtered by older_than timestamp.

    This function stops stale environments in the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        older_than (Optional[str], optional): Filter environments older than this timestamp (ISO 8601 format). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of stopped environments (e.g., {"stopped": ["env1", "env2"]}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await stop_stale_environments(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                older_than="2023-01-01T00:00:00Z"
            )
        print(response)
        {"stopped": ["env1", "env2"]}
    """
    if ctx:
        await ctx.info(f"Stopping stale environments in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.stop_stale_environments(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Stale environments stopped")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_stopped_environments(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete stopped review app environments in a GitLab project.

    This function deletes all stopped review app environments in the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deleted environments (e.g., {"deleted": ["env1", "env2"]}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_stopped_environments(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"deleted": ["env1", "env2"]}
    """
    if ctx:
        await ctx.info(f"Deleting stopped review apps in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_stopped_environments(project_id=project_id)
    if ctx:
        await ctx.info("Stopped review apps deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_protected_environments(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of protected environments in a GitLab project.

    This function queries the GitLab API to fetch protected environments for a specified project.
    It returns a dictionary containing the list of protected environments or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of protected environment details (e.g., [{"name": "prod", "id": 1},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_protected_environments(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        [{"name": "prod", "id": 1},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_protected_environments(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_protected_environment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific protected environment in a GitLab project.

    This function queries the GitLab API to fetch details for a specified protected environment.
    It returns a dictionary containing the protected environment details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the protected environment to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains protected environment details (e.g., {"name": "prod", "id": 1}).
            - If failed, contains an error message (e.g., {"error": "Environment not found"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_protected_environment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="prod"
            )
        print(response)
        {"name": "prod", "id": 1}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_protected_environment(project_id=project_id, name=name)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def protect_environment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    required_approval_count: Optional[int] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Protect an environment in a GitLab project with optional approval count.

    This function protects the specified environment in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the protected environment details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the environment to protect.
        required_approval_count (Optional[int], optional): The number of approvals required for deployment. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains protected environment details (e.g., {"name": "prod", "id": 1}).
            - If failed, contains an error message (e.g., {"error": "Environment not found"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await protect_environment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="prod",
                required_approval_count=2
            )
        print(response)
        {"name": "prod", "id": 1, "required_approval_count": 2}
    """
    if ctx:
        await ctx.info(f"Protecting environment '{name}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.protect_environment(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Environment protected")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def update_protected_environment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    required_approval_count: Optional[int] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Update a protected environment in a GitLab project with new approval count.

    This function updates the specified protected environment in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the updated protected environment details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the protected environment to update.
        required_approval_count (Optional[int], optional): The new number of approvals required for deployment. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated protected environment details (e.g., {"name": "prod", "id": 1}).
            - If failed, contains an error message (e.g., {"error": "Environment not found"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await update_protected_environment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="prod",
                required_approval_count=3
            )
        print(response)
        {"name": "prod", "id": 1, "required_approval_count": 3}
    """
    if ctx:
        await ctx.info(
            f"Updating protected environment '{name}' in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.update_protected_environment(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Protected environment updated")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def unprotect_environment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Unprotect a specific environment in a GitLab project.

    This function unprotects the specified environment in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the environment to unprotect.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of unprotection (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Environment not found"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await unprotect_environment(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="prod"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Unprotecting environment '{name}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.unprotect_environment(project_id=project_id, name=name)
    if ctx:
        await ctx.info("Environment unprotected")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Groups Tools
@mcp.tool()
def get_groups(
    gitlab_instance: str = None,
    access_token: str = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order_by: Optional[str] = None,
    owned: Optional[bool] = None,
    min_access_level: Optional[int] = None,
    top_level_only: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of groups, optionally filtered by search, sort, ownership, or access level.

    This function queries the GitLab API to fetch groups available to the authenticated user.
    It returns a dictionary containing the group list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        search (Optional[str], optional): Filter groups by search term in name or path. Defaults to None.
        sort (Optional[str], optional): Sort order (e.g., "asc", "desc"). Defaults to None.
        order_by (Optional[str], optional): Field to sort by (e.g., "name", "path"). Defaults to None.
        owned (Optional[bool], optional): Filter groups owned by the authenticated user. Defaults to None.
        min_access_level (Optional[int], optional): Filter groups by minimum access level (e.g., 10 for Guest). Defaults to None.
        top_level_only (Optional[bool], optional): Include only top-level groups (exclude subgroups). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of group details (e.g., [{"id": 1, "name": "group1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Authentication failed"}).

    Raises:
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_groups(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                search="mygroup",
                owned=True
            )
        print(response)
        [{"id": 1, "name": "mygroup"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_groups(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_group(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    with_projects: Optional[bool] = None,
    with_custom_attributes: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific GitLab group.

    This function queries the GitLab API to fetch details for a specified group.
    It returns a dictionary containing the group details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        with_projects (Optional[bool], optional): Include projects in the group response. Defaults to None.
        with_custom_attributes (Optional[bool], optional): Include custom attributes in the response. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains group details (e.g., {"id": 1, "name": "group1"}).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                with_projects=True
            )
        print(response)
        {"id": 1, "name": "group1", "projects": [   ]}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group(group_id=group_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def edit_group(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    name: Optional[str] = None,
    path: Optional[str] = None,
    description: Optional[str] = None,
    visibility: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Edit a specific GitLab group's details (name, path, description, or visibility).

    This function updates the specified group and provides progress updates via ctx if available.
    It returns a dictionary containing the updated group details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        name (Optional[str], optional): The new name for the group. Defaults to None.
        path (Optional[str], optional): The new path for the group. Defaults to None.
        description (Optional[str], optional): The new description for the group. Defaults to None.
        visibility (Optional[str], optional): The new visibility level (e.g., "public", "private"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated group details (e.g., {"id": 1, "name": "newname"}).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await edit_group(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                name="newname",
                visibility="public"
            )
        print(response)
        {"id": 1, "name": "newname", "visibility": "public"}
    """
    if ctx:
        await ctx.info(f"Editing group {group_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "group_id",
            "ctx",
        ]
    }
    response = client.edit_group(group_id=group_id, **kwargs)
    if ctx:
        await ctx.info("Group edited")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_group_subgroups(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order_by: Optional[str] = None,
    owned: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of subgroups for a specific GitLab group, optionally filtered.

    This function queries the GitLab API to fetch subgroups of a specified group.
    It returns a dictionary containing the subgroup list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        search (Optional[str], optional): Filter subgroups by search term in name or path. Defaults to None.
        sort (Optional[str], optional): Sort order (e.g., "asc", "desc"). Defaults to None.
        order_by (Optional[str], optional): Field to sort by (e.g., "name", "path"). Defaults to None.
        owned (Optional[bool], optional): Filter subgroups owned by the authenticated user. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of subgroup details (e.g., [{"id": 2, "name": "subgroup1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_subgroups(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                search="subgroup"
            )
        print(response)
        [{"id": 2, "name": "subgroup1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_subgroups(group_id=group_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_group_descendant_groups(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order_by: Optional[str] = None,
    owned: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of all descendant groups for a specific GitLab group, optionally filtered.

    This function queries the GitLab API to fetch all descendant groups (including nested subgroups) of a specified group.
    It returns a dictionary containing the descendant group list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        search (Optional[str], optional): Filter descendant groups by search term in name or path. Defaults to None.
        sort (Optional[str], optional): Sort order (e.g., "asc", "desc"). Defaults to None.
        order_by (Optional[str], optional): Field to sort by (e.g., "name", "path"). Defaults to None.
        owned (Optional[bool], optional): Filter descendant groups owned by the authenticated user. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of descendant group details (e.g., [{"id": 2, "name": "subgroup1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_descendant_groups(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                search="subgroup"
            )
        print(response)
        [{"id": 2, "name": "subgroup1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_descendant_groups(group_id=group_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_group_projects(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    include_subgroups: Optional[bool] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order_by: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of projects associated with a specific GitLab group, optionally including subgroups.

    This function queries the GitLab API to fetch projects associated with a specified group.
    It returns a dictionary containing the project list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        include_subgroups (Optional[bool], optional): Include projects from subgroups. Defaults to None.
        search (Optional[str], optional): Filter projects by search term in name or path. Defaults to None.
        sort (Optional[str], optional): Sort order (e.g., "asc", "desc"). Defaults to None.
        order_by (Optional[str], optional): Field to sort by (e.g., "name", "path"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of project details (e.g., [{"id": 1, "name": "project1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_projects(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                include_subgroups=True
            )
        print(response)
        [{"id": 1, "name": "project1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_projects(group_id=group_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_group_merge_requests(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    state: Optional[str] = None,
    scope: Optional[str] = None,
    milestone: Optional[str] = None,
    search: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of merge requests associated with a specific GitLab group, optionally filtered.

    This function queries the GitLab API to fetch merge requests for a specified group.
    It returns a dictionary containing the merge request list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        state (Optional[str], optional): Filter merge requests by state (e.g., "opened", "closed"). Defaults to None.
        scope (Optional[str], optional): Filter merge requests by scope (e.g., "created_by_me"). Defaults to None.
        milestone (Optional[str], optional): Filter merge requests by milestone title. Defaults to None.
        search (Optional[str], optional): Filter merge requests by search term in title or description. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of merge request details (e.g., [{"iid": 1, "title": "Merge"},    ]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_merge_requests(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                state="opened"
            )
        print(response)
        [{"iid": 1, "title": "Merge"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_merge_requests(group_id=group_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Jobs Tools
@mcp.tool()
def get_project_jobs(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    scope: Optional[str] = None,
    include_retried: Optional[bool] = None,
    include_invisible: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of jobs for a specific GitLab project, optionally filtered by scope (e.g., 'success', 'failed').

    This function queries the GitLab API to fetch jobs for a specified project.
    It returns a dictionary containing the job list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        scope (Optional[str], optional): Filter jobs by scope (e.g., "success", "failed"). Defaults to None.
        include_retried (Optional[bool], optional): Include retried jobs in the response. Defaults to None.
        include_invisible (Optional[bool], optional): Include invisible jobs (e.g., from hidden pipelines). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of job details (e.g., [{"id": 1, "name": "test", "status": "success"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_jobs(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                scope="success"
            )
        print(response)
        [{"id": 1, "name": "test", "status": "success"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_project_jobs(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_job(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    job_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific job in a GitLab project.

    This function queries the GitLab API to fetch details for a specified job.
    It returns a dictionary containing the job details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        job_id (int): The ID of the job to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains job details (e.g., {"id": 1, "name": "test", "status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Job not found"}).

    Raises:
        ValueError: If project_id or job_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_job(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                job_id=1
            )
        print(response)
        {"id": 1, "name": "test", "status": "success"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_project_job(project_id=project_id, job_id=job_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_job_log(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    job_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve the log (trace) of a specific job in a GitLab project.

    This function queries the GitLab API to fetch the log for a specified job.
    It returns a dictionary containing the job log or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        job_id (int): The ID of the job to retrieve the log for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the job log (e.g., {"log": "   "}).
            - If failed, contains an error message (e.g., {"error": "Job not found"}).

    Raises:
        ValueError: If project_id or job_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_job_log(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                job_id=1
            )
        print(response)
        {"log": "   "}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_project_job_log(project_id=project_id, job_id=job_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def cancel_project_job(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    job_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Cancel a specific job in a GitLab project.

    This function cancels the specified job in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        job_id (int): The ID of the job to cancel.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of cancellation (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Job not found"}).

    Raises:
        ValueError: If project_id or job_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await cancel_project_job(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                job_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Cancelling job {job_id} in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.cancel_project_job(project_id=project_id, job_id=job_id)
    if ctx:
        await ctx.info("Job cancelled")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def retry_project_job(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    job_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Retry a specific job in a GitLab project.

    This function retries the specified job in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        job_id (int): The ID of the job to retry.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains job details (e.g., {"id": 1, "name": "test", "status": "pending"}).
            - If failed, contains an error message (e.g., {"error": "Job not found"}).

    Raises:
        ValueError: If project_id or job_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await retry_project_job(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                job_id=1
            )
        print(response)
        {"id": 1, "name": "test", "status": "pending"}
    """
    if ctx:
        await ctx.info(f"Retrying job {job_id} in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.retry_project_job(project_id=project_id, job_id=job_id)
    if ctx:
        await ctx.info("Job retried")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Jobs Tools
@mcp.tool()
async def erase_project_job(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    job_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Erase (delete artifacts and logs of) a specific job in a GitLab project.

    This function erases the specified job's artifacts and logs in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        job_id (int): The ID of the job to erase.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of erasure (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Job not found"}).

    Raises:
        ValueError: If project_id or job_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await erase_project_job(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                job_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Erasing job {job_id} in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.erase_project_job(project_id=project_id, job_id=job_id)
    if ctx:
        await ctx.info("Job erased")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def run_project_job(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    job_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Run (play) a specific manual job in a GitLab project.

    This function triggers a manual job in the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the job details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        job_id (int): The ID of the job to run.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains job details (e.g., {"id": 1, "name": "test", "status": "running"}).
            - If failed, contains an error message (e.g., {"error": "Job not found"}).

    Raises:
        ValueError: If project_id or job_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await run_project_job(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                job_id=1
            )
        print(response)
        {"id": 1, "name": "test", "status": "running"}
    """
    if ctx:
        await ctx.info(f"Running job {job_id} in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.run_project_job(project_id=project_id, job_id=job_id)
    if ctx:
        await ctx.info("Job started")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_pipeline_jobs(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_id: int = None,
    scope: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of jobs for a specific pipeline in a GitLab project, optionally filtered by scope.

    This function queries the GitLab API to fetch jobs for a specified pipeline in a project.
    It returns a dictionary containing the job list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_id (int): The ID of the pipeline to retrieve jobs for.
        scope (Optional[str], optional): Filter jobs by scope (e.g., "success", "failed"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of job details (e.g., [{"id": 1, "name": "test", "status": "success"},    ]).
            - If failed, contains an error message (e.g., {"error": "Pipeline not found"}).

    Raises:
        ValueError: If project_id or pipeline_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_pipeline_jobs(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_id=1,
                scope="success"
            )
        print(response)
        [{"id": 1, "name": "test", "status": "success"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Members Tools
@mcp.tool()
def get_group_members(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    query: Optional[str] = None,
    user_ids: Optional[List[int]] = None,
    skip_users: Optional[List[int]] = None,
    show_seat_info: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of members in a specific GitLab group, optionally filtered by query or user IDs.

    This function queries the GitLab API to fetch members of a specified group.
    It returns a dictionary containing the member list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        query (Optional[str], optional): Filter members by search term in name or username. Defaults to None.
        user_ids (Optional[List[int]], optional): Filter members by user IDs. Defaults to None.
        skip_users (Optional[List[int]], optional): Exclude specified user IDs from the response. Defaults to None.
        show_seat_info (Optional[bool], optional): Include seat information for members. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of member details (e.g., [{"id": 1, "username": "user1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_members(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                query="user1"
            )
        print(response)
        [{"id": 1, "username": "user1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_members(group_id=group_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_members(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    query: Optional[str] = None,
    user_ids: Optional[List[int]] = None,
    skip_users: Optional[List[int]] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of members in a specific GitLab project, optionally filtered by query or user IDs.

    This function queries the GitLab API to fetch members of a specified project.
    It returns a dictionary containing the member list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        query (Optional[str], optional): Filter members by search term in name or username. Defaults to None.
        user_ids (Optional[List[int]], optional): Filter members by user IDs. Defaults to None.
        skip_users (Optional[List[int]], optional): Exclude specified user IDs from the response. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of member details (e.g., [{"id": 1, "username": "user1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_members(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                query="user1"
            )
        print(response)
        [{"id": 1, "username": "user1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_project_members(project_id=project_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Merge Request Tools
@mcp.tool()
async def create_merge_request(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    source_branch: str = None,
    target_branch: str = None,
    title: str = None,
    description: Optional[str] = None,
    assignee_id: Optional[int] = None,
    reviewer_ids: Optional[List[int]] = None,
    labels: Optional[List[str]] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a new merge request in a GitLab project with specified source and target branches.

    This function creates a new merge request in the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the merge request details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        source_branch (str): The source branch for the merge request.
        target_branch (str): The target branch for the merge request.
        title (str): The title of the merge request.
        description (Optional[str], optional): The description of the merge request. Defaults to None.
        assignee_id (Optional[int], optional): The ID of the user to assign the merge request to. Defaults to None.
        reviewer_ids (Optional[List[int]], optional): The IDs of users to set as reviewers. Defaults to None.
        labels (Optional[List[str]], optional): Labels to apply to the merge request. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains merge request details (e.g., {"iid": 1, "title": "Merge"}).
            - If failed, contains an error message (e.g., {"error": "Invalid source branch"}).

    Raises:
        ValueError: If project_id, source_branch, target_branch, or title is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_merge_request(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                source_branch="feature",
                target_branch="main",
                title="New feature merge"
            )
        print(response)
        {"iid": 1, "title": "New feature merge"}
    """
    if ctx:
        await ctx.info(f"Creating merge request '{title}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.create_merge_request(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Merge request created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_merge_requests(
    gitlab_instance: str = None,
    access_token: str = None,
    state: Optional[str] = None,
    scope: Optional[str] = None,
    milestone: Optional[str] = None,
    view: Optional[str] = None,
    labels: Optional[List[str]] = None,
    author_id: Optional[int] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of merge requests across all projects, optionally filtered by state, scope, or labels.

    This function queries the GitLab API to fetch merge requests across all accessible projects.
    It returns a dictionary containing the merge request list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        state (Optional[str], optional): Filter merge requests by state (e.g., "opened", "closed"). Defaults to None.
        scope (Optional[str], optional): Filter merge requests by scope (e.g., "created_by_me"). Defaults to None.
        milestone (Optional[str], optional): Filter merge requests by milestone title. Defaults to None.
        view (Optional[str], optional): Filter merge requests by view (e.g., "simple"). Defaults to None.
        labels (Optional[List[str]], optional): Filter merge requests by labels. Defaults to None.
        author_id (Optional[int], optional): Filter merge requests by author ID. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of merge request details (e.g., [{"iid": 1, "title": "Merge"},    ]).
            - If failed, contains an error message (e.g., {"error": "Authentication failed"}).

    Raises:
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_merge_requests(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                state="opened",
                author_id=1
            )
        print(response)
        [{"iid": 1, "title": "Merge"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_merge_requests(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_merge_requests(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    state: Optional[str] = None,
    scope: Optional[str] = None,
    milestone: Optional[str] = None,
    labels: Optional[List[str]] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of merge requests for a specific GitLab project, optionally filtered.

    This function queries the GitLab API to fetch merge requests for a specified project.
    It returns a dictionary containing the merge request list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        state (Optional[str], optional): Filter merge requests by state (e.g., "opened", "closed"). Defaults to None.
        scope (Optional[str], optional): Filter merge requests by scope (e.g., "created_by_me"). Defaults to None.
        milestone (Optional[str], optional): Filter merge requests by milestone title. Defaults to None.
        labels (Optional[List[str]], optional): Filter merge requests by labels. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of merge request details (e.g., [{"iid": 1, "title": "Merge"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_merge_requests(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                state="opened"
            )
        print(response)
        [{"iid": 1, "title": "Merge"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_project_merge_requests(project_id=project_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_merge_request(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    merge_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific merge request in a GitLab project.

    This function queries the GitLab API to fetch details for a specified merge request.
    It returns a dictionary containing the merge request details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        merge_id (int): The ID of the merge request to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains merge request details (e.g., {"iid": 1, "title": "Merge"}).
            - If failed, contains an error message (e.g., {"error": "Merge request not found"}).

    Raises:
        ValueError: If project_id or merge_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_merge_request(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                merge_id=1
            )
        print(response)
        {"iid": 1, "title": "Merge"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_project_merge_request(
        project_id=project_id, merge_id=merge_id
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Merge Rules Tools
@mcp.tool()
def get_project_level_merge_request_approval_rules(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve project-level merge request approval rules for a GitLab project.

    This function queries the GitLab API to fetch approval rules for a specified project.
    It returns a dictionary containing the approval rules list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of approval rule details (e.g., [{"id": 1, "name": "rule1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_level_merge_request_approval_rules(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        [{"id": 1, "name": "rule1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_project_level_rules(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_level_merge_request_approval_rule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    approval_rule_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific project-level merge request approval rule.

    This function queries the GitLab API to fetch details for a specified approval rule in a project.
    It returns a dictionary containing the approval rule details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        approval_rule_id (int): The ID of the approval rule to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains approval rule details (e.g., {"id": 1, "name": "rule1"}).
            - If failed, contains an error message (e.g., {"error": "Approval rule not found"}).

    Raises:
        ValueError: If project_id or approval_rule_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_level_merge_request_approval_rule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                approval_rule_id=1
            )
        print(response)
        {"id": 1, "name": "rule1"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_project_level_rule(
        project_id=project_id, approval_rule_id=approval_rule_id
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def create_project_level_rule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    approvals_required: Optional[int] = None,
    rule_type: Optional[str] = None,
    user_ids: Optional[List[int]] = None,
    group_ids: Optional[List[int]] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a new project-level merge request approval rule.

    This function creates a new approval rule for merge requests in the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the approval rule details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the approval rule.
        approvals_required (int): The number of approvals required for the rule.
        rule_type (Optional[str], optional): The type of rule (e.g., "regular"). Defaults to None.
        user_ids (Optional[List[int]], optional): List of user IDs required to approve. Defaults to None.
        group_ids (Optional[List[int]], optional): List of group IDs required to approve. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains approval rule details (e.g., {"id": 1, "name": "rule1"}).
            - If failed, contains an error message (e.g., {"error": "Invalid rule name"}).

    Raises:
        ValueError: If project_id, name, or approvals_required is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_project_level_rule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="rule1",
                approvals_required=2
            )
        print(response)
        {"id": 1, "name": "rule1", "approvals_required": 2}
    """
    if ctx:
        await ctx.info(f"Creating approval rule '{name}' for project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.create_project_level_rule(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Approval rule created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def update_project_level_rule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    approval_rule_id: int = None,
    name: Optional[str] = None,
    approvals_required: Optional[int] = None,
    user_ids: Optional[List[int]] = None,
    group_ids: Optional[List[int]] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Update an existing project-level merge request approval rule.

    This function updates the specified approval rule in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the updated approval rule details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        approval_rule_id (int): The ID of the approval rule to update.
        name (Optional[str], optional): The new name for the approval rule. Defaults to None.
        approvals_required (Optional[int], optional): The new number of approvals required. Defaults to None.
        user_ids (Optional[List[int]], optional): Updated list of user IDs required to approve. Defaults to None.
        group_ids (Optional[List[int]], optional): Updated list of group IDs required to approve. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated approval rule details (e.g., {"id": 1, "name": "rule1"}).
            - If failed, contains an error message (e.g., {"error": "Approval rule not found"}).

    Raises:
        ValueError: If project_id or approval_rule_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await update_project_level_rule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                approval_rule_id=1,
                name="updated_rule",
                approvals_required=3
            )
        print(response)
        {"id": 1, "name": "updated_rule", "approvals_required": 3}
    """
    if ctx:
        await ctx.info(
            f"Updating approval rule {approval_rule_id} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "approval_rule_id",
            "ctx",
        ]
    }
    response = client.update_project_level_rule(
        project_id=project_id, approval_rule_id=approval_rule_id, **kwargs
    )
    if ctx:
        await ctx.info("Approval rule updated")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_project_level_rule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    approval_rule_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a project-level merge request approval rule.

    This function deletes the specified approval rule from the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        approval_rule_id (int): The ID of the approval rule to delete.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Approval rule not found"}).

    Raises:
        ValueError: If project_id or approval_rule_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_project_level_rule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                approval_rule_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(
            f"Deleting approval rule {approval_rule_id} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_project_level_rule(
        project_id=project_id, approval_rule_id=approval_rule_id
    )
    if ctx:
        await ctx.info("Approval rule deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def merge_request_level_approvals(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    merge_request_iid: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve approvals for a specific merge request in a GitLab project.

    This function queries the GitLab API to fetch approval details for a specified merge request.
    It returns a dictionary containing the approval details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        merge_request_iid (int): The IID of the merge request to retrieve approvals for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains approval details (e.g., {"approved": true, "approved_by": [   ]}).
            - If failed, contains an error message (e.g., {"error": "Merge request not found"}).

    Raises:
        ValueError: If project_id or merge_request_iid is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = merge_request_level_approvals(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                merge_request_iid=1
            )
        print(response)
        {"approved": true, "approved_by": [{"id": 1, "username": "user1"}]}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.merge_request_level_approvals(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_approval_state_merge_requests(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    merge_request_iid: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve the approval state of a specific merge request in a GitLab project.

    This function queries the GitLab API to fetch the approval state for a specified merge request.
    It returns a dictionary containing the approval state details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        merge_request_iid (int): The IID of the merge request to retrieve approval state for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains approval state details (e.g., {"approved": true, "approvals_required": 2}).
            - If failed, contains an error message (e.g., {"error": "Merge request not found"}).

    Raises:
        ValueError: If project_id or merge_request_iid is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_approval_state_merge_requests(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                merge_request_iid=1
            )
        print(response)
        {"approved": true, "approvals_required": 2}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_approval_state_merge_requests(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_merge_request_level_rules(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    merge_request_iid: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve merge request-level approval rules for a specific merge request in a GitLab project.

    This function queries the GitLab API to fetch approval rules for a specified merge request.
    It returns a dictionary containing the approval rules list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        merge_request_iid (int): The IID of the merge request to retrieve approval rules for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of approval rule details (e.g., [{"id": 1, "name": "rule1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Merge request not found"}).

    Raises:
        ValueError: If project_id or merge_request_iid is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_merge_request_level_rules(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                merge_request_iid=1
            )
        print(response)
        [{"id": 1, "name": "rule1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_merge_request_level_rules(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def approve_merge_request(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    merge_request_iid: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Approve a specific merge request in a GitLab project.

    This function approves the specified merge request in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        merge_request_iid (int): The IID of the merge request to approve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of approval (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Merge request not found"}).

    Raises:
        ValueError: If project_id or merge_request_iid is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await approve_merge_request(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                merge_request_iid=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(
            f"Approving merge request {merge_request_iid} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.approve_merge_request(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    if ctx:
        await ctx.info("Merge request approved")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def unapprove_merge_request(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    merge_request_iid: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Unapprove a specific merge request in a GitLab project.

    This function removes approval from the specified merge request in the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        merge_request_iid (int): The IID of the merge request to unapprove.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of unapproval (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Merge request not found"}).

    Raises:
        ValueError: If project_id or merge_request_iid is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await unapprove_merge_request(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                merge_request_iid=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(
            f"Unapproving merge request {merge_request_iid} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.unapprove_merge_request(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    if ctx:
        await ctx.info("Merge request unapproved")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Merge Rules Settings Tools
@mcp.tool()
def get_group_level_rule(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve merge request approval settings for a specific GitLab group.

    This function queries the GitLab API to fetch approval settings for a specified group.
    It returns a dictionary containing the approval settings or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used_avalon
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains approval settings (e.g., {"allow_author_approval": true}).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_level_rule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234"
            )
        print(response)
        {"allow_author_approval": true, "minimum_approvals": 2}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_group_level_rule(group_id=group_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def edit_group_level_rule(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    allow_author_approval: Optional[bool] = None,
    allow_committer_approval: Optional[bool] = None,
    allow_overrides_to_approver_list: Optional[bool] = None,
    minimum_approvals: Optional[int] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Edit merge request approval settings for a specific GitLab group.

    This function updates the approval settings for a specified group and provides progress updates via ctx if available.
    It returns a dictionary containing the updated settings or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        allow_author_approval (Optional[bool], optional): Whether authors can approve their own merge requests. Defaults to None.
        allow_committer_approval (Optional[bool], optional): Whether committers can approve merge requests. Defaults to None.
        allow_overrides_to_approver_list (Optional[bool], optional): Whether overrides to the approver list are allowed. Defaults to None.
        minimum_approvals (Optional[int], optional): The minimum number of approvals required. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated settings (e.g., {"allow_author_approval": true}).
            - If failed, contains an error message (e.g., {"error": "Invalid parameters"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await edit_group_level_rule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                minimum_approvals=2
            )
        print(response)
        {"minimum_approvals": 2}
    """
    if ctx:
        await ctx.info(f"Editing approval settings for group {group_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "group_id",
            "ctx",
        ]
    }
    response = client.edit_group_level_rule(group_id=group_id, **kwargs)
    if ctx:
        await ctx.info("Approval settings edited")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_level_rule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve merge request approval settings for a specific GitLab project.

    This function queries the GitLab API to fetch approval settings for a specified project.
    It returns a dictionary containing the approval settings or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains approval settings (e.g., {"allow_author_approval": true}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_level_rule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"allow_author_approval": true, "minimum_approvals": 2}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_project_level_rule(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def edit_project_level_rule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    allow_author_approval: Optional[bool] = None,
    allow_committer_approval: Optional[bool] = None,
    allow_overrides_to_approver_list: Optional[bool] = None,
    minimum_approvals: Optional[int] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Edit merge request approval settings for a specific GitLab project.

    This function updates the approval settings for a specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the updated settings or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        allow_author_approval (Optional[bool], optional): Whether authors can approve their own merge requests. Defaults to None.
        allow_committer_approval (Optional[bool], optional): Whether committers can approve merge requests. Defaults to None.
        allow_overrides_to_approver_list (Optional[bool], optional): Whether overrides to the approver list are allowed. Defaults to None.
        minimum_approvals (Optional[int], optional): The minimum number of approvals required. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated settings (e.g., {"allow_author_approval": true}).
            - If failed, contains an error message (e.g., {"error": "Invalid parameters"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await edit_project_level_rule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                minimum_approvals=2
            )
        print(response)
        {"minimum_approvals": 2}
    """
    if ctx:
        await ctx.info(f"Editing approval settings for project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.edit_project_level_rule(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Approval settings edited")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Packages Tools
@mcp.tool()
def get_repository_packages(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    package_type: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of repository packages for a specific GitLab project, optionally filtered by package type.

    This function queries the GitLab API to fetch packages for a specified project.
    It returns a dictionary containing the package list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        package_type (Optional[str], optional): Filter packages by type (e.g., "npm", "maven"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of package details (e.g., [{"id": 1, "name": "package1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_repository_packages(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                package_type="npm"
            )
        print(response)
        [{"id": 1, "name": "package1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_repository_packages(project_id=project_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def publish_repository_package(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    package_name: str = None,
    package_version: str = None,
    file_name: str = None,
    status: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Publish a repository package to a specific GitLab project.

    This function publishes a package to the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the package details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        package_name (str): The name of the package.
        package_version (str): The version of the package.
        file_name (str): The name of the package file.
        status (Optional[str], optional): The status of the package (e.g., "default", "hidden"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains package details (e.g., {"id": 1, "name": "package1"}).
            - If failed, contains an error message (e.g., {"error": "Invalid package"}).

    Raises:
        ValueError: If project_id, package_name, package_version, or file_name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await publish_repository_package(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                package_name="mypackage",
                package_version="1.0.0",
                file_name="mypackage-1.0.0.tar.gz"
            )
        print(response)
        {"id": 1, "name": "mypackage", "version": "1.0.0"}
    """
    if ctx:
        await ctx.info(
            f"Publishing package {package_name}/{package_version} to project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.publish_repository_package(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Package published")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def download_repository_package(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    package_name: str = None,
    package_version: str = None,
    file_name: str = None,
    verify: bool = False,
) -> dict:
    """Download a repository package from a specific GitLab project.

    This function downloads a package file from the specified project.
    It returns a dictionary containing the download details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        package_name (str): The name of the package.
        package_version (str): The version of the package.
        file_name (str): The name of the package file to download.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains download details (e.g., {"url": "https://   "}).
            - If failed, contains an error message (e.g., {"error": "Package not found"}).

    Raises:
        ValueError: If project_id, package_name, package_version, or file_name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = download_repository_package(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                package_name="mypackage",
                package_version="1.0.0",
                file_name="mypackage-1.0.0.tar.gz"
            )
        print(response)
        {"url": "https://   /mypackage-1.0.0.tar.gz"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.download_repository_package(
        project_id=project_id,
        package_name=package_name,
        package_version=package_version,
        file_name=file_name,
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Pipeline Tools
@mcp.tool()
def get_pipelines(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    scope: Optional[str] = None,
    status: Optional[str] = None,
    ref: Optional[str] = None,
    source: Optional[str] = None,
    updated_after: Optional[str] = None,
    updated_before: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of pipelines for a specific GitLab project, optionally filtered by scope, status, or ref.

    This function queries the GitLab API to fetch pipelines for a specified project.
    It returns a dictionary containing the pipeline list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        scope (Optional[str], optional): Filter pipelines by scope (e.g., "running", "branches"). Defaults to None.
        status (Optional[str], optional): Filter pipelines by status (e.g., "success", "failed"). Defaults to None.
        ref (Optional[str], optional): Filter pipelines by reference (e.g., branch or tag name). Defaults to None.
        source (Optional[str], optional): Filter pipelines by source (e.g., "push", "schedule"). Defaults to None.
        updated_after (Optional[str], optional): Filter pipelines updated after this date (ISO 8601 format). Defaults to None.
        updated_before (Optional[str], optional): Filter pipelines updated before this date (ISO 8601 format). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of pipeline details (e.g., [{"id": 1, "status": "success"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_pipelines(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                status="success"
            )
        print(response)
        [{"id": 1, "status": "success"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_pipelines(project_id=project_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_pipeline(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific pipeline in a GitLab project.

    This function queries the GitLab API to fetch details for a specified pipeline.
    It returns a dictionary containing the pipeline details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_id (int): The ID of the pipeline to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains pipeline details (e.g., {"id": 1, "status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Pipeline not found"}).

    Raises:
        ValueError: If project_id or pipeline_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_pipeline(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_id=1
            )
        print(response)
        {"id": 1, "status": "success"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_pipeline(project_id=project_id, pipeline_id=pipeline_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def run_pipeline(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    reference: str = None,
    variables: Optional[Dict[str, str]] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Run a pipeline for a specific GitLab project with a given reference (e.g., branch or tag).

    This function triggers a pipeline in the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the pipeline details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        reference (str): The reference (e.g., branch or tag) to run the pipeline on.
        variables (Optional[Dict[str, str]], optional): Dictionary of pipeline variables. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains pipeline details (e.g., {"id": 1, "status": "pending"}).
            - If failed, contains an error message (e.g., {"error": "Invalid reference"}).

    Raises:
        ValueError: If project_id or reference is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await run_pipeline(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                reference="main"
            )
        print(response)
        {"id": 1, "status": "pending"}
    """
    if ctx:
        await ctx.info(f"Running pipeline for project {project_id} on ref {reference}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.run_pipeline(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Pipeline started")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Pipeline Schedules Tools
@mcp.tool()
def get_pipeline_schedules(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of pipeline schedules for a specific GitLab project.

    This function queries the GitLab API to fetch pipeline schedules for a specified project.
    It returns a dictionary containing the schedule list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of schedule details (e.g., [{"id": 1, "description": "schedule1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_pipeline_schedules(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        [{"id": 1, "description": "schedule1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_pipeline_schedules(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_pipeline_schedule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_schedule_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific pipeline schedule in a GitLab project.

    This function queries the GitLab API to fetch details for a specified pipeline schedule.
    It returns a dictionary containing the schedule details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_schedule_id (int): The ID of the pipeline schedule to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains schedule details (e.g., {"id": 1, "description": "schedule1"}).
            - If failed, contains an error message (e.g., {"error": "Schedule not found"}).

    Raises:
        ValueError: If project_id or pipeline_schedule_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_pipeline_schedule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_schedule_id=1
            )
        print(response)
        {"id": 1, "description": "schedule1"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_pipeline_schedule(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_pipelines_triggered_from_schedule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_schedule_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve pipelines triggered by a specific pipeline schedule in a GitLab project.

    This function queries the GitLab API to fetch pipelines triggered by a specified schedule.
    It returns a dictionary containing the pipeline list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_schedule_id (int): The ID of the pipeline schedule.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of pipeline details (e.g., [{"id": 1, "status": "success"},    ]).
            - If failed, contains an error message (e.g., {"error": "Schedule not found"}).

    Raises:
        ValueError: If project_id or pipeline_schedule_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_pipelines_triggered_from_schedule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_schedule_id=1
            )
        print(response)
        [{"id": 1, "status": "success"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_pipelines_triggered_from_schedule(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def create_pipeline_schedule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    description: Optional[str] = None,
    ref: str = None,
    cron: str = None,
    cron_timezone: Optional[str] = None,
    active: Optional[bool] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a pipeline schedule for a specific GitLab project.

    This function creates a new pipeline schedule for the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the schedule details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        description (str): The description of the pipeline schedule.
        ref (str): The reference (e.g., branch or tag) for the pipeline.
        cron (str): The cron expression defining the schedule (e.g., "0 0 * * *").
        cron_timezone (Optional[str], optional): The timezone for the cron schedule (e.g., "UTC"). Defaults to None.
        active (Optional[bool], optional): Whether the schedule is active. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains schedule details (e.g., {"id": 1, "description": "schedule1"}).
            - If failed, contains an error message (e.g., {"error": "Invalid cron expression"}).

    Raises:
        ValueError: If project_id, description, ref, or cron is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_pipeline_schedule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                description="Daily build",
                ref="main",
                cron="0 0 * * *"
            )
        print(response)
        {"id": 1, "description": "Daily build"}
    """
    if ctx:
        await ctx.info(
            f"Creating pipeline schedule '{description}' for project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.create_pipeline_schedule(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Pipeline schedule created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def edit_pipeline_schedule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_schedule_id: int = None,
    description: Optional[str] = None,
    ref: Optional[str] = None,
    cron: Optional[str] = None,
    cron_timezone: Optional[str] = None,
    active: Optional[bool] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Edit a pipeline schedule in a GitLab project.

    This function updates the specified pipeline schedule and provides progress updates via ctx if available.
    It returns a dictionary containing the updated schedule details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_schedule_id (int): The ID of the pipeline schedule to edit.
        description (Optional[str], optional): The new description of the pipeline schedule. Defaults to None.
        ref (Optional[str], optional): The new reference (e.g., branch or tag) for the pipeline. Defaults to None.
        cron (Optional[str], optional): The new cron expression for the schedule (e.g., "0 0 * * *"). Defaults to None.
        cron_timezone (Optional[str], optional): The new timezone for the cron schedule (e.g., "UTC"). Defaults to None.
        active (Optional[bool], optional): Whether the schedule is active. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated schedule details (e.g., {"id": 1, "description": "schedule1"}).
            - If failed, contains an error message (e.g., {"error": "Schedule not found"}).

    Raises:
        ValueError: If project_id or pipeline_schedule_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await edit_pipeline_schedule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_schedule_id=1,
                description="Updated daily build"
            )
        print(response)
        {"id": 1, "description": "Updated daily build"}
    """
    if ctx:
        await ctx.info(
            f"Editing pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "pipeline_schedule_id",
            "ctx",
        ]
    }
    response = client.edit_pipeline_schedule(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id, **kwargs
    )
    if ctx:
        await ctx.info("Pipeline schedule edited")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def take_pipeline_schedule_ownership(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_schedule_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Take ownership of a pipeline schedule in a GitLab project.

    This function takes ownership of the specified pipeline schedule and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_schedule_id (int): The ID of the pipeline schedule to take ownership of.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of ownership (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Schedule not found"}).

    Raises:
        ValueError: If project_id or pipeline_schedule_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await take_pipeline_schedule_ownership(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_schedule_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(
            f"Taking ownership of pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.take_pipeline_schedule_ownership(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    if ctx:
        await ctx.info("Ownership taken")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_pipeline_schedule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_schedule_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a pipeline schedule in a GitLab project.

    This function deletes the specified pipeline schedule and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_schedule_id (int): The ID of the pipeline schedule to delete.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Schedule not found"}).

    Raises:
        ValueError: If project_id or pipeline_schedule_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_pipeline_schedule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_schedule_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(
            f"Deleting pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_pipeline_schedule(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    if ctx:
        await ctx.info("Pipeline schedule deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def run_pipeline_schedule(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_schedule_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Run a pipeline schedule immediately in a GitLab project.

    This function triggers the specified pipeline schedule and provides progress updates via ctx if available.
    It returns a dictionary containing the pipeline details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_schedule_id (int): The ID of the pipeline schedule to run.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains pipeline details (e.g., {"id": 1, "status": "pending"}).
            - If failed, contains an error message (e.g., {"error": "Schedule not found"}).

    Raises:
        ValueError: If project_id or pipeline_schedule_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await run_pipeline_schedule(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_schedule_id=1
            )
        print(response)
        {"id": 1, "status": "pending"}
    """
    if ctx:
        await ctx.info(
            f"Running pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.run_pipeline_schedule(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id
    )
    if ctx:
        await ctx.info("Pipeline schedule run started")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def create_pipeline_schedule_variable(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_schedule_id: int = None,
    key: str = None,
    value: str = None,
    variable_type: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a variable for a pipeline schedule in a GitLab project.

    This function creates a variable for the specified pipeline schedule and provides progress updates via ctx if available.
    It returns a dictionary containing the variable details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_schedule_id (int): The ID of the pipeline schedule.
        key (str): The key of the variable.
        value (str): The value of the variable.
        variable_type (Optional[str], optional): The type of variable (e.g., "env_var"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains variable details (e.g., {"key": "key1", "value": "value1"}).
            - If failed, contains an error message (e.g., {"error": "Invalid variable"}).

    Raises:
        ValueError: If project_id, pipeline_schedule_id, key, or value is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_pipeline_schedule_variable(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_schedule_id=1,
                key="VAR1",key: str = None,
                value="value1"
            )
        print(response)
        {"key": "VAR1", "value": "value1"}
    """
    if ctx:
        await ctx.info(
            f"Creating variable '{key}' for pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "pipeline_schedule_id",
            "ctx",
        ]
    }
    response = client.create_pipeline_schedule_variable(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id, **kwargs
    )
    if ctx:
        await ctx.info("Variable created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_pipeline_schedule_variable(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    pipeline_schedule_id: int = None,
    key: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a variable from a pipeline schedule in a GitLab project.

    This function deletes the specified variable from a pipeline schedule and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        pipeline_schedule_id (int): The ID of the pipeline schedule.
        key (str): The key of the variable to delete.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Variable not found"}).

    Raises:
        ValueError: If project_id, pipeline_schedule_id, or key is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_pipeline_schedule_variable(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                pipeline_schedule_id=1,
                key="VAR1"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(
            f"Deleting variable '{key}' from pipeline schedule {pipeline_schedule_id} in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_pipeline_schedule_variable(
        project_id=project_id, pipeline_schedule_id=pipeline_schedule_id, key=key
    )
    if ctx:
        await ctx.info("Variable deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Projects Tools
@mcp.tool()
def get_projects(
    gitlab_instance: str = None,
    access_token: str = None,
    owned: Optional[bool] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    visibility: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of projects, optionally filtered by ownership, search, sort, or visibility.

    This function queries the GitLab API to fetch a list of projects accessible to the user.
    It returns a dictionary containing the project list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        owned (Optional[bool], optional): Filter projects owned by the authenticated user. Defaults to None.
        search (Optional[str], optional): Filter projects by search term in name or path. Defaults to None.
        sort (Optional[str], optional): Sort projects by criteria (e.g., "created_at", "name"). Defaults to None.
        visibility (Optional[str], optional): Filter projects by visibility (e.g., "public", "private"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of project details (e.g., [{"id": 1, "name": "project1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Authentication failed"}).

    Raises:
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_projects(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                owned=True,
                visibility="public"
            )
        print(response)
        [{"id": 1, "name": "project1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_projects(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific GitLab project.

    This function queries the GitLab API to fetch details for a specified project.
    It returns a dictionary containing the project details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains project details (e.g., {"id": 1, "name": "project1"}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"id": 1, "name": "project1"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_project(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_nested_projects_by_group(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    per_page: Optional[int] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of nested projects within a GitLab group, including descendant groups.

    This function queries the GitLab API to fetch projects within a specified group and its subgroups.
    It returns a dictionary containing the project list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        per_page (Optional[int], optional): Number of projects per page. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of project details (e.g., [{"id": 1, "name": "project1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_nested_projects_by_group(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                per_page=20
            )
        print(response)
        [{"id": 1, "name": "project1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_nested_projects_by_group(group_id=group_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_contributors(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of contributors to a specific GitLab project.

    This function queries the GitLab API to fetch contributors for a specified project.
    It returns a dictionary containing the contributor list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of contributor details (e.g., [{"id": 1, "name": "user1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_contributors(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        [{"id": 1, "name": "user1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_project_contributors(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_statistics(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve statistics for a specific GitLab project.

    This function queries the GitLab API to fetch statistics for a specified project.
    It returns a dictionary containing the statistics or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains project statistics (e.g., {"commits_count": 100, "storage_size": 1024}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_statistics(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"commits_count": 100, "storage_size": 1024}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_project_statistics(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def edit_project(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    visibility: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Edit a specific GitLab project's details (name, description, or visibility).

    This function updates the specified project's details and provides progress updates via ctx if available.
    It returns a dictionary containing the updated project details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (Optional[str], optional): The new name of the project. Defaults to None.
        description (Optional[str], optional): The new description of the project. Defaults to None.
        visibility (Optional[str], optional): The new visibility of the project (e.g., "public", "private"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated project details (e.g., {"id": 1, "name": "newname"}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await edit_project(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="New Project Name"
            )
        print(response)
        {"id": 1, "name": "New Project Name"}
    """
    if ctx:
        await ctx.info(f"Editing project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.edit_project(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Project edited")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_groups(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    skip_groups: Optional[List[int]] = None,
    search: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of groups associated with a specific GitLab project, optionally filtered.

    This function queries the GitLab API to fetch groups associated with a specified project.
    It returns a dictionary containing the group list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        skip_groups (Optional[List[int]], optional): List of group IDs to exclude. Defaults to None.
        search (Optional[str], optional): Filter groups by search term in name. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of group details (e.g., [{"id": 1, "name": "group1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_groups(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                search="group1"
            )
        print(response)
        [{"id": 1, "name": "group1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_project_groups(project_id=project_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def archive_project(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Archive a specific GitLab project.

    This function archives the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of archiving (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await archive_project(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Archiving project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.archive_project(project_id=project_id)
    if ctx:
        await ctx.info("Project archived")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Projects Tools
@mcp.tool()
async def unarchive_project(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Unarchive a specific GitLab project.

    This function unarchives the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of unarchiving (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await unarchive_project(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Unarchiving project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.unarchive_project(project_id=project_id)
    if ctx:
        await ctx.info("Project unarchived")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_project(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a specific GitLab project.

    This function deletes the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_project(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_project(project_id=project_id)
    if ctx:
        await ctx.info("Project deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def share_project(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    group_id: str = None,
    group_access: str = None,
    expires_at: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Share a specific GitLab project with a group, specifying access level.

    This function shares the specified project with a group and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        group_id (str): The ID or path of the GitLab group to share with (e.g., "5678" or "group/subgroup").
        group_access (str): The access level for the group (e.g., "guest", "developer", "maintainer").
        expires_at (Optional[str], optional): The expiration date for the share in ISO 8601 format. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains share details (e.g., {"project_id": "1234", "group_id": "5678"}).
            - If failed, contains an error message (e.g., {"error": "Project or group not found"}).

    Raises:
        ValueError: If project_id, group_id, or group_access is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await share_project(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                group_id="5678",
                group_access="developer"
            )
        print(response)
        {"project_id": "1234", "group_id": "5678", "group_access": "developer"}
    """
    if ctx:
        await ctx.info(f"Sharing project {project_id} with group {group_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.share_project(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Project shared")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Protected Branches Tools
@mcp.tool()
def get_protected_branches(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of protected branches in a specific GitLab project.

    This function queries the GitLab API to fetch protected branches for a specified project.
    It returns a dictionary containing the branch list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of protected branch details (e.g., [{"name": "main", "push_access_levels": [   ]},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_protected_branches(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        [{"name": "main", "push_access_levels": [   ]},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_protected_branches(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_protected_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    branch: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific protected branch in a GitLab project.

    This function queries the GitLab API to fetch details for a specified protected branch.
    It returns a dictionary containing the branch details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The name of the branch to retrieve (e.g., "main").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains branch details (e.g., {"name": "main", "push_access_levels": [   ]}).
            - If failed, contains an error message (e.g., {"error": "Branch not found"}).

    Raises:
        ValueError: If project_id or branch is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_protected_branch(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                branch="main"
            )
        print(response)
        {"name": "main", "push_access_levels": [   ]}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_protected_branch(project_id=project_id, branch=branch)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def protect_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    branch: str = None,
    push_access_level: Optional[str] = None,
    merge_access_level: Optional[str] = None,
    unprotect_access_level: Optional[str] = None,
    allow_force_push: Optional[bool] = None,
    allowed_to_push: Optional[List[Dict]] = None,
    allowed_to_merge: Optional[List[Dict]] = None,
    allowed_to_unprotect: Optional[List[Dict]] = None,
    code_owner_approval_required: Optional[bool] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Protect a specific branch in a GitLab project with specified access levels.

    This function protects a branch with specified access levels and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The name of the branch to protect (e.g., "main").
        push_access_level (Optional[str], optional): Access level for pushing (e.g., "maintainer"). Defaults to None.
        merge_access_level (Optional[str], optional): Access level for merging (e.g., "developer"). Defaults to None.
        unprotect_access_level (Optional[str], optional): Access level for unprotecting (e.g., "maintainer"). Defaults to None.
        allow_force_push (Optional[bool], optional): Whether force pushes are allowed. Defaults to None.
        allowed_to_push (Optional[List[Dict]], optional): List of users or groups allowed to push. Defaults to None.
        allowed_to_merge (Optional[List[Dict]], optional): List of users or groups allowed to merge. Defaults to None.
        allowed_to_unprotect (Optional[List[Dict]], optional): List of users or groups allowed to unprotect. Defaults to None.
        code_owner_approval_required (Optional[bool], optional): Whether code owner approval is required. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains branch protection details (e.g., {"name": "main", "push_access_levels": [   ]}).
            - If failed, contains an error message (e.g., {"error": "Branch not found"}).

    Raises:
        ValueError: If project_id or branch is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await protect_branch(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                branch="main",
                push_access_level="maintainer"
            )
        print(response)
        {"name": "main", "push_access_levels": [   ], "merge_access_levels": [   ],    }
    """
    if ctx:
        await ctx.info(f"Protecting branch '{branch}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.protect_branch(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Branch protected")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def unprotect_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    branch: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Unprotect a specific branch in a GitLab project.

    This function unprotects the specified branch and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The name of the branch to unprotect (e.g., "main").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of unprotection (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Branch not found"}).

    Raises:
        ValueError: If project_id or branch is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await unprotect_branch(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                branch="main"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Unprotecting branch '{branch}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.unprotect_branch(project_id=project_id, branch=branch)
    if ctx:
        await ctx.info("Branch unprotected")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def require_code_owner_approvals_single_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    branch: str = None,
    code_owner_approval_required: bool = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Require or disable code owner approvals for a specific branch in a GitLab project.

    This function sets the code owner approval requirement for a specified branch and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The name of the branch to set approval requirements for (e.g., "main").
        code_owner_approval_required (bool): Whether code owner approval is required for the branch.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated branch details (e.g., {"name": "main", "code_owner_approval_required": true}).
            - If failed, contains an error message (e.g., {"error": "Branch not found"}).

    Raises:
        ValueError: If project_id, branch, or code_owner_approval_required is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await require_code_owner_approvals_single_branch(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                branch="main",
                code_owner_approval_required=True
            )
        print(response)
        {"name": "main", "code_owner_approval_required": true}
    """
    if ctx:
        await ctx.info(
            f"Setting code owner approval requirement for branch '{branch}' in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.require_code_owner_approvals_single_branch(
        project_id=project_id,
        branch=branch,
        code_owner_approval_required=code_owner_approval_required,
    )
    if ctx:
        await ctx.info("Code owner approval setting updated")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Release Tools
@mcp.tool()
def get_releases(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    include_html_description: Optional[bool] = None,
    sort: Optional[str] = None,
    order_by: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of releases for a specific GitLab project, optionally filtered.

    This function queries the GitLab API to fetch releases for a specified project.
    It returns a dictionary containing the release list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        include_html_description (Optional[bool], optional): Whether to include HTML descriptions in the response. Defaults to None.
        sort (Optional[str], optional): Sort releases by criteria (e.g., "released_at"). Defaults to None.
        order_by (Optional[str], optional): Order releases by criteria (e.g., "asc", "desc"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of release details (e.g., [{"tag_name": "v1.0.0", "name": "Release 1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_releases(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                sort="released_at"
            )
        print(response)
        [{"tag_name": "v1.0.0", "name": "Release 1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_releases(project_id=project_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_latest_release(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of the latest release in a GitLab project.

    This function queries the GitLab API to fetch details for the latest release in a specified project.
    It returns a dictionary containing the release details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains release details (e.g., {"tag_name": "v1.0.0", "name": "Release 1"}).
            - If failed, contains an error message (e.g., {"error": "No releases found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_latest_release(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"tag_name": "v1.0.0", "name": "Release 1"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_latest_release(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_latest_release_evidence(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve evidence for the latest release in a GitLab project.

    This function queries the GitLab API to fetch evidence for the latest release in a specified project.
    It returns a dictionary containing the evidence details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains evidence details (e.g., {"id": 1, "collected_at": "2023-01-01"}).
            - If failed, contains an error message (e.g., {"error": "No release found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_latest_release_evidence(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"id": 1, "collected_at": "2023-01-01"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_latest_release_evidence(project_id=project_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_latest_release_asset(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    direct_asset_path: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve a specific asset for the latest release in a GitLab project.

    This function queries the GitLab API to fetch a specific asset for the latest release in a specified project.
    It returns a dictionary containing the asset details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        direct_asset_path (str): The path to the asset (e.g., "assets/file.zip").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains asset details (e.g., {"url": "https://   /file.zip"}).
            - If failed, contains an error message (e.g., {"error": "Asset not found"}).

    Raises:
        ValueError: If project_id or direct_asset_path is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_latest_release_asset(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                direct_asset_path="assets/file.zip"
            )
        print(response)
        {"url": "https://   /file.zip"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_latest_release_asset(
        project_id=project_id, direct_asset_path=direct_asset_path
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_group_releases(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    include_html_description: Optional[bool] = None,
    sort: Optional[str] = None,
    order_by: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of releases for a specific GitLab group, optionally filtered.

    This function queries the GitLab API to fetch releases for a specified group.
    It returns a dictionary containing the release list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        include_html_description (Optional[bool], optional): Whether to include HTML descriptions in the response. Defaults to None.
        sort (Optional[str], optional): Sort releases by criteria (e.g., "released_at"). Defaults to None.
        order_by (Optional[str], optional): Order releases by criteria (e.g., "asc", "desc"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of release details (e.g., [{"tag_name": "v1.0.0", "name": "Release 1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_releases(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                sort="released_at"
            )
        print(response)
        [{"tag_name": "v1.0.0", "name": "Release 1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_releases(group_id=group_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def download_release_asset(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    tag_name: str = None,
    direct_asset_path: str = None,
    verify: bool = False,
) -> dict:
    """Download a release asset from a group's release in GitLab.

    This function queries the GitLab API to download a specific asset from a group's release.
    It returns a dictionary containing the asset details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        tag_name (str): The tag name of the release (e.g., "v1.0.0").
        direct_asset_path (str): The path to the asset (e.g., "assets/file.zip").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains asset details (e.g., {"url": "https://   /file.zip"}).
            - If failed, contains an error message (e.g., {"error": "Asset not found"}).

    Raises:
        ValueError: If group_id, tag_name, or direct_asset_path is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = download_release_asset(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                tag_name="v1.0.0",
                direct_asset_path="assets/file.zip"
            )
        print(response)
        {"url": "https://   /file.zip"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.download_release_asset(
        group_id=group_id, tag_name=tag_name, direct_asset_path=direct_asset_path
    )
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_release_by_tag(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    tag_name: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a release by its tag in a GitLab project.

    This function queries the GitLab API to fetch details for a release associated with a specific tag.
    It returns a dictionary containing the release details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        tag_name (str): The tag name of the release (e.g., "v1.0.0").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains release details (e.g., {"tag_name": "v1.0.0", "name": "Release 1"}).
            - If failed, contains an error message (e.g., {"error": "Release not found"}).

    Raises:
        ValueError: If project_id or tag_name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_release_by_tag(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                tag_name="v1.0.0"
            )
        print(response)
        {"tag_name": "v1.0.0", "name": "Release 1"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_release_by_tag(project_id=project_id, tag_name=tag_name)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def create_release(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    tag_name: str = None,
    description: Optional[str] = None,
    released_at: Optional[str] = None,
    assets: Optional[Dict] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a new release in a GitLab project.

    This function creates a new release for the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the release details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the release.
        tag_name (str): The tag name associated with the release (e.g., "v1.0.0").
        description (Optional[str], optional): The description of the release. Defaults to None.
        released_at (Optional[str], optional): The release date in ISO 8601 format. Defaults to None.
        assets (Optional[Dict], optional): Dictionary of release assets. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains release details (e.g., {"tag_name": "v1.0.0", "name": "Release 1"}).
            - If failed, contains an error message (e.g., {"error": "Invalid tag"}).

    Raises:
        ValueError: If project_id, name, or tag_name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_release(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="Release 1",
                tag_name="v1.0.0"
            )
        print(response)
        {"tag_name": "v1.0.0", "name": "Release 1"}
    """
    if ctx:
        await ctx.info(f"Creating release '{name}' for project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.create_release(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Release created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def create_release_evidence(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    tag_name: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create evidence for a release in a GitLab project.

    This function creates evidence for a specified release and provides progress updates via ctx if available.
    It returns a dictionary containing the evidence details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        tag_name (str): The tag name of the release (e.g., "v1.0.0").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains evidence details (e.g., {"id": 1, "collected_at": "2023-01-01"}).
            - If failed, contains an error message (e.g., {"error": "Release not found"}).

    Raises:
        ValueError: If project_id or tag_name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_release_evidence(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                tag_name="v1.0.0"
            )
        print(response)
        {"id": 1, "collected_at": "2023-01-01"}
    """
    if ctx:
        await ctx.info(
            f"Creating release evidence for tag '{tag_name}' in project {project_id}"
        )
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.create_release_evidence(project_id=project_id, tag_name=tag_name)
    if ctx:
        await ctx.info("Release evidence created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def update_release(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    tag_name: str = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    released_at: Optional[str] = None,
    assets: Optional[Dict] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Update a release in a GitLab project.

    This function updates the specified release and provides progress updates via ctx if available.
    It returns a dictionary containing the updated release details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        tag_name (str): The tag name of the release to update (e.g., "v1.0.0").
        name (Optional[str], optional): The new name of the release. Defaults to None.
        description (Optional[str], optional): The new description of the release. Defaults to None.
        released_at (Optional[str], optional): The new release date in ISO 8601 format. Defaults to None.
        assets (Optional[Dict], optional): Updated dictionary of release assets. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated release details (e.g., {"tag_name": "v1.0.0", "name": "Updated Release"}).
            - If failed, contains an error message (e.g., {"error": "Release not found"}).

    Raises:
        ValueError: If project_id or tag_name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await update_release(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                tag_name="v1.0.0",
                name="Updated Release"
            )
        print(response)
        {"tag_name": "v1.0.0", "name": "Updated Release"}
    """
    if ctx:
        await ctx.info(f"Updating release for tag '{tag_name}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "tag_name",
            "ctx",
        ]
    }
    response = client.update_release(project_id=project_id, tag_name=tag_name, **kwargs)
    if ctx:
        await ctx.info("Release updated")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_release(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    tag_name: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a release in a GitLab project.

    This function deletes the specified release and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        tag_name (str): The tag name of the release to delete (e.g., "v1.0.0").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Release not found"}).

    Raises:
        ValueError: If project_id or tag_name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_release(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                tag_name="v1.0.0"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting release for tag '{tag_name}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_release(project_id=project_id, tag_name=tag_name)
    if ctx:
        await ctx.info("Release deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Runners Tools
@mcp.tool()
def get_runners(
    gitlab_instance: str = None,
    access_token: str = None,
    scope: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    tag_list: Optional[List[str]] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of runners in GitLab, optionally filtered by scope, type, status, or tags.

    This function queries the GitLab API to fetch a list of runners accessible to the user.
    It returns a dictionary containing the runner list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        scope (Optional[str], optional): Filter runners by scope (e.g., "active"). Defaults to None.
        type (Optional[str], optional): Filter runners by type (e.g., "instance_type"). Defaults to None.
        status (Optional[str], optional): Filter runners by status (e.g., "online"). Defaults to None.
        tag_list (Optional[List[str]], optional): Filter runners by tags. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of runner details (e.g., [{"id": 1, "description": "runner1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Authentication failed"}).

    Raises:
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_runners(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                status="online"
            )
        print(response)
        [{"id": 1, "description": "runner1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify"]
    }
    response = client.get_runners(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_runner(
    gitlab_instance: str = None,
    access_token: str = None,
    runner_id: int = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific GitLab runner.

    This function queries the GitLab API to fetch details for a specified runner.
    It returns a dictionary containing the runner details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        runner_id (int): The ID of the runner to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains runner details (e.g., {"id": 1, "description": "runner1"}).
            - If failed, contains an error message (e.g., {"error": "Runner not found"}).

    Raises:
        ValueError: If runner_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_runner(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                runner_id=1
            )
        print(response)
        {"id": 1, "description": "runner1"}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_runner(runner_id=runner_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def update_runner_details(
    gitlab_instance: str = None,
    access_token: str = None,
    runner_id: int = None,
    description: Optional[str] = None,
    active: Optional[bool] = None,
    tag_list: Optional[List[str]] = None,
    run_untagged: Optional[bool] = None,
    locked: Optional[bool] = None,
    access_level: Optional[str] = None,
    maximum_timeout: Optional[int] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Update details for a specific GitLab runner.

    This function updates the specified runner's details and provides progress updates via ctx if available.
    It returns a dictionary containing the updated runner details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        runner_id (int): The ID of the runner to update.
        description (Optional[str], optional): The new description of the runner. Defaults to None.
        active (Optional[bool], optional): Whether the runner is active. Defaults to None.
        tag_list (Optional[List[str]], optional): List of tags for the runner. Defaults to None.
        run_untagged (Optional[bool], optional): Whether the runner can run untagged jobs. Defaults to None.
        locked (Optional[bool], optional): Whether the runner is locked. Defaults to None.
        access_level (Optional[str], optional): The access level of the runner (e.g., "ref_protected"). Defaults to None.
        maximum_timeout (Optional[int], optional): The maximum timeout for the runner in seconds. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains updated runner details (e.g., {"id": 1, "description": "updated_runner"}).
            - If failed, contains an error message (e.g., {"error": "Runner not found"}).

    Raises:
        ValueError: If runner_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await update_runner_details(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                runner_id=1,
                description="Updated Runner"
            )
        print(response)
        {"id": 1, "description": "Updated Runner"}
    """
    if ctx:
        await ctx.info(f"Updating runner {runner_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "runner_id",
            "ctx",
        ]
    }
    response = client.update_runner_details(runner_id=runner_id, **kwargs)
    if ctx:
        await ctx.info("Runner updated")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def pause_runner(
    gitlab_instance: str = None,
    access_token: str = None,
    runner_id: int = None,
    active: bool = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Pause or unpause a specific GitLab runner.

    This function sets the active status of the specified runner and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        runner_id (int): The ID of the runner to pause or unpause.
        active (bool): Whether the runner should be active (True) or paused (False).
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of status change (e.g., {"id": 1, "active": false}).
            - If failed, contains an error message (e.g., {"error": "Runner not found"}).

    Raises:
        ValueError: If runner_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await pause_runner(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                runner_id=1,
                active=False
            )
        print(response)
        {"id": 1, "active": false}
    """
    if ctx:
        await ctx.info(f"Setting runner {runner_id} active status to {active}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.pause_runner(runner_id=runner_id, active=active)
    if ctx:
        await ctx.info("Runner status updated")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_runner_jobs(
    gitlab_instance: str = None,
    access_token: str = None,
    runner_id: int = None,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve jobs for a specific GitLab runner, optionally filtered by status or sorted.

    This function queries the GitLab API to fetch jobs for a specified runner.
    It returns a dictionary containing the job list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        runner_id (int): The ID of the runner to retrieve jobs for.
        status (Optional[str], optional): Filter jobs by status (e.g., "success", "failed"). Defaults to None.
        sort (Optional[str], optional): Sort jobs by criteria (e.g., "created_at"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of job details (e.g., [{"id": 1, "status": "success"},    ]).
            - If failed, contains an error message (e.g., {"error": "Runner not found"}).

    Raises:
        ValueError: If runner_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_runner_jobs(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                runner_id=1,
                status="success"
            )
        print(response)
        [{"id": 1, "status": "success"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "runner_id"]
    }
    response = client.get_runner_jobs(runner_id=runner_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_project_runners(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    scope: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of runners in a specific GitLab project, optionally filtered by scope.

    This function queries the GitLab API to fetch runners for a specified project.
    It returns a dictionary containing the runner list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        scope (Optional[str], optional): Filter runners by scope (e.g., "active"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of runner details (e.g., [{"id": 1, "description": "runner1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_project_runners(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                scope="active"
            )
        print(response)
        [{"id": 1, "description": "runner1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_project_runners(project_id=project_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def enable_project_runner(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    runner_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Enable a runner in a specific GitLab project.

    This function enables the specified runner for a project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        runner_id (int): The ID of the runner to enable.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of enabling (e.g., {"id": 1, "status": "enabled"}).
            - If failed, contains an error message (e.g., {"error": "Runner not found"}).

    Raises:
        ValueError: If project_id or runner_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await enable_project_runner(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                runner_id=1
            )
        print(response)
        {"id": 1, "status": "enabled"}
    """
    if ctx:
        await ctx.info(f"Enabling runner {runner_id} for project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.enable_project_runner(project_id=project_id, runner_id=runner_id)
    if ctx:
        await ctx.info("Runner enabled")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_project_runner(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    runner_id: int = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a runner from a specific GitLab project.

    This function removes the specified runner from a project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        runner_id (int): The ID of the runner to delete.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Runner not found"}).

    Raises:
        ValueError: If project_id or runner_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_project_runner(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                runner_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting runner {runner_id} from project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_project_runner(project_id=project_id, runner_id=runner_id)
    if ctx:
        await ctx.info("Runner deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_group_runners(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    scope: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of runners in a specific GitLab group, optionally filtered by scope.

    This function queries the GitLab API to fetch runners for a specified group.
    It returns a dictionary containing the runner list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        scope (Optional[str], optional): Filter runners by scope (e.g., "active"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of runner details (e.g., [{"id": 1, "description": "runner1"},    ]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_group_runners(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234",
                scope="active"
            )
        print(response)
        [{"id": 1, "description": "runner1"},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k not in ["client", "gitlab_instance", "access_token", "verify", "group_id"]
    }
    response = client.get_group_runners(group_id=group_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Runners Tools
@mcp.tool()
async def register_new_runner(
    gitlab_instance: str = None,
    access_token: str = None,
    token: str = None,
    description: Optional[str] = None,
    tag_list: Optional[List[str]] = None,
    run_untagged: Optional[bool] = None,
    locked: Optional[bool] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Register a new GitLab runner.

    This function registers a new runner with the provided token and provides progress updates via ctx if available.
    It returns a dictionary containing the runner details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        token (str): The registration token for the runner.
        description (Optional[str], optional): The description of the runner. Defaults to None.
        tag_list (Optional[List[str]], optional): List of tags for the runner. Defaults to None.
        run_untagged (Optional[bool], optional): Whether the runner can run untagged jobs. Defaults to None.
        locked (Optional[bool], optional): Whether the runner is locked. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains runner details (e.g., {"id": 1, "description": "runner1"}).
            - If failed, contains an error message (e.g., {"error": "Invalid token"}).

    Raises:
        ValueError: If token is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await register_new_runner(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                token="runner_token",
                description="New Runner"
            )
        print(response)
        {"id": 1, "description": "New Runner"}
    """
    if ctx:
        await ctx.info("Registering new runner with token")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_runner(
    gitlab_instance: str = None,
    access_token: str = None,
    runner_id: Optional[int] = None,
    token: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a GitLab runner by ID or token.

    This function deletes a runner identified by either its ID or token and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        runner_id (Optional[int], optional): The ID of the runner to delete. Defaults to None.
        token (Optional[str], optional): The token of the runner to delete. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Runner not found"}).

    Raises:
        ValueError: If neither runner_id nor token is provided or if both are invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_runner(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                runner_id=1
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting runner with ID {runner_id or 'token'}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def verify_runner_authentication(
    gitlab_instance: str = None,
    access_token: str = None,
    token: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Verify authentication for a GitLab runner using its token.

    This function verifies the authentication of a runner using its token and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        token (str): The runner token to verify.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains verification details (e.g., {"status": "verified"}).
            - If failed, contains an error message (e.g., {"error": "Invalid token"}).

    Raises:
        ValueError: If token is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await verify_runner_authentication(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                token="runner_token"
            )
        print(response)
        {"status": "verified"}
    """
    if ctx:
        await ctx.info("Verifying runner authentication")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.verify_runner_authentication(token=token)
    if ctx:
        await ctx.info("Runner authentication verified")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def reset_gitlab_runner_token(
    gitlab_instance: str = None,
    access_token: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Reset the GitLab runner registration token.

    This function resets the global runner registration token and provides progress updates via ctx if available.
    It returns a dictionary containing the new token or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the new token (e.g., {"token": "new_token"}).
            - If failed, contains an error message (e.g., {"error": "Permission denied"}).

    Raises:
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await reset_gitlab_runner_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token"
            )
        print(response)
        {"token": "new_token"}
    """
    if ctx:
        await ctx.info("Resetting GitLab runner registration token")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.reset_gitlab_runner_token()
    if ctx:
        await ctx.info("Runner token reset")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def reset_project_runner_token(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Reset the registration token for a project's runner in GitLab.

    This function resets the runner registration token for a specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the new token or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the new token (e.g., {"token": "new_token"}).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await reset_project_runner_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234"
            )
        print(response)
        {"token": "new_token"}
    """
    if ctx:
        await ctx.info(f"Resetting runner token for project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.reset_project_runner_token(project_id=project_id)
    if ctx:
        await ctx.info("Project runner token reset")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def reset_group_runner_token(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Reset the registration token for a group's runner in GitLab.

    This function resets the runner registration token for a specified group and provides progress updates via ctx if available.
    It returns a dictionary containing the new token or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the new token (e.g., {"token": "new_token"}).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await reset_group_runner_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                group_id="1234"
            )
        print(response)
        {"token": "new_token"}
    """
    if ctx:
        await ctx.info(f"Resetting runner token for group {group_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.reset_group_runner_token(group_id=group_id)
    if ctx:
        await ctx.info("Group runner token reset")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def reset_token(
    gitlab_instance: str = None,
    access_token: str = None,
    runner_id: int = None,
    token: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Reset the authentication token for a specific GitLab runner.

    This function resets the authentication token for a specified runner and provides progress updates via ctx if available.
    It returns a dictionary containing the new token or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        runner_id (int): The ID of the runner to reset the token for.
        token (str): The current token of the runner.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the new token (e.g., {"token": "new_token"}).
            - If failed, contains an error message (e.g., {"error": "Runner not found"}).

    Raises:
        ValueError: If runner_id or token is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await reset_token(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                runner_id=1,
                token="current_token"
            )
        print(response)
        {"token": "new_token"}
    """
    if ctx:
        await ctx.info(f"Resetting authentication token for runner {runner_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.reset_token(runner_id=runner_id, token=token)
    if ctx:
        await ctx.info("Runner authentication token reset")
    return response.data if isinstance(response, Response) else {"error": str(response)}


# Tags Tools
@mcp.tool()
def get_tags(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of tags for a specific GitLab project, optionally filtered or sorted.

    This function queries the GitLab API to fetch tags for a specified project.
    It returns a dictionary containing the tag list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        search (Optional[str], optional): Filter tags by search term in name. Defaults to None.
        sort (Optional[str], optional): Sort tags by criteria (e.g., "name", "updated"). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of tag details (e.g., [{"name": "v1.0.0", "commit": {   }},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_tags(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                search="v1"
            )
        print(response)
        [{"name": "v1.0.0", "commit": {   }},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_tags(project_id=project_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_tag(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific tag in a GitLab project.

    This function queries the GitLab API to fetch details for a specified tag.
    It returns a dictionary containing the tag details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the tag to retrieve (e.g., "v1.0.0").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains tag details (e.g., {"name": "v1.0.0", "commit": {   }}).
            - If failed, contains an error message (e.g., {"error": "Tag not found"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_tag(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="v1.0.0"
            )
        print(response)
        {"name": "v1.0.0", "commit": {   }}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_tag(project_id=project_id, name=name)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def create_tag(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    ref: str = None,
    message: Optional[str] = None,
    release_description: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a new tag in a GitLab project.

    This function creates a new tag in the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the tag details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the tag to create (e.g., "v1.0.0").
        ref (str): The reference (e.g., branch or commit SHA) to tag.
        message (Optional[str], optional): The tag message. Defaults to None.
        release_description (Optional[str], optional): The release description associated with the tag. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains tag details (e.g., {"name": "v1.0.0", "commit": {   }}).
            - If failed, contains an error message (e.g., {"error": "Invalid reference"}).

    Raises:
        ValueError: If project_id, name, or ref is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await create_tag(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="v1.0.0",
                ref="main"
            )
        print(response)
        {"name": "v1.0.0", "commit": {   }}
    """
    if ctx:
        await ctx.info(f"Creating tag '{name}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.create_tag(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Tag created")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def delete_tag(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a specific tag in a GitLab project.

    This function deletes the specified tag and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the tag to delete (e.g., "v1.0.0").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of deletion (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Tag not found"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await delete_tag(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="v1.0.0"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting tag '{name}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.delete_tag(project_id=project_id, name=name)
    if ctx:
        await ctx.info("Tag deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_protected_tags(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve a list of protected tags in a specific GitLab project, optionally filtered by name.

    This function queries the GitLab API to fetch protected tags for a specified project.
    It returns a dictionary containing the tag list or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (Optional[str], optional): Filter tags by name. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of protected tag details (e.g., [{"name": "v1.0.0", "create_access_levels": [   ]},    ]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_protected_tags(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="v1"
            )
        print(response)
        [{"name": "v1.0.0", "create_access_levels": [   ]},    ]
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {
        k: v
        for k, v in locals().items()
        if v is not None
        and k
        not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]
    }
    response = client.get_protected_tags(project_id=project_id, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
def get_protected_tag(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific protected tag in a GitLab project.

    This function queries the GitLab API to fetch details for a specified protected tag.
    It returns a dictionary containing the tag details or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the protected tag to retrieve (e.g., "v1.0.0").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains tag details (e.g., {"name": "v1.0.0", "create_access_levels": [   ]}).
            - If failed, contains an error message (e.g., {"error": "Tag not found"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = get_protected_tag(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="v1.0.0"
            )
        print(response)
        {"name": "v1.0.0", "create_access_levels": [   ]}
    """
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.get_protected_tag(project_id=project_id, name=name)
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def protect_tag(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    create_access_level: Optional[str] = None,
    allowed_to_create: Optional[List[Dict]] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Protect a specific tag in a GitLab project with specified access levels.

    This function protects a tag with specified access levels and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the tag to protect (e.g., "v1.0.0").
        create_access_level (Optional[str], optional): Access level for creating the tag (e.g., "maintainer"). Defaults to None.
        allowed_to_create (Optional[List[Dict]], optional): List of users or groups allowed to create the tag. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains tag protection details (e.g., {"name": "v1.0.0", "create_access_levels": [   ]}).
            - If failed, contains an error message (e.g., {"error": "Tag not found"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await protect_tag(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="v1.0.0",
                create_access_level="maintainer"
            )
        print(response)
        {"name": "v1.0.0", "create_access_levels": [   ]}
    """
    if ctx:
        await ctx.info(f"Protecting tag '{name}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
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
            "ctx",
        ]
    }
    response = client.protect_tag(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Tag protected")
    return response.data if isinstance(response, Response) else {"error": str(response)}


@mcp.tool()
async def unprotect_tag(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str = None,
    name: str = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Unprotect a specific tag in a GitLab project.

    This function unprotects the specified tag and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str): The URL of the GitLab instance (e.g., "https://gitlab.com/api/v4/").
            If None, the default instance configured in gitlab_api is used.
            Always ensure the URL includes the API suffix at the end /api/v4/.
        access_token (str): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        name (str): The name of the tag to unprotect (e.g., "v1.0.0").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).
        ctx (Optional[Context], optional): MCP context for progress reporting.

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains confirmation of unprotection (e.g., {"status": "success"}).
            - If failed, contains an error message (e.g., {"error": "Tag not found"}).

    Raises:
        ValueError: If project_id or name is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        response = await unprotect_tag(
                gitlab_instance="https://gitlab.com",
                access_token="your_token",
                project_id="1234",
                name="v1.0.0"
            )
        print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Unprotecting tag '{name}' in project {project_id}")
    client = Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    response = client.unprotect_tag(project_id=project_id, name=name)
    if ctx:
        await ctx.info("Tag unprotected")
    return response.data if isinstance(response, Response) else {"error": str(response)}


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
            port = arg
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
