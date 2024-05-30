import os
import sys

import pytest
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
    assert projects.data.base_type == "Projects"
    assert isinstance(projects.data.projects, list)
    assert len(projects.data.projects) > 3
    group_id = 6
    projects = client.get_nested_projects_by_group(group_id=group_id, per_page=3)
    assert projects.data.base_type == "Projects"
    assert isinstance(projects.data.projects, list)
    assert len(projects.data.projects) > 3


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


if __name__ == "__main__":
    test_get_nested_projects()
    test_create_branch()
    test_create_project_rule()
    test_get_project_rules()
