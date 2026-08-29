from unittest.mock import Mock

import pytest

from gitlab_api.gitlab_gql import (
    GraphQL,
    _reject_unsupported_graphql_parameters,
)


@pytest.fixture
def graphql_client() -> GraphQL:
    """Build an authenticated client without constructing a network transport."""
    client = object.__new__(GraphQL)
    client.headers = {"Authorization": "Bearer test"}
    client.execute_gql = Mock(return_value={})
    return client


@pytest.mark.parametrize(
    ("method_name", "kwargs", "expected_parameters"),
    [
        (
            "get_branches",
            {"project_id": "group/project", "_regex": "release"},
            ("_regex",),
        ),
        (
            "delete_branch",
            {
                "project_id": "group/project",
                "branch": "release",
                "_delete_merged_branches": True,
            },
            ("_delete_merged_branches",),
        ),
        (
            "protect_branch",
            {
                "project_id": "group/project",
                "branch": "release",
                "push_access_level": "maintainer",
                "merge_access_level": "maintainer",
                "unprotect_access_level": "maintainer",
            },
            ("push_access_level", "merge_access_level", "unprotect_access_level"),
        ),
        (
            "get_tags",
            {"project_id": "group/project", "sort": "name_asc"},
            ("sort",),
        ),
        (
            "protect_tag",
            {
                "project_id": "group/project",
                "name": "v1",
                "_create_access_level": "maintainer",
                "_allowed_to_create": [{"user_id": 1}],
            },
            ("_create_access_level", "_allowed_to_create"),
        ),
        (
            "get_commits",
            {
                "project_id": "group/project",
                "path": "src/app.py",
                "_author": "alice",
                "since": "2026-01-01",
                "until": "2026-01-31",
                "all": True,
                "with_stats": True,
            },
            ("path", "_author", "since", "until", "all", "with_stats"),
        ),
        (
            "create_commit",
            {
                "project_id": "group/project",
                "branch": "main",
                "message": "update",
                "actions": [],
                "_start_branch": "base",
                "_start_sha": "abc123",
                "_start_project": "group/base",
                "_stats": True,
                "force": True,
            },
            ("_start_branch", "_start_sha", "_start_project", "_stats", "force"),
        ),
        (
            "get_merge_requests",
            {
                "project_id": "group/project",
                "labels": ["security"],
                "milestone": "v1",
                "author_username": "alice",
                "reviewer_username": "bob",
                "source_branch": "feature",
                "target_branch": "main",
                "search": "security",
            },
            (
                "labels",
                "milestone",
                "author_username",
                "reviewer_username",
                "source_branch",
                "target_branch",
                "search",
            ),
        ),
        (
            "create_merge_request",
            {
                "project_id": "group/project",
                "source_branch": "feature",
                "target_branch": "main",
                "title": "Security update",
                "_milestone_id": 1,
            },
            ("_milestone_id",),
        ),
        (
            "get_pipelines",
            {
                "project_id": "group/project",
                "ref": "main",
                "status": "success",
                "_source": "push",
                "username": "alice",
                "updated_after": "2026-01-01",
                "updated_before": "2026-01-31",
                "order_by": "updated_at",
                "sort": "desc",
            },
            (
                "ref",
                "status",
                "_source",
                "username",
                "updated_after",
                "updated_before",
                "order_by",
                "sort",
            ),
        ),
        (
            "get_jobs",
            {"project_id": "group/project", "scope": ["pending"]},
            ("scope",),
        ),
        (
            "get_packages",
            {
                "project_id": "group/project",
                "_package_type": "npm",
                "package_name": "web-ui",
            },
            ("_package_type", "package_name"),
        ),
        ("get_users", {"username": "alice"}, ("username",)),
        (
            "get_members",
            {
                "project_id": "group/project",
                "_include_inherited": True,
                "search": "alice",
            },
            ("_include_inherited", "search"),
        ),
        (
            "get_issues",
            {
                "project_id": "group/project",
                "milestone": "v1",
                "author_username": "alice",
            },
            ("milestone", "author_username"),
        ),
        ("get_to_dos", {"project_id": "group/project"}, ("project_id",)),
    ],
)
def test_graphql_rejects_unsupported_values(
    graphql_client: GraphQL,
    method_name: str,
    kwargs: dict[str, object],
    expected_parameters: tuple[str, ...],
) -> None:
    with pytest.raises(ValueError, match=r"REST API") as exc_info:
        getattr(graphql_client, method_name)(**kwargs)

    assert "GraphQL does not support" in str(exc_info.value)
    for parameter in expected_parameters:
        assert f"`{parameter}`" in str(exc_info.value)
    graphql_client.execute_gql.assert_not_called()


def test_graphql_unsupported_defaults_remain_noops() -> None:
    _reject_unsupported_graphql_parameters(
        _regex=None,
        _delete_merged_branches=False,
        push_access_level=None,
        labels=[],
        path="",
        _author=None,
        all=False,
        _start_project=None,
        force=False,
        ref=None,
        scope=[],
        project_id=None,
    )


def test_graphql_default_calls_still_execute(graphql_client: GraphQL) -> None:
    graphql_client.get_commits(project_id="group/project")
    graphql_client.get_pipelines(project_id="group/project")

    assert graphql_client.execute_gql.call_count == 2
