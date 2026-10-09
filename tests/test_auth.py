from unittest.mock import patch

import pytest
from requests import Response

from gitlab_api.auth import get_client, get_graphql_client

_DELEGATION_SETTINGS_ENV = {
    "ENABLE_DELEGATION": "true",
    "OIDC_TOKEN_URL": "https://idp.example.invalid/token",
    "OIDC_CLIENT_ID": "gitlab-connector",
    "OIDC_CLIENT_SECRET_REF": "env://TEST_GITLAB_OIDC_SECRET_UNUSED",
    "AUDIENCE": "https://gitlab.example.invalid",
}


def _set_delegation_settings_env(monkeypatch) -> None:
    for key, value in _DELEGATION_SETTINGS_ENV.items():
        monkeypatch.setenv(key, value)


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


def test_get_client_oidc_delegation(monkeypatch):
    """Delegation path: exchange_token's return becomes the client's bearer token."""
    _set_delegation_settings_env(monkeypatch)

    import agent_connector_sdk.auth.delegation as delegation
    from agent_connector_sdk.auth.tokens import AccessToken

    monkeypatch.setattr(delegation, "current_user_token", lambda: "caller-token")
    monkeypatch.setattr(
        delegation,
        "exchange_token",
        lambda settings, *, subject_token, http_client, resolver=None: AccessToken(
            value="delegated_tok", ttl_seconds=3600, expires_at=0.0
        ),
    )

    client = get_client(
        instance="http://gitlab.com", token=None, config={"enable_delegation": True}
    )
    assert client.headers is not None
    assert client.headers["Authorization"] == "Bearer delegated_tok"


def test_get_client_oidc_delegation_failed(monkeypatch):
    _set_delegation_settings_env(monkeypatch)

    import agent_connector_sdk.auth.delegation as delegation

    monkeypatch.setattr(delegation, "current_user_token", lambda: "caller-token")

    def _boom(settings, *, subject_token, http_client, resolver=None):
        raise ValueError("Exchange failed")

    monkeypatch.setattr(delegation, "exchange_token", _boom)

    with pytest.raises(RuntimeError, match="Token exchange failed"):
        get_client(
            instance="http://gitlab.com",
            token=None,
            config={"enable_delegation": True},
        )


def test_get_graphql_client_fixed_credentials():
    gql_client = get_graphql_client(instance="http://gitlab.com", token="valid_token")
    assert gql_client.url == "http://gitlab.com/api/graphql"


def test_get_graphql_client_missing_token():
    with pytest.raises(
        RuntimeError, match="GITLAB_TOKEN environment variable or parameter is missing."
    ):
        get_graphql_client(instance="http://gitlab.com", token=None)


def test_get_graphql_client_oidc_delegation(monkeypatch):
    _set_delegation_settings_env(monkeypatch)

    import agent_connector_sdk.auth.delegation as delegation
    from agent_connector_sdk.auth.tokens import AccessToken

    monkeypatch.setattr(delegation, "current_user_token", lambda: "caller-token")
    monkeypatch.setattr(
        delegation,
        "exchange_token",
        lambda settings, *, subject_token, http_client, resolver=None: AccessToken(
            value="delegated_tok", ttl_seconds=3600, expires_at=0.0
        ),
    )

    gql_client = get_graphql_client(
        instance="http://gitlab.com", token=None, config={"enable_delegation": True}
    )
    assert gql_client.token == "delegated_tok"


def test_get_graphql_client_oidc_delegation_failed(monkeypatch):
    _set_delegation_settings_env(monkeypatch)

    import agent_connector_sdk.auth.delegation as delegation

    monkeypatch.setattr(delegation, "current_user_token", lambda: "caller-token")

    def _boom(settings, *, subject_token, http_client, resolver=None):
        raise ValueError("Exchange failed")

    monkeypatch.setattr(delegation, "exchange_token", _boom)

    with pytest.raises(RuntimeError, match="Token exchange failed"):
        get_graphql_client(
            instance="http://gitlab.com",
            token=None,
            config={"enable_delegation": True},
        )
