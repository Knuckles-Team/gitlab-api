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
    def get_pipeline_jobs(self, **kwargs) -> Response:
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

    def get_pipelines(self, **kwargs) -> Response:
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

    def get_pipeline(self, **kwargs) -> Response:
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
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None or pipeline.pipeline_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{pipeline.project_id}/pipelines/{pipeline.pipeline_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Pipeline(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def run_pipeline(self, **kwargs) -> Response:
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
        pipeline = PipelineModel(**kwargs)
        if pipeline.project_id is None or pipeline.ref is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{pipeline.project_id}/pipeline",
                headers=self.headers,
                json=pipeline.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Pipeline(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_pipeline_schedules(self, **kwargs) -> Response:
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

    def get_pipeline_schedule(self, **kwargs) -> Response:
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
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_pipelines_triggered_from_schedule(self, **kwargs) -> Response:
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

    def create_pipeline_schedule(self, **kwargs) -> Response:
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
        project = ProjectModel(**kwargs)
        if project.project_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules",
                json=project.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def edit_pipeline_schedule(self, **kwargs) -> Response:
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
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}",
                json=project.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def take_pipeline_schedule_ownership(self, **kwargs) -> Response:
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
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/take_ownership",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineSchedule(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_pipeline_schedule(self, **kwargs) -> Response:
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
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.delete(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def run_pipeline_schedule(self, **kwargs) -> Response:
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
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/play",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def create_pipeline_schedule_variable(self, **kwargs) -> Response:
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
        project = ProjectModel(**kwargs)
        if project.project_id is None or project.pipeline_schedule_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/projects/{project.project_id}/pipeline_schedules/{project.pipeline_schedule_id}/variables",
                json=project.data,
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = PipelineVariable(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_pipeline_schedule_variable(self, **kwargs) -> Response:
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
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_runners(self, **kwargs) -> Response:
        """
        Get information about runners.

        Args:
            **kwargs: Additional parameters for the request (e.g., scope, status).

        Returns:
            Response: A wrapper containing the original response and a list of Runner models.

        Raises:
            ParameterError: If invalid parameters are provided.
        """
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

    def get_runner(self, **kwargs) -> Response:
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
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.get(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def update_runner_details(self, **kwargs) -> Response:
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
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def pause_runner(self, **kwargs) -> Response:
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
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None or runner.active is None:
            raise MissingParameterError
        try:
            response = self._session.put(
                url=f"{self.url}/runners/{runner.runner_id}",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def get_runner_jobs(self, **kwargs) -> Response:
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

    def get_group_runners(self, **kwargs) -> Response:
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

    def register_new_runner(self, **kwargs) -> Response:
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
        runner = RunnerModel(**kwargs)
        if runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/runners",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = Runner(**response.json())
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def delete_runner(self, **kwargs) -> Response:
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
        runner = RunnerModel(**kwargs)
        if runner.runner_id is None and runner.token is None:
            raise MissingParameterError
        try:
            if runner.runner_id:
                response = self._session.delete(
                    url=f"{self.url}/runners/{runner.runner_id}",
                    headers=self.headers,
                    verify=self.verify,
                    proxies=self.proxies,
                )
            else:
                response = self._session.delete(
                    url=f"{self.url}/runners",
                    headers=self.headers,
                    json=runner.data,
                    verify=self.verify,
                    proxies=self.proxies,
                )
            response.raise_for_status()
            return Response(response=response)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def verify_runner_authentication(self, **kwargs) -> Response:
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
        runner = RunnerModel(**kwargs)
        if runner.token is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/runners/verify",
                headers=self.headers,
                json=runner.data,
                verify=self.verify,
                proxies=self.proxies,
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
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e

    def reset_group_runner_token(self, **kwargs) -> Response:
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
        runner = RunnerModel(**kwargs)
        if runner.group_id is None:
            raise MissingParameterError
        try:
            response = self._session.post(
                url=f"{self.url}/groups/{runner.group_id}/runners/reset_registration_token",
                headers=self.headers,
                verify=self.verify,
                proxies=self.proxies,
            )
            response.raise_for_status()
            parsed_data = response.json()
            return Response(response=response, data=parsed_data)
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
