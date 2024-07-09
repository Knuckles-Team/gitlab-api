#!/usr/bin/python
# coding: utf-8
import logging

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref, declarative_base
from sqlalchemy import Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    Float,
    JSON,
)

Base = declarative_base()


merge_approval_approvers = Table(
    "merge_approval_approvers",
    Base.metadata,
    Column(
        "merge_approval_id", Integer, ForeignKey("merge_approvals.id"), primary_key=True
    ),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)

merge_approval_approver_groups = Table(
    "merge_approval_approver_groups",
    Base.metadata,
    Column(
        "merge_approval_id", Integer, ForeignKey("merge_approvals.id"), primary_key=True
    ),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)

# Association table for many-to-many relationship between TestReport and TestSuite
test_report_test_suites = Table(
    "test_report_test_suites",
    Base.metadata,
    Column("test_report_id", Integer, ForeignKey("test_reports.id"), primary_key=True),
    Column("test_suite_id", Integer, ForeignKey("test_suites.id"), primary_key=True),
)

project_shared_with_groups = (
    Table(
        "project_shared_with_groups",
        Base.metadata,
        Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
        Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    )
    if "Group" in globals()
    else None
)

runner_projects = (
    Table(
        "runner_projects",
        Base.metadata,
        Column("runner_id", Integer, ForeignKey("runners.id"), primary_key=True),
        Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    )
    if "Project" in globals()
    else None
)

default_branch_protection_push_access = (
    Table(
        "default_branch_protection_push_access",
        Base.metadata,
        Column(
            "default_branch_protection_defaults_id",
            Integer,
            ForeignKey("default_branch_protection_defaults.id"),
            primary_key=True,
        ),
        Column(
            "group_access_id",
            Integer,
            ForeignKey("group_accesses.id"),
            primary_key=True,
        ),
    )
    if "GroupAccess" in globals()
    else None
)

default_branch_protection_merge_access = (
    Table(
        "default_branch_protection_merge_access",
        Base.metadata,
        Column(
            "default_branch_protection_defaults_id",
            Integer,
            ForeignKey("default_branch_protection_defaults.id"),
            primary_key=True,
        ),
        Column(
            "group_access_id",
            Integer,
            ForeignKey("group_accesses.id"),
            primary_key=True,
        ),
    )
    if "GroupAccess" in globals()
    else None
)

branch_push_access_levels = (
    Table(
        "branch_push_access_levels",
        Base.metadata,
        Column("branch_id", Integer, ForeignKey("branches.id"), primary_key=True),
        Column(
            "access_level_id", Integer, ForeignKey("access_levels.id"), primary_key=True
        ),
    )
    if "AccessLevel" in globals()
    else None
)

branch_merge_access_levels = (
    Table(
        "branch_merge_access_levels",
        Base.metadata,
        Column("branch_id", Integer, ForeignKey("branches.id"), primary_key=True),
        Column(
            "access_level_id", Integer, ForeignKey("access_levels.id"), primary_key=True
        ),
    )
    if "AccessLevel" in globals()
    else None
)

branch_unprotect_access_levels = (
    Table(
        "branch_unprotect_access_levels",
        Base.metadata,
        Column("branch_id", Integer, ForeignKey("branches.id"), primary_key=True),
        Column(
            "access_level_id", Integer, ForeignKey("access_levels.id"), primary_key=True
        ),
    )
    if "AccessLevel" in globals()
    else None
)

approval_rule_eligible_approvers = (
    Table(
        "approval_rule_eligible_approvers",
        Base.metadata,
        Column(
            "approval_rule_id",
            Integer,
            ForeignKey("approval_rules.id"),
            primary_key=True,
        ),
        Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    )
    if "User" in globals()
    else None
)

approval_rule_users = (
    Table(
        "approval_rule_users",
        Base.metadata,
        Column(
            "approval_rule_id",
            Integer,
            ForeignKey("approval_rules.id"),
            primary_key=True,
        ),
        Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    )
    if "User" in globals()
    else None
)

approval_rule_groups = (
    Table(
        "approval_rule_groups",
        Base.metadata,
        Column(
            "approval_rule_id",
            Integer,
            ForeignKey("approval_rules.id"),
            primary_key=True,
        ),
        Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    )
    if "Group" in globals()
    else None
)

approval_rule_protected_branches = (
    Table(
        "approval_rule_protected_branches",
        Base.metadata,
        Column(
            "approval_rule_id",
            Integer,
            ForeignKey("approval_rules.id"),
            primary_key=True,
        ),
        Column("branch_id", Integer, ForeignKey("branches.id"), primary_key=True),
    )
    if "Branch" in globals()
    else None
)

approval_rule_approved_by = (
    Table(
        "approval_rule_approved_by",
        Base.metadata,
        Column(
            "approval_rule_id",
            Integer,
            ForeignKey("approval_rules.id"),
            primary_key=True,
        ),
        Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    )
    if "User" in globals()
    else None
)

merge_request_labels = (
    Table(
        "merge_request_labels",
        Base.metadata,
        Column(
            "merge_request_id",
            Integer,
            ForeignKey("merge_requests.id"),
            primary_key=True,
        ),
        Column("label_id", Integer, ForeignKey("labels.id"), primary_key=True),
    )
    if "Label" in globals()
    else None
)

merge_request_reviewers = (
    Table(
        "merge_request_reviewers",
        Base.metadata,
        Column(
            "merge_request_id",
            Integer,
            ForeignKey("merge_requests.id"),
            primary_key=True,
        ),
        Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    )
    if "User" in globals()
    else None
)

release_milestones = (
    Table(
        "release_milestones",
        Base.metadata,
        Column("release_id", String, ForeignKey("releases.id"), primary_key=True),
        Column("milestone_id", String, ForeignKey("milestones.id"), primary_key=True),
    )
    if "Milestone" in globals()
    else None
)

release_evidences = (
    Table(
        "release_evidences",
        Base.metadata,
        Column("release_id", String, ForeignKey("releases.id"), primary_key=True),
        Column("evidence_id", String, ForeignKey("evidences.id"), primary_key=True),
    )
    if "Evidence" in globals()
    else None
)
merge_approval_approvers = (
    Table(
        "merge_approval_approvers",
        Base.metadata,
        Column(
            "merge_approval_id",
            Integer,
            ForeignKey("merge_approvals.id"),
            primary_key=True,
        ),
        Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    )
    if "User" in globals()
    else None
)

merge_approval_approver_groups = (
    Table(
        "merge_approval_approver_groups",
        Base.metadata,
        Column(
            "merge_approval_id",
            Integer,
            ForeignKey("merge_approvals.id"),
            primary_key=True,
        ),
        Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    )
    if "Group" in globals()
    else None
)


# DeployToken Model
class DeployToken(Base):
    __tablename__ = "deploy_tokens"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="DeployToken")
    user_id = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    token = Column(String, nullable=True)
    revoked = Column(Boolean, nullable=True)
    expired = Column(Boolean, nullable=True)
    scopes = Column(ARRAY(String), nullable=True)
    active = Column(Boolean, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)


# Rule Model
class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Rule")
    created_at = Column(DateTime, nullable=True)
    commit_committer_check = Column(Boolean, default=False)
    commit_committer_name_check = Column(Boolean, default=False)
    reject_unsigned_commits = Column(Boolean, default=False)
    commit_message_regex = Column(String, nullable=True)
    commit_message_negative_regex = Column(String, nullable=True)
    branch_name_regex = Column(String, nullable=True)
    deny_delete_tag = Column(Boolean, default=False)
    member_check = Column(Boolean, default=False)
    prevent_secrets = Column(Boolean, default=False)
    author_email_regex = Column(String, nullable=True)
    file_name_regex = Column(String, nullable=True)
    max_file_size = Column(Integer, nullable=True)


