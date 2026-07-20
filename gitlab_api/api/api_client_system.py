#!/usr/bin/python

from typing import Any

from agent_utilities.base_utilities import get_logger
from pydantic import ValidationError

logger = get_logger(__name__)

from agent_utilities.core.exceptions import (
    ParameterError,
)

from gitlab_api.api.api_client_base import GitLabApiBase
from gitlab_api.gitlab_response_models import (
    Response,
)


class GitLabApiSystem(GitLabApiBase):
    def api_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Response:
        """
        Make a custom API request to the GitLab server.

        Args:
            method: The HTTP method to use (GET, POST, PUT, DELETE).
            endpoint: The API endpoint to call.
            data: The data to send in the request body (for form data).
            json: The JSON data to send in the request body.

        Returns:
            Response: A wrapper containing the original response and the response data (if applicable).

        Raises:
            ValueError: If an unsupported HTTP method is provided.
            ParameterError: If invalid parameters are provided.
            HTTPError: If the API request fails.
        """
        if method.upper() not in ["GET", "POST", "PUT", "DELETE"]:
            raise ValueError(f"Unsupported HTTP method: {method.upper()}")
        try:
            request_func = getattr(self._session, method.lower())
            response = request_func(
                url=f"{self.url}/{endpoint.lstrip('/')}",
                headers=self.headers,
                data=data,
                json=json,
            )
            response.raise_for_status()
            parsed_data = (
                response.json()
                if response.content
                and "application/json" in response.headers.get("Content-Type", "")
                else None
            )
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except Exception as e:
            logger.error("GitLab request failed: error_type=%s", type(e).__name__)
            raise
