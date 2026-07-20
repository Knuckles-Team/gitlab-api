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
    DeployTokenModel,
    ProjectModel,
    ReleaseModel,
)
from gitlab_api.gitlab_response_models import (
    DeployToken,
    Environment,
    Release,
    Response,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiEnvironments(GitLabApiBase):
    def get_deploy_tokens(self, **kwargs) -> Response:
        """
        Get all deploy tokens.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of DeployToken models.

        Raises:
            ParameterError: If the request fails or returns invalid data.
        """
        deploy_token = DeployTokenModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/deploy_tokens",
                model=deploy_token,
                id_field=None,
                id_value=None,
            )
            parsed_data = [DeployToken(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get deploy tokens: {type(e).__name__}") from e

    def get_environments(self, **kwargs) -> Response:
        """
        Get a list of environments for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Environment models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/environments",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Environment(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_environment(self, **kwargs) -> Response:
        """
        Get details of a specific environment.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.environment_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}/environments/{project.environment_id}",
                headers=self.headers,
                params=project.api_parameters,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_environment(self, **kwargs) -> Response:
        """
        Create a new environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/environments",
                headers=self.headers,
                json=project.data,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_environment(self, **kwargs) -> Response:
        """
        Update an existing environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.environment_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/environments/{project.environment_id}",
                headers=self.headers,
                json=project.data,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_environment(self, **kwargs) -> Response:
        """
        Delete an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.environment_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/environments/{project.environment_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def stop_environment(self, **kwargs) -> Response:
        """
        Stop an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.environment_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/environments/{project.environment_id}/stop",
                headers=self.headers,
                params=project.api_parameters,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def stop_stale_environments(self, **kwargs) -> Response:
        """
        Stop stale environments for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/environments/stop_stale",
                headers=self.headers,
                params=project.api_parameters,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_stopped_environments(self, **kwargs) -> Response:
        """
        Delete stopped environments (review apps) for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/environments/review_apps",
                headers=self.headers,
                params=project.api_parameters,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_protected_environments(self, **kwargs) -> Response:
        """
        Get a list of protected environments for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Environment models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/protected_environments",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Environment(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_protected_environment(self, **kwargs) -> Response:
        """
        Get details of a specific protected environment.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.name is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}/protected_environments/{project.name}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def protect_environment(self, **kwargs) -> Response:
        """
        Protect an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/protected_environments",
                headers=self.headers,
                json=project.data,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_protected_environment(self, **kwargs) -> Response:
        """
        Update a protected environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/protected_environments/{project.name}",
                headers=self.headers,
                json=project.data,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def unprotect_environment(self, **kwargs) -> Response:
        """
        Unprotect an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/protected_environments/{project.name}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_releases(self, **kwargs) -> Response:
        """
        Get information about releases in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Release models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{release.project_id}/releases",
                model=release,
                id_field="project_id",
                id_value=release.project_id,
            )
            parsed_data = [Release(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_latest_release(self, **kwargs) -> Response:
        """
        Get information about the latest release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{release.project_id}/releases/permalink/latest",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Release(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_latest_release_evidence(self, **kwargs) -> Response:
        """
        Get evidence for the latest release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and the raw evidence data.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{release.project_id}/releases/permalink/latest/evidence",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_latest_release_asset(self, **kwargs) -> Response:
        """
        Get the asset for the latest release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, direct_asset_path).

        Returns:
            Response: A wrapper containing the original response and the raw asset data.

        Raises:
            MissingParameterError: If the project_id or direct_asset_path is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.direct_asset_path is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{release.project_id}/releases/permalink/latest/{release.direct_asset_path}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.content
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def download_release_asset(self, **kwargs) -> Response:
        """
        Download a release asset from a group's release.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, tag_name, direct_asset_path).

        Returns:
            Response: A wrapper containing the original response and the raw asset data.

        Raises:
            MissingParameterError: If the group_id, tag_name, or direct_asset_path is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if (
            release.group_id is None
            or release.tag_name is None
            or release.direct_asset_path is None
        ):
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/groups/{release.group_id}/releases/{release.tag_name}/downloads/{release.direct_asset_path}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.content
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_release(self, **kwargs) -> Response:
        """
        Create a new release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.tag_name is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{release.project_id}/releases",
                json=release.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Release(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_release_evidence(self, **kwargs) -> Response:
        """
        Create evidence for a release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.tag_name is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{release.project_id}/releases/{release.tag_name}/evidence",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_release(self, **kwargs) -> Response:
        """
        Update information about a release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.tag_name is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{release.project_id}/releases/{release.tag_name}",
                json=release.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Release(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_release(self, **kwargs) -> Response:
        """
        Delete a release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.project_id is None or release.tag_name is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{release.project_id}/releases/{release.tag_name}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
