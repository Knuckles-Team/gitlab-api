from unittest.mock import patch

import pytest
from agent_connector_sdk.auth.delegation import DelegationSettings
from agent_connector_sdk.auth.tokens import AccessToken
from requests import Response

from gitlab_api.auth import get_client, get_graphql_client

_DELEGATION_SETTINGS = DelegationSettings(
    enabled=True,
    token_endpoint="https://idp.example/token",
    client_id="gitlab-api",
    client_secret_ref="env://GITLAB_OIDC_CLIENT_SECRET",
    audience="https://gitlab.com",
    scopes="api",
)


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
    fake_token = AccessToken("delegated_tok", 300.0, 0.0)
    with (
        patch.object(
            DelegationSettings, "from_settings", return_value=_DELEGATION_SETTINGS
        ),
        patch("gitlab_api.auth.current_user_token", return_value="user-token"),
        patch("gitlab_api.auth.exchange_token", return_value=fake_token),
    ):
        client = get_client(instance="http://gitlab.com", token=None)
        assert client.headers is not None
        assert client.headers["Authorization"] == "Bearer delegated_tok"


def test_get_client_oidc_delegation_failed():
    with (
        patch.object(
            DelegationSettings, "from_settings", return_value=_DELEGATION_SETTINGS
        ),
        patch("gitlab_api.auth.current_user_token", return_value="user-token"),
        patch(
            "gitlab_api.auth.exchange_token",
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
    fake_token = AccessToken("delegated_tok", 300.0, 0.0)
    with (
        patch.object(
            DelegationSettings, "from_settings", return_value=_DELEGATION_SETTINGS
        ),
        patch("gitlab_api.auth.current_user_token", return_value="user-token"),
        patch("gitlab_api.auth.exchange_token", return_value=fake_token),
    ):
        gql_client = get_graphql_client(instance="http://gitlab.com", token=None)
        assert gql_client.token == "delegated_tok"


def test_get_graphql_client_oidc_delegation_failed():
    with (
        patch.object(
            DelegationSettings, "from_settings", return_value=_DELEGATION_SETTINGS
        ),
        patch("gitlab_api.auth.current_user_token", return_value="user-token"),
        patch(
            "gitlab_api.auth.exchange_token",
            side_effect=Exception("Exchange failed"),
        ),
    ):
        with pytest.raises(RuntimeError, match="Token exchange failed"):
            get_graphql_client(instance="http://gitlab.com", token=None)
