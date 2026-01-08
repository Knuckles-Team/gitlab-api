import os
import sys

import pytest
from gitlab_api import pydantic_to_sqlalchemy

from conftest import reason

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    import gitlab_api
except ImportError:
    skip = True
else:
    skip = False


reason = "do not run on MacOS or windows OR dependency is not installed OR " + reason

# gitlab url
gitlab_url = "http://gitlab.arpa/api/v4"
# get token from env vars
token = os.environ.get("GITLAB_TOKEN", default="NA")
# create client
client = gitlab_api.Api(url=gitlab_url, token=token, verify=False)


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_get_nested_projects():
    # Get nested projects
    group_id = 2
    projects = client.get_nested_projects_by_group(group_id=group_id, per_page=3)
    assert len(projects.data) > 0
    assert isinstance(projects.data, list)
    group_id = 6
    projects = client.get_nested_projects_by_group(group_id=group_id, per_page=3)
    assert len(projects.data) > 0
    assert isinstance(projects.data, list)


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_get_projects():
    # Get nested projects
    group_id = 6
    projects = client.get_projects(group_id=group_id, per_page=3)
    assert len(projects.data) > 0
    assert isinstance(projects.data, list)


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_create_branch():
    # Create branch
    project = 79
    response = client.create_branch(
        project_id=project, branch="test_branch", reference="main"
    )
    assert response.status_code == 201 or response.status_code == 400


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_create_project_rule():
    # Create branch
    project = 79
    response = client.create_project_level_rule(
        project_id=project, name="Test_Rule", approvals_required=9
    )
    assert response.status_code == 201


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_get_project_rules():
    # Create branch
    project = 79
    response = client.get_project_level_rules(project_id=project)
    assert response.status_code == 200


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_edit_group():
    # Get nested projects
    group_id = 6
    group = client.edit_group(group_id=group_id, visibility="internal")
    assert group.data.visibility == "internal"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_edit_project():
    # Get nested projects
    group_id = 6
    group = client.edit_group(group_id=group_id, visibility="internal")
    group_id = 179
    group = client.edit_group(group_id=group_id, visibility="internal")
    project_id = 55
    project = client.edit_project(project_id=project_id, visibility="internal")
    assert project.data.visibility == "internal"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_get_project_jobs():
    # Get project jobs
    group_id = 2
    projects = client.get_nested_projects_by_group(group_id=group_id, per_page=100)
    all_jobs = []
    for project in projects.data:
        jobs = client.get_project_jobs(project_id=project.id, max_pages=1)
        jobs_db_models = pydantic_to_sqlalchemy(schema=jobs)
        print(
            f"\n\ndb models: {jobs_db_models['data']}\nLength: {len(jobs_db_models['data'])}"
        )
        all_jobs.extend(jobs_db_models["data"])
    print(f"\n\nall jobs: {all_jobs}\nLength: {len(all_jobs)}")
    assert isinstance(all_jobs, list)


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_get_project_releases():
    project_id = 55
    releases = client.get_releases(project_id=project_id, per_page=100, max_pages=100)
    print(f"Releases: {releases} \n\nReleases Total: {len(releases.data)}")
    assert isinstance(releases.data, list)


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_get_group_releases():
    group_id = 6
    releases = client.get_group_releases(group_id=group_id, per_page=100, max_pages=100)
    print(f"Releases: {releases} \n\nReleases Total: {len(releases.data)}")
    assert isinstance(releases.data, list)


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_get_group_merge_rule_settings():
    group_id = 6
    settings = client.get_group_level_rule(group_id=group_id)
    print(f"Settings: {settings}")
    assert isinstance(settings.data, dict)


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_get_project_merge_rule_settings():
    project_id = 52
    settings = client.get_project_level_rule(project_id=project_id)
    print(f"Settings: {settings}")
    assert isinstance(settings.data, dict)


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
)
def test_get_project_pipeline_schedules():
    project_id = 52
    pipeline_schedule = client.get_pipeline_schedules(project_id=project_id)
    print(f"Pipeline Schedule: {pipeline_schedule}")
    assert isinstance(pipeline_schedule.data, list)


if __name__ == "__main__":
    test_get_projects()
    test_get_project_pipeline_schedules()
    test_get_nested_projects()
    test_create_branch()
    test_create_project_rule()
    test_get_project_rules()
    test_edit_group()
    test_edit_project()
    test_get_project_jobs()
    test_get_project_releases()
    test_get_group_releases()
    test_get_group_merge_rule_settings()
    test_get_project_merge_rule_settings()
