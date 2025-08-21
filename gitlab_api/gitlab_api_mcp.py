#!/usr/bin/python
# coding: utf-8

import getopt
import sys
import gitlab_api
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
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
            - If successful, contains a list of branch details (e.g., [{"name": "main", "commit": {...}}, ...]).
            - If failed, contains an error message (e.g., {"error": "Invalid project ID"}).

    Raises:
        ValueError: If required parameters (e.g., project_id, when not configured in gitlab_api) are missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_branches(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     search="feature",
        ...     regex="^feature/.*"
        ... )
        >>> print(response)
        {"branches": [{"name": "feature/abc", "commit": {...}}, {"name": "feature/xyz", "commit": {...}}]}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_branches(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    branch: str,
    verify: bool = False,
) -> dict:
    """Retrieve details about a specific branch in a GitLab project.

    This function queries the GitLab API to fetch details for a specified branch in a project.
    It returns a dictionary containing the branch details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The name of the branch to retrieve.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains branch details (e.g., {"name": "main", "commit": {...}}).
            - If failed, contains an error message (e.g., {"error": "Branch not found"}).

    Raises:
        ValueError: If project_id or branch is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_branch(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     branch="main"
        ... )
        >>> print(response)
        {"name": "main", "commit": {...}}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_branch(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def create_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    branch: str,
    ref: str,
    verify: bool = False,
) -> dict:
    """Create a new branch in a GitLab project from a reference (branch name, tag, or commit SHA).

    This function creates a new branch in the specified project using the provided reference.
    It returns a dictionary containing the branch details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The name of the branch to create.
        ref (str): The reference (branch name, tag, or commit SHA) to create the branch from.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains branch details (e.g., {"name": "new-branch", "commit": {...}}).
            - If failed, contains an error message (e.g., {"error": "Reference not found"}).

    Raises:
        ValueError: If project_id, branch, or ref is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = create_branch(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     branch="feature/new",
        ...     ref="main"
        ... )
        >>> print(response)
        {"name": "feature/new", "commit": {...}}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.create_branch(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
async def delete_branch(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    branch: str,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a specific branch in a GitLab project.

    This function deletes the specified branch from the project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
        >>> response = await delete_branch(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     branch="feature/old"
        ... )
        >>> print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting branch '{branch}' in project {project_id}")
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]}
    response = client.delete_branch(**kwargs)
    if ctx:
        await ctx.info("Deletion complete")
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
async def delete_merged_branches(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete all merged branches in a GitLab project (excluding protected branches).

    This function deletes all branches that have been merged into the project's default branch,
    excluding protected branches, and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
        >>> response = await delete_merged_branches(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234"
        ... )
        >>> print(response)
        {"deleted": ["feature/old", "bugfix/123"]}
    """
    if ctx:
        await ctx.info(f"Deleting merged branches in project {project_id}")
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "ctx"]}
    response = client.delete_merged_branches(**kwargs)
    if ctx:
        await ctx.info("Deletion complete")
    return response.data if isinstance(response, Response) else {"error": str(response)}

# Commits Tools
@mcp.tool()
def get_commits(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
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
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
            - If successful, contains a list of commit details (e.g., [{"id": "abc123", "message": "..."}, ...]).
            - If failed, contains an error message (e.g., {"error": "Invalid project ID"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_commits(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     ref_name="main",
        ...     since="2023-01-01T00:00:00Z"
        ... )
        >>> print(response)
        [{"id": "abc123", "message": "Initial commit", ...}, ...]
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_commits(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    stats: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve details about a specific commit in a GitLab project.

    This function queries the GitLab API to fetch details for a specified commit.
    It returns a dictionary containing the commit details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve.
        stats (Optional[bool], optional): Include commit statistics. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains commit details (e.g., {"id": "abc123", "message": "..."}).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_commit(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123",
        ...     stats=True
        ... )
        >>> print(response)
        {"id": "abc123", "message": "Fix bug", "stats": {...}}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id", "commit_hash"]}
    response = client.get_commit(project_id=project_id, commit_hash=commit_hash, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_commit_references(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    type: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Retrieve references (branches/tags) where a commit is pushed in a GitLab project.

    This function queries the GitLab API to fetch references (branches or tags) containing the specified commit.
    The type parameter can filter to 'branch', 'tag', or 'all'.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to query.
        type (Optional[str], optional): Filter references by type ('branch', 'tag', or 'all'). Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of references (e.g., [{"name": "main", "type": "branch"}, ...]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_commit_references(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123",
        ...     type="branch"
        ... )
        >>> print(response)
        [{"name": "main", "type": "branch"}, {"name": "feature/abc", "type": "branch"}]
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id", "commit_hash"]}
    response = client.get_commit_references(project_id=project_id, commit_hash=commit_hash, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def cherry_pick_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    branch: str,
    dry_run: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Cherry-pick a commit into a target branch in a GitLab project.

    This function cherry-picks a specified commit into the target branch.
    Use dry_run to simulate the operation without applying changes.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
        >>> response = cherry_pick_commit(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123",
        ...     branch="main",
        ...     dry_run=True
        ... )
        >>> print(response)
        {"commit_id": "abc123", "branch": "main", "status": "simulated"}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id", "commit_hash"]}
    response = client.cherry_pick_commit(project_id=project_id, commit_hash=commit_hash, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def create_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    branch: str,
    commit_message: str,
    actions: list,
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
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        branch (str): The branch to commit to.
        commit_message (str): The message for the commit.
        actions (list): A list of file actions (e.g., [{"action": "create", "file_path": "file.txt", "content": "..."}]).
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
            - If successful, contains commit details (e.g., {"id": "xyz789", "message": "..."}).
            - If failed, contains an error message (e.g., {"error": "Invalid actions"}).

    Raises:
        ValueError: If project_id, branch, commit_message, or actions is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = create_commit(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     branch="main",
        ...     commit_message="Add new file",
        ...     actions=[{"action": "create", "file_path": "file.txt", "content": "Hello"}]
        ... )
        >>> print(response)
        {"id": "xyz789", "message": "Add new file"}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id"]}
    response = client.create_commit(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def revert_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    branch: str,
    dry_run: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Revert a commit in a target branch in a GitLab project.

    This function reverts a specified commit on the target branch.
    Use dry_run to simulate the operation without applying changes.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
        >>> response = revert_commit(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123",
        ...     branch="main",
        ...     dry_run=True
        ... )
        >>> print(response)
        {"commit_id": "abc123", "branch": "main", "status": "simulated"}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id", "commit_hash"]}
    response = client.revert_commit(project_id=project_id, commit_hash=commit_hash, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_commit_diff(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    unidiff: Optional[bool] = None,
    verify: bool = False,
) -> dict:
    """Retrieve the diff for a specific commit in a GitLab project.

    This function queries the GitLab API to fetch the diff for a specified commit.
    Use unidiff for unified diff format.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve the diff for.
        unidiff (Optional[bool], optional): If True, return the diff in unified format. Defaults to None.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains the diff details (e.g., [{"diff": "...", "new_path": "file.txt"}, ...]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_commit_diff(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123",
        ...     unidiff=True
        ... )
        >>> print(response)
        [{"diff": "...", "new_path": "file.txt"}, ...]
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id", "commit_hash"]}
    response = client.get_commit_diff(project_id=project_id, commit_hash=commit_hash, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_commit_comments(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    verify: bool = False,
) -> dict:
    """Retrieve comments on a specific commit in a GitLab project.

    This function queries the GitLab API to fetch comments on a specified commit.
    Note: This endpoint is deprecated in GitLab; consider using get_commit_discussions.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve comments for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of comments (e.g., [{"id": 1, "note": "Great change"}, ...]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_commit_comments(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123"
        ... )
        >>> print(response)
        [{"id": 1, "note": "Great change"}, ...]
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_commit_comments(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def create_commit_comment(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    note: str,
    path: Optional[str] = None,
    line: Optional[int] = None,
    line_type: Optional[str] = None,
    verify: bool = False,
) -> dict:
    """Create a new comment on a specific commit in a GitLab project.

    This function creates a comment on a specified commit, optionally tied to a file path and line.
    It returns a dictionary containing the comment details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
        >>> response = create_commit_comment(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123",
        ...     note="Looks good!"
        ... )
        >>> print(response)
        {"id": 1, "note": "Looks good!"}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id", "commit_hash"]}
    response = client.create_commit_comment(project_id=project_id, commit_hash=commit_hash, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_commit_discussions(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    verify: bool = False,
) -> dict:
    """Retrieve discussions (threaded comments) on a specific commit in a GitLab project.

    This function queries the GitLab API to fetch threaded discussions for a specified commit.
    It returns a dictionary containing the discussion details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve discussions for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of discussions (e.g., [{"id": "disc1", "notes": [...]}, ...]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_commit_discussions(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123"
        ... )
        >>> print(response)
        [{"id": "disc1", "notes": [{"note": "Great change"}, ...]}, ...]
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_commit_discussions(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_commit_statuses(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
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
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
            - If successful, contains a list of statuses (e.g., [{"name": "test", "status": "success"}, ...]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_commit_statuses(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123",
        ...     name="test"
        ... )
        >>> print(response)
        [{"name": "test", "status": "success"}, ...]
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id", "commit_hash"]}
    response = client.get_commit_statuses(project_id=project_id, commit_hash=commit_hash, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def post_build_status_to_commit(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    state: str,
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
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
        >>> response = post_build_status_to_commit(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123",
        ...     state="success",
        ...     context="ci/build"
        ... )
        >>> print(response)
        {"name": "ci/build", "status": "success"}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id", "commit_hash"]}
    response = client.post_build_status_to_commit(project_id=project_id, commit_hash=commit_hash, **kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_commit_merge_requests(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    verify: bool = False,
) -> dict:
    """Retrieve merge requests associated with a specific commit in a GitLab project.

    This function queries the GitLab API to fetch merge requests that include the specified commit.
    It returns a dictionary containing the merge request details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to query.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of merge requests (e.g., [{"iid": 1, "title": "..."}, ...]).
            - If failed, contains an error message (e.g., {"error": "Commit not found"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_commit_merge_requests(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123"
        ... )
        >>> print(response)
        [{"iid": 1, "title": "Add feature"}, ...]
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_commit_merge_requests(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_commit_gpg_signature(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    commit_hash: str,
    verify: bool = False,
) -> dict:
    """Retrieve the GPG signature for a specific commit in a GitLab project.

    This function queries the GitLab API to fetch the GPG signature for a specified commit.
    It returns a dictionary containing the signature details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        commit_hash (str): The SHA of the commit to retrieve the signature for.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains signature details (e.g., {"signature": "...", "verified": true}).
            - If failed, contains an error message (e.g., {"error": "No GPG signature"}).

    Raises:
        ValueError: If project_id or commit_hash is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_commit_gpg_signature(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     commit_hash="abc123"
        ... )
        >>> print(response)
        {"signature": "...", "verified": true}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
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
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of deploy tokens (e.g., [{"id": 1, "name": "token1"}, ...]).
            - If failed, contains an error message (e.g., {"error": "Authentication failed"}).

    Raises:
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_deploy_tokens(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token"
        ... )
        >>> print(response)
        [{"id": 1, "name": "token1"}, ...]
    """
    client = gitlab_api.Api(
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
    project_id: str,
    verify: bool = False,
) -> dict:
    """Retrieve a list of deploy tokens for a specific GitLab project.

    This function queries the GitLab API to fetch deploy tokens for a specified project.
    It returns a dictionary containing the token list or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        project_id (str): The ID or path of the GitLab project (e.g., "1234" or "namespace/project").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of deploy tokens (e.g., [{"id": 1, "name": "token1"}, ...]).
            - If failed, contains an error message (e.g., {"error": "Project not found"}).

    Raises:
        ValueError: If project_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_project_deploy_tokens(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234"
        ... )
        >>> print(response)
        [{"id": 1, "name": "token1"}, ...]
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_project_deploy_tokens(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_project_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    token_id: int,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific deploy token for a GitLab project.

    This function queries the GitLab API to fetch details for a specified deploy token in a project.
    It returns a dictionary containing the token details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
        >>> response = get_project_deploy_token(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     token_id=1
        ... )
        >>> print(response)
        {"id": 1, "name": "token1"}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_project_deploy_token(project_id=project_id, token=token_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
async def create_project_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    name: str,
    scopes: List[str],
    expires_at: Optional[str] = None,
    username: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a deploy token for a GitLab project with specified name and scopes.

    This function creates a new deploy token for the specified project and provides progress updates via ctx if available.
    It returns a dictionary containing the token details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
            - If successful, contains token details (e.g., {"id": 1, "name": "token1", "token": "..."}).
            - If failed, contains an error message (e.g., {"error": "Invalid scopes"}).

    Raises:
        ValueError: If project_id, name, or scopes is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = await create_project_deploy_token(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     name="deploy-token",
        ...     scopes=["read_repository"]
        ... )
        >>> print(response)
        {"id": 1, "name": "deploy-token", "token": "..."}
    """
    if ctx:
        await ctx.info(f"Creating deploy token '{name}' for project {project_id}")
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify", "project_id", "ctx"]}
    response = client.create_project_deploy_token(project_id=project_id, **kwargs)
    if ctx:
        await ctx.info("Deploy token created")
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
async def delete_project_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    project_id: str,
    token_id: int,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Delete a specific deploy token for a GitLab project.

    This function deletes a specified deploy token from a project and provides progress updates via ctx if available.
    It returns a dictionary containing the result or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
        >>> response = await delete_project_deploy_token(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     project_id="1234",
        ...     token_id=1
        ... )
        >>> print(response)
        {"status": "success"}
    """
    if ctx:
        await ctx.info(f"Deleting deploy token {token_id} for project {project_id}")
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.delete_project_deploy_token(project_id=project_id, token=token_id)
    if ctx:
        await ctx.info("Deploy token deleted")
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_group_deploy_tokens(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str,
    verify: bool = False,
) -> dict:
    """Retrieve a list of deploy tokens for a specific GitLab group.

    This function queries the GitLab API to fetch deploy tokens for a specified group.
    It returns a dictionary containing the token list or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
            If None, the default token configured in gitlab_api is used.
        group_id (str): The ID or path of the GitLab group (e.g., "1234" or "group/subgroup").
        verify (bool, optional): Whether to verify the SSL certificate of the GitLab instance.
            Defaults to False (no verification).

    Returns:
        dict: A dictionary containing the API response.
            - If successful, contains a list of deploy tokens (e.g., [{"id": 1, "name": "token1"}, ...]).
            - If failed, contains an error message (e.g., {"error": "Group not found"}).

    Raises:
        ValueError: If group_id is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = get_group_deploy_tokens(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     group_id="1234"
        ... )
        >>> print(response)
        [{"id": 1, "name": "token1"}, ...]
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_group_deploy_tokens(**kwargs)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
def get_group_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str,
    token_id: int,
    verify: bool = False,
) -> dict:
    """Retrieve details of a specific deploy token for a GitLab group.

    This function queries the GitLab API to fetch details for a specified deploy token in a group.
    It returns a dictionary containing the token details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
        >>> response = get_group_deploy_token(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     group_id="1234",
        ...     token_id=1
        ... )
        >>> print(response)
        {"id": 1, "name": "token1"}
    """
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab_instance", "access_token", "verify"]}
    response = client.get_group_deploy_token(group_id=group_id, token=token_id)
    return response.data if isinstance(response, Response) else {"error": str(response)}

@mcp.tool()
async def create_group_deploy_token(
    gitlab_instance: str = None,
    access_token: str = None,
    group_id: str,
    name: str,
    scopes: List[str],
    expires_at: Optional[str] = None,
    username: Optional[str] = None,
    verify: bool = False,
    ctx: Optional[Context] = None,
) -> dict:
    """Create a deploy token for a GitLab group with specified name and scopes.

    This function creates a new deploy token for the specified group and provides progress updates via ctx if available.
    It returns a dictionary containing the token details or an error message if the request fails.

    Args:
        gitlab_instance (str, optional): The URL of the GitLab instance (e.g., "https://gitlab.com").
            If None, the default instance configured in gitlab_api is used.
        access_token (str, optional): The GitLab personal access token for authentication.
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
            - If successful, contains token details (e.g., {"id": 1, "name": "token1", "token": "..."}).
            - If failed, contains an error message (e.g., {"error": "Invalid scopes"}).

    Raises:
        ValueError: If group_id, name, or scopes is missing or invalid.
        RuntimeError: If the GitLab API request fails due to network issues, authentication errors, or other API-related failures.

    Example:
        >>> response = await create_group_deploy_token(
        ...     gitlab_instance="https://gitlab.com",
        ...     access_token="your_token",
        ...     group_id="1234",
        ...     name="group-token",
        ...     scopes=["read_repository"]
        ... )
        >>> print(response)
        {"id": 1, "name": "group-token", "token": "..."}
    """
    if ctx:
        await ctx.info(f"Creating deploy token '{name}' for group {group_id}")
    client = gitlab_api.Api(
        url=gitlab_instance,
        token=access_token,
        verify=verify,
    )
    kwargs = {k: v for k, v in locals().items() if v is not None and k not in ["client", "gitlab
