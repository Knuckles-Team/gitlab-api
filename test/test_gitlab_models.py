import os
import sys
import urllib.parse

import pytest
from conftest import reason

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    import gitlab_api
    from gitlab_api.gitlab_models import (BranchModel, CommitModel, DeployTokenModel, GroupModel, JobModel,
                                          MembersModel, PackageModel, PipelineModel, ProjectModel, ProtectedBranchModel,
                                          MergeRequestModel, MergeRequestRuleModel, ReleaseModel, RunnerModel,
                                          UserModel, WikiModel)

except ImportError:
    skip = True
    raise ("ERROR IMPORTING", ImportError)
else:
    skip = False


reason = "do not run on MacOS or windows OR dependency is not installed OR " + reason


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_gitlab_api():
    # test Project model group_id
    group_id = 1234
    project = ProjectModel(group_id=1234)
    assert group_id == project.group_id


if __name__ == "__main__":
    test_gitlab_api()