# AccessControl Model
class AccessControl(Base):
    __tablename__ = "access_controls"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="AccessControl")
    name = Column(String, nullable=True)
    access_level = Column(Integer, nullable=True)
    member_role_id = Column(Integer, nullable=True)


# Source Model
class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Source")
    format = Column(String, nullable=True)
    url = Column(String, nullable=True)


# Link Model
class Link(Base):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Link")
    name = Column(String, nullable=True)
    url = Column(String, nullable=True)
    link_type = Column(String, nullable=True)


# Assets Model
class Assets(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Assets")
    count = Column(Integer, nullable=True)
    sources = relationship("Source", backref=backref("assets"))
    links = relationship("Link", backref=backref("assets"))
    evidence_file_path = Column(String, nullable=True)


# Evidence Model
class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Evidence")
    sha = Column(String, nullable=True)
    filepath = Column(String, nullable=True)
    collected_at = Column(DateTime, nullable=True)


# ReleaseLinks Model
class ReleaseLinks(Base):
    __tablename__ = "release_links"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ReleaseLinks")
    closed_issues_url = Column(String, nullable=True)
    closed_merge_requests_url = Column(String, nullable=True)
    edit_url = Column(String, nullable=True)
    merged_merge_requests_url = Column(String, nullable=True)
    opened_issues_url = Column(String, nullable=True)
    opened_merge_requests_url = Column(String, nullable=True)
    self_url = Column(String, nullable=True)


# Token Model
class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Token")
    token = Column(String, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)


# ToDo Model
class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ToDo")
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action_name = Column(String, nullable=True)
    target_type = Column(String, nullable=True)
    target_id = Column(Integer, ForeignKey("issues.id"), nullable=True)
    target_url = Column(String, nullable=True)
    body = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)

    project = (
        relationship("Project", backref=backref("todos"))
        if "Project" in globals()
        else None
    )
    author = (
        relationship("User", backref=backref("todos")) if "User" in globals() else None
    )
    target = (
        relationship("Issue", backref=backref("todos"))
        if "Issue" in globals()
        else None
    )


# WikiPage Model
class WikiPage(Base):
    __tablename__ = "wiki_pages"
    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="WikiPage")
    content = Column(String, nullable=True)
    format = Column(String, nullable=True)
    slug = Column(String, nullable=True)
    title = Column(String, nullable=True)
    encoding = Column(String, nullable=True)


# WikiAttachmentLink Model
class WikiAttachmentLink(Base):
    __tablename__ = "wiki_attachment_links"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="WikiAttachmentLink")
    url = Column(String, nullable=True)
    markdown = Column(String, nullable=True)


# PipelineVariable Model
class PipelineVariable(Base):
    __tablename__ = "pipeline_variables"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="PipelineVariable")
    key = Column(String, nullable=True)
    variable_type = Column(String, nullable=True)
    value = Column(String, nullable=True)


# WikiAttachment Model
class WikiAttachment(Base):
    __tablename__ = "wiki_attachments"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="WikiAttachment")
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    branch = Column(String, nullable=True)
    link_id = Column(Integer, ForeignKey("wiki_attachment_links.id"), nullable=True)

    link = (
        relationship("WikiAttachmentLink", backref=backref("wiki_attachment"))
        if "WikiAttachmentLink" in globals()
        else None
    )


# Agent Model
class Agent(Base):
    __tablename__ = "agent"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Agent")
    config_project_id = Column(Integer, ForeignKey("project_configs.id"), nullable=True)

    config_project = (
        relationship("ProjectConfig", backref=backref("agents"))
        if "ProjectConfig" in globals()
        else None
    )


