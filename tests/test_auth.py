from unittest.mock import patch

import pytest
from requests import Response

from gitlab_api.auth import get_client, get_graphql_client


def test_get_client_fixed_credentials():
    client = get_client(instance="http://gitlab.com", token="valid_token")
    assert client.url == "http://gitlab.com/api/v4"


def test_get_client_auth_error():
    mock_response = Response()
    mock_response.status_code = 401
    mock_response._content = b"Unauthorized"
    with patch("requests.Session.get", return_value=mock_response):
        with pytest.raises(RuntimeError, match="AUTHENTICATION ERROR"):
            get_client(instance="http://gitlab.com", token="bad_token")


def test_get_client_oidc_delegation():
    with (
        patch(
            "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
            return_value=True,
        ),
        patch(
            "agent_utilities.mcp.delegated_auth.get_delegated_token",
            return_value="delegated_tok",
        ),
    ):
        client = get_client(
            instance="http://gitlab.com", token=None, config={"some": "config"}
        )
        assert client.headers is not None
        assert client.headers["Authorization"] == "Bearer delegated_tok"


def test_get_client_oidc_delegation_failed():
    with (
        patch(
            "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
            return_value=True,
        ),
        patch(
            "agent_utilities.mcp.delegated_auth.get_delegated_token",
            side_effect=Exception("Exchange failed"),
        ),
    ):
        with pytest.raises(RuntimeError, match="Token exchange failed"):
            get_client(instance="http://gitlab.com", token=None)


def test_get_graphql_client_fixed_credentials():
    gql_client = get_graphql_client(instance="http://gitlab.com", token="valid_token")
    assert gql_client.url == "http://gitlab.com/api/graphql"


def test_get_graphql_client_missing_token():
    with pytest.raises(
        RuntimeError, match="GITLAB_TOKEN environment variable or parameter is missing."
    ):
        get_graphql_client(instance="http://gitlab.com", token=None)


def test_get_graphql_client_oidc_delegation():
    with (
        patch(
            "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
            return_value=True,
        ),
        patch(
            "agent_utilities.mcp.delegated_auth.get_delegated_token",
            return_value="delegated_tok",
        ),
    ):
        gql_client = get_graphql_client(
            instance="http://gitlab.com", token=None, config={"some": "config"}
        )
        assert gql_client.token == "delegated_tok"


def test_get_graphql_client_oidc_delegation_failed():
    with (
        patch(
            "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
            return_value=True,
        ),
        patch(
            "agent_utilities.mcp.delegated_auth.get_delegated_token",
            side_effect=Exception("Exchange failed"),
        ),
    ):
        with pytest.raises(RuntimeError, match="Token exchange failed"):
            get_graphql_client(instance="http://gitlab.com", token=None)
