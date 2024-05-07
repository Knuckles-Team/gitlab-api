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
def test_branch_model():
    project_id = 2
    branch_name = "test_branch"
    reference = "main"
    branch = BranchModel(project_id=project_id, branch=branch_name, reference=reference)
    assert branch.project_id == project_id
    assert branch.api_parameters == "?branch=test_branch&ref=main"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_commit_model():
    project_id = 2
    branch_name = "test_branch"
    commit = CommitModel(project_id=project_id, branch_name=branch_name)
    assert commit.project_id == project_id


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_merge_request_model():
    project_id = 2
    title = "test merge"
    author_id = 12341
    source_branch = "development"
    target_branch = "production"
    merge_request_rule = MergeRequestModel(project_id=project_id, title=title, author_id=author_id,
                                           source_branch=source_branch, target_branch=target_branch)
    assert merge_request_rule.project_id == project_id
    assert merge_request_rule.title == title
    assert merge_request_rule.author_id == author_id
    assert merge_request_rule.target_branch == target_branch
    assert merge_request_rule.source_branch == source_branch


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_merge_request_rule_model():
    project_id = 2
    name = "test rule"
    merge_request_rule = MergeRequestRuleModel(project_id=project_id, name=name, approvals_required=9)
    assert merge_request_rule.project_id == project_id
    assert merge_request_rule.name == name
    assert merge_request_rule.approvals_required == 9



@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_pipeline_model():
    project_id = 1234
    pipeline = PipelineModel(project_id=project_id, per_page=100, reference="test")
    assert project_id == pipeline.project_id
    assert pipeline.api_parameters == "?per_page=100&ref=test"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_project_model():
    group_id = 1234
    project_id = 5679
    project = ProjectModel(group_id=group_id)
    assert group_id == project.group_id
    project = ProjectModel(project_id=project_id)
    assert project_id == project.project_id
    project = ProjectModel(project_id=project_id,group_id=group_id)
    assert project_id == project.project_id
    assert group_id == project.group_id
    assert project.api_parameters == "?group_id=1234"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_protected_branches_model():
    project_id = 5679
    protected_branch = ProtectedBranchModel(project_id=project_id, branch="test")
    assert project_id == protected_branch.project_id


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_release_model():
    project_id = 5679
    release = ReleaseModel(project_id=project_id, simple=True)
    assert project_id == release.project_id
    assert release.api_parameters == "?simple=True"


@pytest.mark.skipif(
    sys.platform in ["darwin"] or skip,
    reason=reason,
    )
def test_wiki_model():
    project_id = 5679
    wiki = WikiModel(project_id=project_id, with_content=True)
    assert project_id == wiki.project_id
    assert wiki.api_parameters == "?with_content=True"


if __name__ == "__main__":
    test_branch_model()
    test_commit_model()
    test_merge_request_model()
    test_merge_request_rule_model()
    test_pipeline_model()
    test_project_model()
    test_protected_branches_model()
    test_release_model()
    test_wiki_model()