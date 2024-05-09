#!/usr/bin/env python
# coding: utf-8
from gitlab_api.version import __version__, __author__, __credits__
from gitlab_api.gitlab_api import Api
from gitlab_api.gitlab_models import (
    BranchModel,
    CommitModel,
    DeployTokenModel,
    GroupModel,
    JobModel,
    MembersModel,
    PackageModel,
    PipelineModel,
    ProjectModel,
    ProtectedBranchModel,
    MergeRequestModel,
    MergeRequestRuleModel,
    ReleaseModel,
    RunnerModel,
    UserModel,
    WikiModel,
)

"""
GitLab API

A Python Wrapper for GitLab API
"""

__version__ = __version__
__author__ = __author__
__credits__ = __credits__

__all__ = [
    "Api",
    "BranchModel",
    "CommitModel",
    "DeployTokenModel",
    "GroupModel",
    "JobModel",
    "MembersModel",
    "PackageModel",
    "PipelineModel",
    "ProjectModel",
    "ProtectedBranchModel",
    "MergeRequestModel",
    "ReleaseModel",
    "RunnerModel",
    "UserModel",
    "WikiModel",
]