# Agents Model
class Agents(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Agents")
    allowed_agents = relationship("Agent", backref=backref("agents"))
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    job = relationship("Job", backref=backref("agents")) if "Job" in globals() else None
    pipeline = (
        relationship("Pipeline", backref=backref("agents"))
        if "Pipeline" in globals()
        else None
    )
    project = (
        relationship("Project", backref=backref("agents"))
        if "Project" in globals()
        else None
    )
    user = (
        relationship("User", backref=backref("agents")) if "User" in globals() else None
    )


class Release(Base):
    __tablename__ = "releases"

    id = Column(String, primary_key=True)
    base_type = Column(String, default="Release")
    tag_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    released_at = Column(DateTime, nullable=True)
    commit_path = Column(String, nullable=True)
    tag_path = Column(String, nullable=True)
    evidence_sha = Column(String, nullable=True)

    # Relationships (optional)
    author_id = Column(String, ForeignKey("users.id"), nullable=True)
    commit_id = Column(String, ForeignKey("commits.id"), nullable=True)
    assets_id = Column(String, ForeignKey("assets.id"), nullable=True)
    links_id = Column(String, ForeignKey("release_links.id"), nullable=True)

    author = (
        relationship("User", backref=backref("releases"), foreign_keys=[author_id])
        if "User" in globals()
        else None
    )
    commit = (
        relationship("Commit", backref=backref("releases"), foreign_keys=[commit_id])
        if "Commit" in globals()
        else None
    )
    milestones = (
        relationship(
            "Milestone", secondary="release_milestones", backref=backref("releases")
        )
        if "Milestone" in globals()
        else None
    )
    evidences = (
        relationship(
            "Evidence", secondary="release_evidences", backref=backref("releases")
        )
        if "Evidence" in globals()
        else None
    )
    assets = (
        relationship("Assets", backref=backref("release"), foreign_keys=[assets_id])
        if "Assets" in globals()
        else None
    )
    links = (
        relationship(
            "ReleaseLinks", backref=backref("release"), foreign_keys=[links_id]
        )
        if "ReleaseLinks" in globals()
        else None
    )


# Branch Model
class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Branch")
    name = Column(String, nullable=True)
    merged = Column(Boolean, nullable=True)
    protected = Column(Boolean, nullable=True)
    default = Column(Boolean, nullable=True)
    developers_can_push = Column(Boolean, nullable=True)
    developers_can_merge = Column(Boolean, nullable=True)
    can_push = Column(Boolean, nullable=True)
    web_url = Column(String, nullable=True)
    allow_force_push = Column(Boolean, nullable=True)
    code_owner_approval_required = Column(Boolean, nullable=True)
    inherited = Column(Boolean, nullable=True)

    commit_id = Column(Integer, ForeignKey("commits.id"), nullable=True)
    commit = (
        relationship("Commit", backref=backref("branches"))
        if "Commit" in globals()
        else None
    )
    push_access_levels = (
        relationship(
            "AccessLevel",
            secondary="branch_push_access_levels",
            backref=backref("branches"),
        )
        if "AccessLevel" in globals()
        else None
    )
    merge_access_levels = (
        relationship(
            "AccessLevel",
            secondary="branch_merge_access_levels",
            backref=backref("branches"),
        )
        if "AccessLevel" in globals()
        else None
    )
    unprotect_access_levels = (
        relationship(
            "AccessLevel",
            secondary="branch_unprotect_access_levels",
            backref=backref("branches"),
        )
        if "AccessLevel" in globals()
        else None
    )


# ApprovalRule Model
class ApprovalRule(Base):
    __tablename__ = "approval_rules"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ApprovalRule")
    name = Column(String, nullable=True)
    rule_type = Column(String, nullable=True)
    approvals_required = Column(Integer, nullable=True)
    contains_hidden_groups = Column(Boolean, nullable=True)
    applies_to_all_protected_branches = Column(Boolean, nullable=True)
    source_rule = Column(String, nullable=True)
    approved = Column(Boolean, nullable=True)
    overridden = Column(Boolean, nullable=True)

    eligible_approvers = (
        relationship(
            "User",
            secondary="approval_rule_eligible_approvers",
            backref=backref("approval_rules"),
        )
        if "User" in globals()
        else None
    )
    users = (
        relationship(
            "User",
            secondary="approval_rule_users",
            backref=backref("approval_rules_users"),
        )
        if "User" in globals()
        else None
    )
    groups = (
        relationship(
            "Group",
            secondary="approval_rule_groups",
            backref=backref("approval_rules_groups"),
        )
        if "Group" in globals()
        else None
    )
    protected_branches = (
        relationship(
            "Branch",
            secondary="approval_rule_protected_branches",
            backref=backref("approval_rules_branches"),
        )
        if "Branch" in globals()
        else None
    )
    approved_by = (
        relationship(
            "User",
            secondary="approval_rule_approved_by",
            backref=backref("approval_rules_approved_by"),
        )
        if "User" in globals()
        else None
    )


# MergeRequest Model
class MergeRequest(Base):
    __tablename__ = "merge_requests"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="MergeRequest")
    iid = Column(Integer, nullable=True)
    project_id = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    target_branch = Column(String, nullable=True)
    source_branch = Column(String, nullable=True)
    upvotes = Column(Integer, nullable=True)
    downvotes = Column(Integer, nullable=True)
    source_project_id = Column(Integer, nullable=True)
    target_project_id = Column(Integer, nullable=True)
    work_in_progress = Column(Boolean, nullable=True)
    merge_when_pipeline_succeeds = Column(Boolean, nullable=True)
    merge_status = Column(String, nullable=True)
    sha = Column(String, nullable=True)
    merge_commit_sha = Column(String, nullable=True)
    draft = Column(Boolean, nullable=True)
    squash_commit_sha = Column(String, nullable=True)
    squash_on_merge = Column(Boolean, nullable=True)
    user_notes_count = Column(Integer, nullable=True)
    discussion_locked = Column(Boolean, nullable=True)
    should_remove_source_branch = Column(Boolean, nullable=True)
    force_remove_source_branch = Column(Boolean, nullable=True)
    allow_collaboration = Column(Boolean, nullable=True)
    allow_maintainer_to_push = Column(Boolean, nullable=True)
    web_url = Column(String, nullable=True)
    reference = Column(String, nullable=True)
    squash = Column(Boolean, nullable=True)
    has_conflicts = Column(Boolean, nullable=True)
    blocking_discussions_resolved = Column(Boolean, nullable=True)
    changes_count = Column(String, nullable=True)
    rebase_in_progress = Column(Boolean, nullable=True)
    approvals_before_merge = Column(Integer, nullable=True)
    tag_list = Column(ARRAY(String), nullable=True)
    imported = Column(Boolean, nullable=True)
    imported_from = Column(String, nullable=True)
    prepared_at = Column(DateTime, nullable=True)
    detailed_merge_status = Column(String, nullable=True)
    subscribed = Column(Boolean, nullable=True)
    overflow = Column(Boolean, nullable=True)
    diverged_commits_count = Column(Integer, nullable=True)
    merge_error = Column(String, nullable=True)
    approvals_required = Column(Integer, nullable=True)
    approvals_left = Column(Integer, nullable=True)
    approval_rules_overwritten = Column(Boolean, nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    milestone_id = Column(Integer, ForeignKey("milestones.id"), nullable=True)
    merged_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    closed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    head_pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)

    author = (
        relationship(
            "User", foreign_keys=[author_id], backref=backref("authored_merge_requests")
        )
        if "User" in globals()
        else None
    )
    assignee = (
        relationship(
            "User",
            foreign_keys=[assignee_id],
            backref=backref("assigned_merge_requests"),
        )
        if "User" in globals()
        else None
    )
    milestone = (
        relationship("Milestone", backref=backref("merge_requests"))
        if "Milestone" in globals()
        else None
    )
    merged_by = (
        relationship(
            "User",
            foreign_keys=[merged_by_id],
            backref=backref("merged_merge_requests"),
        )
        if "User" in globals()
        else None
    )
    closed_by = (
        relationship(
            "User",
            foreign_keys=[closed_by_id],
            backref=backref("closed_merge_requests"),
        )
        if "User" in globals()
        else None
    )
    pipeline = (
        relationship(
            "Pipeline", foreign_keys=[pipeline_id], backref=backref("merge_requests")
        )
        if "Pipeline" in globals()
        else None
    )
    head_pipeline = (
        relationship(
            "Pipeline",
            foreign_keys=[head_pipeline_id],
            backref=backref("head_merge_requests"),
        )
        if "Pipeline" in globals()
        else None
    )

    labels = (
        relationship(
            "Label", secondary="merge_request_labels", backref=backref("merge_requests")
        )
        if "Label" in globals()
        else None
    )
    references_id = Column(Integer, ForeignKey("references.id"), nullable=True)
    references = (
        relationship("References", backref=backref("merge_requests"))
        if "References" in globals()
        else None
    )
    time_stats_id = Column(Integer, ForeignKey("time_stats.id"), nullable=True)
    time_stats = (
        relationship("TimeStats", backref=backref("merge_requests"))
        if "TimeStats" in globals()
        else None
    )
    task_completion_status_id = Column(
        Integer, ForeignKey("task_completion_status.id"), nullable=True
    )
    task_completion_status = (
        relationship("TaskCompletionStatus", backref=backref("merge_requests"))
        if "TaskCompletionStatus" in globals()
        else None
    )
    changes = (
        relationship("Diff", backref=backref("merge_requests"))
        if "Diff" in globals()
        else None
    )
    reviewers = (
        relationship(
            "User",
            secondary="merge_request_reviewers",
            backref=backref("reviewed_merge_requests"),
        )
        if "User" in globals()
        else None
    )
    approved_by = (
        relationship("ApprovedByUser", backref=backref("merge_requests"))
        if "ApprovedByUser" in globals()
        else None
    )
    rules = (
        relationship("ApprovalRule", backref=backref("merge_requests"))
        if "ApprovalRule" in globals()
        else None
    )


# MergeRequests Model


# GroupAccess Model
class GroupAccess(Base):
    __tablename__ = "group_accesses"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="GroupAccess")
    access_level = Column(Integer, nullable=True)


# DefaultBranchProtectionDefaults Model
class DefaultBranchProtectionDefaults(Base):
    __tablename__ = "default_branch_protection_defaults"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="DefaultBranchProtectionDefaults")
    allow_force_push = Column(Boolean, nullable=True)

    allowed_to_push = (
        relationship(
            "GroupAccess",
            secondary="default_branch_protection_push_access",
            backref=backref("push_defaults"),
        )
        if "GroupAccess" in globals()
        else None
    )
    allowed_to_merge = (
        relationship(
            "GroupAccess",
            secondary="default_branch_protection_merge_access",
            backref=backref("merge_defaults"),
        )
        if "GroupAccess" in globals()
        else None
    )


