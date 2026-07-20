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
    NoteModel,
    PackageModel,
    RunnerModel,
    SnippetModel,
    WikiModel,
)
from gitlab_api.gitlab_response_models import (
    Note,
    Package,
    Response,
    Runner,
    Snippet,
    WikiPage,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiOther(GitLabApiBase):
    def get_repository_packages(self, **kwargs) -> Response:
        """
        Get information about repository packages for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of Package models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        package = PackageModel(**kwargs)
        if package.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{package.project_id}/packages",
                model=package,
                id_field="project_id",
                id_value=package.project_id,
            )
            parsed_data = [Package(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def publish_repository_package(self, **kwargs) -> Response:
        """
        Publish a repository package for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, package_name, package_version, file_name).

        Returns:
            Response: A wrapper containing the original response and a Package model.

        Raises:
            MissingParameterError: If the project_id, package_name, package_version, or file_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        package = PackageModel(**kwargs)
        if (
            package.project_id is None
            or package.package_name is None
            or package.package_version is None
            or package.file_name is None
        ):
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{package.project_id}/packages/generic/{package.package_name}/{package.package_version}/{package.file_name}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Package(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def download_repository_package(self, **kwargs) -> Response:
        """
        Download a repository package for a specific project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, package_name, package_version, file_name).

        Returns:
            Response: A wrapper containing the original response and the raw package file data.

        Raises:
            MissingParameterError: If the project_id, package_name, package_version, or file_name is missing.
            ParameterError: If invalid parameters are provided.
        """
        package = PackageModel(**kwargs)
        if (
            package.project_id is None
            or package.package_name is None
            or package.package_version is None
            or package.file_name is None
        ):
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{package.project_id}/packages/generic/{package.package_name}/{package.package_version}/{package.file_name}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = response.content
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def reset_token(self, **kwargs) -> Response:
        """
        Reset authentication token for a runner.

        Args:
            **kwargs: Additional parameters for the request (e.g., runner_id, token).

        Returns:
            Response: A wrapper containing the original response and a Runner model.

        Raises:
            MissingParameterError: If the runner_id or token is missing.
            ParameterError: If invalid parameters are provided.
        """
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None or runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/runners/{runner.runner_id}/reset_authentication_token",
                headers=self.headers,
                json=runner.data,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_wiki_list(self, **kwargs) -> Response:
        """
        Get a list of wiki pages for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a list of WikiPage models.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None:
            raise MissingParameterError
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{wiki.project_id}/wikis",
                model=wiki,
                id_field="project_id",
                id_value=wiki.project_id,
            )
            parsed_data = [WikiPage(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_wiki_page(self, **kwargs) -> Response:
        """
        Get information about a specific wiki page.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, slug).

        Returns:
            Response: A wrapper containing the original response and a WikiPage model.

        Raises:
            MissingParameterError: If the project_id or slug is missing.
            ParameterError: If invalid parameters are provided.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = WikiPage(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_wiki_page(self, **kwargs) -> Response:
        """
        Create a new wiki page for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id).

        Returns:
            Response: A wrapper containing the original response and a WikiPage model.

        Raises:
            MissingParameterError: If the project_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{wiki.project_id}/wikis",
                headers=self.headers,
                json=wiki.data,
            )
            response.raise_for_status()
            parsed_data = WikiPage(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_wiki_page(self, **kwargs) -> Response:
        """
        Update an existing wiki page for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, slug).

        Returns:
            Response: A wrapper containing the original response and a WikiPage model.

        Raises:
            MissingParameterError: If the project_id or slug is missing.
            ParameterError: If invalid parameters are provided.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}",
                headers=self.headers,
                json=wiki.data,
            )
            response.raise_for_status()
            parsed_data = WikiPage(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_wiki_page(self, **kwargs) -> Response:
        """
        Delete a wiki page for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, slug).

        Returns:
            Response: A wrapper containing the original response (no data for successful deletion).

        Raises:
            MissingParameterError: If the project_id or slug is missing.
            ParameterError: If invalid parameters are provided.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.slug is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/{wiki.slug}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def upload_wiki_page_attachment(self, **kwargs) -> Response:
        """
        Upload an attachment to a wiki page for a project.

        Args:
            **kwargs: Additional parameters for the request (e.g., project_id, file, branch).

        Returns:
            Response: A wrapper containing the original response and the raw attachment data.

        Raises:
            MissingParameterError: If the project_id, file, or branch is missing.
            ParameterError: If invalid parameters are provided.
        """
        wiki = WikiModel(**kwargs)
        if wiki.project_id is None or wiki.file is None or wiki.branch is None:
            raise MissingParameterError
        try:
            headers = self.headers.copy() if self.headers else {}
            headers["Content-Type"] = "multipart/form-data"
            response = self._session.post(
                url=f"{self.url}/projects/{wiki.project_id}/wikis/attachments",
                headers=headers,
                files={"file": wiki.file},
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_snippet(self, **kwargs) -> Response:
        """
        Create a project snippet or personal snippet.
        """
        snippet = SnippetModel(**kwargs)
        if (
            snippet.title is None
            or snippet.file_name is None
            or snippet.content is None
        ):
            raise MissingParameterError(
                "Missing required parameters: title, file_name, content"
            )
        try:
            if snippet.project_id:
                url = f"{self.url}/projects/{snippet.project_id}/snippets"
            else:
                url = f"{self.url}/snippets"
            response = self._session.post(
                url=url,
                json=snippet.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Snippet(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_snippets(self, **kwargs) -> Response:
        """
        Get list of snippets. Can filter by project_id.
        """
        snippet = SnippetModel(**kwargs)
        try:
            if snippet.project_id:
                endpoint = f"/projects/{snippet.project_id}/snippets"
            else:
                endpoint = "/snippets"
            response, data = self._fetch_all_pages(
                endpoint=endpoint,
                model=snippet,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Snippet(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_snippet(self, **kwargs) -> Response:
        """
        Get a specific snippet.
        """
        snippet = SnippetModel(**kwargs)
        if snippet.snippet_id is None:
            raise MissingParameterError("Missing snippet_id")
        try:
            if snippet.project_id:
                url = f"{self.url}/projects/{snippet.project_id}/snippets/{snippet.snippet_id}"
            else:
                url = f"{self.url}/snippets/{snippet.snippet_id}"
            response = self._session.get(
                url=url,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Snippet(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_snippet(self, **kwargs) -> Response:
        """
        Update a snippet.
        """
        snippet = SnippetModel(**kwargs)
        if snippet.snippet_id is None:
            raise MissingParameterError("Missing snippet_id")
        try:
            if snippet.project_id:
                url = f"{self.url}/projects/{snippet.project_id}/snippets/{snippet.snippet_id}"
            else:
                url = f"{self.url}/snippets/{snippet.snippet_id}"
            response = self._session.put(
                url=url,
                json=snippet.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Snippet(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_snippet(self, **kwargs) -> Response:
        """
        Delete a snippet.
        """
        snippet = SnippetModel(**kwargs)
        if snippet.snippet_id is None:
            raise MissingParameterError("Missing snippet_id")
        try:
            if snippet.project_id:
                url = f"{self.url}/projects/{snippet.project_id}/snippets/{snippet.snippet_id}"
            else:
                url = f"{self.url}/snippets/{snippet.snippet_id}"
            response = self._session.delete(
                url=url,
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response, data=None)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_note(self, **kwargs) -> Response:
        """
        Create a new note/comment on an issue.
        """
        note = NoteModel(**kwargs)
        if note.project_id is None or note.issue_iid is None or note.body is None:
            raise MissingParameterError(
                "Missing required parameters: project_id, issue_iid, body"
            )
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{note.project_id}/issues/{note.issue_iid}/notes",
                json=note.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Note(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_notes(self, **kwargs) -> Response:
        """
        Get all notes for a specific issue.
        """
        note = NoteModel(**kwargs)
        if note.project_id is None or note.issue_iid is None:
            raise MissingParameterError(
                "Missing required parameters: project_id, issue_iid"
            )
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{note.project_id}/issues/{note.issue_iid}/notes",
                model=note,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Note(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_note(self, **kwargs) -> Response:
        """
        Get a specific note.
        """
        note = NoteModel(**kwargs)
        if note.project_id is None or note.issue_iid is None or note.note_id is None:
            raise MissingParameterError(
                "Missing required parameters: project_id, issue_iid, note_id"
            )
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{note.project_id}/issues/{note.issue_iid}/notes/{note.note_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Note(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_note(self, **kwargs) -> Response:
        """
        Update a note.
        """
        note = NoteModel(**kwargs)
        if (
            note.project_id is None
            or note.issue_iid is None
            or note.note_id is None
            or note.body is None
        ):
            raise MissingParameterError(
                "Missing required parameters: project_id, issue_iid, note_id, body"
            )
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{note.project_id}/issues/{note.issue_iid}/notes/{note.note_id}",
                json=note.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Note(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_note(self, **kwargs) -> Response:
        """
        Delete a note.
        """
        note = NoteModel(**kwargs)
        if note.project_id is None or note.issue_iid is None or note.note_id is None:
            raise MissingParameterError(
                "Missing required parameters: project_id, issue_iid, note_id"
            )
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{note.project_id}/issues/{note.issue_iid}/notes/{note.note_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response, data=None)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
