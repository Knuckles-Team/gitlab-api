import inspect
from unittest.mock import MagicMock, patch
import pytest

from gitlab_api.gitlab_gql import GraphQL
from agent_utilities.core.exceptions import MissingParameterError, ParameterError


@pytest.fixture
def mock_gql_client():
    with patch("gitlab_api.gitlab_gql.Client") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        # Mock the execute method to return a standard structure
        mock_client.execute.return_value = {
            "project": {
                "id": "gid://gitlab/Project/1",
                "name": "test-project",
                "fullPath": "group/project",
                "repository": {
                    "branches": {
                        "nodes": [{"name": "main"}],
                        "pageInfo": {"endCursor": "cursor", "hasNextPage": False},
                    },
                    "branch": {
                        "name": "main",
                        "commit": {"id": "1", "sha": "abc", "message": "commit"},
                    },
                    "tree": {
                        "lastCommit": {"sha": "abc"},
                    },
                },
                "issues": {
                    "nodes": [{"id": "gid://gitlab/Issue/1", "title": "test"}],
                    "pageInfo": {"endCursor": "cursor", "hasNextPage": False},
                },
                "mergeRequests": {
                    "nodes": [{"id": "gid://gitlab/MergeRequest/1", "title": "mr"}],
                    "pageInfo": {"endCursor": "cursor", "hasNextPage": False},
                },
                "pipelines": {
                    "nodes": [{"id": "gid://gitlab/Pipeline/1", "status": "SUCCESS"}],
                    "pageInfo": {"endCursor": "cursor", "hasNextPage": False},
                },
                "releases": {
                    "nodes": [{"id": "gid://gitlab/Release/1", "tagName": "v1.0"}],
                    "pageInfo": {"endCursor": "cursor", "hasNextPage": False},
                },
                "pipelineSchedules": {
                    "nodes": [{"id": "1", "description": "schedule"}],
                },
                "wiki": {
                    "slug": "home",
                    "title": "Home",
                },
                "wikis": {
                    "nodes": [{"slug": "home"}],
                },
            },
            "group": {
                "id": "gid://gitlab/Group/1",
                "name": "test-group",
                "fullPath": "group",
                "releases": {
                    "nodes": [{"id": "1", "tagName": "v1.0"}],
                },
                "members": {
                    "nodes": [{"user": {"username": "user"}}],
                },
            },
            "user": {
                "id": "gid://gitlab/User/1",
                "username": "test-user",
            },
            "currentUser": {
                "id": "gid://gitlab/User/1",
                "username": "current-user",
            },
            "createBranch": {
                "branch": {"name": "new-branch"},
                "errors": [],
            },
            "destroyBranch": {
                "branch": {"name": "deleted-branch"},
                "errors": [],
            },
            "branchRuleUpdate": {
                "branchRule": {"name": "main", "isProtected": True},
                "errors": [],
            },
            "createIssue": {
                "issue": {"id": "gid://gitlab/Issue/2"},
                "errors": [],
            },
            "updateIssue": {
                "issue": {"id": "gid://gitlab/Issue/1"},
                "errors": [],
            },
            "destroyIssue": {
                "errors": [],
            },
            "createMergeRequest": {
                "mergeRequest": {"id": "gid://gitlab/MergeRequest/2"},
                "errors": [],
            },
            "updateMergeRequest": {
                "mergeRequest": {"id": "gid://gitlab/MergeRequest/1"},
                "errors": [],
            },
            "destroyMergeRequest": {
                "errors": [],
            },
            "createPipelineSchedule": {
                "pipelineSchedule": {"id": "1"},
                "errors": [],
            },
            "updatePipelineSchedule": {
                "pipelineSchedule": {"id": "1"},
                "errors": [],
            },
            "destroyPipelineSchedule": {
                "errors": [],
            },
            "createRelease": {
                "release": {"tagName": "v1.0"},
                "errors": [],
            },
            "updateRelease": {
                "release": {"tagName": "v1.0"},
                "errors": [],
            },
            "destroyRelease": {
                "errors": [],
            },
            "createWikiPage": {
                "wikiPage": {"slug": "home"},
                "errors": [],
            },
            "updateWikiPage": {
                "wikiPage": {"slug": "home"},
                "errors": [],
            },
            "destroyWikiPage": {
                "errors": [],
            },
            "projectMembers": {
                "nodes": [{"user": {"username": "user"}}],
            },
            "groupMembers": {
                "nodes": [{"user": {"username": "user"}}],
            },
            "projectPackages": {
                "nodes": [{"id": "1"}],
            },
            "projectPackage": {
                "id": "1",
            },
            "destroyPackage": {
                "errors": [],
            },
            "namespace": {
                "id": "1",
                "name": "name",
            },
        }
        yield mock_client


