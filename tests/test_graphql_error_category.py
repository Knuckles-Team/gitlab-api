"""GraphQL failures reach the caller as typed errors, without server text."""

from __future__ import annotations

from typing import Any

import pytest
from gql.transport.exceptions import TransportQueryError
from scion_sdk.transports.graphql import GraphQLExecutionError

from gitlab_api.gitlab_gql import GraphQL

_SERVER_TEXT = "private-gitlab-text for group/secret-project"


class _Fake:
    def __init__(self, outcome: Exception | dict[str, Any]) -> None:
        self.outcome = outcome

    def execute(self, *args: object, **kwargs: object) -> dict[str, Any]:
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self.outcome


def _graphql(outcome: Exception | dict[str, Any]) -> GraphQL:
    api = GraphQL(url="https://gitlab.example.invalid", token="synthetic-token")
    api.client._client = _Fake(outcome)
    api.client.max_retries = 0
    return api


def _update(api: GraphQL) -> dict[str, Any]:
    return api.update_merge_request("group/project", 999, title="new title")


@pytest.mark.spec("CONN-GITLAB-API-R006.1")
@pytest.mark.parametrize(
    ("message", "category"),
    [
        (
            "The resource that you are attempting to access does not exist "
            f"or you don't have permission to perform this action {_SERVER_TEXT}",
            "not_found",
        ),
        (f"You are forbidden to do that {_SERVER_TEXT}", "forbidden"),
        (f"Variable $input of type is invalid {_SERVER_TEXT}", "invalid_input"),
        (f"something else {_SERVER_TEXT}", "unknown"),
    ],
)
def test_missing_merge_request_update_is_not_found_without_server_text(
    message: str, category: str
) -> None:
    api = _graphql(TransportQueryError(message, errors=[{"message": message}]))
    with pytest.raises(GraphQLExecutionError) as caught:
        _update(api)
    error = caught.value
    assert error.category == category
    assert str(error) == f"Query execution failed: TransportQueryError ({category})"
    assert error.payload()["retryable"] is False
    assert _SERVER_TEXT not in str(error.payload()) + str(error)


@pytest.mark.spec("CONN-GITLAB-API-R006.1")
def test_mutation_errors_list_raises_invalid_input() -> None:
    api = _graphql(
        {"mergeRequestUpdate": {"mergeRequest": None, "errors": [_SERVER_TEXT]}}
    )
    with pytest.raises(GraphQLExecutionError) as caught:
        _update(api)
    assert caught.value.category == "invalid_input"
    assert _SERVER_TEXT not in str(caught.value.payload())


@pytest.mark.spec("CONN-GITLAB-API-R006.1")
def test_successful_update_returns_the_payload() -> None:
    ok = {"mergeRequestUpdate": {"mergeRequest": {"iid": "1"}, "errors": []}}
    assert _update(_graphql(ok)) == ok