# Group Model
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Group")
    organization_id = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    path = Column(String, nullable=True)
    description = Column(String, nullable=True)
    visibility = Column(String, nullable=True)
    shared_runners_setting = Column(String, nullable=True)
    share_with_group_lock = Column(Boolean, nullable=True)
    require_two_factor_authentication = Column(Boolean, nullable=True)
    two_factor_grace_period = Column(Integer, nullable=True)
    project_creation_level = Column(String, nullable=True)
    auto_devops_enabled = Column(Boolean, nullable=True)
    subgroup_creation_level = Column(String, nullable=True)
    emails_disabled = Column(Boolean, nullable=True)
    emails_enabled = Column(Boolean, nullable=True)
    mentions_disabled = Column(Boolean, nullable=True)
    lfs_enabled = Column(Boolean, nullable=True)
    default_branch = Column(String, nullable=True)
    default_branch_protection = Column(Integer, nullable=True)
    avatar_url = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    request_access_enabled = Column(Boolean, nullable=True)
    repository_storage = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    full_path = Column(String, nullable=True)
    file_template_project_id = Column(Integer, nullable=True)
    parent_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    wiki_access_level = Column(String, nullable=True)
    duo_features_enabled = Column(Boolean, nullable=True)
    lock_duo_features_enabled = Column(Boolean, nullable=True)
    runners_token = Column(String, nullable=True)
    enabled_git_access_protocol = Column(String, nullable=True)
    prevent_sharing_groups_outside_hierarchy = Column(Boolean, nullable=True)
    ip_restriction_ranges = Column(String, nullable=True)
    math_rendering_limits_enabled = Column(Boolean, nullable=True)
    lock_math_rendering_limits_enabled = Column(Boolean, nullable=True)
    shared_runners_minutes_limit = Column(Integer, nullable=True)
    extra_shared_runners_minutes_limit = Column(Integer, nullable=True)
    marked_for_deletion_on = Column(DateTime, nullable=True)
    membership_lock = Column(Boolean, nullable=True)
    ldap_cn = Column(String, nullable=True)
    ldap_access = Column(String, nullable=True)
    prevent_forking_outside_group = Column(Boolean, nullable=True)

    default_branch_protection_defaults_id = Column(
        Integer, ForeignKey("default_branch_protection_defaults.id"), nullable=True
    )
    default_branch_protection_defaults = (
        relationship("DefaultBranchProtectionDefaults", backref=backref("groups"))
        if "DefaultBranchProtectionDefaults" in globals()
        else None
    )
    statistics_id = Column(Integer, ForeignKey("statistics.id"), nullable=True)
    statistics = (
        relationship("Statistics", backref=backref("groups"))
        if "Statistics" in globals()
        else None
    )
    projects = (
        relationship("Project", backref=backref("group_projects"))
        if "Project" in globals()
        else None
    )
    shared_projects = (
        relationship("Project", backref=backref("shared_group_projects"))
        if "Project" in globals()
        else None
    )


# Webhook Model
class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Webhook")
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    group_id = Column(Integer, nullable=False)
    push_events = Column(Boolean, nullable=False)
    push_events_branch_filter = Column(String, nullable=True)
    issues_events = Column(Boolean, nullable=False)
    confidential_issues_events = Column(Boolean, nullable=False)
    merge_requests_events = Column(Boolean, nullable=False)
    tag_push_events = Column(Boolean, nullable=False)
    note_events = Column(Boolean, nullable=False)
    confidential_note_events = Column(Boolean, nullable=False)
    job_events = Column(Boolean, nullable=False)
    pipeline_events = Column(Boolean, nullable=False)
    wiki_page_events = Column(Boolean, nullable=False)
    deployment_events = Column(Boolean, nullable=False)
    releases_events = Column(Boolean, nullable=False)
    subgroup_events = Column(Boolean, nullable=False)
    member_events = Column(Boolean, nullable=False)
    enable_ssl_verification = Column(Boolean, nullable=False)
    repository_update_events = Column(Boolean, default=False)
    alert_status = Column(String, nullable=True)
    disabled_until = Column(DateTime, nullable=True)
    url_variables = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    resource_access_token_events = Column(Boolean, nullable=False)
    custom_webhook_template = Column(String, nullable=True)


# AccessLevel Model
class AccessLevel(Base):
    __tablename__ = "access_levels"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="AccessLevel")
    access_level = Column(Integer, nullable=True)
    access_level_description = Column(String, nullable=True)
    deploy_key_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    group_id = Column(Integer, nullable=True)


class ApprovedByUser(Base):
    __tablename__ = "approved_by_users"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ApprovedByUser")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = (
        relationship("User", backref=backref("approved_by_users"))
        if "User" in globals()
        else None
    )


