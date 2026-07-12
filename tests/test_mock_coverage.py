import sys
import logging
import inspect
from unittest.mock import MagicMock, patch
import pytest
import requests
from pydantic import ValidationError

from gitlab_api.api_client import Api
from agent_utilities.core.exceptions import (
    AuthError,
    MissingParameterError,
    ParameterError,
    UnauthorizedError,
)
import gitlab_api
from gitlab_api.gitlab_input_models import ProjectModel, CommitModel
from gitlab_api.mcp_server import get_mcp_instance


def test_init_getattr_and_availability():
    # Test __dir__
    dir_list = dir(gitlab_api)
    assert "Api" in dir_list

    # Test dynamic attributes
    assert gitlab_api._MCP_AVAILABLE is True
    assert gitlab_api._AGENT_AVAILABLE is True

    # Test custom import failure inside __getattr__
    with patch("gitlab_api._import_module_safely", return_value=None):
        # We temporarily mock OPTIONAL_MODULES to trigger alternative paths
        with patch.dict(
            "gitlab_api.OPTIONAL_MODULES", {"gitlab_api.mcp_server": "mcp"}
        ):
            # Test __getattr__ for unknown attributes
            with pytest.raises(AttributeError, match="has no attribute"):
                _ = gitlab_api.non_existent_attribute


def test_client_initialization_variations():
    # 1. Debug enabled
    client_debug = Api(url="http://gitlab.com", token="tok", debug=True)
    assert client_debug.debug is True

    # 2. Missing URL
    with pytest.raises(MissingParameterError):
        Api(url=None, token="tok")

    # 3. Missing credentials
    with pytest.raises(MissingParameterError):
        Api(url="http://gitlab.com", token=None)

    # 4. Basic authentication (username & password)
    mock_auth_resp = requests.Response()
    mock_auth_resp.status_code = 200
    with patch("requests.Session.get", return_value=mock_auth_resp):
        client_basic = Api(url="http://gitlab.com", username="user", password="pwd")
        assert client_basic.headers is not None
        assert "Authorization" in client_basic.headers
        assert client_basic.headers["Authorization"].startswith("Basic ")

    # 5. Switch parallel headers
    client_parallel = Api(url="http://gitlab.com", tokens=["tok1", "tok2"])
    assert client_parallel.headers is not None
    assert client_parallel.headers["Authorization"] == "Bearer tok1"
    assert client_parallel.switch_to_next_headers() is True
    assert client_parallel.headers is not None
    assert client_parallel.headers["Authorization"] == "Bearer tok2"
    assert client_parallel.switch_to_next_headers() is True
    assert client_parallel.headers is not None
    assert client_parallel.headers["Authorization"] == "Bearer tok1"

    # Switch headers when no parallel headers exist
    client_single = Api(url="http://gitlab.com", token="tok")
    assert client_single.switch_to_next_headers() is False


def test_api_client_error_status_codes():
    # Mock real requests.Response objects
    r_401 = requests.Response()
    r_401.status_code = 401
    r_401._content = b"Unauthorized access"

    r_403 = requests.Response()
    r_403.status_code = 403
    r_403._content = b"Forbidden access"

    r_404 = requests.Response()
    r_404.status_code = 404
    r_404._content = b"Not found"

    with patch("requests.Session.get", return_value=r_401):
        with pytest.raises(AuthError):
            Api(url="http://gitlab.com", token="tok")

    with patch("requests.Session.get", return_value=r_403):
        with pytest.raises(UnauthorizedError):
            Api(url="http://gitlab.com", token="tok")

    with patch("requests.Session.get", return_value=r_404):
        with pytest.raises(ParameterError):
            Api(url="http://gitlab.com", token="tok")


def test_paginated_fetching_and_fallbacks():
    client = Api(url="http://gitlab.com", token="tok")

    # 1. Fetching single page with non-list response (fallback to empty list)
    resp_dict = requests.Response()
    resp_dict.status_code = 200
    resp_dict._content = b'{"error": "not a list"}'
    with patch("requests.Session.get", return_value=resp_dict):
        model = ProjectModel(owned=True)
        res = client._fetch_next_page("/projects", model, {}, 1)
        assert res == []

    # 2. Multi-page pagination loop
    from requests.structures import CaseInsensitiveDict

    resp_page_1 = requests.Response()
    resp_page_1.status_code = 200
    resp_page_1._content = b'[{"id": 1}, {"id": 2}]'
    resp_page_1.headers = CaseInsensitiveDict(
        {"X-Next-Page": "2", "X-Total-Pages": "2"}
    )

    resp_page_2 = requests.Response()
    resp_page_2.status_code = 200
    resp_page_2._content = b'[{"id": 3}]'
    resp_page_2.headers = CaseInsensitiveDict({"X-Next-Page": "", "X-Total-Pages": "2"})

    page_counter = 0

    def mock_get(*args, **kwargs):
        nonlocal page_counter
        page_counter += 1
        if page_counter == 1:
            return resp_page_1
        return resp_page_2

    with patch("requests.Session.get", side_effect=mock_get):
        model = ProjectModel(owned=True)
        resp_obj, data_list = client._fetch_all_pages("/projects", model)
        assert len(data_list) == 3
        assert data_list[0]["id"] == 1
        assert data_list[2]["id"] == 3


