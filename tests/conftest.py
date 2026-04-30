from unittest.mock import patch

import pytest
from dotenv import load_dotenv

# Use a reason variable for skipped tests
reason = "Unit tests using mocks"


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("GITLAB_URL", "http://test.gitlab.com")
    monkeypatch.setenv("GITLAB_TOKEN", "mock_token")


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(autouse=True)
def mock_requests():
    def mock_side_effect(*args, **kwargs):
        import json

        from requests import Response

        mock_response = Response()
        mock_response.status_code = 200
        url = kwargs.get("url", "")

        # Determine if it should be a list or a dict
        if any(
            url.endswith(x)
            for x in [
                "/jobs",
                "/pipelines",
                "/releases",
                "/projects",
                "/groups",
                "/members",
            ]
        ):
            data: list[dict[str, object]] | dict[str, object] = [{"id": 1, "name": "test"}]  # Return at least one item with ID
        elif "/projects?" in url or "/groups?" in url:
            data = [{"id": 1, "name": "test"}]
        else:
            # For objects, try to echo back passed data
            data = kwargs.get("json", {})
            if not data:
                data = {"id": 1, "name": "test"}

        mock_response._content = json.dumps(data).encode("utf-8")
        mock_response.headers["X-Total-Pages"] = "1"
        return mock_response

    with (
        patch("requests.Session.get", side_effect=mock_side_effect) as mock_get,
        patch("requests.Session.post", side_effect=mock_side_effect) as mock_post,
        patch("requests.Session.delete", side_effect=mock_side_effect) as mock_delete,
        patch("requests.Session.put", side_effect=mock_side_effect) as mock_put,
    ):
        yield {
            "get": mock_get,
            "post": mock_post,
            "delete": mock_delete,
            "put": mock_put,
        }
