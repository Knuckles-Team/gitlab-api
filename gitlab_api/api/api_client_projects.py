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
    JobModel,
    MembersModel,
    MergeRequestModel,
    MergeRequestRuleModel,
    MergeRequestRuleSettingsModel,
    ProjectModel,
    RunnerModel,
)
from gitlab_api.gitlab_response_models import (
    ApprovalRule,
    DeployToken,
    Group,
    Job,
    Membership,
    MergeRequest,
    MergeRequestRuleSettings,
    Project,
    Response,
    Runner,
    User,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiProjects(GitLabApiBase):
    def get_project_deploy_tokens(
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
        Get deploy tokens for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

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
        if deploy_token.project_id is None:
            raise MissingParameterError("project_id is required")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{deploy_token.project_id}/deploy_tokens",
                model=deploy_token,
                id_field="project_id",
                id_value=deploy_token.project_id,
            )
            parsed_data = [DeployToken(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to get project deploy tokens: {type(e).__name__}"
            ) from e

    def get_project_deploy_token(
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
        Get a specific deploy token for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, deploy_token_id).

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
        if deploy_token.project_id is None or deploy_token.deploy_token_id is None:  # type: ignore
            raise MissingParameterError("project_id and deploy_token_id are required")
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.deploy_token_id}",  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = DeployToken(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to get project deploy token: {type(e).__name__}"
            ) from e

    def create_project_deploy_token(
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
        Create a deploy token for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name, scopes).

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
            deploy_token.project_id is None
            or deploy_token.name is None
            or deploy_token.scopes is None
        ):
            raise MissingParameterError("project_id, name, and scopes are required")
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens",
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
                f"Failed to create project deploy token: {type(e).__name__}"
            ) from e

    def delete_project_deploy_token(
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
        Delete a deploy token for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, deploy_token_id).

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
        if deploy_token.project_id is None or deploy_token.deploy_token_id is None:  # type: ignore
            raise MissingParameterError("project_id and deploy_token_id are required")
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{deploy_token.project_id}/deploy_tokens/{deploy_token.deploy_token_id}",  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            raise ParameterError(
                f"Failed to delete project deploy token: {type(e).__name__}"
            ) from e

    def get_group_projects(
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
        Get projects associated with a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Project models.

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
                endpoint="/groups/{id}/projects",
                model=group,
                id_field="group_id",
                id_value=group.group_id,
            )
            parsed_data = [Project(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_jobs(
        self,
        *,
        project_id: int | str | None = None,
        pipeline_id: int | str | None = None,
        job_id: int | str | None = None,
        scope: list[str] | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_retried: bool | None = None,
        job_variable_attributes: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get jobs associated with a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Job models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "pipeline_id": pipeline_id,
                "job_id": job_id,
                "scope": scope,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "include_retried": include_retried,
                "job_variable_attributes": job_variable_attributes,
            }.items()
            if v is not None
        }
        job = JobModel(**kwargs)
        if job.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{job.project_id}/jobs",
                model=job,
                id_field="project_id",
                id_value=job.project_id,
            )
            parsed_data = [Job(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_job(
        self,
        *,
        project_id: int | str | None = None,
        pipeline_id: int | str | None = None,
        job_id: int | str | None = None,
        scope: list[str] | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_retried: bool | None = None,
        job_variable_attributes: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get details of a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "pipeline_id": pipeline_id,
                "job_id": job_id,
                "scope": scope,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "include_retried": include_retried,
                "job_variable_attributes": job_variable_attributes,
            }.items()
            if v is not None
        }
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_job_log(
        self,
        *,
        project_id: int | str | None = None,
        pipeline_id: int | str | None = None,
        job_id: int | str | None = None,
        scope: list[str] | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_retried: bool | None = None,
        job_variable_attributes: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get the log of a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and the raw job log data.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "pipeline_id": pipeline_id,
                "job_id": job_id,
                "scope": scope,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "include_retried": include_retried,
                "job_variable_attributes": job_variable_attributes,
            }.items()
            if v is not None
        }
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/trace",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.text
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def cancel_project_job(
        self,
        *,
        project_id: int | str | None = None,
        pipeline_id: int | str | None = None,
        job_id: int | str | None = None,
        scope: list[str] | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_retried: bool | None = None,
        job_variable_attributes: dict[str, Any] | None = None,
    ) -> Response:
        """
        Cancel a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "pipeline_id": pipeline_id,
                "job_id": job_id,
                "scope": scope,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "include_retried": include_retried,
                "job_variable_attributes": job_variable_attributes,
            }.items()
            if v is not None
        }
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/cancel",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def retry_project_job(
        self,
        *,
        project_id: int | str | None = None,
        pipeline_id: int | str | None = None,
        job_id: int | str | None = None,
        scope: list[str] | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_retried: bool | None = None,
        job_variable_attributes: dict[str, Any] | None = None,
    ) -> Response:
        """
        Retry a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "pipeline_id": pipeline_id,
                "job_id": job_id,
                "scope": scope,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "include_retried": include_retried,
                "job_variable_attributes": job_variable_attributes,
            }.items()
            if v is not None
        }
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/retry",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def erase_project_job(
        self,
        *,
        project_id: int | str | None = None,
        pipeline_id: int | str | None = None,
        job_id: int | str | None = None,
        scope: list[str] | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_retried: bool | None = None,
        job_variable_attributes: dict[str, Any] | None = None,
    ) -> Response:
        """
        Erase a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "pipeline_id": pipeline_id,
                "job_id": job_id,
                "scope": scope,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "include_retried": include_retried,
                "job_variable_attributes": job_variable_attributes,
            }.items()
            if v is not None
        }
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/erase",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def run_project_job(
        self,
        *,
        project_id: int | str | None = None,
        pipeline_id: int | str | None = None,
        job_id: int | str | None = None,
        scope: list[str] | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        include_retried: bool | None = None,
        job_variable_attributes: dict[str, Any] | None = None,
    ) -> Response:
        """
        Run a specific job within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, job_id).

        Returns:
            Response: A wrapper containing the original response and a Job model.

        Raises:
            MissingParameterError: If the project_id or job_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "pipeline_id": pipeline_id,
                "job_id": job_id,
                "scope": scope,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "include_retried": include_retried,
                "job_variable_attributes": job_variable_attributes,
            }.items()
            if v is not None
        }
        job = JobModel(**kwargs)
        if job.project_id is None or job.job_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{job.project_id}/jobs/{job.job_id}/play",
                headers=self.headers,
                json=job.data,  # type: ignore
            )
            response.raise_for_status()
            parsed_data = Job(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_members(
        self,
        *,
        group_id: int | str | None = None,
        project_id: int | str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """
        Get members of a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Membership models.

        Raises:
            MissingParameterError: If the project_id is missing.
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
        if members.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{members.project_id}/members",
                model=members,
                id_field="project_id",
                id_value=members.project_id,
            )
            parsed_data = [Membership(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_merge_requests(
        self,
        *,
        approved_by_ids: list[int] | None = None,
        approver_ids: list[int] | None = None,
        assignee_id: int | str | None = None,
        author_id: int | str | None = None,
        author_username: str | None = None,
        created_after: str | None = None,
        created_before: str | None = None,
        deployed_after: str | None = None,
        deployed_before: str | None = None,
        environment: str | None = None,
        search_in: str | None = None,
        labels: str | None = None,
        milestone: str | None = None,
        my_reaction_emoji: str | None = None,
        project_id: int | str | None = None,
        search_exclude: str | None = None,
        order_by: str | None = None,
        reviewer_id: int | str | None = None,
        reviewer_username: str | None = None,
        scope: list[str] | None = None,
        search: str | None = None,
        sort: str | None = None,
        source_branch: str | None = None,
        state: str | None = None,
        target_branch: str | None = None,
        updated_after: str | None = None,
        updated_before: str | None = None,
        view: str | None = None,
        with_labels_details: bool | None = None,
        with_merge_status_recheck: bool | None = None,
        wip: str | None = None,
        title: str | None = None,
        allow_collaboration: bool | None = None,
        allow_maintainer_to_push: bool | None = None,
        approvals_before_merge: int | None = None,
        assignee_ids: list[int] | None = None,
        description: str | None = None,
        milestone_id: int | str | None = None,
        remove_source_branch: str | None = None,
        reviewer_ids: list[int] | None = None,
        squash: bool | None = None,
        target_project_id: int | str | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get merge requests for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of MergeRequest models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "approved_by_ids": approved_by_ids,
                "approver_ids": approver_ids,
                "assignee_id": assignee_id,
                "author_id": author_id,
                "author_username": author_username,
                "created_after": created_after,
                "created_before": created_before,
                "deployed_after": deployed_after,
                "deployed_before": deployed_before,
                "environment": environment,
                "search_in": search_in,
                "labels": labels,
                "milestone": milestone,
                "my_reaction_emoji": my_reaction_emoji,
                "project_id": project_id,
                "search_exclude": search_exclude,
                "order_by": order_by,
                "reviewer_id": reviewer_id,
                "reviewer_username": reviewer_username,
                "scope": scope,
                "search": search,
                "sort": sort,
                "source_branch": source_branch,
                "state": state,
                "target_branch": target_branch,
                "updated_after": updated_after,
                "updated_before": updated_before,
                "view": view,
                "with_labels_details": with_labels_details,
                "with_merge_status_recheck": with_merge_status_recheck,
                "wip": wip,
                "title": title,
                "allow_collaboration": allow_collaboration,
                "allow_maintainer_to_push": allow_maintainer_to_push,
                "approvals_before_merge": approvals_before_merge,
                "assignee_ids": assignee_ids,
                "description": description,
                "milestone_id": milestone_id,
                "remove_source_branch": remove_source_branch,
                "reviewer_ids": reviewer_ids,
                "squash": squash,
                "target_project_id": target_project_id,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "data": data,
            }.items()
            if v is not None
        }
        merge_request = MergeRequestModel(**kwargs)
        if merge_request.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{merge_request.project_id}/merge_requests",
                model=merge_request,
                id_field="project_id",
                id_value=merge_request.project_id,
            )
            parsed_data = [MergeRequest(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_merge_request(
        self,
        *,
        approved_by_ids: list[int] | None = None,
        approver_ids: list[int] | None = None,
        assignee_id: int | str | None = None,
        author_id: int | str | None = None,
        author_username: str | None = None,
        created_after: str | None = None,
        created_before: str | None = None,
        deployed_after: str | None = None,
        deployed_before: str | None = None,
        environment: str | None = None,
        search_in: str | None = None,
        labels: str | None = None,
        milestone: str | None = None,
        my_reaction_emoji: str | None = None,
        project_id: int | str | None = None,
        search_exclude: str | None = None,
        order_by: str | None = None,
        reviewer_id: int | str | None = None,
        reviewer_username: str | None = None,
        scope: list[str] | None = None,
        search: str | None = None,
        sort: str | None = None,
        source_branch: str | None = None,
        state: str | None = None,
        target_branch: str | None = None,
        updated_after: str | None = None,
        updated_before: str | None = None,
        view: str | None = None,
        with_labels_details: bool | None = None,
        with_merge_status_recheck: bool | None = None,
        wip: str | None = None,
        title: str | None = None,
        allow_collaboration: bool | None = None,
        allow_maintainer_to_push: bool | None = None,
        approvals_before_merge: int | None = None,
        assignee_ids: list[int] | None = None,
        description: str | None = None,
        milestone_id: int | str | None = None,
        remove_source_branch: str | None = None,
        reviewer_ids: list[int] | None = None,
        squash: bool | None = None,
        target_project_id: int | str | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get details of a specific merge request in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response and a MergeRequest model.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "approved_by_ids": approved_by_ids,
                "approver_ids": approver_ids,
                "assignee_id": assignee_id,
                "author_id": author_id,
                "author_username": author_username,
                "created_after": created_after,
                "created_before": created_before,
                "deployed_after": deployed_after,
                "deployed_before": deployed_before,
                "environment": environment,
                "search_in": search_in,
                "labels": labels,
                "milestone": milestone,
                "my_reaction_emoji": my_reaction_emoji,
                "project_id": project_id,
                "search_exclude": search_exclude,
                "order_by": order_by,
                "reviewer_id": reviewer_id,
                "reviewer_username": reviewer_username,
                "scope": scope,
                "search": search,
                "sort": sort,
                "source_branch": source_branch,
                "state": state,
                "target_branch": target_branch,
                "updated_after": updated_after,
                "updated_before": updated_before,
                "view": view,
                "with_labels_details": with_labels_details,
                "with_merge_status_recheck": with_merge_status_recheck,
                "wip": wip,
                "title": title,
                "allow_collaboration": allow_collaboration,
                "allow_maintainer_to_push": allow_maintainer_to_push,
                "approvals_before_merge": approvals_before_merge,
                "assignee_ids": assignee_ids,
                "description": description,
                "milestone_id": milestone_id,
                "remove_source_branch": remove_source_branch,
                "reviewer_ids": reviewer_ids,
                "squash": squash,
                "target_project_id": target_project_id,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "data": data,
            }.items()
            if v is not None
        }
        merge_request = MergeRequestModel(**kwargs)
        if merge_request.project_id is None or merge_request.merge_request_iid is None:  # type: ignore
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_request.project_id}/merge_requests/{merge_request.merge_request_iid}",  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_level_merge_request_rules(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        approval_rule_id: int | str | None = None,
        approvals_required: int | None = None,
        name: str | None = None,
        applies_to_all_protected_branches: bool | None = None,
        group_ids: list[int] | None = None,
        merge_request_iid: int | str | None = None,
        protected_branch_ids: list[int] | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list[int] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get project-level merge request approval rules.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of ApprovalRule models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "approval_rule_id": approval_rule_id,
                "approvals_required": approvals_required,
                "name": name,
                "applies_to_all_protected_branches": applies_to_all_protected_branches,
                "group_ids": group_ids,
                "merge_request_iid": merge_request_iid,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "data": data,
            }.items()
            if v is not None
        }
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{merge_rule.project_id}/approval_rules",
                model=merge_rule,
                id_field="project_id",
                id_value=merge_rule.project_id,
            )
            parsed_data = [ApprovalRule(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_level_merge_request_rule(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        approval_rule_id: int | str | None = None,
        approvals_required: int | None = None,
        name: str | None = None,
        applies_to_all_protected_branches: bool | None = None,
        group_ids: list[int] | None = None,
        merge_request_iid: int | str | None = None,
        protected_branch_ids: list[int] | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list[int] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get details of a specific project-level merge request approval rule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, approval_rule_id).

        Returns:
            Response: A wrapper containing the original response and an ApprovalRule model.

        Raises:
            MissingParameterError: If the project_id or approval_rule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "approval_rule_id": approval_rule_id,
                "approvals_required": approvals_required,
                "name": name,
                "applies_to_all_protected_branches": applies_to_all_protected_branches,
                "group_ids": group_ids,
                "merge_request_iid": merge_request_iid,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "data": data,
            }.items()
            if v is not None
        }
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.approval_rule_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules/{merge_rule.approval_rule_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = ApprovalRule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_project_level_rule(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        approval_rule_id: int | str | None = None,
        approvals_required: int | None = None,
        name: str | None = None,
        applies_to_all_protected_branches: bool | None = None,
        group_ids: list[int] | None = None,
        merge_request_iid: int | str | None = None,
        protected_branch_ids: list[int] | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list[int] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Create a new project-level merge request approval rule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name, approvals_required).

        Returns:
            Response: A wrapper containing the original response and an ApprovalRule model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "approval_rule_id": approval_rule_id,
                "approvals_required": approvals_required,
                "name": name,
                "applies_to_all_protected_branches": applies_to_all_protected_branches,
                "group_ids": group_ids,
                "merge_request_iid": merge_request_iid,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "data": data,
            }.items()
            if v is not None
        }
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules",
                headers=self.headers,
                json=merge_rule.data,
            )
            response.raise_for_status()
            parsed_data = ApprovalRule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_project_level_rule(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        approval_rule_id: int | str | None = None,
        approvals_required: int | None = None,
        name: str | None = None,
        applies_to_all_protected_branches: bool | None = None,
        group_ids: list[int] | None = None,
        merge_request_iid: int | str | None = None,
        protected_branch_ids: list[int] | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list[int] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Update an existing project-level merge request approval rule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, approval_rule_id).

        Returns:
            Response: A wrapper containing the original response and an ApprovalRule model.

        Raises:
            MissingParameterError: If the project_id or approval_rule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "approval_rule_id": approval_rule_id,
                "approvals_required": approvals_required,
                "name": name,
                "applies_to_all_protected_branches": applies_to_all_protected_branches,
                "group_ids": group_ids,
                "merge_request_iid": merge_request_iid,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "data": data,
            }.items()
            if v is not None
        }
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.approval_rule_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules/{merge_rule.approval_rule_id}",
                headers=self.headers,
                json=merge_rule.data,
            )
            response.raise_for_status()
            parsed_data = ApprovalRule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_project_level_rule(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        approval_rule_id: int | str | None = None,
        approvals_required: int | None = None,
        name: str | None = None,
        applies_to_all_protected_branches: bool | None = None,
        group_ids: list[int] | None = None,
        merge_request_iid: int | str | None = None,
        protected_branch_ids: list[int] | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list[int] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Delete a project-level merge request approval rule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, approval_rule_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or approval_rule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "approval_rule_id": approval_rule_id,
                "approvals_required": approvals_required,
                "name": name,
                "applies_to_all_protected_branches": applies_to_all_protected_branches,
                "group_ids": group_ids,
                "merge_request_iid": merge_request_iid,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "data": data,
            }.items()
            if v is not None
        }
        merge_rule = MergeRequestRuleModel(**kwargs)
        if merge_rule.project_id is None or merge_rule.approval_rule_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{merge_rule.project_id}/approval_rules/{merge_rule.approval_rule_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_level_rule(
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
        Get details of a project-level merge request approval setting.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a MergeRequestRuleSettings model.

        Raises:
            MissingParameterError: If the project_id is missing.
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
        if merge_rule_setting.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_rule_setting.project_id}/merge_request_approval_setting",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = MergeRequestRuleSettings(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def edit_project_level_rule(
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
        Edit a project-level merge request approval setting.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a MergeRequestRuleSettings model.

        Raises:
            MissingParameterError: If the project_id is missing.
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
        if merge_rule_setting.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{merge_rule_setting.project_id}/merge_request_approval_setting",
                headers=self.headers,
                json=merge_rule_setting.data,
            )
            response.raise_for_status()
            parsed_data = MergeRequestRuleSettings(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_projects(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        allow_merge_on_skipped_pipeline: bool | None = None,
        only_allow_merge_if_all_status_checks_passed: bool | None = None,
        analytics_access_level: str | None = None,
        approvals_before_merge: int | None = None,
        auto_cancel_pending_pipelines: str | None = None,
        auto_devops_deploy_strategy: str | None = None,
        auto_devops_enabled: bool | None = None,
        autoclose_referenced_issues: bool | None = None,
        avatar: str | None = None,
        build_git_strategy: str | None = None,
        build_timeout: int | None = None,
        builds_access_level: str | None = None,
        ci_config_path: str | None = None,
        ci_default_git_depth: int | None = None,
        ci_forward_deployment_enabled: bool | None = None,
        ci_allow_fork_pipelines_to_run_in_parent_project: bool | None = None,
        ci_separated_caches: bool | None = None,
        container_expiration_policy_attributes: str | None = None,
        container_registry_access_level: str | None = None,
        default_branch: str | None = None,
        description: str | None = None,
        emails_disabled: bool | None = None,
        enforce_auth_checks_on_uploads: bool | None = None,
        external_authorization_classification_label: str | None = None,
        expires_at: str | None = None,
        forking_access_level: str | None = None,
        group_access: int | None = None,
        import_url: Any = None,
        issues_access_level: str | None = None,
        issues_template: str | None = None,
        keep_latest_artifact: bool | None = None,
        lfs_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        merge_commit_template: str | None = None,
        merge_method: str | None = None,
        merge_pipelines_enabled: bool | None = None,
        merge_requests_access_level: str | None = None,
        merge_requests_template: str | None = None,
        merge_trains_enabled: bool | None = None,
        mirror_overwrites_diverged_branches: bool | None = None,
        mirror_trigger_builds: bool | None = None,
        mirror_user_id: int | str | None = None,
        mirror: bool | None = None,
        mr_default_target_self: bool | None = None,
        name: str | None = None,
        tag_name: str | None = None,
        order_by: str | None = None,
        only_allow_merge_if_all_discussions_are_resolved: bool | None = None,
        only_allow_merge_if_pipeline_succeeds: bool | None = None,
        only_mirror_protected_branches: bool | None = None,
        operations_access_level: str | None = None,
        packages_enabled: bool | None = None,
        pages_access_level: str | None = None,
        path: str | None = None,
        printing_merge_request_link_enabled: bool | None = None,
        public_builds: bool | None = None,
        releases_access_level: str | None = None,
        remove_source_branch_after_merge: bool | None = None,
        repository_access_level: str | None = None,
        repository_storage: str | None = None,
        request_access_enabled: bool | None = None,
        requirements_access_level: str | None = None,
        resolve_outdated_diff_discussions: bool | None = None,
        restrict_user_defined_variables: bool | None = None,
        security_and_compliance_access_level: str | None = None,
        service_desk_enabled: bool | None = None,
        shared_runners_enabled: bool | None = None,
        snippets_access_level: str | None = None,
        squash_commit_template: str | None = None,
        squash_option: str | None = None,
        suggestion_commit_message: str | None = None,
        tag_list: list[str] | None = None,
        topics: list[str] | None = None,
        visibility: str | None = None,
        archived: bool | None = None,
        id_after: int | None = None,
        id_before: int | None = None,
        imported: bool | None = None,
        include_hidden: bool | None = None,
        include_pending_delete: bool | None = None,
        membership: bool | None = None,
        search: str | None = None,
        sort: str | None = None,
        min_access_level: int | None = None,
        owned: bool | None = None,
        statistics: bool | None = None,
        simple: bool | None = None,
        starred: bool | None = None,
        topic: str | None = None,
        topic_id: int | str | None = None,
        repository_checksum_failed: bool | None = None,
        allowed_to_create: list[dict[str, Any]] | None = None,
        deploy_access_levels: list[dict[str, Any]] | None = None,
        approval_rules: list[dict[str, Any]] | None = None,
        search_namespaces: bool | None = None,
        environment_id: int | str | None = None,
        environment_name: str | None = None,
        wiki_access_level: str | None = None,
        create_access_level: int | None = None,
        cluster_agent_id: str | None = None,
        external_url: str | None = None,
        tier: str | None = None,
        kubernetes_namespace: str | None = None,
        flux_resource_path: str | None = None,
        auto_stop_setting: str | None = None,
        states: str | None = None,
        before: str | None = None,
        limit: int | None = None,
        dry_run: int | None = None,
        force: bool | None = None,
        pipeline_schedule_id: int | str | None = None,
        cron: str | None = None,
        cron_timezone: str | None = None,
        id: int | str | None = None,
        ref: str | None = None,
        active: bool | None = None,
        key: str | None = None,
        value: str | None = None,
        variable_type: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get information about projects.

        Args:
            **kwargs: Additional parameters for the request (e.g., owned, membership).

        Returns:
            Response: A wrapper containing the original response and a list of Project models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "allow_merge_on_skipped_pipeline": allow_merge_on_skipped_pipeline,
                "only_allow_merge_if_all_status_checks_passed": only_allow_merge_if_all_status_checks_passed,
                "analytics_access_level": analytics_access_level,
                "approvals_before_merge": approvals_before_merge,
                "auto_cancel_pending_pipelines": auto_cancel_pending_pipelines,
                "auto_devops_deploy_strategy": auto_devops_deploy_strategy,
                "auto_devops_enabled": auto_devops_enabled,
                "autoclose_referenced_issues": autoclose_referenced_issues,
                "avatar": avatar,
                "build_git_strategy": build_git_strategy,
                "build_timeout": build_timeout,
                "builds_access_level": builds_access_level,
                "ci_config_path": ci_config_path,
                "ci_default_git_depth": ci_default_git_depth,
                "ci_forward_deployment_enabled": ci_forward_deployment_enabled,
                "ci_allow_fork_pipelines_to_run_in_parent_project": ci_allow_fork_pipelines_to_run_in_parent_project,
                "ci_separated_caches": ci_separated_caches,
                "container_expiration_policy_attributes": container_expiration_policy_attributes,
                "container_registry_access_level": container_registry_access_level,
                "default_branch": default_branch,
                "description": description,
                "emails_disabled": emails_disabled,
                "enforce_auth_checks_on_uploads": enforce_auth_checks_on_uploads,
                "external_authorization_classification_label": external_authorization_classification_label,
                "expires_at": expires_at,
                "forking_access_level": forking_access_level,
                "group_access": group_access,
                "import_url": import_url,
                "issues_access_level": issues_access_level,
                "issues_template": issues_template,
                "keep_latest_artifact": keep_latest_artifact,
                "lfs_enabled": lfs_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "merge_commit_template": merge_commit_template,
                "merge_method": merge_method,
                "merge_pipelines_enabled": merge_pipelines_enabled,
                "merge_requests_access_level": merge_requests_access_level,
                "merge_requests_template": merge_requests_template,
                "merge_trains_enabled": merge_trains_enabled,
                "mirror_overwrites_diverged_branches": mirror_overwrites_diverged_branches,
                "mirror_trigger_builds": mirror_trigger_builds,
                "mirror_user_id": mirror_user_id,
                "mirror": mirror,
                "mr_default_target_self": mr_default_target_self,
                "name": name,
                "tag_name": tag_name,
                "order_by": order_by,
                "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
                "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
                "only_mirror_protected_branches": only_mirror_protected_branches,
                "operations_access_level": operations_access_level,
                "packages_enabled": packages_enabled,
                "pages_access_level": pages_access_level,
                "path": path,
                "printing_merge_request_link_enabled": printing_merge_request_link_enabled,
                "public_builds": public_builds,
                "releases_access_level": releases_access_level,
                "remove_source_branch_after_merge": remove_source_branch_after_merge,
                "repository_access_level": repository_access_level,
                "repository_storage": repository_storage,
                "request_access_enabled": request_access_enabled,
                "requirements_access_level": requirements_access_level,
                "resolve_outdated_diff_discussions": resolve_outdated_diff_discussions,
                "restrict_user_defined_variables": restrict_user_defined_variables,
                "security_and_compliance_access_level": security_and_compliance_access_level,
                "service_desk_enabled": service_desk_enabled,
                "shared_runners_enabled": shared_runners_enabled,
                "snippets_access_level": snippets_access_level,
                "squash_commit_template": squash_commit_template,
                "squash_option": squash_option,
                "suggestion_commit_message": suggestion_commit_message,
                "tag_list": tag_list,
                "topics": topics,
                "visibility": visibility,
                "archived": archived,
                "id_after": id_after,
                "id_before": id_before,
                "imported": imported,
                "include_hidden": include_hidden,
                "include_pending_delete": include_pending_delete,
                "membership": membership,
                "search": search,
                "sort": sort,
                "min_access_level": min_access_level,
                "owned": owned,
                "statistics": statistics,
                "simple": simple,
                "starred": starred,
                "topic": topic,
                "topic_id": topic_id,
                "repository_checksum_failed": repository_checksum_failed,
                "allowed_to_create": allowed_to_create,
                "deploy_access_levels": deploy_access_levels,
                "approval_rules": approval_rules,
                "search_namespaces": search_namespaces,
                "environment_id": environment_id,
                "environment_name": environment_name,
                "wiki_access_level": wiki_access_level,
                "create_access_level": create_access_level,
                "cluster_agent_id": cluster_agent_id,
                "external_url": external_url,
                "tier": tier,
                "kubernetes_namespace": kubernetes_namespace,
                "flux_resource_path": flux_resource_path,
                "auto_stop_setting": auto_stop_setting,
                "states": states,
                "before": before,
                "limit": limit,
                "dry_run": dry_run,
                "force": force,
                "pipeline_schedule_id": pipeline_schedule_id,
                "cron": cron,
                "cron_timezone": cron_timezone,
                "id": id,
                "ref": ref,
                "active": active,
                "key": key,
                "value": value,
                "variable_type": variable_type,
                "data": data,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint="/projects",
                model=project,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Project(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get information about a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_nested_projects_by_group(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        allow_merge_on_skipped_pipeline: bool | None = None,
        only_allow_merge_if_all_status_checks_passed: bool | None = None,
        analytics_access_level: str | None = None,
        approvals_before_merge: int | None = None,
        auto_cancel_pending_pipelines: str | None = None,
        auto_devops_deploy_strategy: str | None = None,
        auto_devops_enabled: bool | None = None,
        autoclose_referenced_issues: bool | None = None,
        avatar: str | None = None,
        build_git_strategy: str | None = None,
        build_timeout: int | None = None,
        builds_access_level: str | None = None,
        ci_config_path: str | None = None,
        ci_default_git_depth: int | None = None,
        ci_forward_deployment_enabled: bool | None = None,
        ci_allow_fork_pipelines_to_run_in_parent_project: bool | None = None,
        ci_separated_caches: bool | None = None,
        container_expiration_policy_attributes: str | None = None,
        container_registry_access_level: str | None = None,
        default_branch: str | None = None,
        description: str | None = None,
        emails_disabled: bool | None = None,
        enforce_auth_checks_on_uploads: bool | None = None,
        external_authorization_classification_label: str | None = None,
        expires_at: str | None = None,
        forking_access_level: str | None = None,
        group_access: int | None = None,
        import_url: Any = None,
        issues_access_level: str | None = None,
        issues_template: str | None = None,
        keep_latest_artifact: bool | None = None,
        lfs_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        merge_commit_template: str | None = None,
        merge_method: str | None = None,
        merge_pipelines_enabled: bool | None = None,
        merge_requests_access_level: str | None = None,
        merge_requests_template: str | None = None,
        merge_trains_enabled: bool | None = None,
        mirror_overwrites_diverged_branches: bool | None = None,
        mirror_trigger_builds: bool | None = None,
        mirror_user_id: int | str | None = None,
        mirror: bool | None = None,
        mr_default_target_self: bool | None = None,
        name: str | None = None,
        tag_name: str | None = None,
        order_by: str | None = None,
        only_allow_merge_if_all_discussions_are_resolved: bool | None = None,
        only_allow_merge_if_pipeline_succeeds: bool | None = None,
        only_mirror_protected_branches: bool | None = None,
        operations_access_level: str | None = None,
        packages_enabled: bool | None = None,
        pages_access_level: str | None = None,
        path: str | None = None,
        printing_merge_request_link_enabled: bool | None = None,
        public_builds: bool | None = None,
        releases_access_level: str | None = None,
        remove_source_branch_after_merge: bool | None = None,
        repository_access_level: str | None = None,
        repository_storage: str | None = None,
        request_access_enabled: bool | None = None,
        requirements_access_level: str | None = None,
        resolve_outdated_diff_discussions: bool | None = None,
        restrict_user_defined_variables: bool | None = None,
        security_and_compliance_access_level: str | None = None,
        service_desk_enabled: bool | None = None,
        shared_runners_enabled: bool | None = None,
        snippets_access_level: str | None = None,
        squash_commit_template: str | None = None,
        squash_option: str | None = None,
        suggestion_commit_message: str | None = None,
        tag_list: list[str] | None = None,
        topics: list[str] | None = None,
        visibility: str | None = None,
        archived: bool | None = None,
        id_after: int | None = None,
        id_before: int | None = None,
        imported: bool | None = None,
        include_hidden: bool | None = None,
        include_pending_delete: bool | None = None,
        membership: bool | None = None,
        search: str | None = None,
        sort: str | None = None,
        min_access_level: int | None = None,
        owned: bool | None = None,
        statistics: bool | None = None,
        simple: bool | None = None,
        starred: bool | None = None,
        topic: str | None = None,
        topic_id: int | str | None = None,
        repository_checksum_failed: bool | None = None,
        allowed_to_create: list[dict[str, Any]] | None = None,
        deploy_access_levels: list[dict[str, Any]] | None = None,
        approval_rules: list[dict[str, Any]] | None = None,
        search_namespaces: bool | None = None,
        environment_id: int | str | None = None,
        environment_name: str | None = None,
        wiki_access_level: str | None = None,
        create_access_level: int | None = None,
        cluster_agent_id: str | None = None,
        external_url: str | None = None,
        tier: str | None = None,
        kubernetes_namespace: str | None = None,
        flux_resource_path: str | None = None,
        auto_stop_setting: str | None = None,
        states: str | None = None,
        before: str | None = None,
        limit: int | None = None,
        dry_run: int | None = None,
        force: bool | None = None,
        pipeline_schedule_id: int | str | None = None,
        cron: str | None = None,
        cron_timezone: str | None = None,
        id: int | str | None = None,
        ref: str | None = None,
        active: bool | None = None,
        key: str | None = None,
        value: str | None = None,
        variable_type: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get information about nested projects within a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, per_page).

        Returns:
            Response: A wrapper containing the original response and a list of Project models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "allow_merge_on_skipped_pipeline": allow_merge_on_skipped_pipeline,
                "only_allow_merge_if_all_status_checks_passed": only_allow_merge_if_all_status_checks_passed,
                "analytics_access_level": analytics_access_level,
                "approvals_before_merge": approvals_before_merge,
                "auto_cancel_pending_pipelines": auto_cancel_pending_pipelines,
                "auto_devops_deploy_strategy": auto_devops_deploy_strategy,
                "auto_devops_enabled": auto_devops_enabled,
                "autoclose_referenced_issues": autoclose_referenced_issues,
                "avatar": avatar,
                "build_git_strategy": build_git_strategy,
                "build_timeout": build_timeout,
                "builds_access_level": builds_access_level,
                "ci_config_path": ci_config_path,
                "ci_default_git_depth": ci_default_git_depth,
                "ci_forward_deployment_enabled": ci_forward_deployment_enabled,
                "ci_allow_fork_pipelines_to_run_in_parent_project": ci_allow_fork_pipelines_to_run_in_parent_project,
                "ci_separated_caches": ci_separated_caches,
                "container_expiration_policy_attributes": container_expiration_policy_attributes,
                "container_registry_access_level": container_registry_access_level,
                "default_branch": default_branch,
                "description": description,
                "emails_disabled": emails_disabled,
                "enforce_auth_checks_on_uploads": enforce_auth_checks_on_uploads,
                "external_authorization_classification_label": external_authorization_classification_label,
                "expires_at": expires_at,
                "forking_access_level": forking_access_level,
                "group_access": group_access,
                "import_url": import_url,
                "issues_access_level": issues_access_level,
                "issues_template": issues_template,
                "keep_latest_artifact": keep_latest_artifact,
                "lfs_enabled": lfs_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "merge_commit_template": merge_commit_template,
                "merge_method": merge_method,
                "merge_pipelines_enabled": merge_pipelines_enabled,
                "merge_requests_access_level": merge_requests_access_level,
                "merge_requests_template": merge_requests_template,
                "merge_trains_enabled": merge_trains_enabled,
                "mirror_overwrites_diverged_branches": mirror_overwrites_diverged_branches,
                "mirror_trigger_builds": mirror_trigger_builds,
                "mirror_user_id": mirror_user_id,
                "mirror": mirror,
                "mr_default_target_self": mr_default_target_self,
                "name": name,
                "tag_name": tag_name,
                "order_by": order_by,
                "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
                "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
                "only_mirror_protected_branches": only_mirror_protected_branches,
                "operations_access_level": operations_access_level,
                "packages_enabled": packages_enabled,
                "pages_access_level": pages_access_level,
                "path": path,
                "printing_merge_request_link_enabled": printing_merge_request_link_enabled,
                "public_builds": public_builds,
                "releases_access_level": releases_access_level,
                "remove_source_branch_after_merge": remove_source_branch_after_merge,
                "repository_access_level": repository_access_level,
                "repository_storage": repository_storage,
                "request_access_enabled": request_access_enabled,
                "requirements_access_level": requirements_access_level,
                "resolve_outdated_diff_discussions": resolve_outdated_diff_discussions,
                "restrict_user_defined_variables": restrict_user_defined_variables,
                "security_and_compliance_access_level": security_and_compliance_access_level,
                "service_desk_enabled": service_desk_enabled,
                "shared_runners_enabled": shared_runners_enabled,
                "snippets_access_level": snippets_access_level,
                "squash_commit_template": squash_commit_template,
                "squash_option": squash_option,
                "suggestion_commit_message": suggestion_commit_message,
                "tag_list": tag_list,
                "topics": topics,
                "visibility": visibility,
                "archived": archived,
                "id_after": id_after,
                "id_before": id_before,
                "imported": imported,
                "include_hidden": include_hidden,
                "include_pending_delete": include_pending_delete,
                "membership": membership,
                "search": search,
                "sort": sort,
                "min_access_level": min_access_level,
                "owned": owned,
                "statistics": statistics,
                "simple": simple,
                "starred": starred,
                "topic": topic,
                "topic_id": topic_id,
                "repository_checksum_failed": repository_checksum_failed,
                "allowed_to_create": allowed_to_create,
                "deploy_access_levels": deploy_access_levels,
                "approval_rules": approval_rules,
                "search_namespaces": search_namespaces,
                "environment_id": environment_id,
                "environment_name": environment_name,
                "wiki_access_level": wiki_access_level,
                "create_access_level": create_access_level,
                "cluster_agent_id": cluster_agent_id,
                "external_url": external_url,
                "tier": tier,
                "kubernetes_namespace": kubernetes_namespace,
                "flux_resource_path": flux_resource_path,
                "auto_stop_setting": auto_stop_setting,
                "states": states,
                "before": before,
                "limit": limit,
                "dry_run": dry_run,
                "force": force,
                "pipeline_schedule_id": pipeline_schedule_id,
                "cron": cron,
                "cron_timezone": cron_timezone,
                "id": id,
                "ref": ref,
                "active": active,
                "key": key,
                "value": value,
                "variable_type": variable_type,
                "data": data,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        all_groups = []
        all_projects = []

        if project.group_id is None:
            raise MissingParameterError

        try:
            group_response = self.get_group(group_id=project.group_id)  # type: ignore
            all_groups.append(group_response.data)

            groups_response = self.get_group_descendant_groups(  # type: ignore
                group_id=project.group_id, per_page=project.per_page
            )
            all_groups.extend(groups_response.data)

            last_response = None
            for group in all_groups:
                response, data = self._fetch_all_pages(
                    endpoint=f"/groups/{group.id}/projects",
                    model=project,
                    id_field="group_id",
                    id_value=group.id,
                )
                parsed_data = [Project(**item) for item in data]
                all_projects.extend(parsed_data)
                last_response = response

            return Response(response=last_response, data=all_projects)  # type: ignore
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_contributors(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        allow_merge_on_skipped_pipeline: bool | None = None,
        only_allow_merge_if_all_status_checks_passed: bool | None = None,
        analytics_access_level: str | None = None,
        approvals_before_merge: int | None = None,
        auto_cancel_pending_pipelines: str | None = None,
        auto_devops_deploy_strategy: str | None = None,
        auto_devops_enabled: bool | None = None,
        autoclose_referenced_issues: bool | None = None,
        avatar: str | None = None,
        build_git_strategy: str | None = None,
        build_timeout: int | None = None,
        builds_access_level: str | None = None,
        ci_config_path: str | None = None,
        ci_default_git_depth: int | None = None,
        ci_forward_deployment_enabled: bool | None = None,
        ci_allow_fork_pipelines_to_run_in_parent_project: bool | None = None,
        ci_separated_caches: bool | None = None,
        container_expiration_policy_attributes: str | None = None,
        container_registry_access_level: str | None = None,
        default_branch: str | None = None,
        description: str | None = None,
        emails_disabled: bool | None = None,
        enforce_auth_checks_on_uploads: bool | None = None,
        external_authorization_classification_label: str | None = None,
        expires_at: str | None = None,
        forking_access_level: str | None = None,
        group_access: int | None = None,
        import_url: Any = None,
        issues_access_level: str | None = None,
        issues_template: str | None = None,
        keep_latest_artifact: bool | None = None,
        lfs_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        merge_commit_template: str | None = None,
        merge_method: str | None = None,
        merge_pipelines_enabled: bool | None = None,
        merge_requests_access_level: str | None = None,
        merge_requests_template: str | None = None,
        merge_trains_enabled: bool | None = None,
        mirror_overwrites_diverged_branches: bool | None = None,
        mirror_trigger_builds: bool | None = None,
        mirror_user_id: int | str | None = None,
        mirror: bool | None = None,
        mr_default_target_self: bool | None = None,
        name: str | None = None,
        tag_name: str | None = None,
        order_by: str | None = None,
        only_allow_merge_if_all_discussions_are_resolved: bool | None = None,
        only_allow_merge_if_pipeline_succeeds: bool | None = None,
        only_mirror_protected_branches: bool | None = None,
        operations_access_level: str | None = None,
        packages_enabled: bool | None = None,
        pages_access_level: str | None = None,
        path: str | None = None,
        printing_merge_request_link_enabled: bool | None = None,
        public_builds: bool | None = None,
        releases_access_level: str | None = None,
        remove_source_branch_after_merge: bool | None = None,
        repository_access_level: str | None = None,
        repository_storage: str | None = None,
        request_access_enabled: bool | None = None,
        requirements_access_level: str | None = None,
        resolve_outdated_diff_discussions: bool | None = None,
        restrict_user_defined_variables: bool | None = None,
        security_and_compliance_access_level: str | None = None,
        service_desk_enabled: bool | None = None,
        shared_runners_enabled: bool | None = None,
        snippets_access_level: str | None = None,
        squash_commit_template: str | None = None,
        squash_option: str | None = None,
        suggestion_commit_message: str | None = None,
        tag_list: list[str] | None = None,
        topics: list[str] | None = None,
        visibility: str | None = None,
        archived: bool | None = None,
        id_after: int | None = None,
        id_before: int | None = None,
        imported: bool | None = None,
        include_hidden: bool | None = None,
        include_pending_delete: bool | None = None,
        membership: bool | None = None,
        search: str | None = None,
        sort: str | None = None,
        min_access_level: int | None = None,
        owned: bool | None = None,
        statistics: bool | None = None,
        simple: bool | None = None,
        starred: bool | None = None,
        topic: str | None = None,
        topic_id: int | str | None = None,
        repository_checksum_failed: bool | None = None,
        allowed_to_create: list[dict[str, Any]] | None = None,
        deploy_access_levels: list[dict[str, Any]] | None = None,
        approval_rules: list[dict[str, Any]] | None = None,
        search_namespaces: bool | None = None,
        environment_id: int | str | None = None,
        environment_name: str | None = None,
        wiki_access_level: str | None = None,
        create_access_level: int | None = None,
        cluster_agent_id: str | None = None,
        external_url: str | None = None,
        tier: str | None = None,
        kubernetes_namespace: str | None = None,
        flux_resource_path: str | None = None,
        auto_stop_setting: str | None = None,
        states: str | None = None,
        before: str | None = None,
        limit: int | None = None,
        dry_run: int | None = None,
        force: bool | None = None,
        pipeline_schedule_id: int | str | None = None,
        cron: str | None = None,
        cron_timezone: str | None = None,
        id: int | str | None = None,
        ref: str | None = None,
        active: bool | None = None,
        key: str | None = None,
        value: str | None = None,
        variable_type: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get information about contributors to a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of User models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "allow_merge_on_skipped_pipeline": allow_merge_on_skipped_pipeline,
                "only_allow_merge_if_all_status_checks_passed": only_allow_merge_if_all_status_checks_passed,
                "analytics_access_level": analytics_access_level,
                "approvals_before_merge": approvals_before_merge,
                "auto_cancel_pending_pipelines": auto_cancel_pending_pipelines,
                "auto_devops_deploy_strategy": auto_devops_deploy_strategy,
                "auto_devops_enabled": auto_devops_enabled,
                "autoclose_referenced_issues": autoclose_referenced_issues,
                "avatar": avatar,
                "build_git_strategy": build_git_strategy,
                "build_timeout": build_timeout,
                "builds_access_level": builds_access_level,
                "ci_config_path": ci_config_path,
                "ci_default_git_depth": ci_default_git_depth,
                "ci_forward_deployment_enabled": ci_forward_deployment_enabled,
                "ci_allow_fork_pipelines_to_run_in_parent_project": ci_allow_fork_pipelines_to_run_in_parent_project,
                "ci_separated_caches": ci_separated_caches,
                "container_expiration_policy_attributes": container_expiration_policy_attributes,
                "container_registry_access_level": container_registry_access_level,
                "default_branch": default_branch,
                "description": description,
                "emails_disabled": emails_disabled,
                "enforce_auth_checks_on_uploads": enforce_auth_checks_on_uploads,
                "external_authorization_classification_label": external_authorization_classification_label,
                "expires_at": expires_at,
                "forking_access_level": forking_access_level,
                "group_access": group_access,
                "import_url": import_url,
                "issues_access_level": issues_access_level,
                "issues_template": issues_template,
                "keep_latest_artifact": keep_latest_artifact,
                "lfs_enabled": lfs_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "merge_commit_template": merge_commit_template,
                "merge_method": merge_method,
                "merge_pipelines_enabled": merge_pipelines_enabled,
                "merge_requests_access_level": merge_requests_access_level,
                "merge_requests_template": merge_requests_template,
                "merge_trains_enabled": merge_trains_enabled,
                "mirror_overwrites_diverged_branches": mirror_overwrites_diverged_branches,
                "mirror_trigger_builds": mirror_trigger_builds,
                "mirror_user_id": mirror_user_id,
                "mirror": mirror,
                "mr_default_target_self": mr_default_target_self,
                "name": name,
                "tag_name": tag_name,
                "order_by": order_by,
                "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
                "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
                "only_mirror_protected_branches": only_mirror_protected_branches,
                "operations_access_level": operations_access_level,
                "packages_enabled": packages_enabled,
                "pages_access_level": pages_access_level,
                "path": path,
                "printing_merge_request_link_enabled": printing_merge_request_link_enabled,
                "public_builds": public_builds,
                "releases_access_level": releases_access_level,
                "remove_source_branch_after_merge": remove_source_branch_after_merge,
                "repository_access_level": repository_access_level,
                "repository_storage": repository_storage,
                "request_access_enabled": request_access_enabled,
                "requirements_access_level": requirements_access_level,
                "resolve_outdated_diff_discussions": resolve_outdated_diff_discussions,
                "restrict_user_defined_variables": restrict_user_defined_variables,
                "security_and_compliance_access_level": security_and_compliance_access_level,
                "service_desk_enabled": service_desk_enabled,
                "shared_runners_enabled": shared_runners_enabled,
                "snippets_access_level": snippets_access_level,
                "squash_commit_template": squash_commit_template,
                "squash_option": squash_option,
                "suggestion_commit_message": suggestion_commit_message,
                "tag_list": tag_list,
                "topics": topics,
                "visibility": visibility,
                "archived": archived,
                "id_after": id_after,
                "id_before": id_before,
                "imported": imported,
                "include_hidden": include_hidden,
                "include_pending_delete": include_pending_delete,
                "membership": membership,
                "search": search,
                "sort": sort,
                "min_access_level": min_access_level,
                "owned": owned,
                "statistics": statistics,
                "simple": simple,
                "starred": starred,
                "topic": topic,
                "topic_id": topic_id,
                "repository_checksum_failed": repository_checksum_failed,
                "allowed_to_create": allowed_to_create,
                "deploy_access_levels": deploy_access_levels,
                "approval_rules": approval_rules,
                "search_namespaces": search_namespaces,
                "environment_id": environment_id,
                "environment_name": environment_name,
                "wiki_access_level": wiki_access_level,
                "create_access_level": create_access_level,
                "cluster_agent_id": cluster_agent_id,
                "external_url": external_url,
                "tier": tier,
                "kubernetes_namespace": kubernetes_namespace,
                "flux_resource_path": flux_resource_path,
                "auto_stop_setting": auto_stop_setting,
                "states": states,
                "before": before,
                "limit": limit,
                "dry_run": dry_run,
                "force": force,
                "pipeline_schedule_id": pipeline_schedule_id,
                "cron": cron,
                "cron_timezone": cron_timezone,
                "id": id,
                "ref": ref,
                "active": active,
                "key": key,
                "value": value,
                "variable_type": variable_type,
                "data": data,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/repository/contributors",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [User(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_statistics(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get statistics for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and the raw statistics data.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}?statistics=true",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_project(
        self,
        name: str | None = None,
        path: str | None = None,
        namespace_id: int | None = None,
        visibility: str | None = None,
        description: str | None = None,
        initialize_with_readme: bool | None = None,
        default_branch: str | None = None,
        topics: list[str] | None = None,
        issues_enabled: bool | None = None,
        merge_requests_enabled: bool | None = None,
        wiki_enabled: bool | None = None,
        snippets_enabled: bool | None = None,
        container_registry_enabled: bool | None = None,
        shared_runners_enabled: bool | None = None,
        lfs_enabled: bool | None = None,
        only_allow_merge_if_pipeline_succeeds: bool | None = None,
        squash_option: str | None = None,
        template_name: str | None = None,
        import_url: str | None = None,
    ) -> Response:
        """
        Create a new project.

        Args:
            name: Project name (required unless path is given).
            path: Repository path.
            namespace_id: Group or user namespace id.
            visibility: 'private', 'internal' or 'public'.
            description: Project description.
            initialize_with_readme: Create an initial README.
            default_branch: Default branch name.
            topics: Project topics.
            issues_enabled: Enable issues.
            merge_requests_enabled: Enable merge requests.
            wiki_enabled: Enable the wiki.
            snippets_enabled: Enable snippets.
            container_registry_enabled: Enable the container registry.
            shared_runners_enabled: Enable shared runners.
            lfs_enabled: Enable Git LFS.
            only_allow_merge_if_pipeline_succeeds: Require a green pipeline to merge.
            squash_option: 'never', 'always', 'default_on' or 'default_off'.
            template_name: Instance template to start from.
            import_url: URL to import the repository from.

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If neither name nor path is provided.
            ParameterError: If invalid parameters are provided.
        """
        if not name and not path:
            raise MissingParameterError
        body = {
            k: v
            for k, v in {
                "name": name,
                "path": path,
                "namespace_id": namespace_id,
                "visibility": visibility,
                "description": description,
                "initialize_with_readme": initialize_with_readme,
                "default_branch": default_branch,
                "topics": topics,
                "issues_enabled": issues_enabled,
                "merge_requests_enabled": merge_requests_enabled,
                "wiki_enabled": wiki_enabled,
                "snippets_enabled": snippets_enabled,
                "container_registry_enabled": container_registry_enabled,
                "shared_runners_enabled": shared_runners_enabled,
                "lfs_enabled": lfs_enabled,
                "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
                "squash_option": squash_option,
                "template_name": template_name,
                "import_url": import_url,
            }.items()
            if v is not None
        }
        try:
            response = self._session.post(
                url=f"{self.url}/projects",
                json=body,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def edit_project(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        allow_merge_on_skipped_pipeline: bool | None = None,
        only_allow_merge_if_all_status_checks_passed: bool | None = None,
        analytics_access_level: str | None = None,
        approvals_before_merge: int | None = None,
        auto_cancel_pending_pipelines: str | None = None,
        auto_devops_deploy_strategy: str | None = None,
        auto_devops_enabled: bool | None = None,
        autoclose_referenced_issues: bool | None = None,
        avatar: str | None = None,
        build_git_strategy: str | None = None,
        build_timeout: int | None = None,
        builds_access_level: str | None = None,
        ci_config_path: str | None = None,
        ci_default_git_depth: int | None = None,
        ci_forward_deployment_enabled: bool | None = None,
        ci_allow_fork_pipelines_to_run_in_parent_project: bool | None = None,
        ci_separated_caches: bool | None = None,
        container_expiration_policy_attributes: str | None = None,
        container_registry_access_level: str | None = None,
        default_branch: str | None = None,
        description: str | None = None,
        emails_disabled: bool | None = None,
        enforce_auth_checks_on_uploads: bool | None = None,
        external_authorization_classification_label: str | None = None,
        expires_at: str | None = None,
        forking_access_level: str | None = None,
        group_access: int | None = None,
        import_url: Any = None,
        issues_access_level: str | None = None,
        issues_template: str | None = None,
        keep_latest_artifact: bool | None = None,
        lfs_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        merge_commit_template: str | None = None,
        merge_method: str | None = None,
        merge_pipelines_enabled: bool | None = None,
        merge_requests_access_level: str | None = None,
        merge_requests_template: str | None = None,
        merge_trains_enabled: bool | None = None,
        mirror_overwrites_diverged_branches: bool | None = None,
        mirror_trigger_builds: bool | None = None,
        mirror_user_id: int | str | None = None,
        mirror: bool | None = None,
        mr_default_target_self: bool | None = None,
        name: str | None = None,
        tag_name: str | None = None,
        order_by: str | None = None,
        only_allow_merge_if_all_discussions_are_resolved: bool | None = None,
        only_allow_merge_if_pipeline_succeeds: bool | None = None,
        only_mirror_protected_branches: bool | None = None,
        operations_access_level: str | None = None,
        packages_enabled: bool | None = None,
        pages_access_level: str | None = None,
        path: str | None = None,
        printing_merge_request_link_enabled: bool | None = None,
        public_builds: bool | None = None,
        releases_access_level: str | None = None,
        remove_source_branch_after_merge: bool | None = None,
        repository_access_level: str | None = None,
        repository_storage: str | None = None,
        request_access_enabled: bool | None = None,
        requirements_access_level: str | None = None,
        resolve_outdated_diff_discussions: bool | None = None,
        restrict_user_defined_variables: bool | None = None,
        security_and_compliance_access_level: str | None = None,
        service_desk_enabled: bool | None = None,
        shared_runners_enabled: bool | None = None,
        snippets_access_level: str | None = None,
        squash_commit_template: str | None = None,
        squash_option: str | None = None,
        suggestion_commit_message: str | None = None,
        tag_list: list[str] | None = None,
        topics: list[str] | None = None,
        visibility: str | None = None,
        archived: bool | None = None,
        id_after: int | None = None,
        id_before: int | None = None,
        imported: bool | None = None,
        include_hidden: bool | None = None,
        include_pending_delete: bool | None = None,
        membership: bool | None = None,
        search: str | None = None,
        sort: str | None = None,
        min_access_level: int | None = None,
        owned: bool | None = None,
        statistics: bool | None = None,
        simple: bool | None = None,
        starred: bool | None = None,
        topic: str | None = None,
        topic_id: int | str | None = None,
        repository_checksum_failed: bool | None = None,
        allowed_to_create: list[dict[str, Any]] | None = None,
        deploy_access_levels: list[dict[str, Any]] | None = None,
        approval_rules: list[dict[str, Any]] | None = None,
        search_namespaces: bool | None = None,
        environment_id: int | str | None = None,
        environment_name: str | None = None,
        wiki_access_level: str | None = None,
        create_access_level: int | None = None,
        cluster_agent_id: str | None = None,
        external_url: str | None = None,
        tier: str | None = None,
        kubernetes_namespace: str | None = None,
        flux_resource_path: str | None = None,
        auto_stop_setting: str | None = None,
        states: str | None = None,
        before: str | None = None,
        limit: int | None = None,
        dry_run: int | None = None,
        force: bool | None = None,
        pipeline_schedule_id: int | str | None = None,
        cron: str | None = None,
        cron_timezone: str | None = None,
        id: int | str | None = None,
        ref: str | None = None,
        active: bool | None = None,
        key: str | None = None,
        value: str | None = None,
        variable_type: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Edit a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "allow_merge_on_skipped_pipeline": allow_merge_on_skipped_pipeline,
                "only_allow_merge_if_all_status_checks_passed": only_allow_merge_if_all_status_checks_passed,
                "analytics_access_level": analytics_access_level,
                "approvals_before_merge": approvals_before_merge,
                "auto_cancel_pending_pipelines": auto_cancel_pending_pipelines,
                "auto_devops_deploy_strategy": auto_devops_deploy_strategy,
                "auto_devops_enabled": auto_devops_enabled,
                "autoclose_referenced_issues": autoclose_referenced_issues,
                "avatar": avatar,
                "build_git_strategy": build_git_strategy,
                "build_timeout": build_timeout,
                "builds_access_level": builds_access_level,
                "ci_config_path": ci_config_path,
                "ci_default_git_depth": ci_default_git_depth,
                "ci_forward_deployment_enabled": ci_forward_deployment_enabled,
                "ci_allow_fork_pipelines_to_run_in_parent_project": ci_allow_fork_pipelines_to_run_in_parent_project,
                "ci_separated_caches": ci_separated_caches,
                "container_expiration_policy_attributes": container_expiration_policy_attributes,
                "container_registry_access_level": container_registry_access_level,
                "default_branch": default_branch,
                "description": description,
                "emails_disabled": emails_disabled,
                "enforce_auth_checks_on_uploads": enforce_auth_checks_on_uploads,
                "external_authorization_classification_label": external_authorization_classification_label,
                "expires_at": expires_at,
                "forking_access_level": forking_access_level,
                "group_access": group_access,
                "import_url": import_url,
                "issues_access_level": issues_access_level,
                "issues_template": issues_template,
                "keep_latest_artifact": keep_latest_artifact,
                "lfs_enabled": lfs_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "merge_commit_template": merge_commit_template,
                "merge_method": merge_method,
                "merge_pipelines_enabled": merge_pipelines_enabled,
                "merge_requests_access_level": merge_requests_access_level,
                "merge_requests_template": merge_requests_template,
                "merge_trains_enabled": merge_trains_enabled,
                "mirror_overwrites_diverged_branches": mirror_overwrites_diverged_branches,
                "mirror_trigger_builds": mirror_trigger_builds,
                "mirror_user_id": mirror_user_id,
                "mirror": mirror,
                "mr_default_target_self": mr_default_target_self,
                "name": name,
                "tag_name": tag_name,
                "order_by": order_by,
                "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
                "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
                "only_mirror_protected_branches": only_mirror_protected_branches,
                "operations_access_level": operations_access_level,
                "packages_enabled": packages_enabled,
                "pages_access_level": pages_access_level,
                "path": path,
                "printing_merge_request_link_enabled": printing_merge_request_link_enabled,
                "public_builds": public_builds,
                "releases_access_level": releases_access_level,
                "remove_source_branch_after_merge": remove_source_branch_after_merge,
                "repository_access_level": repository_access_level,
                "repository_storage": repository_storage,
                "request_access_enabled": request_access_enabled,
                "requirements_access_level": requirements_access_level,
                "resolve_outdated_diff_discussions": resolve_outdated_diff_discussions,
                "restrict_user_defined_variables": restrict_user_defined_variables,
                "security_and_compliance_access_level": security_and_compliance_access_level,
                "service_desk_enabled": service_desk_enabled,
                "shared_runners_enabled": shared_runners_enabled,
                "snippets_access_level": snippets_access_level,
                "squash_commit_template": squash_commit_template,
                "squash_option": squash_option,
                "suggestion_commit_message": suggestion_commit_message,
                "tag_list": tag_list,
                "topics": topics,
                "visibility": visibility,
                "archived": archived,
                "id_after": id_after,
                "id_before": id_before,
                "imported": imported,
                "include_hidden": include_hidden,
                "include_pending_delete": include_pending_delete,
                "membership": membership,
                "search": search,
                "sort": sort,
                "min_access_level": min_access_level,
                "owned": owned,
                "statistics": statistics,
                "simple": simple,
                "starred": starred,
                "topic": topic,
                "topic_id": topic_id,
                "repository_checksum_failed": repository_checksum_failed,
                "allowed_to_create": allowed_to_create,
                "deploy_access_levels": deploy_access_levels,
                "approval_rules": approval_rules,
                "search_namespaces": search_namespaces,
                "environment_id": environment_id,
                "environment_name": environment_name,
                "wiki_access_level": wiki_access_level,
                "create_access_level": create_access_level,
                "cluster_agent_id": cluster_agent_id,
                "external_url": external_url,
                "tier": tier,
                "kubernetes_namespace": kubernetes_namespace,
                "flux_resource_path": flux_resource_path,
                "auto_stop_setting": auto_stop_setting,
                "states": states,
                "before": before,
                "limit": limit,
                "dry_run": dry_run,
                "force": force,
                "pipeline_schedule_id": pipeline_schedule_id,
                "cron": cron,
                "cron_timezone": cron_timezone,
                "id": id,
                "ref": ref,
                "active": active,
                "key": key,
                "value": value,
                "variable_type": variable_type,
                "data": data,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}",
                json=project.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_groups(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        allow_merge_on_skipped_pipeline: bool | None = None,
        only_allow_merge_if_all_status_checks_passed: bool | None = None,
        analytics_access_level: str | None = None,
        approvals_before_merge: int | None = None,
        auto_cancel_pending_pipelines: str | None = None,
        auto_devops_deploy_strategy: str | None = None,
        auto_devops_enabled: bool | None = None,
        autoclose_referenced_issues: bool | None = None,
        avatar: str | None = None,
        build_git_strategy: str | None = None,
        build_timeout: int | None = None,
        builds_access_level: str | None = None,
        ci_config_path: str | None = None,
        ci_default_git_depth: int | None = None,
        ci_forward_deployment_enabled: bool | None = None,
        ci_allow_fork_pipelines_to_run_in_parent_project: bool | None = None,
        ci_separated_caches: bool | None = None,
        container_expiration_policy_attributes: str | None = None,
        container_registry_access_level: str | None = None,
        default_branch: str | None = None,
        description: str | None = None,
        emails_disabled: bool | None = None,
        enforce_auth_checks_on_uploads: bool | None = None,
        external_authorization_classification_label: str | None = None,
        expires_at: str | None = None,
        forking_access_level: str | None = None,
        group_access: int | None = None,
        import_url: Any = None,
        issues_access_level: str | None = None,
        issues_template: str | None = None,
        keep_latest_artifact: bool | None = None,
        lfs_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        merge_commit_template: str | None = None,
        merge_method: str | None = None,
        merge_pipelines_enabled: bool | None = None,
        merge_requests_access_level: str | None = None,
        merge_requests_template: str | None = None,
        merge_trains_enabled: bool | None = None,
        mirror_overwrites_diverged_branches: bool | None = None,
        mirror_trigger_builds: bool | None = None,
        mirror_user_id: int | str | None = None,
        mirror: bool | None = None,
        mr_default_target_self: bool | None = None,
        name: str | None = None,
        tag_name: str | None = None,
        order_by: str | None = None,
        only_allow_merge_if_all_discussions_are_resolved: bool | None = None,
        only_allow_merge_if_pipeline_succeeds: bool | None = None,
        only_mirror_protected_branches: bool | None = None,
        operations_access_level: str | None = None,
        packages_enabled: bool | None = None,
        pages_access_level: str | None = None,
        path: str | None = None,
        printing_merge_request_link_enabled: bool | None = None,
        public_builds: bool | None = None,
        releases_access_level: str | None = None,
        remove_source_branch_after_merge: bool | None = None,
        repository_access_level: str | None = None,
        repository_storage: str | None = None,
        request_access_enabled: bool | None = None,
        requirements_access_level: str | None = None,
        resolve_outdated_diff_discussions: bool | None = None,
        restrict_user_defined_variables: bool | None = None,
        security_and_compliance_access_level: str | None = None,
        service_desk_enabled: bool | None = None,
        shared_runners_enabled: bool | None = None,
        snippets_access_level: str | None = None,
        squash_commit_template: str | None = None,
        squash_option: str | None = None,
        suggestion_commit_message: str | None = None,
        tag_list: list[str] | None = None,
        topics: list[str] | None = None,
        visibility: str | None = None,
        archived: bool | None = None,
        id_after: int | None = None,
        id_before: int | None = None,
        imported: bool | None = None,
        include_hidden: bool | None = None,
        include_pending_delete: bool | None = None,
        membership: bool | None = None,
        search: str | None = None,
        sort: str | None = None,
        min_access_level: int | None = None,
        owned: bool | None = None,
        statistics: bool | None = None,
        simple: bool | None = None,
        starred: bool | None = None,
        topic: str | None = None,
        topic_id: int | str | None = None,
        repository_checksum_failed: bool | None = None,
        allowed_to_create: list[dict[str, Any]] | None = None,
        deploy_access_levels: list[dict[str, Any]] | None = None,
        approval_rules: list[dict[str, Any]] | None = None,
        search_namespaces: bool | None = None,
        environment_id: int | str | None = None,
        environment_name: str | None = None,
        wiki_access_level: str | None = None,
        create_access_level: int | None = None,
        cluster_agent_id: str | None = None,
        external_url: str | None = None,
        tier: str | None = None,
        kubernetes_namespace: str | None = None,
        flux_resource_path: str | None = None,
        auto_stop_setting: str | None = None,
        states: str | None = None,
        before: str | None = None,
        limit: int | None = None,
        dry_run: int | None = None,
        force: bool | None = None,
        pipeline_schedule_id: int | str | None = None,
        cron: str | None = None,
        cron_timezone: str | None = None,
        id: int | str | None = None,
        ref: str | None = None,
        active: bool | None = None,
        key: str | None = None,
        value: str | None = None,
        variable_type: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get groups associated with a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Group models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "allow_merge_on_skipped_pipeline": allow_merge_on_skipped_pipeline,
                "only_allow_merge_if_all_status_checks_passed": only_allow_merge_if_all_status_checks_passed,
                "analytics_access_level": analytics_access_level,
                "approvals_before_merge": approvals_before_merge,
                "auto_cancel_pending_pipelines": auto_cancel_pending_pipelines,
                "auto_devops_deploy_strategy": auto_devops_deploy_strategy,
                "auto_devops_enabled": auto_devops_enabled,
                "autoclose_referenced_issues": autoclose_referenced_issues,
                "avatar": avatar,
                "build_git_strategy": build_git_strategy,
                "build_timeout": build_timeout,
                "builds_access_level": builds_access_level,
                "ci_config_path": ci_config_path,
                "ci_default_git_depth": ci_default_git_depth,
                "ci_forward_deployment_enabled": ci_forward_deployment_enabled,
                "ci_allow_fork_pipelines_to_run_in_parent_project": ci_allow_fork_pipelines_to_run_in_parent_project,
                "ci_separated_caches": ci_separated_caches,
                "container_expiration_policy_attributes": container_expiration_policy_attributes,
                "container_registry_access_level": container_registry_access_level,
                "default_branch": default_branch,
                "description": description,
                "emails_disabled": emails_disabled,
                "enforce_auth_checks_on_uploads": enforce_auth_checks_on_uploads,
                "external_authorization_classification_label": external_authorization_classification_label,
                "expires_at": expires_at,
                "forking_access_level": forking_access_level,
                "group_access": group_access,
                "import_url": import_url,
                "issues_access_level": issues_access_level,
                "issues_template": issues_template,
                "keep_latest_artifact": keep_latest_artifact,
                "lfs_enabled": lfs_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "merge_commit_template": merge_commit_template,
                "merge_method": merge_method,
                "merge_pipelines_enabled": merge_pipelines_enabled,
                "merge_requests_access_level": merge_requests_access_level,
                "merge_requests_template": merge_requests_template,
                "merge_trains_enabled": merge_trains_enabled,
                "mirror_overwrites_diverged_branches": mirror_overwrites_diverged_branches,
                "mirror_trigger_builds": mirror_trigger_builds,
                "mirror_user_id": mirror_user_id,
                "mirror": mirror,
                "mr_default_target_self": mr_default_target_self,
                "name": name,
                "tag_name": tag_name,
                "order_by": order_by,
                "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
                "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
                "only_mirror_protected_branches": only_mirror_protected_branches,
                "operations_access_level": operations_access_level,
                "packages_enabled": packages_enabled,
                "pages_access_level": pages_access_level,
                "path": path,
                "printing_merge_request_link_enabled": printing_merge_request_link_enabled,
                "public_builds": public_builds,
                "releases_access_level": releases_access_level,
                "remove_source_branch_after_merge": remove_source_branch_after_merge,
                "repository_access_level": repository_access_level,
                "repository_storage": repository_storage,
                "request_access_enabled": request_access_enabled,
                "requirements_access_level": requirements_access_level,
                "resolve_outdated_diff_discussions": resolve_outdated_diff_discussions,
                "restrict_user_defined_variables": restrict_user_defined_variables,
                "security_and_compliance_access_level": security_and_compliance_access_level,
                "service_desk_enabled": service_desk_enabled,
                "shared_runners_enabled": shared_runners_enabled,
                "snippets_access_level": snippets_access_level,
                "squash_commit_template": squash_commit_template,
                "squash_option": squash_option,
                "suggestion_commit_message": suggestion_commit_message,
                "tag_list": tag_list,
                "topics": topics,
                "visibility": visibility,
                "archived": archived,
                "id_after": id_after,
                "id_before": id_before,
                "imported": imported,
                "include_hidden": include_hidden,
                "include_pending_delete": include_pending_delete,
                "membership": membership,
                "search": search,
                "sort": sort,
                "min_access_level": min_access_level,
                "owned": owned,
                "statistics": statistics,
                "simple": simple,
                "starred": starred,
                "topic": topic,
                "topic_id": topic_id,
                "repository_checksum_failed": repository_checksum_failed,
                "allowed_to_create": allowed_to_create,
                "deploy_access_levels": deploy_access_levels,
                "approval_rules": approval_rules,
                "search_namespaces": search_namespaces,
                "environment_id": environment_id,
                "environment_name": environment_name,
                "wiki_access_level": wiki_access_level,
                "create_access_level": create_access_level,
                "cluster_agent_id": cluster_agent_id,
                "external_url": external_url,
                "tier": tier,
                "kubernetes_namespace": kubernetes_namespace,
                "flux_resource_path": flux_resource_path,
                "auto_stop_setting": auto_stop_setting,
                "states": states,
                "before": before,
                "limit": limit,
                "dry_run": dry_run,
                "force": force,
                "pipeline_schedule_id": pipeline_schedule_id,
                "cron": cron,
                "cron_timezone": cron_timezone,
                "id": id,
                "ref": ref,
                "active": active,
                "key": key,
                "value": value,
                "variable_type": variable_type,
                "data": data,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/groups",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Group(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def archive_project(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Archive a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/archive",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def unarchive_project(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Unarchive a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/unarchive",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_project(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Delete a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def share_project(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        allow_merge_on_skipped_pipeline: bool | None = None,
        only_allow_merge_if_all_status_checks_passed: bool | None = None,
        analytics_access_level: str | None = None,
        approvals_before_merge: int | None = None,
        auto_cancel_pending_pipelines: str | None = None,
        auto_devops_deploy_strategy: str | None = None,
        auto_devops_enabled: bool | None = None,
        autoclose_referenced_issues: bool | None = None,
        avatar: str | None = None,
        build_git_strategy: str | None = None,
        build_timeout: int | None = None,
        builds_access_level: str | None = None,
        ci_config_path: str | None = None,
        ci_default_git_depth: int | None = None,
        ci_forward_deployment_enabled: bool | None = None,
        ci_allow_fork_pipelines_to_run_in_parent_project: bool | None = None,
        ci_separated_caches: bool | None = None,
        container_expiration_policy_attributes: str | None = None,
        container_registry_access_level: str | None = None,
        default_branch: str | None = None,
        description: str | None = None,
        emails_disabled: bool | None = None,
        enforce_auth_checks_on_uploads: bool | None = None,
        external_authorization_classification_label: str | None = None,
        expires_at: str | None = None,
        forking_access_level: str | None = None,
        group_access: int | None = None,
        import_url: Any = None,
        issues_access_level: str | None = None,
        issues_template: str | None = None,
        keep_latest_artifact: bool | None = None,
        lfs_enabled: bool | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        merge_commit_template: str | None = None,
        merge_method: str | None = None,
        merge_pipelines_enabled: bool | None = None,
        merge_requests_access_level: str | None = None,
        merge_requests_template: str | None = None,
        merge_trains_enabled: bool | None = None,
        mirror_overwrites_diverged_branches: bool | None = None,
        mirror_trigger_builds: bool | None = None,
        mirror_user_id: int | str | None = None,
        mirror: bool | None = None,
        mr_default_target_self: bool | None = None,
        name: str | None = None,
        tag_name: str | None = None,
        order_by: str | None = None,
        only_allow_merge_if_all_discussions_are_resolved: bool | None = None,
        only_allow_merge_if_pipeline_succeeds: bool | None = None,
        only_mirror_protected_branches: bool | None = None,
        operations_access_level: str | None = None,
        packages_enabled: bool | None = None,
        pages_access_level: str | None = None,
        path: str | None = None,
        printing_merge_request_link_enabled: bool | None = None,
        public_builds: bool | None = None,
        releases_access_level: str | None = None,
        remove_source_branch_after_merge: bool | None = None,
        repository_access_level: str | None = None,
        repository_storage: str | None = None,
        request_access_enabled: bool | None = None,
        requirements_access_level: str | None = None,
        resolve_outdated_diff_discussions: bool | None = None,
        restrict_user_defined_variables: bool | None = None,
        security_and_compliance_access_level: str | None = None,
        service_desk_enabled: bool | None = None,
        shared_runners_enabled: bool | None = None,
        snippets_access_level: str | None = None,
        squash_commit_template: str | None = None,
        squash_option: str | None = None,
        suggestion_commit_message: str | None = None,
        tag_list: list[str] | None = None,
        topics: list[str] | None = None,
        visibility: str | None = None,
        archived: bool | None = None,
        id_after: int | None = None,
        id_before: int | None = None,
        imported: bool | None = None,
        include_hidden: bool | None = None,
        include_pending_delete: bool | None = None,
        membership: bool | None = None,
        search: str | None = None,
        sort: str | None = None,
        min_access_level: int | None = None,
        owned: bool | None = None,
        statistics: bool | None = None,
        simple: bool | None = None,
        starred: bool | None = None,
        topic: str | None = None,
        topic_id: int | str | None = None,
        repository_checksum_failed: bool | None = None,
        allowed_to_create: list[dict[str, Any]] | None = None,
        deploy_access_levels: list[dict[str, Any]] | None = None,
        approval_rules: list[dict[str, Any]] | None = None,
        search_namespaces: bool | None = None,
        environment_id: int | str | None = None,
        environment_name: str | None = None,
        wiki_access_level: str | None = None,
        create_access_level: int | None = None,
        cluster_agent_id: str | None = None,
        external_url: str | None = None,
        tier: str | None = None,
        kubernetes_namespace: str | None = None,
        flux_resource_path: str | None = None,
        auto_stop_setting: str | None = None,
        states: str | None = None,
        before: str | None = None,
        limit: int | None = None,
        dry_run: int | None = None,
        force: bool | None = None,
        pipeline_schedule_id: int | str | None = None,
        cron: str | None = None,
        cron_timezone: str | None = None,
        id: int | str | None = None,
        ref: str | None = None,
        active: bool | None = None,
        key: str | None = None,
        value: str | None = None,
        variable_type: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Share a specific project with a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, group_id, group_access).

        Returns:
            Response: A wrapper containing the original response and a Project model.

        Raises:
            MissingParameterError: If the project_id, group_id, or group_access is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "allow_merge_on_skipped_pipeline": allow_merge_on_skipped_pipeline,
                "only_allow_merge_if_all_status_checks_passed": only_allow_merge_if_all_status_checks_passed,
                "analytics_access_level": analytics_access_level,
                "approvals_before_merge": approvals_before_merge,
                "auto_cancel_pending_pipelines": auto_cancel_pending_pipelines,
                "auto_devops_deploy_strategy": auto_devops_deploy_strategy,
                "auto_devops_enabled": auto_devops_enabled,
                "autoclose_referenced_issues": autoclose_referenced_issues,
                "avatar": avatar,
                "build_git_strategy": build_git_strategy,
                "build_timeout": build_timeout,
                "builds_access_level": builds_access_level,
                "ci_config_path": ci_config_path,
                "ci_default_git_depth": ci_default_git_depth,
                "ci_forward_deployment_enabled": ci_forward_deployment_enabled,
                "ci_allow_fork_pipelines_to_run_in_parent_project": ci_allow_fork_pipelines_to_run_in_parent_project,
                "ci_separated_caches": ci_separated_caches,
                "container_expiration_policy_attributes": container_expiration_policy_attributes,
                "container_registry_access_level": container_registry_access_level,
                "default_branch": default_branch,
                "description": description,
                "emails_disabled": emails_disabled,
                "enforce_auth_checks_on_uploads": enforce_auth_checks_on_uploads,
                "external_authorization_classification_label": external_authorization_classification_label,
                "expires_at": expires_at,
                "forking_access_level": forking_access_level,
                "group_access": group_access,
                "import_url": import_url,
                "issues_access_level": issues_access_level,
                "issues_template": issues_template,
                "keep_latest_artifact": keep_latest_artifact,
                "lfs_enabled": lfs_enabled,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "merge_commit_template": merge_commit_template,
                "merge_method": merge_method,
                "merge_pipelines_enabled": merge_pipelines_enabled,
                "merge_requests_access_level": merge_requests_access_level,
                "merge_requests_template": merge_requests_template,
                "merge_trains_enabled": merge_trains_enabled,
                "mirror_overwrites_diverged_branches": mirror_overwrites_diverged_branches,
                "mirror_trigger_builds": mirror_trigger_builds,
                "mirror_user_id": mirror_user_id,
                "mirror": mirror,
                "mr_default_target_self": mr_default_target_self,
                "name": name,
                "tag_name": tag_name,
                "order_by": order_by,
                "only_allow_merge_if_all_discussions_are_resolved": only_allow_merge_if_all_discussions_are_resolved,
                "only_allow_merge_if_pipeline_succeeds": only_allow_merge_if_pipeline_succeeds,
                "only_mirror_protected_branches": only_mirror_protected_branches,
                "operations_access_level": operations_access_level,
                "packages_enabled": packages_enabled,
                "pages_access_level": pages_access_level,
                "path": path,
                "printing_merge_request_link_enabled": printing_merge_request_link_enabled,
                "public_builds": public_builds,
                "releases_access_level": releases_access_level,
                "remove_source_branch_after_merge": remove_source_branch_after_merge,
                "repository_access_level": repository_access_level,
                "repository_storage": repository_storage,
                "request_access_enabled": request_access_enabled,
                "requirements_access_level": requirements_access_level,
                "resolve_outdated_diff_discussions": resolve_outdated_diff_discussions,
                "restrict_user_defined_variables": restrict_user_defined_variables,
                "security_and_compliance_access_level": security_and_compliance_access_level,
                "service_desk_enabled": service_desk_enabled,
                "shared_runners_enabled": shared_runners_enabled,
                "snippets_access_level": snippets_access_level,
                "squash_commit_template": squash_commit_template,
                "squash_option": squash_option,
                "suggestion_commit_message": suggestion_commit_message,
                "tag_list": tag_list,
                "topics": topics,
                "visibility": visibility,
                "archived": archived,
                "id_after": id_after,
                "id_before": id_before,
                "imported": imported,
                "include_hidden": include_hidden,
                "include_pending_delete": include_pending_delete,
                "membership": membership,
                "search": search,
                "sort": sort,
                "min_access_level": min_access_level,
                "owned": owned,
                "statistics": statistics,
                "simple": simple,
                "starred": starred,
                "topic": topic,
                "topic_id": topic_id,
                "repository_checksum_failed": repository_checksum_failed,
                "allowed_to_create": allowed_to_create,
                "deploy_access_levels": deploy_access_levels,
                "approval_rules": approval_rules,
                "search_namespaces": search_namespaces,
                "environment_id": environment_id,
                "environment_name": environment_name,
                "wiki_access_level": wiki_access_level,
                "create_access_level": create_access_level,
                "cluster_agent_id": cluster_agent_id,
                "external_url": external_url,
                "tier": tier,
                "kubernetes_namespace": kubernetes_namespace,
                "flux_resource_path": flux_resource_path,
                "auto_stop_setting": auto_stop_setting,
                "states": states,
                "before": before,
                "limit": limit,
                "dry_run": dry_run,
                "force": force,
                "pipeline_schedule_id": pipeline_schedule_id,
                "cron": cron,
                "cron_timezone": cron_timezone,
                "id": id,
                "ref": ref,
                "active": active,
                "key": key,
                "value": value,
                "variable_type": variable_type,
                "data": data,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if (
            project.project_id is None
            or project.group_id is None
            or project.group_access is None
        ):
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/share",
                json=project.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Project(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_shared_project_link(
        self,
        *,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Unshare a specific project from a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, group_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "group_id": group_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/share/{project.group_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_project_runners(
        self,
        *,
        runner_id: str | int | None = None,
        description: str | None = None,
        active: bool | None = None,
        paused: bool | None = None,
        tag_list: list[str] | None = None,
        run_untagged: bool | None = None,
        locked: bool | None = None,
        access_level: str | None = None,
        maintenance_note: str | None = None,
        info: str | None = None,
        token: str | None = None,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        maximum_timeout: int | None = None,
        runner_type: str | None = None,
        status: str | None = None,
        all_runners: bool | None = None,
        max_pages: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get information about runners in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Runner models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "runner_id": runner_id,
                "description": description,
                "active": active,
                "paused": paused,
                "tag_list": tag_list,
                "run_untagged": run_untagged,
                "locked": locked,
                "access_level": access_level,
                "maintenance_note": maintenance_note,
                "info": info,
                "token": token,
                "project_id": project_id,
                "group_id": group_id,
                "maximum_timeout": maximum_timeout,
                "runner_type": runner_type,
                "status": status,
                "all_runners": all_runners,
                "max_pages": max_pages,
                "data": data,
            }.items()
            if v is not None
        }
        runner = RunnerModel(**kwargs)
        if runner.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{runner.project_id}/runners",
                model=runner,
                id_field="project_id",
                id_value=runner.project_id,
            )
            parsed_data = [Runner(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def enable_project_runner(
        self,
        *,
        runner_id: str | int | None = None,
        description: str | None = None,
        active: bool | None = None,
        paused: bool | None = None,
        tag_list: list[str] | None = None,
        run_untagged: bool | None = None,
        locked: bool | None = None,
        access_level: str | None = None,
        maintenance_note: str | None = None,
        info: str | None = None,
        token: str | None = None,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        maximum_timeout: int | None = None,
        runner_type: str | None = None,
        status: str | None = None,
        all_runners: bool | None = None,
        max_pages: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Enable a runner in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, runner_id).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the project_id or runner_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "runner_id": runner_id,
                "description": description,
                "active": active,
                "paused": paused,
                "tag_list": tag_list,
                "run_untagged": run_untagged,
                "locked": locked,
                "access_level": access_level,
                "maintenance_note": maintenance_note,
                "info": info,
                "token": token,
                "project_id": project_id,
                "group_id": group_id,
                "maximum_timeout": maximum_timeout,
                "runner_type": runner_type,
                "status": status,
                "all_runners": all_runners,
                "max_pages": max_pages,
                "data": data,
            }.items()
            if v is not None
        }
        runner = RunnerModel(**kwargs)
        if runner.project_id is None or runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{runner.project_id}/runners",
                headers=self.headers,
                json=runner.data,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_project_runner(
        self,
        *,
        runner_id: str | int | None = None,
        description: str | None = None,
        active: bool | None = None,
        paused: bool | None = None,
        tag_list: list[str] | None = None,
        run_untagged: bool | None = None,
        locked: bool | None = None,
        access_level: str | None = None,
        maintenance_note: str | None = None,
        info: str | None = None,
        token: str | None = None,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        maximum_timeout: int | None = None,
        runner_type: str | None = None,
        status: str | None = None,
        all_runners: bool | None = None,
        max_pages: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Delete a runner from a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, runner_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or runner_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "runner_id": runner_id,
                "description": description,
                "active": active,
                "paused": paused,
                "tag_list": tag_list,
                "run_untagged": run_untagged,
                "locked": locked,
                "access_level": access_level,
                "maintenance_note": maintenance_note,
                "info": info,
                "token": token,
                "project_id": project_id,
                "group_id": group_id,
                "maximum_timeout": maximum_timeout,
                "runner_type": runner_type,
                "status": status,
                "all_runners": all_runners,
                "max_pages": max_pages,
                "data": data,
            }.items()
            if v is not None
        }
        runner = RunnerModel(**kwargs)
        if runner.project_id is None or runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{runner.project_id}/runners/{runner.runner_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def reset_project_runner_token(
        self,
        *,
        runner_id: str | int | None = None,
        description: str | None = None,
        active: bool | None = None,
        paused: bool | None = None,
        tag_list: list[str] | None = None,
        run_untagged: bool | None = None,
        locked: bool | None = None,
        access_level: str | None = None,
        maintenance_note: str | None = None,
        info: str | None = None,
        token: str | None = None,
        project_id: int | str | None = None,
        group_id: int | str | None = None,
        maximum_timeout: int | None = None,
        runner_type: str | None = None,
        status: str | None = None,
        all_runners: bool | None = None,
        max_pages: int | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Reset registration token for a project's runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and the raw token data.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "runner_id": runner_id,
                "description": description,
                "active": active,
                "paused": paused,
                "tag_list": tag_list,
                "run_untagged": run_untagged,
                "locked": locked,
                "access_level": access_level,
                "maintenance_note": maintenance_note,
                "info": info,
                "token": token,
                "project_id": project_id,
                "group_id": group_id,
                "maximum_timeout": maximum_timeout,
                "runner_type": runner_type,
                "status": status,
                "all_runners": all_runners,
                "max_pages": max_pages,
                "data": data,
            }.items()
            if v is not None
        }
        runner = RunnerModel(**kwargs)
        if runner.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{runner.project_id}/runners/reset_registration_token",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
