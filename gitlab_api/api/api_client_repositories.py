#!/usr/bin/python

from typing import TypeVar

from agent_utilities.base_utilities import get_logger
from pydantic import ValidationError

logger = get_logger(__name__)

from agent_utilities.core.exceptions import (
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
    def get_branches(self, **kwargs) -> Response:
        """
        Retrieve information about branches in a project.

        Args:
            **kwargs: Additional keyword arguments to initialize the BranchModel.

        Returns:
            Response: The response object containing a list of Branch models.

        Raises:
            ParameterError: If the provided parameters are invalid based on the BranchModel.
        """
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

    def get_branch(self, **kwargs) -> Response:
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

    def create_branch(self, **kwargs) -> Response:
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

    def delete_branch(self, **kwargs) -> Response:
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

    def delete_merged_branches(self, **kwargs) -> Response:
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

    def get_commits(self, **kwargs) -> Response:
        """
        Get commits.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Commit models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_commit(self, **kwargs) -> Response:
        """
        Get a specific commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_commit_references(self, **kwargs) -> Response:
        """
        Get references of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of reference dictionaries.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def cherry_pick_commit(self, **kwargs) -> Response:
        """
        Cherry-pick a commit into a new branch.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def create_commit(self, **kwargs) -> Response:
        """
        Create a new commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def revert_commit(self, **kwargs) -> Response:
        """
        Revert a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_commit_diff(self, **kwargs) -> Response:
        """
        Get the diff of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Diff models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_commit_comments(self, **kwargs) -> Response:
        """
        Get comments on a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Comment models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def create_commit_comment(self, **kwargs) -> Response:
        """
        Create a comment on a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Comment model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_commit_discussions(self, **kwargs) -> Response:
        """
        Get discussions on a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Discussion models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_commit_statuses(self, **kwargs) -> Response:
        """
        Get statuses of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of Status models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def post_build_status_to_commit(self, **kwargs) -> Response:
        """
        Post build status to a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a Commit model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_commit_merge_requests(self, **kwargs) -> Response:
        """
        Get merge requests associated with a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a list of MergeRequest models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_commit_gpg_signature(self, **kwargs) -> Response:
        """
        Get GPG signature of a commit.

        Args:
            **kwargs: Additional parameters for the request.

        Returns:
            Response: A wrapper containing the original response and a CommitSignature model.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_protected_branches(self, **kwargs) -> Response:
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

    def get_protected_branch(self, **kwargs) -> Response:
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

    def protect_branch(self, **kwargs) -> Response:
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

    def unprotect_branch(self, **kwargs) -> Response:
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

    def require_code_owner_approvals_single_branch(self, **kwargs) -> Response:
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

    def get_release_by_tag(self, **kwargs) -> Response:
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

    def get_tags(self, **kwargs) -> Response:
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

    def get_tag(self, **kwargs) -> Response:
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

    def create_tag(self, **kwargs) -> Response:
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

    def delete_tag(self, **kwargs) -> Response:
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

    def get_protected_tags(self, **kwargs) -> Response:
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

    def get_protected_tag(self, **kwargs) -> Response:
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

    def protect_tag(self, **kwargs) -> Response:
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

    def unprotect_tag(self, **kwargs) -> Response:
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
