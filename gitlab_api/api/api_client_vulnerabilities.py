#!/usr/bin/python

from typing import TypeVar

import requests
from agent_utilities.base_utilities import get_logger
from pydantic import ValidationError

logger = get_logger(__name__)

from agent_utilities.core.exceptions import (
    MissingParameterError,
    ParameterError,
)

from gitlab_api.gitlab_input_models import (
    VulnerabilityModel,
)
from gitlab_api.gitlab_response_models import (
    Response,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiVulnerabilities(GitLabApiBase):
    """Dependency list + security vulnerability surface — the GitLab counterpart
    to GitHub's Dependabot (Dependency List, Vulnerabilities, and findings APIs)."""

    def get_project_dependencies(self, **kwargs) -> Response:
        """
        Get a project's Dependency List (all detected dependencies).

        GET /projects/{project_id}/dependencies

        Args:
            **kwargs: project_id (required); optional package_manager filter and
                pagination (page, per_page, max_pages).

        Returns:
            Response: wrapper containing the original response and the parsed
                dependency list (list of dicts).

        Raises:
            MissingParameterError: If project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        vulnerability = VulnerabilityModel(**kwargs)
        if vulnerability.project_id is None:
            raise MissingParameterError("project_id is required")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{vulnerability.project_id}/dependencies",
                model=vulnerability,
                id_field="project_id",
                id_value=vulnerability.project_id,
            )
            return Response(response=response, data=data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get project dependencies: {str(e)}") from e

    def get_project_vulnerabilities(self, **kwargs) -> Response:
        """
        Get a project's security vulnerabilities (Ultimate).

        GET /projects/{project_id}/vulnerabilities

        Args:
            **kwargs: project_id (required); optional pagination.

        Returns:
            Response: wrapper containing the original response and the parsed
                vulnerabilities (list of dicts).

        Raises:
            MissingParameterError: If project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        vulnerability = VulnerabilityModel(**kwargs)
        if vulnerability.project_id is None:
            raise MissingParameterError("project_id is required")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{vulnerability.project_id}/vulnerabilities",
                model=vulnerability,
                id_field="project_id",
                id_value=vulnerability.project_id,
            )
            return Response(response=response, data=data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to get project vulnerabilities: {str(e)}"
            ) from e

    def get_group_vulnerabilities(self, **kwargs) -> Response:
        """
        Get a group's security vulnerability findings (Ultimate).

        GET /groups/{group_id}/vulnerability_findings

        Args:
            **kwargs: group_id (required); optional pagination.

        Returns:
            Response: wrapper containing the original response and the parsed
                vulnerability findings (list of dicts).

        Raises:
            MissingParameterError: If group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        vulnerability = VulnerabilityModel(**kwargs)
        if vulnerability.group_id is None:
            raise MissingParameterError("group_id is required")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{vulnerability.group_id}/vulnerability_findings",
                model=vulnerability,
                id_field="group_id",
                id_value=vulnerability.group_id,
            )
            return Response(response=response, data=data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to get group vulnerabilities: {str(e)}"
            ) from e

    def get_vulnerability(self, **kwargs) -> Response:
        """
        Get a single vulnerability by its global ID (Ultimate).

        GET /vulnerabilities/{vulnerability_id}

        Args:
            **kwargs: vulnerability_id (required).

        Returns:
            Response: wrapper containing the original response and the parsed
                vulnerability (dict).

        Raises:
            MissingParameterError: If vulnerability_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        vulnerability = VulnerabilityModel(**kwargs)
        if vulnerability.vulnerability_id is None:
            raise MissingParameterError("vulnerability_id is required")
        try:
            response = self._session.get(
                url=f"{self.url}/vulnerabilities/{vulnerability.vulnerability_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response, data=response.json())
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get vulnerability: {str(e)}") from e
