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
    EpicModel,
    IssueModel,
    LabelModel,
    MilestoneModel,
)
from gitlab_api.gitlab_response_models import (
    Epic,
    Issue,
    Label,
    Milestone,
    Response,
)

T = TypeVar("T")

from gitlab_api.api.api_client_base import GitLabApiBase


class GitLabApiIssues(GitLabApiBase):
    def create_issue(self, **kwargs) -> Response:
        """
        Create a new issue.
        """
        issue = IssueModel(**kwargs)
        if issue.project_id is None or issue.title is None:
            raise MissingParameterError(
                "Missing required parameters: project_id and title"
            )
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{issue.project_id}/issues",
                json=issue.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Issue(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_issues(self, **kwargs) -> Response:
        """
        Get list of issues. Can filter by project_id.
        """
        issue = IssueModel(**kwargs)
        try:
            endpoint = (
                f"/projects/{issue.project_id}/issues"
                if issue.project_id
                else "/issues"
            )
            response, data = self._fetch_all_pages(
                endpoint=endpoint,
                model=issue,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Issue(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_group_issues(self, **kwargs) -> Response:
        """
        Get the list of issues for a group (and, by default, its subgroups).

        Args:
            **kwargs: group_id (required) plus optional filters (state, labels,
                assignee_username, milestone, search, order_by, ...).

        Returns:
            Response: A wrapper containing the original response and a list of Issue models.

        Raises:
            MissingParameterError: If the group_id is missing.
            ParameterError: If invalid parameters are provided.
        """
        issue = IssueModel(**kwargs)
        if issue.group_id is None:
            raise MissingParameterError("Missing required parameter: group_id")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{issue.group_id}/issues",
                model=issue,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Issue(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_issue(self, **kwargs) -> Response:
        """
        Get a single issue.
        """
        issue = IssueModel(**kwargs)
        if issue.project_id is None or issue.issue_iid is None:
            raise MissingParameterError(
                "Missing required parameters: project_id and issue_iid"
            )
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{issue.project_id}/issues/{issue.issue_iid}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Issue(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_issue(self, **kwargs) -> Response:
        """
        Update an issue.
        """
        issue = IssueModel(**kwargs)
        if issue.project_id is None or issue.issue_iid is None:
            raise MissingParameterError(
                "Missing required parameters: project_id and issue_iid"
            )
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{issue.project_id}/issues/{issue.issue_iid}",
                json=issue.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Issue(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_issue(self, **kwargs) -> Response:
        """
        Delete an issue.
        """
        issue = IssueModel(**kwargs)
        if issue.project_id is None or issue.issue_iid is None:
            raise MissingParameterError(
                "Missing required parameters: project_id and issue_iid"
            )
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{issue.project_id}/issues/{issue.issue_iid}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response, data=None)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_label(self, **kwargs) -> Response:
        """
        Create a new label.
        """
        label = LabelModel(**kwargs)
        if label.project_id is None or label.name is None or label.color is None:
            raise MissingParameterError(
                "Missing required parameters: project_id, name, color"
            )
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{label.project_id}/labels",
                json=label.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Label(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_labels(self, **kwargs) -> Response:
        """
        Get all labels for a project.
        """
        label = LabelModel(**kwargs)
        if label.project_id is None:
            raise MissingParameterError("Missing project_id")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{label.project_id}/labels",
                model=label,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Label(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_label(self, **kwargs) -> Response:
        """
        Get a specific label by name.
        """
        label = LabelModel(**kwargs)
        if label.project_id is None or label.name is None:
            raise MissingParameterError("Missing project_id or name")
        try:
            response = self.get_labels(**kwargs)
            if response.data is None:
                raise ValueError("Label not found")
            matched = [lbl for lbl in response.data if lbl.name == label.name]
            if not matched:
                raise ValueError("Label not found")
            return Response(response=response.response, data=matched[0])
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_label(self, **kwargs) -> Response:
        """
        Update an existing label.
        """
        label = LabelModel(**kwargs)
        if label.project_id is None or label.name is None:
            raise MissingParameterError("Missing required parameters: project_id, name")
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{label.project_id}/labels",
                json=label.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Label(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_label(self, **kwargs) -> Response:
        """
        Delete a label.
        """
        label = LabelModel(**kwargs)
        if label.project_id is None or label.name is None:
            raise MissingParameterError("Missing required parameters: project_id, name")
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{label.project_id}/labels",
                json=label.data,
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response, data=None)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_milestone(self, **kwargs) -> Response:
        """
        Create a project milestone.
        """
        milestone = MilestoneModel(**kwargs)
        if milestone.project_id is None or milestone.title is None:
            raise MissingParameterError(
                "Missing required parameters: project_id, title"
            )
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{milestone.project_id}/milestones",
                json=milestone.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Milestone(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_milestones(self, **kwargs) -> Response:
        """
        Get all milestones for a project.
        """
        milestone = MilestoneModel(**kwargs)
        if milestone.project_id is None:
            raise MissingParameterError("Missing project_id")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/projects/{milestone.project_id}/milestones",
                model=milestone,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Milestone(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_milestone(self, **kwargs) -> Response:
        """
        Get a specific project milestone.
        """
        milestone = MilestoneModel(**kwargs)
        if milestone.project_id is None or milestone.milestone_id is None:
            raise MissingParameterError("Missing project_id or milestone_id")
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{milestone.project_id}/milestones/{milestone.milestone_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Milestone(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_milestone(self, **kwargs) -> Response:
        """
        Update a project milestone.
        """
        milestone = MilestoneModel(**kwargs)
        if milestone.project_id is None or milestone.milestone_id is None:
            raise MissingParameterError(
                "Missing required parameters: project_id, milestone_id"
            )
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{milestone.project_id}/milestones/{milestone.milestone_id}",
                json=milestone.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Milestone(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_milestone(self, **kwargs) -> Response:
        """
        Delete a project milestone.
        """
        milestone = MilestoneModel(**kwargs)
        if milestone.project_id is None or milestone.milestone_id is None:
            raise MissingParameterError(
                "Missing required parameters: project_id, milestone_id"
            )
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{milestone.project_id}/milestones/{milestone.milestone_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response, data=None)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_epic(self, **kwargs) -> Response:
        """
        Create a new group epic.
        """
        epic = EpicModel(**kwargs)
        if epic.group_id is None or epic.title is None:
            raise MissingParameterError("Missing required parameters: group_id, title")
        try:
            response = self._session.post(
                url=f"{self.url}/groups/{epic.group_id}/epics",
                json=epic.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Epic(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_epics(self, **kwargs) -> Response:
        """
        Get all epics for a group.
        """
        epic = EpicModel(**kwargs)
        if epic.group_id is None:
            raise MissingParameterError("Missing group_id")
        try:
            response, data = self._fetch_all_pages(
                endpoint=f"/groups/{epic.group_id}/epics",
                model=epic,
                id_field=None,
                id_value=None,
            )
            parsed_data = [Epic(**item) for item in data]
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_epic(self, **kwargs) -> Response:
        """
        Get a specific group epic.
        """
        epic = EpicModel(**kwargs)
        if epic.group_id is None or epic.epic_iid is None:
            raise MissingParameterError("Missing group_id or epic_iid")
        try:
            response = self._session.get(
                url=f"{self.url}/groups/{epic.group_id}/epics/{epic.epic_iid}",
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Epic(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_epic(self, **kwargs) -> Response:
        """
        Update a group epic.
        """
        epic = EpicModel(**kwargs)
        if epic.group_id is None or epic.epic_iid is None:
            raise MissingParameterError(
                "Missing required parameters: group_id, epic_iid"
            )
        try:
            response = self._session.put(
                url=f"{self.url}/groups/{epic.group_id}/epics/{epic.epic_iid}",
                json=epic.data,
                headers=self.headers,
            )
            response.raise_for_status()
            parsed_data = Epic(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_epic(self, **kwargs) -> Response:
        """
        Delete a group epic.
        """
        epic = EpicModel(**kwargs)
        if epic.group_id is None or epic.epic_iid is None:
            raise MissingParameterError(
                "Missing required parameters: group_id, epic_iid"
            )
        try:
            response = self._session.delete(
                url=f"{self.url}/groups/{epic.group_id}/epics/{epic.epic_iid}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Response(response=response, data=None)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