def test_pagination_limits_and_ranges():
    client = Api(url="http://gitlab.com", token="tok")
    from requests.structures import CaseInsensitiveDict

    # Test case 1: total_pages = 15, max_pages default (None). It should fetch min(15, 10) = 10 pages.
    call_count_1 = 0
    requested_pages_1 = []

    def side_effect_get_1(url, params=None, **kwargs):
        nonlocal call_count_1
        call_count_1 += 1
        page_val = params.get("page", 1) if params else 1
        requested_pages_1.append(page_val)
        r = requests.Response()
        r.status_code = 200
        r._content = b'[{"id": 999}]'
        if call_count_1 == 1:
            r.headers = CaseInsensitiveDict({"X-Next-Page": "2", "X-Total-Pages": "15"})
            r._content = b'[{"id": 1}]'
        return r

    with patch("requests.Session.get", side_effect=side_effect_get_1):
        model = ProjectModel(owned=True)
        model.max_pages = None
        resp_obj, data_list = client._fetch_all_pages("/projects", model)
        assert model.max_pages == 10
        assert sorted(requested_pages_1) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Test case 2: total_pages = 15, max_pages explicitly set to 4. It should fetch exactly 4 pages.
    call_count_2 = 0
    requested_pages_2 = []

    def side_effect_get_2(url, params=None, **kwargs):
        nonlocal call_count_2
        call_count_2 += 1
        page_val = params.get("page", 1) if params else 1
        requested_pages_2.append(page_val)
        r = requests.Response()
        r.status_code = 200
        r._content = b'[{"id": 999}]'
        if call_count_2 == 1:
            r.headers = CaseInsensitiveDict({"X-Next-Page": "2", "X-Total-Pages": "15"})
            r._content = b'[{"id": 1}]'
        return r

    with patch("requests.Session.get", side_effect=side_effect_get_2):
        model = ProjectModel(owned=True)
        model.max_pages = 4
        resp_obj, data_list = client._fetch_all_pages("/projects", model)
        assert model.max_pages == 4
        assert sorted(requested_pages_2) == [1, 2, 3, 4]


def test_input_model_validation_failures():
    # Test validate_bool_fields with invalid input
    with pytest.raises(ValidationError):
        # Stats must be a bool, so passing a string should fail on CommitModel
        CommitModel(project_id="123", stats="invalid_bool")  # type: ignore

    # Test passing invalid parameters to trigger parameter error in CRUD functions
    client = Api(url="http://gitlab.com", token="tok")
    # For instance, get_project with invalid args
    mock_resp = requests.Response()
    mock_resp.status_code = 200
    mock_resp._content = b'[{"id": "not_an_int"}]'
    with patch("requests.Session.get", return_value=mock_resp):
        with pytest.raises(ParameterError):
            client.get_projects(owned=True)


def test_get_merge_requests_empty_response_returns_empty_list():
    """Regression test: listing merge requests with no project id (or any
    other filter) must not raise a MergeRequestModel validation error when
    GitLab returns a non-list / empty-shaped body such as ``{}`` or
    ``{"data": {}}``. It should return an empty list instead of attempting
    to validate the response as a single MergeRequestModel/MergeRequest.
    """
    client = Api(url="http://gitlab.com", token="tok")

    # GitLab-style non-list response body for a global (no project) MR list.
    mock_resp = requests.Response()
    mock_resp.status_code = 200
    mock_resp._content = b'{"data": {}}'
    with patch("requests.Session.get", return_value=mock_resp):
        response = client.get_merge_requests()
        assert response.data == []

    # Plain empty dict body should behave the same way.
    mock_resp_empty = requests.Response()
    mock_resp_empty.status_code = 200
    mock_resp_empty._content = b"{}"
    with patch("requests.Session.get", return_value=mock_resp_empty):
        response = client.get_project_merge_requests(project_id=1)
        assert response.data == []


