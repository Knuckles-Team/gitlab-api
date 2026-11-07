#!/usr/bin/python

import logging
from typing import Any, TypeVar

import requests
from pydantic import ValidationError

logger = logging.getLogger(__name__)

from scion_sdk.exceptions import (
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
    CreatedDeployToken,
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
    def get_group_deploy_tokens(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        token: str | None = None,
        name: str | None = None,
        expires_at: str | None = None,
        username: str | None = None,
        scopes: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "token": token,
                "name": name,
                "expires_at": expires_at,
                "username": username,
                "scopes": scopes,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
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
            raise ParameterError(
                f"Failed to get group deploy tokens: {type(e).__name__}"
            ) from e

    def get_group_deploy_token(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        token: str | None = None,
        name: str | None = None,
        expires_at: str | None = None,
        username: str | None = None,
        scopes: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "token": token,
                "name": name,
                "expires_at": expires_at,
                "username": username,
                "scopes": scopes,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
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
            raise ParameterError(
                f"Failed to get group deploy token: {type(e).__name__}"
            ) from e

    def create_group_deploy_token(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        token: str | None = None,
        name: str | None = None,
        expires_at: str | None = None,
        username: str | None = None,
        scopes: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Create a deploy token for a group.

        Returns a secret: the new token string is returned once, at creation, and never
        by any read call. Store it now.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, name, scopes).

        Returns:
            Response: A wrapper containing the original response and a DeployToken model.

        Raises:
            ParameterError: If invalid parameters are provided.
            MissingParameterError: If required parameters are missing.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "token": token,
                "name": name,
                "expires_at": expires_at,
                "username": username,
                "scopes": scopes,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
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
            parsed_data = CreatedDeployToken(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to create group deploy token: {type(e).__name__}"
            ) from e

    def delete_group_deploy_token(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        token: str | None = None,
        name: str | None = None,
        expires_at: str | None = None,
        username: str | None = None,
        scopes: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "token": token,
                "name": name,
                "expires_at": expires_at,
                "username": username,
                "scopes": scopes,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
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

    def get_groups(
        self,
        *,
        group_id: int | str | None = None,
        name: str | None = None,
        path: str | None = None,
        auto_devops_enabled: bool | None = None,
        avatar: Any = None,
        default_branch: str | None = None,
        default_branch_protection: int | None = None,
        default_branch_protection_defaults: dict[str, Any] | None = None,
        description: str | None = None,
        enabled_git_access_protocol: str | None = None,
        emails_enabled: bool | None = None,
        lfs_enabled: bool | None = None,
        mentions_disabled: bool | None = None,
        prevent_sharing_groups_outside_hierarchy: bool | None = None,
        project_creation_level: str | None = None,
        request_access_enabled: bool | None = None,
        require_two_factor_authentication: bool | None = None,
        shared_runners_setting: str | None = None,
        share_with_group_lock: bool | None = None,
        subgroup_creation_level: str | None = None,
        two_factor_grace_period: int | None = None,
        visibility: str | None = None,
        extra_shared_runners_minutes_limit: int | None = None,
        file_template_project_id: int | str | None = None,
        membership_lock: bool | None = None,
        prevent_forking_outside_group: bool | None = None,
        shared_runners_minutes_limit: int | None = None,
        unique_project_download_limit: int | None = None,
        unique_project_download_limit_interval_in_seconds: int | None = None,
        unique_project_download_limit_allowlist: list[str] | None = None,
        unique_project_download_limit_alertlist: list[int] | None = None,
        auto_ban_user_on_excessive_projects_download: bool | None = None,
        ip_restriction_ranges: str | None = None,
        allowed_email_domains_list: str | None = None,
        wiki_access_level: str | None = None,
        math_rendering_limits_enabled: bool | None = None,
        lock_math_rendering_limits_enabled: bool | None = None,
        duo_features_enabled: bool | None = None,
        lock_duo_features_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        argument: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get a list of groups.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Group models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "group_id": group_id,
                "name": name,
                "path": path,
                "auto_devops_enabled": auto_devops_enabled,
                "avatar": avatar,
                "default_branch": default_branch,
                "default_branch_protection": default_branch_protection,
                "default_branch_protection_defaults": default_branch_protection_defaults,
                "description": description,
                "enabled_git_access_protocol": enabled_git_access_protocol,
                "emails_enabled": emails_enabled,
                "lfs_enabled": lfs_enabled,
                "mentions_disabled": mentions_disabled,
                "prevent_sharing_groups_outside_hierarchy": prevent_sharing_groups_outside_hierarchy,
                "project_creation_level": project_creation_level,
                "request_access_enabled": request_access_enabled,
                "require_two_factor_authentication": require_two_factor_authentication,
                "shared_runners_setting": shared_runners_setting,
                "share_with_group_lock": share_with_group_lock,
                "subgroup_creation_level": subgroup_creation_level,
                "two_factor_grace_period": two_factor_grace_period,
                "visibility": visibility,
                "extra_shared_runners_minutes_limit": extra_shared_runners_minutes_limit,
                "file_template_project_id": file_template_project_id,
                "membership_lock": membership_lock,
                "prevent_forking_outside_group": prevent_forking_outside_group,
                "shared_runners_minutes_limit": shared_runners_minutes_limit,
                "unique_project_download_limit": unique_project_download_limit,
                "unique_project_download_limit_interval_in_seconds": unique_project_download_limit_interval_in_seconds,
                "unique_project_download_limit_allowlist": unique_project_download_limit_allowlist,
                "unique_project_download_limit_alertlist": unique_project_download_limit_alertlist,
                "auto_ban_user_on_excessive_projects_download": auto_ban_user_on_excessive_projects_download,
                "ip_restriction_ranges": ip_restriction_ranges,
                "allowed_email_domains_list": allowed_email_domains_list,
                "wiki_access_level": wiki_access_level,
                "math_rendering_limits_enabled": math_rendering_limits_enabled,
                "lock_math_rendering_limits_enabled": lock_math_rendering_limits_enabled,
                "duo_features_enabled": duo_features_enabled,
                "lock_duo_features_enabled": lock_duo_features_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "argument": argument,
                "data": data,
            }.items()
            if v is not None
        }
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

    def get_group(
        self,
        *,
        group_id: int | str | None = None,
        name: str | None = None,
        path: str | None = None,
        auto_devops_enabled: bool | None = None,
        avatar: Any = None,
        default_branch: str | None = None,
        default_branch_protection: int | None = None,
        default_branch_protection_defaults: dict[str, Any] | None = None,
        description: str | None = None,
        enabled_git_access_protocol: str | None = None,
        emails_enabled: bool | None = None,
        lfs_enabled: bool | None = None,
        mentions_disabled: bool | None = None,
        prevent_sharing_groups_outside_hierarchy: bool | None = None,
        project_creation_level: str | None = None,
        request_access_enabled: bool | None = None,
        require_two_factor_authentication: bool | None = None,
        shared_runners_setting: str | None = None,
        share_with_group_lock: bool | None = None,
        subgroup_creation_level: str | None = None,
        two_factor_grace_period: int | None = None,
        visibility: str | None = None,
        extra_shared_runners_minutes_limit: int | None = None,
        file_template_project_id: int | str | None = None,
        membership_lock: bool | None = None,
        prevent_forking_outside_group: bool | None = None,
        shared_runners_minutes_limit: int | None = None,
        unique_project_download_limit: int | None = None,
        unique_project_download_limit_interval_in_seconds: int | None = None,
        unique_project_download_limit_allowlist: list[str] | None = None,
        unique_project_download_limit_alertlist: list[int] | None = None,
        auto_ban_user_on_excessive_projects_download: bool | None = None,
        ip_restriction_ranges: str | None = None,
        allowed_email_domains_list: str | None = None,
        wiki_access_level: str | None = None,
        math_rendering_limits_enabled: bool | None = None,
        lock_math_rendering_limits_enabled: bool | None = None,
        duo_features_enabled: bool | None = None,
        lock_duo_features_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        argument: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "group_id": group_id,
                "name": name,
                "path": path,
                "auto_devops_enabled": auto_devops_enabled,
                "avatar": avatar,
                "default_branch": default_branch,
                "default_branch_protection": default_branch_protection,
                "default_branch_protection_defaults": default_branch_protection_defaults,
                "description": description,
                "enabled_git_access_protocol": enabled_git_access_protocol,
                "emails_enabled": emails_enabled,
                "lfs_enabled": lfs_enabled,
                "mentions_disabled": mentions_disabled,
                "prevent_sharing_groups_outside_hierarchy": prevent_sharing_groups_outside_hierarchy,
                "project_creation_level": project_creation_level,
                "request_access_enabled": request_access_enabled,
                "require_two_factor_authentication": require_two_factor_authentication,
                "shared_runners_setting": shared_runners_setting,
                "share_with_group_lock": share_with_group_lock,
                "subgroup_creation_level": subgroup_creation_level,
                "two_factor_grace_period": two_factor_grace_period,
                "visibility": visibility,
                "extra_shared_runners_minutes_limit": extra_shared_runners_minutes_limit,
                "file_template_project_id": file_template_project_id,
                "membership_lock": membership_lock,
                "prevent_forking_outside_group": prevent_forking_outside_group,
                "shared_runners_minutes_limit": shared_runners_minutes_limit,
                "unique_project_download_limit": unique_project_download_limit,
                "unique_project_download_limit_interval_in_seconds": unique_project_download_limit_interval_in_seconds,
                "unique_project_download_limit_allowlist": unique_project_download_limit_allowlist,
                "unique_project_download_limit_alertlist": unique_project_download_limit_alertlist,
                "auto_ban_user_on_excessive_projects_download": auto_ban_user_on_excessive_projects_download,
                "ip_restriction_ranges": ip_restriction_ranges,
                "allowed_email_domains_list": allowed_email_domains_list,
                "wiki_access_level": wiki_access_level,
                "math_rendering_limits_enabled": math_rendering_limits_enabled,
                "lock_math_rendering_limits_enabled": lock_math_rendering_limits_enabled,
                "duo_features_enabled": duo_features_enabled,
                "lock_duo_features_enabled": lock_duo_features_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "argument": argument,
                "data": data,
            }.items()
            if v is not None
        }
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

    def edit_group(
        self,
        *,
        group_id: int | str | None = None,
        name: str | None = None,
        path: str | None = None,
        auto_devops_enabled: bool | None = None,
        avatar: Any = None,
        default_branch: str | None = None,
        default_branch_protection: int | None = None,
        default_branch_protection_defaults: dict[str, Any] | None = None,
        description: str | None = None,
        enabled_git_access_protocol: str | None = None,
        emails_enabled: bool | None = None,
        lfs_enabled: bool | None = None,
        mentions_disabled: bool | None = None,
        prevent_sharing_groups_outside_hierarchy: bool | None = None,
        project_creation_level: str | None = None,
        request_access_enabled: bool | None = None,
        require_two_factor_authentication: bool | None = None,
        shared_runners_setting: str | None = None,
        share_with_group_lock: bool | None = None,
        subgroup_creation_level: str | None = None,
        two_factor_grace_period: int | None = None,
        visibility: str | None = None,
        extra_shared_runners_minutes_limit: int | None = None,
        file_template_project_id: int | str | None = None,
        membership_lock: bool | None = None,
        prevent_forking_outside_group: bool | None = None,
        shared_runners_minutes_limit: int | None = None,
        unique_project_download_limit: int | None = None,
        unique_project_download_limit_interval_in_seconds: int | None = None,
        unique_project_download_limit_allowlist: list[str] | None = None,
        unique_project_download_limit_alertlist: list[int] | None = None,
        auto_ban_user_on_excessive_projects_download: bool | None = None,
        ip_restriction_ranges: str | None = None,
        allowed_email_domains_list: str | None = None,
        wiki_access_level: str | None = None,
        math_rendering_limits_enabled: bool | None = None,
        lock_math_rendering_limits_enabled: bool | None = None,
        duo_features_enabled: bool | None = None,
        lock_duo_features_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        argument: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "group_id": group_id,
                "name": name,
                "path": path,
                "auto_devops_enabled": auto_devops_enabled,
                "avatar": avatar,
                "default_branch": default_branch,
                "default_branch_protection": default_branch_protection,
                "default_branch_protection_defaults": default_branch_protection_defaults,
                "description": description,
                "enabled_git_access_protocol": enabled_git_access_protocol,
                "emails_enabled": emails_enabled,
                "lfs_enabled": lfs_enabled,
                "mentions_disabled": mentions_disabled,
                "prevent_sharing_groups_outside_hierarchy": prevent_sharing_groups_outside_hierarchy,
                "project_creation_level": project_creation_level,
                "request_access_enabled": request_access_enabled,
                "require_two_factor_authentication": require_two_factor_authentication,
                "shared_runners_setting": shared_runners_setting,
                "share_with_group_lock": share_with_group_lock,
                "subgroup_creation_level": subgroup_creation_level,
                "two_factor_grace_period": two_factor_grace_period,
                "visibility": visibility,
                "extra_shared_runners_minutes_limit": extra_shared_runners_minutes_limit,
                "file_template_project_id": file_template_project_id,
                "membership_lock": membership_lock,
                "prevent_forking_outside_group": prevent_forking_outside_group,
                "shared_runners_minutes_limit": shared_runners_minutes_limit,
                "unique_project_download_limit": unique_project_download_limit,
                "unique_project_download_limit_interval_in_seconds": unique_project_download_limit_interval_in_seconds,
                "unique_project_download_limit_allowlist": unique_project_download_limit_allowlist,
                "unique_project_download_limit_alertlist": unique_project_download_limit_alertlist,
                "auto_ban_user_on_excessive_projects_download": auto_ban_user_on_excessive_projects_download,
                "ip_restriction_ranges": ip_restriction_ranges,
                "allowed_email_domains_list": allowed_email_domains_list,
                "wiki_access_level": wiki_access_level,
                "math_rendering_limits_enabled": math_rendering_limits_enabled,
                "lock_math_rendering_limits_enabled": lock_math_rendering_limits_enabled,
                "duo_features_enabled": duo_features_enabled,
                "lock_duo_features_enabled": lock_duo_features_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "argument": argument,
                "data": data,
            }.items()
            if v is not None
        }
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

    def get_group_subgroups(
        self,
        *,
        group_id: int | str | None = None,
        name: str | None = None,
        path: str | None = None,
        auto_devops_enabled: bool | None = None,
        avatar: Any = None,
        default_branch: str | None = None,
        default_branch_protection: int | None = None,
        default_branch_protection_defaults: dict[str, Any] | None = None,
        description: str | None = None,
        enabled_git_access_protocol: str | None = None,
        emails_enabled: bool | None = None,
        lfs_enabled: bool | None = None,
        mentions_disabled: bool | None = None,
        prevent_sharing_groups_outside_hierarchy: bool | None = None,
        project_creation_level: str | None = None,
        request_access_enabled: bool | None = None,
        require_two_factor_authentication: bool | None = None,
        shared_runners_setting: str | None = None,
        share_with_group_lock: bool | None = None,
        subgroup_creation_level: str | None = None,
        two_factor_grace_period: int | None = None,
        visibility: str | None = None,
        extra_shared_runners_minutes_limit: int | None = None,
        file_template_project_id: int | str | None = None,
        membership_lock: bool | None = None,
        prevent_forking_outside_group: bool | None = None,
        shared_runners_minutes_limit: int | None = None,
        unique_project_download_limit: int | None = None,
        unique_project_download_limit_interval_in_seconds: int | None = None,
        unique_project_download_limit_allowlist: list[str] | None = None,
        unique_project_download_limit_alertlist: list[int] | None = None,
        auto_ban_user_on_excessive_projects_download: bool | None = None,
        ip_restriction_ranges: str | None = None,
        allowed_email_domains_list: str | None = None,
        wiki_access_level: str | None = None,
        math_rendering_limits_enabled: bool | None = None,
        lock_math_rendering_limits_enabled: bool | None = None,
        duo_features_enabled: bool | None = None,
        lock_duo_features_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        argument: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "group_id": group_id,
                "name": name,
                "path": path,
                "auto_devops_enabled": auto_devops_enabled,
                "avatar": avatar,
                "default_branch": default_branch,
                "default_branch_protection": default_branch_protection,
                "default_branch_protection_defaults": default_branch_protection_defaults,
                "description": description,
                "enabled_git_access_protocol": enabled_git_access_protocol,
                "emails_enabled": emails_enabled,
                "lfs_enabled": lfs_enabled,
                "mentions_disabled": mentions_disabled,
                "prevent_sharing_groups_outside_hierarchy": prevent_sharing_groups_outside_hierarchy,
                "project_creation_level": project_creation_level,
                "request_access_enabled": request_access_enabled,
                "require_two_factor_authentication": require_two_factor_authentication,
                "shared_runners_setting": shared_runners_setting,
                "share_with_group_lock": share_with_group_lock,
                "subgroup_creation_level": subgroup_creation_level,
                "two_factor_grace_period": two_factor_grace_period,
                "visibility": visibility,
                "extra_shared_runners_minutes_limit": extra_shared_runners_minutes_limit,
                "file_template_project_id": file_template_project_id,
                "membership_lock": membership_lock,
                "prevent_forking_outside_group": prevent_forking_outside_group,
                "shared_runners_minutes_limit": shared_runners_minutes_limit,
                "unique_project_download_limit": unique_project_download_limit,
                "unique_project_download_limit_interval_in_seconds": unique_project_download_limit_interval_in_seconds,
                "unique_project_download_limit_allowlist": unique_project_download_limit_allowlist,
                "unique_project_download_limit_alertlist": unique_project_download_limit_alertlist,
                "auto_ban_user_on_excessive_projects_download": auto_ban_user_on_excessive_projects_download,
                "ip_restriction_ranges": ip_restriction_ranges,
                "allowed_email_domains_list": allowed_email_domains_list,
                "wiki_access_level": wiki_access_level,
                "math_rendering_limits_enabled": math_rendering_limits_enabled,
                "lock_math_rendering_limits_enabled": lock_math_rendering_limits_enabled,
                "duo_features_enabled": duo_features_enabled,
                "lock_duo_features_enabled": lock_duo_features_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "argument": argument,
                "data": data,
            }.items()
            if v is not None
        }
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

    def get_group_descendant_groups(
        self,
        *,
        group_id: int | str | None = None,
        name: str | None = None,
        path: str | None = None,
        auto_devops_enabled: bool | None = None,
        avatar: Any = None,
        default_branch: str | None = None,
        default_branch_protection: int | None = None,
        default_branch_protection_defaults: dict[str, Any] | None = None,
        description: str | None = None,
        enabled_git_access_protocol: str | None = None,
        emails_enabled: bool | None = None,
        lfs_enabled: bool | None = None,
        mentions_disabled: bool | None = None,
        prevent_sharing_groups_outside_hierarchy: bool | None = None,
        project_creation_level: str | None = None,
        request_access_enabled: bool | None = None,
        require_two_factor_authentication: bool | None = None,
        shared_runners_setting: str | None = None,
        share_with_group_lock: bool | None = None,
        subgroup_creation_level: str | None = None,
        two_factor_grace_period: int | None = None,
        visibility: str | None = None,
        extra_shared_runners_minutes_limit: int | None = None,
        file_template_project_id: int | str | None = None,
        membership_lock: bool | None = None,
        prevent_forking_outside_group: bool | None = None,
        shared_runners_minutes_limit: int | None = None,
        unique_project_download_limit: int | None = None,
        unique_project_download_limit_interval_in_seconds: int | None = None,
        unique_project_download_limit_allowlist: list[str] | None = None,
        unique_project_download_limit_alertlist: list[int] | None = None,
        auto_ban_user_on_excessive_projects_download: bool | None = None,
        ip_restriction_ranges: str | None = None,
        allowed_email_domains_list: str | None = None,
        wiki_access_level: str | None = None,
        math_rendering_limits_enabled: bool | None = None,
        lock_math_rendering_limits_enabled: bool | None = None,
        duo_features_enabled: bool | None = None,
        lock_duo_features_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        argument: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "group_id": group_id,
                "name": name,
                "path": path,
                "auto_devops_enabled": auto_devops_enabled,
                "avatar": avatar,
                "default_branch": default_branch,
                "default_branch_protection": default_branch_protection,
                "default_branch_protection_defaults": default_branch_protection_defaults,
                "description": description,
                "enabled_git_access_protocol": enabled_git_access_protocol,
                "emails_enabled": emails_enabled,
                "lfs_enabled": lfs_enabled,
                "mentions_disabled": mentions_disabled,
                "prevent_sharing_groups_outside_hierarchy": prevent_sharing_groups_outside_hierarchy,
                "project_creation_level": project_creation_level,
                "request_access_enabled": request_access_enabled,
                "require_two_factor_authentication": require_two_factor_authentication,
                "shared_runners_setting": shared_runners_setting,
                "share_with_group_lock": share_with_group_lock,
                "subgroup_creation_level": subgroup_creation_level,
                "two_factor_grace_period": two_factor_grace_period,
                "visibility": visibility,
                "extra_shared_runners_minutes_limit": extra_shared_runners_minutes_limit,
                "file_template_project_id": file_template_project_id,
                "membership_lock": membership_lock,
                "prevent_forking_outside_group": prevent_forking_outside_group,
                "shared_runners_minutes_limit": shared_runners_minutes_limit,
                "unique_project_download_limit": unique_project_download_limit,
                "unique_project_download_limit_interval_in_seconds": unique_project_download_limit_interval_in_seconds,
                "unique_project_download_limit_allowlist": unique_project_download_limit_allowlist,
                "unique_project_download_limit_alertlist": unique_project_download_limit_alertlist,
                "auto_ban_user_on_excessive_projects_download": auto_ban_user_on_excessive_projects_download,
                "ip_restriction_ranges": ip_restriction_ranges,
                "allowed_email_domains_list": allowed_email_domains_list,
                "wiki_access_level": wiki_access_level,
                "math_rendering_limits_enabled": math_rendering_limits_enabled,
                "lock_math_rendering_limits_enabled": lock_math_rendering_limits_enabled,
                "duo_features_enabled": duo_features_enabled,
                "lock_duo_features_enabled": lock_duo_features_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "argument": argument,
                "data": data,
            }.items()
            if v is not None
        }
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

    def get_group_members(
        self,
        *,
        group_id: int | str | None = None,
        project_id: int | str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "group_id": group_id,
                "project_id": project_id,
                "per_page": per_page,
                "page": page,
            }.items()
            if v is not None
        }
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

    def get_group_level_rule(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        allow_author_approval: bool | None = None,
        allow_committer_approval: bool | None = None,
        allow_overrides_to_approver_list_per_merge_request: bool | None = None,
        retain_approvals_on_push: bool | None = None,
        selective_code_owner_removals: bool | None = None,
        require_reauthentication_to_approve: bool | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "allow_author_approval": allow_author_approval,
                "allow_committer_approval": allow_committer_approval,
                "allow_overrides_to_approver_list_per_merge_request": allow_overrides_to_approver_list_per_merge_request,
                "retain_approvals_on_push": retain_approvals_on_push,
                "selective_code_owner_removals": selective_code_owner_removals,
                "require_reauthentication_to_approve": require_reauthentication_to_approve,
                "data": data,
            }.items()
            if v is not None
        }
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

    def edit_group_level_rule(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        allow_author_approval: bool | None = None,
        allow_committer_approval: bool | None = None,
        allow_overrides_to_approver_list_per_merge_request: bool | None = None,
        retain_approvals_on_push: bool | None = None,
        selective_code_owner_removals: bool | None = None,
        require_reauthentication_to_approve: bool | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "allow_author_approval": allow_author_approval,
                "allow_committer_approval": allow_committer_approval,
                "allow_overrides_to_approver_list_per_merge_request": allow_overrides_to_approver_list_per_merge_request,
                "retain_approvals_on_push": retain_approvals_on_push,
                "selective_code_owner_removals": selective_code_owner_removals,
                "require_reauthentication_to_approve": require_reauthentication_to_approve,
                "data": data,
            }.items()
            if v is not None
        }
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

    def get_group_releases(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        order_by: str | None = None,
        sort: str | None = None,
        simple: bool | None = None,
        include_html_description: bool | None = None,
        tag_name: str | None = None,
        description: str | None = None,
        tag_message: str | None = None,
        ref: str | None = None,
        direct_asset_path: str | None = None,
        name: list[str] | None = None,
        milestones: str | None = None,
        released_at: str | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "order_by": order_by,
                "sort": sort,
                "simple": simple,
                "include_html_description": include_html_description,
                "tag_name": tag_name,
                "description": description,
                "tag_message": tag_message,
                "ref": ref,
                "direct_asset_path": direct_asset_path,
                "name": name,
                "milestones": milestones,
                "released_at": released_at,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "data": data,
            }.items()
            if v is not None
        }
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

    def get_users(
        self,
        *,
        username: str | None = None,
        active: bool | None = None,
        blocked: bool | None = None,
        external: bool | None = None,
        humans: bool | None = None,
        exclude_internal: bool | None = None,
        exclude_external: bool | None = None,
        without_project_bots: bool | None = None,
        extern_uid: str | None = None,
        provider: str | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        with_custom_attributes: str | None = None,
        sort: str | None = None,
        order_by: str | None = None,
        two_factor: str | None = None,
        without_projects: bool | None = None,
        admins: bool | None = None,
        saml_provider_id: str | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sudo: bool | None = None,
        user_id: str | int | None = None,
        email: str | None = None,
        password: str | None = None,
        name: str | None = None,
        admin: bool | None = None,
        skips_confirmation: bool | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get information about users.

        Args:
            **kwargs: Additional parameters for the request (e.g., per_page, page).

        Returns:
            Response: A wrapper containing the original response and a list of User models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "username": username,
                "active": active,
                "blocked": blocked,
                "external": external,
                "humans": humans,
                "exclude_internal": exclude_internal,
                "exclude_external": exclude_external,
                "without_project_bots": without_project_bots,
                "extern_uid": extern_uid,
                "provider": provider,
                "created_before": created_before,
                "created_after": created_after,
                "with_custom_attributes": with_custom_attributes,
                "sort": sort,
                "order_by": order_by,
                "two_factor": two_factor,
                "without_projects": without_projects,
                "admins": admins,
                "saml_provider_id": saml_provider_id,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "sudo": sudo,
                "user_id": user_id,
                "email": email,
                "password": password,
                "name": name,
                "admin": admin,
                "skips_confirmation": skips_confirmation,
                "data": data,
            }.items()
            if v is not None
        }
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

    def get_user(
        self,
        *,
        username: str | None = None,
        active: bool | None = None,
        blocked: bool | None = None,
        external: bool | None = None,
        humans: bool | None = None,
        exclude_internal: bool | None = None,
        exclude_external: bool | None = None,
        without_project_bots: bool | None = None,
        extern_uid: str | None = None,
        provider: str | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        with_custom_attributes: str | None = None,
        sort: str | None = None,
        order_by: str | None = None,
        two_factor: str | None = None,
        without_projects: bool | None = None,
        admins: bool | None = None,
        saml_provider_id: str | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sudo: bool | None = None,
        user_id: str | int | None = None,
        email: str | None = None,
        password: str | None = None,
        name: str | None = None,
        admin: bool | None = None,
        skips_confirmation: bool | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "username": username,
                "active": active,
                "blocked": blocked,
                "external": external,
                "humans": humans,
                "exclude_internal": exclude_internal,
                "exclude_external": exclude_external,
                "without_project_bots": without_project_bots,
                "extern_uid": extern_uid,
                "provider": provider,
                "created_before": created_before,
                "created_after": created_after,
                "with_custom_attributes": with_custom_attributes,
                "sort": sort,
                "order_by": order_by,
                "two_factor": two_factor,
                "without_projects": without_projects,
                "admins": admins,
                "saml_provider_id": saml_provider_id,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "sudo": sudo,
                "user_id": user_id,
                "email": email,
                "password": password,
                "name": name,
                "admin": admin,
                "skips_confirmation": skips_confirmation,
                "data": data,
            }.items()
            if v is not None
        }
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

    def get_namespaces(
        self,
        *,
        namespace_id: int | str | None = None,
        search: str | None = None,
        owned_only: bool | None = None,
        top_level_only: bool | None = None,
        max_pages: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get information about namespaces.

        Args:
            **kwargs: Additional parameters for the request (e.g., per_page).

        Returns:
            Response: A wrapper containing the original response and a list of Namespace models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "namespace_id": namespace_id,
                "search": search,
                "owned_only": owned_only,
                "top_level_only": top_level_only,
                "max_pages": max_pages,
                "data": data,
            }.items()
            if v is not None
        }
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

    def get_namespace(
        self,
        *,
        namespace_id: int | str | None = None,
        search: str | None = None,
        owned_only: bool | None = None,
        top_level_only: bool | None = None,
        max_pages: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "namespace_id": namespace_id,
                "search": search,
                "owned_only": owned_only,
                "top_level_only": top_level_only,
                "max_pages": max_pages,
                "data": data,
            }.items()
            if v is not None
        }
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

    def create_user(
        self,
        *,
        username: str | None = None,
        active: bool | None = None,
        blocked: bool | None = None,
        external: bool | None = None,
        humans: bool | None = None,
        exclude_internal: bool | None = None,
        exclude_external: bool | None = None,
        without_project_bots: bool | None = None,
        extern_uid: str | None = None,
        provider: str | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        with_custom_attributes: str | None = None,
        sort: str | None = None,
        order_by: str | None = None,
        two_factor: str | None = None,
        without_projects: bool | None = None,
        admins: bool | None = None,
        saml_provider_id: str | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sudo: bool | None = None,
        user_id: str | int | None = None,
        email: str | None = None,
        password: str | None = None,
        name: str | None = None,
        admin: bool | None = None,
        skips_confirmation: bool | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Create a new user.
        """
        kwargs = {
            k: v
            for k, v in {
                "username": username,
                "active": active,
                "blocked": blocked,
                "external": external,
                "humans": humans,
                "exclude_internal": exclude_internal,
                "exclude_external": exclude_external,
                "without_project_bots": without_project_bots,
                "extern_uid": extern_uid,
                "provider": provider,
                "created_before": created_before,
                "created_after": created_after,
                "with_custom_attributes": with_custom_attributes,
                "sort": sort,
                "order_by": order_by,
                "two_factor": two_factor,
                "without_projects": without_projects,
                "admins": admins,
                "saml_provider_id": saml_provider_id,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "sudo": sudo,
                "user_id": user_id,
                "email": email,
                "password": password,
                "name": name,
                "admin": admin,
                "skips_confirmation": skips_confirmation,
                "data": data,
            }.items()
            if v is not None
        }
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

    def update_user(
        self,
        *,
        username: str | None = None,
        active: bool | None = None,
        blocked: bool | None = None,
        external: bool | None = None,
        humans: bool | None = None,
        exclude_internal: bool | None = None,
        exclude_external: bool | None = None,
        without_project_bots: bool | None = None,
        extern_uid: str | None = None,
        provider: str | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        with_custom_attributes: str | None = None,
        sort: str | None = None,
        order_by: str | None = None,
        two_factor: str | None = None,
        without_projects: bool | None = None,
        admins: bool | None = None,
        saml_provider_id: str | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sudo: bool | None = None,
        user_id: str | int | None = None,
        email: str | None = None,
        password: str | None = None,
        name: str | None = None,
        admin: bool | None = None,
        skips_confirmation: bool | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Update an existing user.
        """
        kwargs = {
            k: v
            for k, v in {
                "username": username,
                "active": active,
                "blocked": blocked,
                "external": external,
                "humans": humans,
                "exclude_internal": exclude_internal,
                "exclude_external": exclude_external,
                "without_project_bots": without_project_bots,
                "extern_uid": extern_uid,
                "provider": provider,
                "created_before": created_before,
                "created_after": created_after,
                "with_custom_attributes": with_custom_attributes,
                "sort": sort,
                "order_by": order_by,
                "two_factor": two_factor,
                "without_projects": without_projects,
                "admins": admins,
                "saml_provider_id": saml_provider_id,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "sudo": sudo,
                "user_id": user_id,
                "email": email,
                "password": password,
                "name": name,
                "admin": admin,
                "skips_confirmation": skips_confirmation,
                "data": data,
            }.items()
            if v is not None
        }
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

    def delete_user(
        self,
        *,
        username: str | None = None,
        active: bool | None = None,
        blocked: bool | None = None,
        external: bool | None = None,
        humans: bool | None = None,
        exclude_internal: bool | None = None,
        exclude_external: bool | None = None,
        without_project_bots: bool | None = None,
        extern_uid: str | None = None,
        provider: str | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        with_custom_attributes: str | None = None,
        sort: str | None = None,
        order_by: str | None = None,
        two_factor: str | None = None,
        without_projects: bool | None = None,
        admins: bool | None = None,
        saml_provider_id: str | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        sudo: bool | None = None,
        user_id: str | int | None = None,
        email: str | None = None,
        password: str | None = None,
        name: str | None = None,
        admin: bool | None = None,
        skips_confirmation: bool | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Delete a user.
        """
        kwargs = {
            k: v
            for k, v in {
                "username": username,
                "active": active,
                "blocked": blocked,
                "external": external,
                "humans": humans,
                "exclude_internal": exclude_internal,
                "exclude_external": exclude_external,
                "without_project_bots": without_project_bots,
                "extern_uid": extern_uid,
                "provider": provider,
                "created_before": created_before,
                "created_after": created_after,
                "with_custom_attributes": with_custom_attributes,
                "sort": sort,
                "order_by": order_by,
                "two_factor": two_factor,
                "without_projects": without_projects,
                "admins": admins,
                "saml_provider_id": saml_provider_id,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "sudo": sudo,
                "user_id": user_id,
                "email": email,
                "password": password,
                "name": name,
                "admin": admin,
                "skips_confirmation": skips_confirmation,
                "data": data,
            }.items()
            if v is not None
        }
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