# Project Model
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Project")
    description = Column(String, nullable=True)
    description_html = Column(String, nullable=True)
    name = Column(String, nullable=True)
    name_with_namespace = Column(String, nullable=True)
    path = Column(String, nullable=True)
    path_with_namespace = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    default_branch = Column(String, nullable=True)
    tag_list = Column(JSON, nullable=True)
    topics = Column(JSON, nullable=True)
    ssh_url_to_repo = Column(String, nullable=True)
    http_url_to_repo = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    readme_url = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    forks_count = Column(Integer, nullable=True)
    star_count = Column(Integer, nullable=True)
    last_activity_at = Column(DateTime, nullable=True)
    container_registry_image_prefix = Column(String, nullable=True)
    packages_enabled = Column(Boolean, nullable=True)
    empty_repo = Column(Boolean, nullable=True)
    archived = Column(Boolean, nullable=True)
    visibility = Column(String, nullable=True)
    resolve_outdated_diff_discussions = Column(Boolean, nullable=True)
    releases_access_level = Column(String, nullable=True)
    environments_access_level = Column(String, nullable=True)
    feature_flags_access_level = Column(String, nullable=True)
    infrastructure_access_level = Column(String, nullable=True)
    monitor_access_level = Column(String, nullable=True)
    machine_learning_model_experiments_access_level = Column(String, nullable=True)
    machine_learning_model_registry_access_level = Column(String, nullable=True)
    issues_enabled = Column(Boolean, nullable=True)
    merge_requests_enabled = Column(Boolean, nullable=True)
    wiki_enabled = Column(Boolean, nullable=True)
    jobs_enabled = Column(Boolean, nullable=True)
    snippets_enabled = Column(Boolean, nullable=True)
    container_registry_enabled = Column(Boolean, nullable=True)
    container_registry_access_level = Column(String, nullable=True)
    security_and_compliance_access_level = Column(String, nullable=True)
    creator_id = Column(Integer, nullable=True)
    import_url = Column(String, nullable=True)
    import_type = Column(String, nullable=True)
    import_status = Column(String, nullable=True)
    import_error = Column(String, nullable=True)
    shared_runners_enabled = Column(Boolean, nullable=True)
    group_runners_enabled = Column(Boolean, nullable=True)
    lfs_enabled = Column(Boolean, nullable=True)
    ci_default_git_depth = Column(Integer, nullable=True)
    ci_forward_deployment_enabled = Column(Boolean, nullable=True)
    ci_forward_deployment_rollback_allowed = Column(Boolean, nullable=True)
    ci_allow_fork_pipelines_to_run_in_parent_project = Column(Boolean, nullable=True)
    ci_separated_caches = Column(Boolean, nullable=True)
    ci_restrict_pipeline_cancellation_role = Column(String, nullable=True)
    forked_from_project = Column(JSON, nullable=True)
    mr_default_target_self = Column(Boolean, nullable=True)
    public_jobs = Column(Boolean, nullable=True)
    only_allow_merge_if_pipeline_succeeds = Column(Boolean, nullable=True)
    allow_merge_on_skipped_pipeline = Column(Boolean, nullable=True)
    restrict_user_defined_variables = Column(Boolean, nullable=True)
    code_suggestions = Column(Boolean, nullable=True)
    only_allow_merge_if_all_discussions_are_resolved = Column(Boolean, nullable=True)
    remove_source_branch_after_merge = Column(Boolean, nullable=True)
    request_access_enabled = Column(Boolean, nullable=True)
    merge_pipelines_enabled = Column(Boolean, nullable=True)
    merge_trains_skip_train_allowed = Column(Boolean, nullable=True)
    allow_pipeline_trigger_approve_deployment = Column(Boolean, nullable=True)
    repository_object_format = Column(String, nullable=True)
    merge_method = Column(String, nullable=True)
    squash_option = Column(String, nullable=True)
    enforce_auth_checks_on_uploads = Column(Boolean, nullable=True)
    suggestion_commit_message = Column(String, nullable=True)
    compliance_frameworks = Column(JSON, nullable=True)
    issues_template = Column(String, nullable=True)
    merge_requests_template = Column(String, nullable=True)
    packages_relocation_enabled = Column(Boolean, nullable=True)
    requirements_enabled = Column(Boolean, nullable=True)
    build_git_strategy = Column(String, nullable=True)
    build_timeout = Column(Integer, nullable=True)
    auto_cancel_pending_pipelines = Column(String, nullable=True)
    build_coverage_regex = Column(String, nullable=True)
    ci_config_path = Column(String, nullable=True)
    shared_runners_minutes_limit = Column(Integer, nullable=True)
    extra_shared_runners_minutes_limit = Column(Integer, nullable=True)
    printing_merge_request_link_enabled = Column(Boolean, nullable=True)
    merge_trains_enabled = Column(Boolean, nullable=True)
    has_open_issues = Column(Boolean, nullable=True)
    approvals_before_merge = Column(Integer, nullable=True)
    mirror = Column(Boolean, nullable=True)
    mirror_user_id = Column(Integer, nullable=True)
    mirror_trigger_builds = Column(Boolean, nullable=True)
    only_mirror_protected_branches = Column(Boolean, nullable=True)
    mirror_overwrites_diverged_branches = Column(Boolean, nullable=True)
    service_desk_enabled = Column(Boolean, nullable=True)
    can_create_merge_request_in = Column(Boolean, nullable=True)
    repository_access_level = Column(String, nullable=True)
    merge_requests_access_level = Column(String, nullable=True)
    issues_access_level = Column(String, nullable=True)
    forking_access_level = Column(String, nullable=True)
    wiki_access_level = Column(String, nullable=True)
    builds_access_level = Column(String, nullable=True)
    snippets_access_level = Column(String, nullable=True)
    pages_access_level = Column(String, nullable=True)
    analytics_access_level = Column(String, nullable=True)
    emails_disabled = Column(Boolean, nullable=True)
    emails_enabled = Column(Boolean, nullable=True)
    open_issues_count = Column(Integer, nullable=True)
    ci_job_token_scope_enabled = Column(Boolean, nullable=True)
    merge_commit_template = Column(String, nullable=True)
    squash_commit_template = Column(String, nullable=True)
    issue_branch_template = Column(String, nullable=True)
    auto_devops_enabled = Column(Boolean, nullable=True)
    auto_devops_deploy_strategy = Column(String, nullable=True)
    autoclose_referenced_issues = Column(Boolean, nullable=True)
    keep_latest_artifact = Column(Boolean, nullable=True)
    runner_token_expiration_interval = Column(Boolean, nullable=True)
    external_authorization_classification_label = Column(String, nullable=True)
    requirements_access_level = Column(String, nullable=True)
    security_and_compliance_enabled = Column(Boolean, nullable=True)
    warn_about_potentially_unwanted_characters = Column(Boolean, nullable=True)
    runners_token = Column(String, nullable=True)
    repository_storage = Column(String, nullable=True)
    service_desk_address = Column(String, nullable=True)
    marked_for_deletion_at = Column(DateTime, nullable=True)
    marked_for_deletion_on = Column(DateTime, nullable=True)
    operations_access_level = Column(String, nullable=True)
    ci_dockerfile = Column(String, nullable=True)
    public = Column(Boolean, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = (
        relationship("User", backref=backref("owned_projects"))
        if "User" in globals()
        else None
    )
    namespace_id = Column(Integer, ForeignKey("namespaces.id"), nullable=True)
    namespace = (
        relationship("Namespace", backref=backref("projects"))
        if "Namespace" in globals()
        else None
    )
    container_expiration_policy_id = Column(
        Integer, ForeignKey("container_expiration_policies.id"), nullable=True
    )
    container_expiration_policy = (
        relationship("ContainerExpirationPolicy", backref=backref("projects"))
        if "ContainerExpirationPolicy" in globals()
        else None
    )
    statistics_id = Column(Integer, ForeignKey("statistics.id"), nullable=True)
    statistics = (
        relationship("Statistics", backref=backref("projects"))
        if "Statistics" in globals()
        else None
    )
    links_id = Column(Integer, ForeignKey("links.id"), nullable=True)
    links = (
        relationship("Links", backref=backref("projects"))
        if "Links" in globals()
        else None
    )
    permissions_id = Column(Integer, ForeignKey("permissions.id"), nullable=True)
    permissions = (
        relationship("Permissions", backref=backref("projects"))
        if "Permissions" in globals()
        else None
    )
    shared_with_groups = (
        relationship(
            "Group",
            secondary="project_shared_with_groups",
            backref=backref("shared_projects"),
        )
        if "Group" in globals()
        else None
    )


# Runner Model
class Runner(Base):
    __tablename__ = "runners"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Runner")
    description = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)
    paused = Column(Boolean, nullable=True)
    is_shared = Column(Boolean, nullable=True)
    runner_type = Column(String, nullable=True)
    name = Column(String, nullable=True)
    online = Column(Boolean, nullable=True)
    status = Column(String, nullable=True)
    contacted_at = Column(DateTime, nullable=True)
    architecture = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    revision = Column(String, nullable=True)
    version = Column(String, nullable=True)
    access_level = Column(String, nullable=True)
    maximum_timeout = Column(Integer, nullable=True)
    maintenance_note = Column(String, nullable=True)
    tag_list = Column(JSON, nullable=True)

    projects = (
        relationship("Project", secondary="runner_projects", backref=backref("runners"))
        if "Project" in globals()
        else None
    )


