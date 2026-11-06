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
    def get_deploy_tokens(
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
        Get all deploy tokens.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of DeployToken models.

        Raises:
            ParameterError: If the request fails or returns invalid data.
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
            raise ParameterError(
                f"Failed to get deploy tokens: {type(e).__name__}"
            ) from e

    def get_environments(
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
        Get a list of environments for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Environment models.

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
                endpoint=f"/projects/{project.project_id}/environments",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Environment(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_environment(
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
        Get details of a specific environment.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
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

    def create_environment(
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
        Create a new environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

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

    def update_environment(
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
        Update an existing environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
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

    def delete_environment(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        environment_id: int | str | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "environment_id": environment_id,
            }.items()
            if v is not None
        }
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

    def stop_environment(
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
        Stop an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, environment_id).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

        Raises:
            MissingParameterError: If the project_id or environment_id is missing.
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

    def stop_stale_environments(
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
        Stop stale environments for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

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
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/environments/stop_stale",
                headers=self.headers,
                params=project.api_parameters,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_stopped_environments(
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
        Delete stopped environments (review apps) for a project.

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
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/environments/review_apps",
                headers=self.headers,
                params=project.api_parameters,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_protected_environments(
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
        Get a list of protected environments for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Environment models.

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
                endpoint=f"/projects/{project.project_id}/protected_environments",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Environment(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_protected_environment(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        name: str | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "name": name,
            }.items()
            if v is not None
        }
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

    def protect_environment(
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
        Protect an environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

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

    def update_protected_environment(
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
        Update a protected environment for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and an Environment model.

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
                url=f"{self.url}/projects/{project.project_id}/protected_environments/{project.name}",
                headers=self.headers,
                json=project.data,
            )
            response.raise_for_status()
            parsed_data = Environment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def unprotect_environment(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        name: str | None = None,
    ) -> Response:
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
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "name": name,
            }.items()
            if v is not None
        }
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

    def get_releases(
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
        Get information about releases in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Release models.

        Raises:
            MissingParameterError: If the project_id is missing.
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

    def get_latest_release(
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
        Get information about the latest release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id is missing.
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

    def get_latest_release_evidence(
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
        Get evidence for the latest release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and the raw evidence data.

        Raises:
            MissingParameterError: If the project_id is missing.
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

    def get_latest_release_asset(
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
        Get the asset for the latest release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, direct_asset_path).

        Returns:
            Response: A wrapper containing the original response and the raw asset data.

        Raises:
            MissingParameterError: If the project_id or direct_asset_path is missing.
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

    def download_release_asset(
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
        Download a release asset from a group's release.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id, tag_name, direct_asset_path).

        Returns:
            Response: A wrapper containing the original response and the raw asset data.

        Raises:
            MissingParameterError: If the group_id, tag_name, or direct_asset_path is missing.
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

    def create_release(
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
        Create a new release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
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

    def create_release_evidence(
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
        Create evidence for a release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
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

    def update_release(
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
        Update information about a release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response and a Release model.

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
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

    def delete_release(
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
        Delete a release in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, tag_name).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or tag_name is missing.
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