def test_agent_server_cli_execution():
    from gitlab_api.agent_server import agent_server

    # Set up argparse mock and create_agent_server mock
    mock_args = MagicMock()
    mock_args.debug = True
    mock_args.mcp_url = "http://localhost:8000"
    mock_args.mcp_config = "mcp_config.json"
    mock_args.host = "127.0.0.1"
    mock_args.port = 8000
    mock_args.provider = "openai"
    mock_args.model_id = "gpt-4o"
    mock_args.base_url = None
    mock_args.api_key = None
    mock_args.custom_skills_directory = None
    mock_args.web = False
    mock_args.otel = False

    with (
        patch("argparse.ArgumentParser.parse_args", return_value=mock_args),
        patch("agent_utilities.create_agent_server") as mock_create_server,
        patch("agent_utilities.initialize_workspace"),
        patch("agent_utilities.load_identity") as mock_identity,
    ):
        mock_identity.return_value = {"name": "Test GitLab Agent"}
        agent_server()
        mock_create_server.assert_called_once()


@pytest.mark.anyio
async def test_mcp_server_graphql_exception():
    # Initialize FastMCP instance
    mcp, _, _, _ = get_mcp_instance()

    # Get the graphql tool handler using list_tools API
    tool_objs = (
        await mcp.list_tools()
        if inspect.iscoroutinefunction(mcp.list_tools)
        else mcp.list_tools()
    )
    graphql_tool = None
    for tool in tool_objs:
        if tool.name == "gitlab_graphql":
            graphql_tool = tool
            break

    assert graphql_tool is not None

    # Call it, but mock client.execute_gql to raise an exception
    mock_client = MagicMock()
    mock_client.execute_gql.side_effect = Exception("Internal GraphQL Error")

    with patch("gitlab_api.auth.get_graphql_client", return_value=mock_client):
        # Run the tool's handler with explicit parameters to avoid Pydantic Field default objects
        result = await graphql_tool.fn(
            query="{ query }",
            variables="{}",
            operation_name=None,
            client=mock_client,
            ctx=None,
        )
        assert "error" in result
        assert "Internal GraphQL Error" in result["error"]


@pytest.mark.anyio
async def test_archive_unarchive_methods_and_mcp():
    # 1. Test Api.archive_project and Api.unarchive_project methods
    client = Api(url="http://gitlab.com", token="tok")

    mock_resp = requests.Response()
    mock_resp.status_code = 200
    mock_resp._content = b'{"id": 123, "name": "archived-project", "archived": true}'

    with patch("requests.Session.post", return_value=mock_resp) as mock_post:
        res = client.archive_project(project_id=123)
        project = res.data
        assert project is not None
        assert not isinstance(project, list)
        assert project.archived is True
        assert project.id == 123
        mock_post.assert_called_once()
        assert (
            mock_post.call_args.kwargs["url"]
            == "http://gitlab.com/api/v4/projects/123/archive"
        )
        assert mock_post.call_args.kwargs["headers"] == client.headers

    mock_resp_un = requests.Response()
    mock_resp_un.status_code = 200
    mock_resp_un._content = (
        b'{"id": 123, "name": "archived-project", "archived": false}'
    )

    with patch("requests.Session.post", return_value=mock_resp_un) as mock_post:
        res = client.unarchive_project(project_id=123)
        project = res.data
        assert project is not None
        assert not isinstance(project, list)
        assert project.archived is False
        assert project.id == 123
        mock_post.assert_called_once()
        assert (
            mock_post.call_args.kwargs["url"]
            == "http://gitlab.com/api/v4/projects/123/unarchive"
        )
        assert mock_post.call_args.kwargs["headers"] == client.headers

    # 2. Test the FastMCP tool for gitlab_projects archive/unarchive actions
    mcp, _, _, _ = get_mcp_instance()
    tool_objs = (
        await mcp.list_tools()
        if inspect.iscoroutinefunction(mcp.list_tools)
        else mcp.list_tools()
    )

    projects_tool = None
    for tool in tool_objs:
        if tool.name == "gitlab_projects":
            projects_tool = tool
            break

    assert projects_tool is not None

    mock_client = MagicMock()
    mock_client.archive_project.return_value = {
        "status": "success",
        "action": "archive",
    }
    mock_client.unarchive_project.return_value = {
        "status": "success",
        "action": "unarchive",
    }

    # Test action="archive"
    res_archive = await projects_tool.fn(
        action="archive",
        params_json='{"project_id": 123}',
        client=mock_client,
        ctx=None,
    )
    assert res_archive == {"status": "success", "action": "archive"}
    mock_client.archive_project.assert_called_once_with(project_id=123)

    # Test action="unarchive"
    res_unarchive = await projects_tool.fn(
        action="unarchive",
        params_json='{"project_id": 123}',
        client=mock_client,
        ctx=None,
    )
    assert res_unarchive == {"status": "success", "action": "unarchive"}
    mock_client.unarchive_project.assert_called_once_with(project_id=123)