# Job Model
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Job")
    coverage = Column(Float, nullable=True)
    archived = Column(Boolean, nullable=True)
    allow_failure = Column(Boolean, nullable=True)
    created_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    erased_at = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)
    queued_duration = Column(Float, nullable=True)
    artifacts_expire_at = Column(DateTime, nullable=True)
    tag_list = Column(JSON, nullable=True)
    name = Column(String, nullable=True)
    ref = Column(String, nullable=True)
    stage = Column(String, nullable=True)
    status = Column(String, nullable=True)
    failure_reason = Column(String, nullable=True)
    tag = Column(Boolean, nullable=True)
    web_url = Column(String, nullable=True)

    commit_id = Column(Integer, ForeignKey("commits.id"), nullable=True)
    commit = (
        relationship("Commit", backref=backref("jobs"))
        if "Commit" in globals()
        else None
    )
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    pipeline = (
        relationship("Pipeline", backref=backref("jobs"))
        if "Pipeline" in globals()
        else None
    )
    runner_id = Column(Integer, ForeignKey("runners.id"), nullable=True)
    runner = (
        relationship("Runner", backref=backref("jobs"))
        if "Runner" in globals()
        else None
    )
    runner_manager_id = Column(Integer, ForeignKey("runner_managers.id"), nullable=True)
    runner_manager = (
        relationship("RunnerManager", backref=backref("jobs"))
        if "RunnerManager" in globals()
        else None
    )
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = (
        relationship("Project", backref=backref("jobs"))
        if "Project" in globals()
        else None
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = (
        relationship("User", backref=backref("jobs")) if "User" in globals() else None
    )
    downstream_pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    downstream_pipeline = (
        relationship(
            "Pipeline",
            foreign_keys=[downstream_pipeline_id],
            backref=backref("jobs_downstream"),
        )
        if "Pipeline" in globals()
        else None
    )
    artifacts_file_id = Column(Integer, ForeignKey("artifacts_files.id"), nullable=True)
    artifacts_file = (
        relationship("ArtifactsFile", backref=backref("jobs"))
        if "ArtifactsFile" in globals()
        else None
    )
    artifacts = (
        relationship("Artifact", backref=backref("jobs"))
        if "Artifact" in globals()
        else None
    )


# Pipeline Model
class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Pipeline")
    iid = Column(Integer, nullable=True)
    ref = Column(String, nullable=True)
    sha = Column(String, nullable=True)
    status = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    before_sha = Column(String, nullable=True)
    tag = Column(Boolean, nullable=True)
    yaml_errors = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    committed_at = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)
    queued_duration = Column(Float, nullable=True)
    coverage = Column(String, nullable=True)
    name = Column(String, nullable=True)
    source = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = (
        relationship("User", backref=backref("pipelines"))
        if "User" in globals()
        else None
    )
    detailed_status_id = Column(
        Integer, ForeignKey("detailed_status.id"), nullable=True
    )
    detailed_status = (
        relationship("DetailedStatus", backref=backref("pipelines"))
        if "DetailedStatus" in globals()
        else None
    )


# PackageLink Model
class PackageLink(Base):
    __tablename__ = "package_links"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="PackageLink")
    web_path = Column(String, nullable=True)
    delete_api_path = Column(String, nullable=True)


# PackageVersion Model
class PackageVersion(Base):
    __tablename__ = "package_versions"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="PackageVersion")
    version = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)

    pipelines = (
        relationship(
            "Pipeline",
            secondary="package_version_pipelines",
            backref=backref("package_versions"),
        )
        if "Pipeline" in globals()
        else None
    )


# Package Model
class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Package")
    name = Column(String, nullable=True)
    version = Column(String, nullable=True)
    package_type = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    last_downloaded_at = Column(DateTime, nullable=True)
    conan_package_name = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    file_name = Column(String, nullable=True)
    file_md5 = Column(String, nullable=True)
    file_sha1 = Column(String, nullable=True)
    file_sha256 = Column(String, nullable=True)

    links_id = Column(Integer, ForeignKey("package_links.id"), nullable=True)
    links = (
        relationship("PackageLink", backref=backref("packages"))
        if "PackageLink" in globals()
        else None
    )
    pipelines = (
        relationship(
            "Pipeline", secondary="package_pipelines", backref=backref("packages")
        )
        if "Pipeline" in globals()
        else None
    )
    versions = (
        relationship("PackageVersion", backref=backref("packages"))
        if "PackageVersion" in globals()
        else None
    )


# Contributor Model
class Contributor(Base):
    __tablename__ = "contributors"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Contributor")
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    commits = Column(Integer, nullable=True)
    additions = Column(Integer, nullable=True)
    deletions = Column(Integer, nullable=True)


# CommitStats Model
class CommitStats(Base):
    __tablename__ = "commit_stats"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="CommitStats")
    additions = Column(Integer, nullable=True)
    deletions = Column(Integer, nullable=True)
    total = Column(Integer, nullable=True)


# CommitSignature Model
class CommitSignature(Base):
    __tablename__ = "commit_signatures"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="CommitSignature")
    signature_type = Column(String, nullable=True)
    verification_status = Column(String, nullable=True)
    commit_source = Column(String, nullable=True)
    gpg_key_id = Column(Integer, nullable=True)
    gpg_key_primary_keyid = Column(String, nullable=True)
    gpg_key_user_name = Column(String, nullable=True)
    gpg_key_user_email = Column(String, nullable=True)
    gpg_key_subkey_id = Column(String, nullable=True)
    key = Column(JSON, nullable=True)
    x509_certificate = Column(JSON, nullable=True)
    message = Column(String, nullable=True)


