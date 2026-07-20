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
    GroupModel,
    MembersModel,
    MergeRequestRuleSettingsModel,
    NamespaceModel,
    ReleaseModel,
    UserModel,
)
from gitlab_api.gitlab_response_models import (
    DeployToken,
    Group,
    Membership,
    MergeRequestRuleSettings,
    Namespace,
    Release,
    Response,
    User,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiUsersGroups(GitLabApiBase):
    def get_group_deploy_tokens(self, **kwargs) -> Response:
        """
        Get deploy tokens for a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of DeployToken models.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.group_id is None:
            raise MissingParameterError("group_id is required")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{deploy_token.group_id}/deploy_tokens",
                model=deploy_token,
                id_field="group_id",
                id_value=deploy_token.group_id,
            )
            parsed_data = [DeployToken(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get group deploy tokens: {type(e).__name__}") from e

    def get_group_deploy_token(self, **kwargs) -> Response:
        """
        Get a specific deploy token for a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, deploy_token_id).

        Returns:
            Response: A wrapper containing the original response and a DeployToken model.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.group_id is None or deploy_token.deploy_token_id is None:  # type: ignore
            raise MissingParameterError("group_id and deploy_token_id are required")
        try:
            response = self._session.get(
                url=f"{self.url}/groups/{deploy_token.group_id}/deploy_tokens/{deploy_token.deploy_token_id}",  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = DeployToken(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(f"Failed to get group deploy token: {type(e).__name__}") from e

    def create_group_deploy_token(self, **kwargs) -> Response:
        """
        Create a deploy token for a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, name, scopes).

        Returns:
            Response: A wrapper containing the original response and a DeployToken model.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if (
            deploy_token.group_id is None
            or deploy_token.name is None
            or deploy_token.scopes is None
        ):
            raise MissingParameterError("group_id, name, and scopes are required")
        try:
            response = self._session.post(
                url=f"{self.url}/groups/{deploy_token.group_id}/deploy_tokens",
                headers=self.headers,
                json=deploy_token.model_dump(exclude_none=True),
            )
            response.raise_for_status()
            parsed_data = DeployToken(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to create group deploy token: {type(e).__name__}"
            ) from e

    def delete_group_deploy_token(self, **kwargs) -> Response:
        """
        Delete a deploy token for a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, deploy_token_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        deploy_token = DeployTokenModel(**kwargs)
        if deploy_token.group_id is None or deploy_token.deploy_token_id is None:  # type: ignore
            raise MissingParameterError("group_id and deploy_token_id are required")
        try:
            response = self._session.delete(
                url=f"{self.url}/groups/{deploy_token.group_id}/deploy_tokens/{deploy_token.deploy_token_id}",  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to delete group deploy token: {type(e).__name__}"
            ) from e

    def get_groups(self, **kwargs) -> Response:
        """
        Get a list of groups.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Group models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/groups",
                model=group,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Group(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_group(self, **kwargs) -> Response:
        """
        Get details of a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a Group model.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/groups/{group.group_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Group(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def edit_group(self, **kwargs) -> Response:
        """
        Edit a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a Group model.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/groups/{group.group_id}",
                json=group.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Group(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_group_subgroups(self, **kwargs) -> Response:
        """
        Get subgroups of a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Group models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint="/groups/{id}/subgroups",
                model=group,
                id_field="group_id",
                id_value=group.group_id,
            )
            parsed_data = [Group(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_group_descendant_groups(self, **kwargs) -> Response:
        """
        Get descendant groups of a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Group models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        group = GroupModel(**kwargs)
        if group.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint="/groups/{id}/descendant_groups",
                model=group,
                id_field="group_id",
                id_value=group.group_id,
            )
            parsed_data = [Group(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_group_members(self, **kwargs) -> Response:
        """
        Get members of a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Membership models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        members = MembersModel(**kwargs)
        if members.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{members.group_id}/members",
                model=members,
                id_field="group_id",
                id_value=members.group_id,
            )
            parsed_data = [Membership(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_group_level_rule(self, **kwargs) -> Response:
        """
        Get details of a group-level merge request approval setting.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a MergeRequestRuleSettings model.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule_setting = MergeRequestRuleSettingsModel(**kwargs)
        if merge_rule_setting.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/groups/{merge_rule_setting.group_id}/merge_request_approval_setting",
                headers=self.headers,
                params=merge_rule_setting.api_parameters,
            )
            response.raise_for_status()
            parsed_data = MergeRequestRuleSettings(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def edit_group_level_rule(self, **kwargs) -> Response:
        """
        Edit a group-level merge request approval setting.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a MergeRequestRuleSettings model.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        merge_rule_setting = MergeRequestRuleSettingsModel(**kwargs)
        if merge_rule_setting.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/groups/{merge_rule_setting.group_id}/merge_request_approval_setting",
                headers=self.headers,
                json=merge_rule_setting.data,
            )
            response.raise_for_status()
            parsed_data = MergeRequestRuleSettings(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_group_releases(self, **kwargs) -> Response:
        """
        Get information about releases in a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Release models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        release = ReleaseModel(**kwargs)
        if release.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{release.group_id}/releases",
                model=release,
                id_field="group_id",
                id_value=release.group_id,
            )
            parsed_data = [Release(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_users(self, **kwargs) -> Response:
        """
        Get information about users.

        Args:
            **kwargs: Additional parameters for the request (e.g., per_page, page).

        Returns:
            Response: A wrapper containing the original response and a list of User models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        user = UserModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/users",
                model=user,
                id_field=None,
                id_value=None,
            )
            parsed_data = [User(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_user(self, **kwargs) -> Response:
        """
        Get information about a specific user.

        Args:
            **kwargs: Additional parameters for the request (e.g., user_id).

        Returns:
            Response: A wrapper containing the original response and a User model.

        Raises:
            MissingParameterError: If the user_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        user = UserModel(**kwargs)
        if user.user_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/users/{user.user_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = User(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_namespaces(self, **kwargs) -> Response:
        """
        Get information about namespaces.

        Args:
            **kwargs: Additional parameters for the request (e.g., per_page).

        Returns:
            Response: A wrapper containing the original response and a list of Namespace models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        namespace = NamespaceModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/namespaces",
                model=namespace,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Namespace(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_namespace(self, **kwargs) -> Response:
        """
        Get information about a specific namespace.

        Args:
            **kwargs: Additional parameters for the request (e.g., namespace_id).

        Returns:
            Response: A wrapper containing the original response and a Namespace model.

        Raises:
            MissingParameterError: If the namespace_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        namespace = NamespaceModel(**kwargs)
        if namespace.namespace_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/namespaces/{namespace.namespace_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Namespace(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_user(self, **kwargs) -> Response:
        """
        Create a new user.
        """
        user = UserModel(**kwargs)
        if (
            user.email is None
            or user.password is None
            or user.username is None
            or user.name is None
        ):
            raise MissingParameterError(
                "Missing required parameters for user creation (email, password, username, name)"
            )
        try:
            response = self._session.post(
                url=f"{self.url}/users",
                json=user.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = User(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_user(self, **kwargs) -> Response:
        """
        Update an existing user.
        """
        user = UserModel(**kwargs)
        if user.user_id is None:
            raise MissingParameterError("Missing user_id")
        try:
            response = self._session.put(
                url=f"{self.url}/users/{user.user_id}",
                json=user.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = User(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_user(self, **kwargs) -> Response:
        """
        Delete a user.
        """
        user = UserModel(**kwargs)
        if user.user_id is None:
            raise MissingParameterError("Missing user_id")
        try:
            response = self._session.delete(
                url=f"{self.url}/users/{user.user_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response, data=None)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