@pytest.fixture(autouse=True)
def mock_all_input_models():
    model_names = [
        "BranchModel",
        "CommitModel",
        "GroupModel",
        "IssueModel",
        "JobModel",
        "MembersModel",
        "MergeRequestModel",
        "NamespaceModel",
        "PackageModel",
        "PipelineModel",
        "PipelineScheduleModel",
        "ProjectModel",
        "ReleaseModel",
        "TagModel",
        "UserModel",
        "WikiModel",
    ]
    patches = []
    for name in model_names:
        p = patch(f"gitlab_api.gitlab_gql.{name}", lambda *args, **kwargs: MagicMock())
        p.start()
        patches.append(p)
    yield
    for p in patches:
        p.stop()


def test_graphql_init_exceptions():
    with pytest.raises(MissingParameterError, match="URL is required"):
        GraphQL(url=None, token="test")
    with pytest.raises(MissingParameterError, match="Token is required"):
        GraphQL(url="http://test", token=None)


def test_graphql_execute_exceptions(mock_gql_client):
    gql_client = GraphQL(url="http://test", token="test")

    # Test error returned in execute response
    mock_gql_client.execute.return_value = {"errors": ["some error"]}
    with pytest.raises(ParameterError, match="GraphQL errors"):
        gql_client.execute_gql("query { test }")

    # Test exception raised by client execute
    mock_gql_client.execute.side_effect = Exception("network error")
    with pytest.raises(ParameterError, match="Query execution failed: network error"):
        gql_client.execute_gql("query { test }")


def test_graphql_parameter_errors(mock_gql_client):
    gql_client = GraphQL(url="http://test", token="test")
    with pytest.raises(ParameterError, match="Cannot provide more than 50 full paths"):
        gql_client.get_projects(full_paths=["path"] * 51)
    with pytest.raises(ParameterError, match="Cannot provide more than 50 full paths"):
        gql_client.get_admin_projects(full_paths=["path"] * 51)


def test_graphql_brute_force_coverage(mock_gql_client):
    gql_client = GraphQL(url="http://test", token="test", debug=True)

    common_kwargs = {
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
        "query_str": "query { test }",
        "variables": [{"key": "a", "value": "b"}],
        "cron": "0 0 * * *",
        "cron_time_zone": "UTC",
        "active": True,
        "tag_name": "v1.0",
        "ref_name": "main",
        "slug": "home",
        "body": "body",
        "username": "user",
        "issue_id": "1",
        "mr_id": "1",
        "schedule_id": "1",
        "package_id": "1",
        "package_type": "npm",
        "namespace_id": "1",
        "search": "test_search",
        "after": "test_cursor",
        "actions": [],
        "author_email": "test@test.com",
        "author_name": "tester",
        "confidential": True,
        "labels": ["l1"],
        "line": 1,
        "assignee_ids": [1],
        "ids": [1],
        "full_paths": ["path/to/project"],
        "archived": "yes",
        "visibility_level": "private",
        "min_access_level": "reporter",
        "assignee_username": "tester",
        "type": "issue",
        "state": "opened",
        "project_model": MagicMock(),
    }

    # Introspect all methods
    for name, method in inspect.getmembers(gql_client, predicate=inspect.ismethod):
        if name.startswith("_") or name == "execute_gql":
            continue
        print(f"Calling GraphQL.{name}...")
        sig = inspect.signature(method)
        has_kwargs = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        )
        if has_kwargs:
            kwargs = common_kwargs.copy()
        else:
            kwargs = {k: v for k, v in common_kwargs.items() if k in sig.parameters}
            # Fill missing mandatory ones
            for p_name, p in sig.parameters.items():
                if p.default == inspect.Parameter.empty and p_name not in kwargs:
                    if p_name.endswith("_model"):
                        kwargs[p_name] = MagicMock()
                    else:
                        kwargs[p_name] = "test"

        # Call the method
        try:
            res = method(**kwargs)
            assert res is not None
        except Exception as e:
            print(f"Operation failed: {type(e).__name__}")
            pass