# Comment Model
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Comment")
    type = Column(String, nullable=True)
    body = Column(String, nullable=True)
    note = Column(String, nullable=True)
    attachment = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    system = Column(Boolean, nullable=True)
    noteable_id = Column(Integer, nullable=True)
    noteable_type = Column(String, nullable=True)
    resolvable = Column(Boolean, nullable=True)
    confidential = Column(Boolean, nullable=True)
    noteable_iid = Column(Integer, nullable=True)
    commands_changes = Column(JSON, nullable=True)
    line_type = Column(String, nullable=True)
    path = Column(String, nullable=True)
    line = Column(Integer, nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    author = (
        relationship("User", backref=backref("comments"))
        if "User" in globals()
        else None
    )


# Commit Model
class Commit(Base):
    __tablename__ = "commits"

    id = Column(String, primary_key=True)
    base_type = Column(String, default="Commit")
    short_id = Column(String, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    parent_ids = Column(JSON, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    message = Column(String, nullable=True)
    author_name = Column(String, nullable=True)
    author_email = Column(String, nullable=True)
    authored_date = Column(DateTime, nullable=True)
    committer_name = Column(String, nullable=True)
    committer_email = Column(String, nullable=True)
    committed_date = Column(DateTime, nullable=True)
    name = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    trailers = Column(JSON, nullable=True)
    extended_trailers = Column(JSON, nullable=True)
    status = Column(String, nullable=True)
    sha = Column(String, nullable=True)
    count = Column(Integer, nullable=True)
    dry_run = Column(String, nullable=True)
    individual_note = Column(Boolean, nullable=True)
    allow_failure = Column(Boolean, nullable=True)
    target_url = Column(String, nullable=True)
    ref = Column(String, nullable=True)
    error_code = Column(String, nullable=True)
    coverage = Column(Float, nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    author = (
        relationship("User", backref=backref("commits"))
        if "User" in globals()
        else None
    )
    stats_id = Column(Integer, ForeignKey("commit_stats.id"), nullable=True)
    stats = (
        relationship("CommitStats", backref=backref("commits"))
        if "CommitStats" in globals()
        else None
    )
    last_pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    last_pipeline = (
        relationship("Pipeline", backref=backref("commits"))
        if "Pipeline" in globals()
        else None
    )
    signature_id = Column(Integer, ForeignKey("commit_signatures.id"), nullable=True)
    signature = (
        relationship("CommitSignature", backref=backref("commits"))
        if "CommitSignature" in globals()
        else None
    )
    notes = (
        relationship("Comment", backref=backref("commit_comments"))
        if "Comment" in globals()
        else None
    )


# Membership Model
class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Membership")
    source_id = Column(Integer, nullable=True)
    source_full_name = Column(String, nullable=True)
    source_members_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    access_level = Column(JSON, nullable=True)


# Issue Model
class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Issue")
    state = Column(String, nullable=True)
    description = Column(String, nullable=True)
    project_id = Column(Integer, nullable=True)
    type = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    changes_count = Column(String, nullable=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    moved_to_id = Column(Integer, nullable=True)
    iid = Column(Integer, nullable=True)
    labels = Column(ARRAY(String), nullable=True)
    upvotes = Column(Integer, nullable=True)
    downvotes = Column(Integer, nullable=True)
    merge_requests_count = Column(Integer, nullable=True)
    user_notes_count = Column(Integer, nullable=True)
    due_date = Column(String, nullable=True)
    imported = Column(Boolean, nullable=True)
    imported_from = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    has_tasks = Column(Boolean, nullable=True)
    task_status = Column(String, nullable=True)
    confidential = Column(Boolean, nullable=True)
    discussion_locked = Column(Boolean, nullable=True)
    issue_type = Column(String, nullable=True)
    severity = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
    epic_iid = Column(Integer, nullable=True)
    health_status = Column(String, nullable=True)
    subscribed = Column(Boolean, nullable=True)
    service_desk_reply_to = Column(String, nullable=True)
    blocking_issues_count = Column(Integer, nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    milestone_id = Column(Integer, ForeignKey("milestones.id"), nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    closed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    iteration_id = Column(Integer, ForeignKey("iterations.id"), nullable=True)
    epic_id = Column(Integer, ForeignKey("epics.id"), nullable=True)

    author = (
        relationship("User", backref=backref("authored_issues"))
        if "User" in globals()
        else None
    )
    milestone = (
        relationship("Milestone", backref=backref("issues"))
        if "Milestone" in globals()
        else None
    )
    assignee = (
        relationship(
            "User", foreign_keys=[assignee_id], backref=backref("assigned_issues")
        )
        if "User" in globals()
        else None
    )
    closed_by = (
        relationship(
            "User", foreign_keys=[closed_by_id], backref=backref("closed_issues")
        )
        if "User" in globals()
        else None
    )
    iteration = (
        relationship("Iteration", backref=backref("issues"))
        if "Iteration" in globals()
        else None
    )
    epic = (
        relationship("Epic", backref=backref("issues")) if "Epic" in globals() else None
    )


class IssueStats(Base):
    __tablename__ = "issue_stats"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="IssueStats")
    total = Column(Integer, nullable=True)
    closed = Column(Integer, nullable=True)
    opened = Column(Integer, nullable=True)


# Milestone Model
class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Milestone")
    iid = Column(Integer, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    due_date = Column(String, nullable=True)
    start_date = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    closed_at = Column(DateTime, nullable=True)

    issue_stats_id = Column(Integer, ForeignKey("issue_stats.id"), nullable=True)
    issue_stats = (
        relationship("IssueStats", backref=backref("milestones"))
        if "IssueStats" in globals()
        else None
    )


# TimeStats Model
class TimeStats(Base):
    __tablename__ = "time_stats"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="TimeStats")
    time_estimate = Column(Integer, nullable=True)
    total_time_spent = Column(Integer, nullable=True)
    human_time_estimate = Column(String, nullable=True)
    human_total_time_spent = Column(String, nullable=True)


# TaskCompletionStatus Model
class TaskCompletionStatus(Base):
    __tablename__ = "task_completion_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="TaskCompletionStatus")
    count = Column(Integer, nullable=True)
    completed_count = Column(Integer, nullable=True)


# References Model
class References(Base):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="References")
    short = Column(String, nullable=True)
    relative = Column(String, nullable=True)
    full = Column(String, nullable=True)


# Artifact Model
class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Artifact")
    file_type = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
    filename = Column(String, nullable=True)
    file_format = Column(String, nullable=True)


# ArtifactsFile Model
class ArtifactsFile(Base):
    __tablename__ = "artifacts_files"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ArtifactsFile")
    filename = Column(String, nullable=True)
    size = Column(Integer, nullable=True)


# RunnerManager Model
class RunnerManager(Base):
    __tablename__ = "runner_managers"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="RunnerManager")
    system_id = Column(String, nullable=True)
    version = Column(String, nullable=True)
    revision = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    architecture = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    contacted_at = Column(DateTime, nullable=True)
    ip_address = Column(String, nullable=True)
    status = Column(String, nullable=True)


# Configuration Model
class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Configuration")
    approvals_before_merge = Column(Integer, nullable=True)
    reset_approvals_on_push = Column(Boolean, nullable=True)
    selective_code_owner_removals = Column(Boolean, nullable=True)
    disable_overriding_approvers_per_merge_request = Column(Boolean, nullable=True)
    merge_requests_author_approval = Column(Boolean, nullable=True)
    merge_requests_disable_committers_approval = Column(Boolean, nullable=True)
    require_password_to_approve = Column(Boolean, nullable=True)


# Iteration Model
class Iteration(Base):
    __tablename__ = "iterations"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Iteration")
    iid = Column(Integer, nullable=True)
    sequence = Column(Integer, nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    state = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    start_date = Column(String, nullable=True)
    due_date = Column(String, nullable=True)
    web_url = Column(String, nullable=True)


# Identity Model
class Identity(Base):
    __tablename__ = "identities"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Identity")
    provider = Column(String, nullable=True)
    extern_uid = Column(String, nullable=True)


# GroupSamlIdentity Model
class GroupSamlIdentity(Base):
    __tablename__ = "group_saml_identities"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="GroupSamlIdentity")
    extern_uid = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    saml_provider_id = Column(Integer, nullable=True)


# CreatedBy Model
class CreatedBy(Base):
    __tablename__ = "created_by"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="CreatedBy")
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    state = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    web_url = Column(String, nullable=True)


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="User")
    username = Column(String, nullable=True)
    user = Column(String, nullable=True)
    email = Column(String, nullable=True)
    name = Column(String, nullable=True)
    state = Column(String, nullable=True)
    locked = Column(Boolean, nullable=True)
    avatar_url = Column(String, nullable=True)
    web_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    is_admin = Column(Boolean, nullable=True)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    skype = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    discord = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    last_sign_in_at = Column(DateTime, nullable=True)
    confirmed_at = Column(DateTime, nullable=True)
    theme_id = Column(Integer, nullable=True)
    last_activity_on = Column(DateTime, nullable=True)
    color_scheme_id = Column(Integer, nullable=True)
    projects_limit = Column(Integer, nullable=True)
    current_sign_in_at = Column(DateTime, nullable=True)
    note = Column(String, nullable=True)
    can_create_group = Column(Boolean, nullable=True)
    can_create_project = Column(Boolean, nullable=True)
    two_factor_enabled = Column(Boolean, nullable=True)
    external = Column(Boolean, nullable=True)
    private_profile = Column(Boolean, nullable=True)
    current_sign_in_ip = Column(String, nullable=True)
    last_sign_in_ip = Column(String, nullable=True)
    namespace_id = Column(Integer, ForeignKey("namespaces.id"), nullable=True)
    email_reset_offered_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    access_level = Column(Integer, nullable=True)
    approved = Column(Boolean, nullable=True)
    invited = Column(Boolean, nullable=True)
    public_email = Column(String, nullable=True)
    pronouns = Column(String, nullable=True)
    bot = Column(Boolean, nullable=True)
    work_information = Column(String, nullable=True)
    followers = Column(Integer, nullable=True)
    following = Column(Integer, nullable=True)
    local_time = Column(String, nullable=True)
    commit_email = Column(String, nullable=True)
    shared_runners_minutes_limit = Column(Integer, nullable=True)
    extra_shared_runners_minutes_limit = Column(Integer, nullable=True)
    membership_type = Column(String, nullable=True)
    removable = Column(Boolean, nullable=True)
    last_login_at = Column(DateTime, nullable=True)

    identities = (
        relationship("Identity", backref=backref("users"))
        if "Identity" in globals()
        else None
    )
    created_by_id = Column(Integer, ForeignKey("created_by.id"), nullable=True)
    created_by = (
        relationship("CreatedBy", backref=backref("users"))
        if "CreatedBy" in globals()
        else None
    )
    group_saml_identity_id = Column(
        Integer, ForeignKey("group_saml_identities.id"), nullable=True
    )
    group_saml_identity = (
        relationship("GroupSamlIdentity", backref=backref("users"))
        if "GroupSamlIdentity" in globals()
        else None
    )


# Namespace Model
class Namespace(Base):
    __tablename__ = "namespaces"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Namespace")
    name = Column(String, nullable=True)
    path = Column(String, nullable=True)
    kind = Column(String, nullable=True)
    full_path = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("namespaces.id"), nullable=True)
    avatar_url = Column(String, nullable=True)
    web_url = Column(String, nullable=True)


# ContainerExpirationPolicy Model
class ContainerExpirationPolicy(Base):
    __tablename__ = "container_expiration_policies"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ContainerExpirationPolicy")
    cadence = Column(String, nullable=True)
    enabled = Column(Boolean, nullable=True)
    keep_n = Column(Integer, nullable=True)
    older_than = Column(String, nullable=True)
    name_regex = Column(String, nullable=True)
    name_regex_keep = Column(String, nullable=True)
    next_run_at = Column(DateTime, nullable=True)


# Permissions Model
class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Permissions")
    project_access = Column(JSON, nullable=True)
    group_access = Column(JSON, nullable=True)


# Statistics Model
class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Statistics")
    commit_count = Column(Integer, nullable=True)
    storage_size = Column(Integer, nullable=True)
    repository_size = Column(Integer, nullable=True)
    wiki_size = Column(Integer, nullable=True)
    lfs_objects_size = Column(Integer, nullable=True)
    job_artifacts_size = Column(Integer, nullable=True)
    pipeline_artifacts_size = Column(Integer, nullable=True)
    packages_size = Column(Integer, nullable=True)
    snippets_size = Column(Integer, nullable=True)
    uploads_size = Column(Integer, nullable=True)


# Links Model
class Links(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Links")
    self_link = Column(String, nullable=True)
    issues = Column(String, nullable=True)
    merge_requests = Column(String, nullable=True)
    repo_branches = Column(String, nullable=True)
    labels = Column(String, nullable=True)
    events = Column(String, nullable=True)
    members = Column(String, nullable=True)
    cluster_agents = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    award_emoji = Column(String, nullable=True)
    project = Column(String, nullable=True)
    closed_as_duplicate_of = Column(String, nullable=True)


# Diff Model
class Diff(Base):
    __tablename__ = "diffs"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Diff")
    merge_request_id = Column(Integer, ForeignKey("merge_requests.id"), nullable=True)
    head_commit_sha = Column(String, nullable=True)
    base_commit_sha = Column(String, nullable=True)
    start_commit_sha = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    state = Column(String, nullable=True)
    real_size = Column(String, nullable=True)
    patch_id_sha = Column(String, nullable=True)
    diff = Column(String, nullable=True)
    new_path = Column(String, nullable=True)
    old_path = Column(String, nullable=True)
    a_mode = Column(String, nullable=True)
    b_mode = Column(String, nullable=True)
    new_file = Column(Boolean, nullable=True)
    renamed_file = Column(Boolean, nullable=True)
    deleted_file = Column(Boolean, nullable=True)
    generated_file = Column(Boolean, nullable=True)


class MergeApprovals(Base):
    __tablename__ = "merge_approvals"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="MergeApprovals")
    approvals_before_merge = Column(Integer, nullable=True)
    reset_approvals_on_push = Column(Boolean, nullable=True)
    selective_code_owner_removals = Column(Boolean, nullable=True)
    disable_overriding_approvers_per_merge_request = Column(Boolean, nullable=True)
    merge_requests_author_approval = Column(Boolean, nullable=True)
    merge_requests_disable_committers_approval = Column(Boolean, nullable=True)
    require_password_to_approve = Column(Boolean, nullable=True)

    approvers = relationship(
        "User", secondary="merge_approval_approvers", backref=backref("merge_approvals")
    )

    approver_groups = relationship(
        "Group",
        secondary="merge_approval_approver_groups",
        backref=backref("merge_approvals"),
    )


# DetailedStatus Model
class DetailedStatus(Base):
    __tablename__ = "detailed_status"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="DetailedStatus")
    icon = Column(String, nullable=True)
    text = Column(String, nullable=True)
    label = Column(String, nullable=True)
    group = Column(String, nullable=True)
    tooltip = Column(String, nullable=True)
    has_details = Column(Boolean, nullable=True)
    details_path = Column(String, nullable=True)
    illustration = Column(JSON, nullable=True)
    favicon = Column(String, nullable=True)


