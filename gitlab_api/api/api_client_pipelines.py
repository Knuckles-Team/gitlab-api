#!/usr/bin/python

import logging
from typing import Any, TypeVar

from pydantic import ValidationError

logger = logging.getLogger(__name__)

from scion_sdk.exceptions import (
    MissingParameterError,
    ParameterError,
)

from gitlab_api.gitlab_input_models import (
    JobModel,
    PipelineModel,
    ProjectModel,
    RunnerModel,
)
from gitlab_api.gitlab_response_models import (
    Job,
    Pipeline,
    PipelineSchedule,
    PipelineVariable,
    Response,
    Runner,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiPipelines(GitLabApiBase):
    def get_pipeline_jobs(
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
        Get jobs associated with a specific pipeline within a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_id).

        Returns:
            Response: A wrapper containing the original response and a list of Job models.

        Raises:
            MissingParameterError: If the project_id or pipeline_id is missing.
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
        if job.project_id is None or job.pipeline_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{job.project_id}/pipelines/{job.pipeline_id}/jobs",
                model=job,
                id_field="project_id",
                id_value=job.project_id,
            )
            parsed_data = [Job(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_pipelines(
        self,
        *,
        project_id: int | str | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        status: str | None = None,
        pipeline_id: int | str | None = None,
        ref: str | None = None,
        variables: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get information about pipelines for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Pipeline models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "status": status,
                "pipeline_id": pipeline_id,
                "ref": ref,
                "variables": variables,
                "data": data,
            }.items()
            if v is not None
        }
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{pipeline.project_id}/pipelines",
                model=pipeline,
                id_field="project_id",
                id_value=pipeline.project_id,
            )
            parsed_data = [Pipeline(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_pipeline(
        self,
        *,
        project_id: int | str | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        status: str | None = None,
        pipeline_id: int | str | None = None,
        ref: str | None = None,
        variables: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Get information about a specific pipeline in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_id).

        Returns:
            Response: A wrapper containing the original response and a Pipeline model.

        Raises:
            MissingParameterError: If the project_id or pipeline_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "status": status,
                "pipeline_id": pipeline_id,
                "ref": ref,
                "variables": variables,
                "data": data,
            }.items()
            if v is not None
        }
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None or pipeline.pipeline_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{pipeline.project_id}/pipelines/{pipeline.pipeline_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Pipeline(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def run_pipeline(
        self,
        *,
        project_id: int | str | None = None,
        total_pages: int | None = None,
        max_pages: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
        status: str | None = None,
        pipeline_id: int | str | None = None,
        ref: str | None = None,
        variables: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """
        Run a pipeline for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, ref).

        Returns:
            Response: A wrapper containing the original response and a Pipeline model.

        Raises:
            MissingParameterError: If the project_id or ref is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "total_pages": total_pages,
                "max_pages": max_pages,
                "per_page": per_page,
                "page": page,
                "status": status,
                "pipeline_id": pipeline_id,
                "ref": ref,
                "variables": variables,
                "data": data,
            }.items()
            if v is not None
        }
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None or pipeline.ref is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{pipeline.project_id}/pipeline",
                headers=self.headers,
                json=pipeline.data,
            )
            response.raise_for_status()
            parsed_data = Pipeline(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_pipeline_schedules(
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
        Get pipeline schedules for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of PipelineSchedule models.

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
                endpoint="/projects/{id}/pipeline_schedules",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [PipelineSchedule(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_pipeline_schedule(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        pipeline_schedule_id: int | str | None = None,
    ) -> Response:
        """
        Get information about a specific pipeline schedule in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response and a PipelineSchedule model.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "pipeline_schedule_id": pipeline_schedule_id,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_pipelines_triggered_from_schedule(
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
        Get pipelines triggered from a specific pipeline schedule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response and a list of Pipeline models.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
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
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/pipelines",
                model=project,
                id_field="project_id",
                id_value=project.project_id,
            )
            parsed_data = [Pipeline(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_pipeline_schedule(
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
        Create a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a PipelineSchedule model.

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
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules",
                json=project.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def edit_pipeline_schedule(
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
        Edit a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response and a PipelineSchedule model.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
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
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}",
                json=project.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def take_pipeline_schedule_ownership(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        pipeline_schedule_id: int | str | None = None,
    ) -> Response:
        """
        Take ownership of a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response and a PipelineSchedule model.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "pipeline_schedule_id": pipeline_schedule_id,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/take_ownership",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_pipeline_schedule(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        pipeline_schedule_id: int | str | None = None,
    ) -> Response:
        """
        Delete a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "pipeline_schedule_id": pipeline_schedule_id,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def run_pipeline_schedule(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        pipeline_schedule_id: int | str | None = None,
    ) -> Response:
        """
        Run a pipeline schedule for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "pipeline_schedule_id": pipeline_schedule_id,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/play",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_pipeline_schedule_variable(
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
        Create a variable for a pipeline schedule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id, key).

        Returns:
            Response: A wrapper containing the original response and a PipelineVariable model.

        Raises:
            MissingParameterError: If the project_id or pipeline_schedule_id is missing.
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
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/variables",
                json=project.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = PipelineVariable(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_pipeline_schedule_variable(
        self,
        *,
        project_id: int | str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
        pipeline_schedule_id: int | str | None = None,
        key: str | None = None,
    ) -> Response:
        """
        Delete a variable from a pipeline schedule.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, pipeline_schedule_id, key).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id, pipeline_schedule_id, or key is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
                "pipeline_schedule_id": pipeline_schedule_id,
                "key": key,
            }.items()
            if v is not None
        }
        project = ProjectModel(**kwargs)
        if (
            project.project_id is None
            or project.pipeline_schedule_id is None
            or project.key is None
        ):
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/variables/{project.key}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_runners(
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
        Get information about runners.

        Args:
            **kwargs: Additional parameters for the request (e.g., scope, status).

        Returns:
            Response: A wrapper containing the original response and a list of Runner models.

        Raises:
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
        try:
            response, data = self._fetch_all_pages(
                endpoint="/runners",
                model=runner,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Runner(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_runner(
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
        Get information about a specific runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the runner_id is missing.
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
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_runner_details(
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
        Update details for a specific runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the runner_id is missing.
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
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
                json=runner.data,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def pause_runner(
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
        Pause or unpause a specific runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id, active).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the runner_id or active status is missing.
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
        if runner.runner_id is None or runner.active is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
                json=runner.data,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_runner_jobs(
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
        Get jobs for a specific runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id).

        Returns:
            Response: A wrapper containing the original response and a list of Job models.

        Raises:
            MissingParameterError: If the runner_id is missing.
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
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/runners/{runner.runner_id}/jobs",
                model=runner,
                id_field="runner_id",
                id_value=runner.runner_id,
            )
            parsed_data = [Job(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_group_runners(
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
        Get information about runners in a group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of Runner models.

        Raises:
            MissingParameterError: If the group_id is missing.
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
        if runner.group_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{runner.group_id}/runners",
                model=runner,
                id_field="group_id",
                id_value=runner.group_id,
            )
            parsed_data = [Runner(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def register_new_runner(
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
        Register a new runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., token).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the token is missing.
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
        if runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/runners",
                headers=self.headers,
                json=runner.data,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_runner(
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
        Delete a runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id, token).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the runner_id or token is missing.
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
        if runner.runner_id is None and runner.token is None:
            raise MissingParameterError
        try:
            if runner.runner_id:
                response = self._session.delete(
                    url=f"{self.url}/runners/{runner.runner_id}",
                    headers=self.headers,
                )
            else:
                response = self._session.delete(
                    url=f"{self.url}/runners",
                    headers=self.headers,
                    json=runner.data,
                )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def verify_runner_authentication(
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
        Verify runner authentication.

        Args:
            **kwargs: Additional parameters for the request (e.g., token).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the token is missing.
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
        if runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/runners/verify",
                headers=self.headers,
                json=runner.data,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def reset_gitlab_runner_token(self) -> Response:
        """
        Reset GitLab runner registration token.

        Returns:
            Response: A wrapper containing the original response and the raw token data.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        try:
            response = self._session.post(
                url=f"{self.url}/runners/reset_registration_token",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def reset_group_runner_token(
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
        Reset registration token for a group's runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and the raw token data.

        Raises:
            MissingParameterError: If the group_id is missing.
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
        if runner.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/groups/{runner.group_id}/runners/reset_registration_token",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
