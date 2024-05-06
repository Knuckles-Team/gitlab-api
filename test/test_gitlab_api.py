import os
import sys
import urllib.parse
from typing import List

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
    sys.platform in ["darwin", "win32"] or skip,
    reason=reason,
    )
def test_gitlab_api():
    # gitlab url
    gitlab_url = "http://gitlab.com/api/v4/"
    # get token from env vars
    token = os.environ.get("token", default="NA")
    # create client
    client = gitlab_api.Api(url=gitlab_url, token=token, verify=False)
    projects = client.get_nested_projects_by_group(group_id="891091").json()
    assert projects == List


if __name__ == "__main__":
    test_gitlab_api()
