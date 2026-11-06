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
    GroupModel,
    MergeRequestModel,
    MergeRequestRuleModel,
)
from gitlab_api.gitlab_response_models import (
    ApprovalRule,
    MergeRequest,
    Response,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiMergeRequests(GitLabApiBase):
    def get_group_merge_requests(
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
        Get merge requests associated with a specific group.

        Args:
            **kwargs: Additional parameters for the request (e.g., group_id).

        Returns:
            Response: A wrapper containing the original response and a list of MergeRequest models.

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
                endpoint="/groups/{id}/merge_requests",
                model=group,
                id_field="group_id",
                id_value=group.group_id,
            )
            parsed_data = [MergeRequest(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_merge_request(
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
        Create a new merge request.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, source_branch, target_branch, title).

        Returns:
            Response: A wrapper containing the original response and a MergeRequest model.

        Raises:
            MissingParameterError: If the project_id, source_branch, target_branch, or title is missing.
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
        if (
            merge_request.project_id is None
            or merge_request.source_branch is None
            or merge_request.target_branch is None
            or merge_request.title is None
        ):
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_request.project_id}/merge_requests",
                headers=self.headers,
                json=merge_request.data,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_merge_requests(
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
        Get a list of merge requests.

        Args:
            **kwargs: Additional parameters for the request (e.g., state, scope).

        Returns:
            Response: A wrapper containing the original response and a list of MergeRequest models.

        Raises:
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
        try:
            response, data = self._fetch_all_pages(
                endpoint="/merge_requests",
                model=merge_request,
                id_field=None,
                id_value=None,
            )
            parsed_data = [MergeRequest(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def merge_request_level_approvals(
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
        Get approvals for a specific merge request.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response and the raw approval data.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
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
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approvals",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_approval_state_merge_requests(
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
        Get the approval state of merge requests for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response and the raw approval state data.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
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
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approval_state",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_merge_request_level_rules(
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
        Get merge request-level approval rules for a specific project and merge request.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response and a list of ApprovalRule models.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
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
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approval_rules",
                model=merge_rule,
                id_field="project_id",
                id_value=merge_rule.project_id,
            )
            parsed_data = [ApprovalRule(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def approve_merge_request(
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
        Approve a specific merge request.

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
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/approve",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def accept_merge_request(
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
        Accept (merge) a merge request.

        Pass ``merge_when_pipeline_succeeds=True`` to set auto-merge (merge once
        the pipeline succeeds) rather than merging immediately. Optional body
        params: merge_commit_message, squash_commit_message, squash,
        should_remove_source_branch, sha.

        Args:
            **kwargs: project_id and merge_request_iid (required) plus optional
                merge parameters listed above.

        Returns:
            Response: A wrapper containing the original response and a MergeRequest model.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
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
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        payload = {
            key: kwargs[key]
            for key in (
                "merge_commit_message",
                "squash_commit_message",
                "squash",
                "should_remove_source_branch",
                "merge_when_pipeline_succeeds",
                "sha",
            )
            if key in kwargs
        }
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/merge",
                headers=self.headers,
                json=payload or None,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def cancel_merge_when_pipeline_succeeds(
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
        Cancel a merge request's queued "merge when pipeline succeeds" (auto-merge).

        Args:
            **kwargs: project_id and merge_request_iid (required).

        Returns:
            Response: A wrapper containing the original response and a MergeRequest model.

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
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
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/cancel_merge_when_pipeline_succeeds",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = MergeRequest(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def unapprove_merge_request(
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
        Unapprove a specific merge request.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, merge_request_iid).

        Returns:
            Response: A wrapper containing the original response (no data for successful operation).

        Raises:
            MissingParameterError: If the project_id or merge_request_iid is missing.
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
        if merge_rule.project_id is None or merge_rule.merge_request_iid is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{merge_rule.project_id}/merge_requests/{merge_rule.merge_request_iid}/unapprove",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
