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
    BranchModel,
    CommitModel,
    ReleaseModel,
    TagModel,
)
from gitlab_api.gitlab_response_models import (
    Branch,
    Comment,
    Commit,
    CommitSignature,
    Diff,
    MergeRequest,
    Release,
    Response,
    Tag,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiRepositories(GitLabApiBase):
    def get_branches(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Retrieve information about branches in a project.

        Args:
            **kwargs: Additional keyword arguments to initialize the BranchModel.

        Returns:
            Response: The response object containing a list of Branch models.

        Raises:
            ParameterError: If the provided parameters are invalid based on the BranchModel.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        branch = BranchModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{branch.project_id}/repository/branches",
                model=branch,
                id_field="project_id",
                id_value=branch.project_id,
            )
            parsed_data = [Branch(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_branch(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Retrieve information about a specific branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: The response object containing a Branch model.

        Raises:
            MissingParameterError: If the project ID or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        branch = BranchModel(**kwargs)
        if branch.project_id is None or branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{branch.project_id}/repository/branches/{branch.branch}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_branch(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Create a new branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch, ref).

        Returns:
            Response: The response object containing a Branch model.

        Raises:
            MissingParameterError: If required parameters are missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        branch = BranchModel(**kwargs)
        if branch.project_id is None or branch.branch is None or branch.ref is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{branch.project_id}/repository/branches",
                headers=self.headers,
                json=branch.api_parameters,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_branch(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Delete a branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: The response object (no data for successful deletion).

        Raises:
            MissingParameterError: If required parameters are missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        branch = BranchModel(**kwargs)
        if branch.project_id is None or branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{branch.project_id}/repository/branches/{branch.branch}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_merged_branches(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Delete all merged branches in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: The response object (no data for successful deletion).

        Raises:
            MissingParameterError: If required parameters are missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        branch = BranchModel(**kwargs)
        if branch.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{branch.project_id}/repository/merged_branches",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_commits(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get commits.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Commit models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{commit.project_id}/repository/commits",
                model=commit,
                id_field="project_id",
                id_value=commit.project_id,
            )
            parsed_data = [Commit(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_commit(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get a specific commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_commit_references(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get references of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of reference dictionaries.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/refs",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def cherry_pick_commit(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Cherry-pick a commit into a new branch.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/cherry_pick",
                headers=self.headers,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_commit(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Create a new commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits",
                headers=self.headers,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def revert_commit(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Revert a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/revert",
                headers=self.headers,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_commit_diff(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get the diff of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Diff models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/diff",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = [Diff(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_commit_comments(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get comments on a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Comment models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/comments",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = [Comment(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_commit_comment(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Create a comment on a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Comment model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/comments",
                headers=self.headers,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Comment(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_commit_discussions(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get discussions on a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Discussion models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/discussions",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = [Comment(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_commit_statuses(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get statuses of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Status models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/statuses",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = [Commit(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def post_build_status_to_commit(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Post build status to a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{commit.project_id}/statuses/{commit.commit_hash}",
                headers=self.headers,
                json=commit.data,
            )
            response.raise_for_status()
            parsed_data = Commit(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_commit_merge_requests(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get merge requests associated with a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of MergeRequest models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/merge_requests",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = [MergeRequest(**item) for item in response.json()]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_commit_gpg_signature(
        self,
        *,
        project_id: int | str = None,
        commit_hash: str | None = None,
        branch: str | None = None,
        dry_run: bool | None = None,
        message: str | None = None,
        state: str | None = None,
        ref: str | None = None,
        name: str | None = None,
        context: str | None = None,
        target_url: Any = None,
        description: str | None = None,
        coverage: float | str | None = None,
        pipeline_id: int | str | None = None,
        actions: list | None = None,
        start_branch: str | None = None,
        start_sha: str | None = None,
        start_project: int | str | None = None,
        author_email: Any = None,
        author_name: str | None = None,
        stats: bool | None = None,
        force: bool | None = None,
        line: int | None = None,
        line_type: str | None = None,
        note: str | None = None,
        path: str | None = None,
        group_ids: list | None = None,
        protected_branch_ids: list | None = None,
        report_type: str | None = None,
        rule_type: str | None = None,
        user_ids: list | None = None,
        since: str | None = None,
        until: str | None = None,
        all: bool | None = None,
        with_stats: bool | None = None,
        ref_name: str | None = None,
        data: dict[str, Any] | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get GPG signature of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a CommitSignature model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "commit_hash": commit_hash,
                "branch": branch,
                "dry_run": dry_run,
                "message": message,
                "state": state,
                "ref": ref,
                "name": name,
                "context": context,
                "target_url": target_url,
                "description": description,
                "coverage": coverage,
                "pipeline_id": pipeline_id,
                "actions": actions,
                "start_branch": start_branch,
                "start_sha": start_sha,
                "start_project": start_project,
                "author_email": author_email,
                "author_name": author_name,
                "stats": stats,
                "force": force,
                "line": line,
                "line_type": line_type,
                "note": note,
                "path": path,
                "group_ids": group_ids,
                "protected_branch_ids": protected_branch_ids,
                "report_type": report_type,
                "rule_type": rule_type,
                "user_ids": user_ids,
                "since": since,
                "until": until,
                "all": all,
                "with_stats": with_stats,
                "ref_name": ref_name,
                "data": data,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        commit = CommitModel(**kwargs)
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{commit.project_id}/repository/commits/{commit.commit_hash}/signatures",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = CommitSignature(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_protected_branches(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get information about protected branches in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Branch models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{protected_branch.project_id}/protected_branches",
                model=protected_branch,
                id_field="project_id",
                id_value=protected_branch.project_id,
            )
            parsed_data = [Branch(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_protected_branch(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get information about a specific protected branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: A wrapper containing the original response and a Branch model.

        Raises:
            MissingParameterError: If the project_id or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches/{protected_branch.branch}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def protect_branch(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Protect a specific branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: A wrapper containing the original response and a Branch model.

        Raises:
            MissingParameterError: If the project_id or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches",
                json=protected_branch.data,  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def unprotect_branch(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Unprotect a specific branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches/{protected_branch.branch}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def require_code_owner_approvals_single_branch(
        self,
        *,
        project_id: int | str = None,
        branch: str | None = None,
        ref: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Require code owner approvals for a specific branch in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, branch).

        Returns:
            Response: A wrapper containing the original response and a Branch model.

        Raises:
            MissingParameterError: If the project_id or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "branch": branch,
                "ref": ref,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        protected_branch = BranchModel(**kwargs)
        if protected_branch.project_id is None or protected_branch.branch is None:
            raise MissingParameterError
        try:
            response = self._session.patch(
                url=f"{self.url}/projects/{protected_branch.project_id}/protected_branches/{protected_branch.branch}",
                json=protected_branch.data,  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Branch(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_release_by_tag(
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
        Get information about a release by its tag in a project.

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
            response = self._session.get(
                url=f"{self.url}/projects/{release.project_id}/releases/{release.tag_name}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Release(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_tags(
        self,
        *,
        project_id: int | str | None = None,
        tag: str | None = None,
        ref: str | None = None,
        message: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get information about tags in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Tag models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "tag": tag,
                "ref": ref,
                "message": message,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        tag = TagModel(**kwargs)
        if tag.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{tag.project_id}/repository/tags",
                model=tag,
                id_field="project_id",
                id_value=tag.project_id,
            )
            parsed_data = [Tag(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_tag(
        self,
        *,
        project_id: int | str | None = None,
        tag: str | None = None,
        ref: str | None = None,
        message: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get information about a specific tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and a Tag model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "tag": tag,
                "ref": ref,
                "message": message,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:  # type: ignore
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{tag.project_id}/repository/tags/{tag.name}",  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Tag(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_tag(
        self,
        *,
        project_id: int | str | None = None,
        tag: str | None = None,
        ref: str | None = None,
        message: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Create a tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and a Tag model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "tag": tag,
                "ref": ref,
                "message": message,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:  # type: ignore
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{tag.project_id}/repository/tags",
                json=tag.data,  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Tag(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_tag(
        self,
        *,
        project_id: int | str | None = None,
        tag: str | None = None,
        ref: str | None = None,
        message: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Delete a tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "tag": tag,
                "ref": ref,
                "message": message,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:  # type: ignore
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{tag.project_id}/repository/tags/{tag.name}",  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_protected_tags(
        self,
        *,
        project_id: int | str | None = None,
        tag: str | None = None,
        ref: str | None = None,
        message: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get information about protected tags in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Tag models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "tag": tag,
                "ref": ref,
                "message": message,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        tag = TagModel(**kwargs)
        if tag.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{tag.project_id}/protected_tags",
                model=tag,
                id_field="project_id",
                id_value=tag.project_id,
            )
            parsed_data = [Tag(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_protected_tag(
        self,
        *,
        project_id: int | str | None = None,
        tag: str | None = None,
        ref: str | None = None,
        message: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Get information about a specific protected tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and a Tag model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "tag": tag,
                "ref": ref,
                "message": message,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:  # type: ignore
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{tag.project_id}/protected_tags/{tag.name}",  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Tag(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def protect_tag(
        self,
        *,
        project_id: int | str | None = None,
        tag: str | None = None,
        ref: str | None = None,
        message: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Protect a tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response and a Tag model.

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "tag": tag,
                "ref": ref,
                "message": message,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:  # type: ignore
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{tag.project_id}/protected_tags",
                json=tag.data,  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Tag(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def unprotect_tag(
        self,
        *,
        project_id: int | str | None = None,
        tag: str | None = None,
        ref: str | None = None,
        message: str | None = None,
        max_pages: int | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response:
        """
        Unprotect a tag in a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, name).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or name is missing.
            ParameterError: If invalid parameters are provided.
        """
        kwargs = {
            k: v
            for k, v in {
                "project_id": project_id,
                "tag": tag,
                "ref": ref,
                "message": message,
                "max_pages": max_pages,
                "page": page,
                "per_page": per_page,
            }.items()
            if v is not None
        }
        tag = TagModel(**kwargs)
        if tag.project_id is None or tag.name is None:  # type: ignore
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{tag.project_id}/protected_tags/{tag.name}",  # type: ignore
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
