import os
import sys
import urllib.parse
from typing import List
import json

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


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_gitlab_api():
    # gitlab url
    gitlab_url = "http://gitlab.arpa/api/v4/"
    # get token from env vars
    token = os.environ.get("GITLAB_TOKEN", default="NA")
    # create client
    client = gitlab_api.Api(url=gitlab_url, token=token, verify=False)

    # Get nested projects
    group_id = 2
    projects = client.get_nested_projects_by_group(group_id=group_id)
    assert isinstance(projects, List)

    # Create branch
    project = 79
    response = client.create_branch(project_id=project, branch="test_branch", reference="main")
    assert response.status_code == 201


if __name__ == "__main__":
    test_gitlab_api()