class TestReport(Base):
    __tablename__ = "test_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_type = Column(String, default="TestReport")
    total_time = Column(Integer, nullable=True)
    total_count = Column(Integer, nullable=True)
    success_count = Column(Integer, nullable=True)
    failed_count = Column(Integer, nullable=True)
    skipped_count = Column(Integer, nullable=True)
    error_count = Column(Integer, nullable=True)

    total_id = Column(Integer, ForeignKey("test_report_totals.id"), nullable=True)
    total = relationship("TestReportTotal", backref=backref("test_reports"))

    test_suites = relationship(
        "TestSuite",
        secondary="test_report_test_suites",
        backref=backref("test_reports"),
    )


class ProjectConfig(Base):
    __tablename__ = "project_configs"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ProjectConfig")
    description = Column(String, nullable=True)
    name = Column(String, nullable=False)
    name_with_namespace = Column(String, nullable=False)
    path = Column(String, nullable=False)
    path_with_namespace = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


# Epic Model
class Epic(Base):
    __tablename__ = "epics"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Epic")
    iid = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    url = Column(String, nullable=True)
    group_id = Column(Integer, nullable=True)


# TestCase Model
class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="TestCase")
    status = Column(String, nullable=True)
    name = Column(String, nullable=True)
    classname = Column(String, nullable=True)
    execution_time = Column(Float, nullable=True)
    system_output = Column(String, nullable=True)
    stack_trace = Column(String, nullable=True)


# TestSuite Model
class TestSuite(Base):
    __tablename__ = "test_suites"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="TestSuite")
    name = Column(String, nullable=True)
    total_time = Column(Float, nullable=True)
    total_count = Column(Integer, nullable=True)
    success_count = Column(Integer, nullable=True)
    failed_count = Column(Integer, nullable=True)
    skipped_count = Column(Integer, nullable=True)
    error_count = Column(Integer, nullable=True)
    suite_error = Column(String, nullable=True)

    test_cases = relationship("TestCase", backref=backref("test_suites"))


# TestReportTotal Model
class TestReportTotal(Base):
    __tablename__ = "test_report_totals"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="TestReportTotal")
    time = Column(Integer, nullable=True)
    count = Column(Integer, nullable=True)
    success = Column(Integer, nullable=True)
    failed = Column(Integer, nullable=True)
    skipped = Column(Integer, nullable=True)
    error = Column(Integer, nullable=True)
    suite_error = Column(String, nullable=True)
