#!/usr/bin/python
# coding: utf-8
import logging

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

from sqlalchemy import Column, String, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref, declarative_base
from sqlalchemy import Integer, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    Float,
    JSON,
)

Base = declarative_base()

# Evidence Model
class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Evidence")
    sha = Column(String, nullable=True)
    filepath = Column(String, nullable=True)
    collected_at = Column(DateTime, nullable=True)


# IssueStats Model
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
    issue_stats = relationship(
        "IssueStats", foreign_keys=[issue_stats_id], backref=backref("milestones")
    )

    release_id = Column(
        Integer,
        ForeignKey("releases.id", name="fk_release_milestone_id"),
        nullable=True,
    )
    releases = relationship(
        "Release", foreign_keys=[release_id], backref=backref("milestone_associations")
    )


release_milestones = (
    Table(
        "release_milestones",
        Base.metadata,
        Column("release_id", Integer, ForeignKey("releases.id"), primary_key=True),
        Column("milestone_id", Integer, ForeignKey("milestones.id"), primary_key=True),
        extend_existing=True,
    )
    if "Milestone" in globals()
    else None
)

release_evidences = (
    Table(
        "release_evidences",
        Base.metadata,
        Column("release_id", Integer, ForeignKey("releases.id"), primary_key=True),
        Column("evidence_id", Integer, ForeignKey("evidences.id"), primary_key=True),
        extend_existing=True,
    )
    if "Evidence" in globals()
    else None
)


# DeployToken Model
class DeployToken(Base):
    __tablename__ = "deploy_tokens"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="DeployToken")
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

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship(
        "User", foreign_keys=[user_id], backref=backref("deploy_tokens")
    )


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

    assets_id = Column(Integer, ForeignKey("assets.id"))
    assets = relationship(
        "Assets", foreign_keys=[assets_id], backref=backref("sources")
    )


# Link Model
class Link(Base):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Link")
    name = Column(String, nullable=True)
    url = Column(String, nullable=True)
    link_type = Column(String, nullable=True)

    assets_id = Column(Integer, ForeignKey("assets.id"))
    assets = relationship("Assets", foreign_keys=[assets_id], backref=backref("link"))


# Assets Model
class Assets(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Assets")
    count = Column(Integer, nullable=True)
    evidence_file_path = Column(String, nullable=True)


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
    action_name = Column(String, nullable=True)
    target_type = Column(String, nullable=True)
    target_url = Column(String, nullable=True)
    body = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = relationship(
        "Project", foreign_keys=[project_id], backref=backref("todos_project")
    )

    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    author = relationship(
        "User", foreign_keys=[author_id], backref=backref("todos_author")
    )

    target_id = Column(Integer, ForeignKey("issues.id"), nullable=True)
    target = relationship(
        "Issue", foreign_keys=[target_id], backref=backref("todos_target")
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
    link = relationship(
        "WikiAttachmentLink",
        foreign_keys=[link_id],
        backref=backref("wiki_attachments"),
    )


# Agent Model
class Agent(Base):
    __tablename__ = "agent"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Agent")

    config_project_id = Column(Integer, ForeignKey("project_configs.id"), nullable=True)
    config_project = relationship(
        "ProjectConfig", foreign_keys=[config_project_id], backref=backref("agent")
    )


# Agents Model
class Agents(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Agents")

    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    job = relationship("Job", foreign_keys=[job_id], backref=backref("agents"))

    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    pipeline = relationship(
        "Pipeline", foreign_keys=[pipeline_id], backref=backref("agents")
    )

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = relationship(
        "Project", foreign_keys=[project_id], backref=backref("agents")
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", foreign_keys=[user_id], backref=backref("agents"))


# Release Model
class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True)
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

    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    author = relationship("User", backref=backref("releases"), foreign_keys=[author_id])

    commit_id = Column(Integer, ForeignKey("commits.id"), nullable=True)
    commit = relationship(
        "Commit", backref=backref("releases"), foreign_keys=[commit_id]
    )
    milestones_id = Column(Integer, ForeignKey("milestones.id"), nullable=True)
    milestones = relationship(
        "Milestone",
        # secondary="release_milestones",
        foreign_keys=[milestones_id],
        backref=backref("release_associations"),
    )

    evidences_id = Column(Integer, ForeignKey("evidences.id"), nullable=True)
    evidences = relationship(
        "Evidence",
        # secondary="release_evidences",
        foreign_keys=[evidences_id],
        backref=backref("release_evidences"),
    )

    assets_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    assets = relationship(
        "Assets", backref=backref("release"), foreign_keys=[assets_id]
    )

    links_id = Column(Integer, ForeignKey("release_links.id"), nullable=True)
    links = relationship(
        "ReleaseLinks", backref=backref("release"), foreign_keys=[links_id]
    )


# AccessLevel Model
class AccessLevel(Base):
    __tablename__ = "access_levels"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="AccessLevel")
    access_level = Column(Integer, nullable=True)
    access_level_description = Column(String, nullable=True)
    deploy_key_id = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship(
        "User", foreign_keys=[user_id], backref=backref("access_levels")
    )

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship(
        "Group", foreign_keys=[group_id], backref=backref("access_levels")
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
    commit = relationship("Commit", backref=backref("branches_commit"))

    push_access_levels_id = Column(
        Integer, ForeignKey("access_levels.id"), nullable=True
    )
    push_access_levels = relationship(
        "AccessLevel",
        # secondary="branch_push_access_levels",
        foreign_keys=[push_access_levels_id],
        backref=backref("branches_push_access_levels"),
    )

    merge_access_levels_id = Column(
        Integer, ForeignKey("access_levels.id"), nullable=True
    )
    merge_access_levels = relationship(
        "AccessLevel",
        # secondary="branch_merge_access_levels",
        foreign_keys=[merge_access_levels_id],
        backref=backref("branches_merge_access_levels"),
    )

    unprotect_access_levels_id = Column(
        Integer, ForeignKey("access_levels.id"), nullable=True
    )
    unprotect_access_levels = relationship(
        "AccessLevel",
        # secondary="branch_unprotect_access_levels",
        foreign_keys=[unprotect_access_levels_id],
        backref=backref("branches_unprotect_access_levels"),
    )


# Label Model
class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    text_color = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    description_html = Column(Text, nullable=True)
    open_issues_count = Column(Integer, nullable=False, default=0)
    closed_issues_count = Column(Integer, nullable=False, default=0)
    open_merge_requests_count = Column(Integer, nullable=False, default=0)
    subscribed = Column(Boolean, nullable=False, default=False)
    priority = Column(Integer, nullable=True)
    is_project_label = Column(Boolean, nullable=False, default=True)


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

    eligible_approvers_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_eligible_approvers_rules"),
        nullable=True,
    )
    eligible_approvers = relationship(
        "User",
        # secondary="approval_rule_eligible_approvers",
        foreign_keys=[eligible_approvers_id],
        backref=backref("approval_rules"),
    )

    users_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_users_rules"),
        nullable=True,
    )
    users = relationship(
        "User",
        # secondary="approval_rule_users",
        foreign_keys=[users_id],
        backref=backref("approval_rules_users"),
    )

    groups_id = Column(
        Integer,
        ForeignKey("groups.id", name="fk_groups_rules"),
        nullable=True,
    )
    groups = relationship(
        "Group",
        # secondary="approval_rule_groups",
        foreign_keys=[groups_id],
        backref=backref("approval_rules_groups"),
    )

    protected_branches_id = Column(
        Integer,
        ForeignKey("branches.id", name="fk_protected_branches_rules"),
        nullable=True,
    )
    protected_branches = relationship(
        "Branch",
        # secondary="approval_rule_protected_branches",
        foreign_keys=[protected_branches_id],
        backref=backref("approval_rules_branches"),
    )

    approved_by_id = Column(
        Integer,
        ForeignKey("approved_by.id", name="fk_approval_rule_user_by_id"),
        nullable=True,
    )
    approved_by = relationship(
        "ApprovedBy",
        # secondary="approval_rule_approved_by",
        foreign_keys=[approved_by_id],
        backref=backref("approval_rules_approved_by"),
    )


# MergeRequest Model
class MergeRequest(Base):
    __tablename__ = "merge_requests"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="MergeRequest")
    iid = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    state = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    target_branch = Column(String, nullable=True)
    source_branch = Column(String, nullable=True)
    upvotes = Column(Integer, nullable=True)
    downvotes = Column(Integer, nullable=True)
    source_project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    target_project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
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
    author = relationship(
        "User", foreign_keys=[author_id], backref=backref("authored_merge_requests")
    )

    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assignee = relationship(
        "User", foreign_keys=[assignee_id], backref=backref("assigned_merge_requests")
    )

    milestone_id = Column(Integer, ForeignKey("milestones.id"), nullable=True)
    milestone = relationship(
        "Milestone", foreign_keys=[milestone_id], backref=backref("merge_requests")
    )

    merged_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    merged_by = relationship(
        "User", foreign_keys=[merged_by_id], backref=backref("merged_merge_requests")
    )

    closed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    closed_by = relationship(
        "User", foreign_keys=[closed_by_id], backref=backref("closed_merge_requests")
    )

    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    pipeline = relationship(
        "Pipeline",
        foreign_keys=[pipeline_id],
        backref=backref("merge_requests_pipeline"),
    )

    head_pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    head_pipeline = relationship(
        "Pipeline",
        foreign_keys=[head_pipeline_id],
        backref=backref("head_merge_requests"),
    )

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    projects = relationship(
        "Project",
        foreign_keys=[project_id],
        backref=backref("project_merge_requests"),
    )

    labels_id = Column(Integer, ForeignKey("labels.id"), nullable=True)
    labels = relationship(
        "Label",
        # secondary="merge_request_labels",
        foreign_keys=[labels_id],
        backref=backref("merge_requests_labels"),
    )

    references_id = Column(Integer, ForeignKey("references.id"), nullable=True)
    references = relationship(
        "References", foreign_keys=[references_id], backref=backref("merge_requests")
    )

    time_stats_id = Column(Integer, ForeignKey("time_stats.id"), nullable=True)

    time_stats = relationship(
        "TimeStats", foreign_keys=[time_stats_id], backref=backref("merge_requests")
    )

    task_completion_status_id = Column(
        Integer, ForeignKey("task_completion_status.id"), nullable=True
    )
    task_completion_status = relationship(
        "TaskCompletionStatus",
        foreign_keys=[task_completion_status_id],
        backref=backref("merge_requests"),
    )

    change_id = Column(
        Integer,
        ForeignKey("diffs.id", name="fk_merge_request_diff"),
        nullable=True,
    )
    changes = relationship(
        "Diff", foreign_keys=[change_id], backref=backref("merge_requests")
    )

    reviewers_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_user_approved_by_id"),
        nullable=True,
    )
    reviewers = relationship(
        "User",
        # secondary="merge_request_reviewers",
        foreign_keys=[reviewers_id],
        backref=backref("reviewed_merge_requests"),
    )

    approved_by_id = Column(
        Integer,
        ForeignKey("approved_by.id", name="fk_user_approved_by_id"),
        nullable=True,
    )
    approved_by = relationship(
        "ApprovedBy",
        foreign_keys=[approved_by_id],
        backref=backref("approved_users_merge_request"),
    )

    rule_id = Column(
        Integer, ForeignKey("approval_rules.id", name="fk_rule_id"), nullable=True
    )
    rules = relationship(
        "ApprovalRule",
        foreign_keys=[rule_id],
        backref=backref("approval_rules_merge_request"),
    )


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
    allowed_to_push_id = Column(
        Integer,
        ForeignKey("group_accesses.id", name="fk_default_rules_allow_push"),
        nullable=True,
    )
    allowed_to_push = relationship(
        "GroupAccess",
        # secondary="default_branch_protection_push_access",
        foreign_keys=[allowed_to_push_id],
        backref=backref("push_defaults"),
    )
    allowed_to_merge_id = Column(
        Integer,
        ForeignKey("group_accesses.id", name="fk_default_rules_allow_merge"),
        nullable=True,
    )
    allowed_to_merge = relationship(
        "GroupAccess",
        # secondary="default_branch_protection_merge_access",
        foreign_keys=[allowed_to_merge_id],
        backref=backref("merge_defaults"),
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
    default_branch_protection_defaults = relationship(
        "DefaultBranchProtectionDefaults",
        foreign_keys=[default_branch_protection_defaults_id],
        backref=backref("groups"),
    )
    statistics_id = Column(Integer, ForeignKey("statistics.id"), nullable=True)
    statistics = relationship(
        "Statistics", foreign_keys=[statistics_id], backref=backref("groups")
    )
    projects_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    projects = relationship(
        "Project", foreign_keys=[projects_id], backref=backref("group_projects")
    )
    shared_projects_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    shared_projects = relationship(
        "Project",
        # secondary="project_shared_with_groups",
        foreign_keys=[shared_projects_id],
        backref=backref("shared_group_projects"),
    )

    parent_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    parent = relationship("Group", foreign_keys=[parent_id], remote_side=[id])


# Webhook Model
class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Webhook")
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
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

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    group = relationship("Group", foreign_keys=[group_id], backref=backref("webhooks"))


class ApprovedBy(Base):
    __tablename__ = "approved_by"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="ApprovedBy")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship(
        "User", foreign_keys=[user_id], backref=backref("approved_by_users")
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
    owner = relationship(
        "User", foreign_keys=[owner_id], backref=backref("owned_projects")
    )

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    creator = relationship(
        "User", foreign_keys=[creator_id], backref=backref("created_projects")
    )

    namespace_id = Column(Integer, ForeignKey("namespaces.id"), nullable=True)
    namespace = relationship(
        "Namespace", foreign_keys=[namespace_id], backref=backref("projects")
    )

    container_expiration_policy_id = Column(
        Integer, ForeignKey("container_expiration_policies.id"), nullable=True
    )
    container_expiration_policy = relationship(
        "ContainerExpirationPolicy",
        foreign_keys=[container_expiration_policy_id],
        backref=backref("projects"),
    )

    statistics_id = Column(Integer, ForeignKey("statistics.id"), nullable=True)
    statistics = relationship(
        "Statistics", foreign_keys=[statistics_id], backref=backref("projects")
    )

    links_id = Column(Integer, ForeignKey("links.id"), nullable=True)
    links = relationship("Links", foreign_keys=[links_id], backref=backref("projects"))

    permissions_id = Column(Integer, ForeignKey("permissions.id"), nullable=True)
    permissions = relationship(
        "Permissions", foreign_keys=[permissions_id], backref=backref("projects")
    )

    shared_with_groups_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    shared_with_groups = relationship(
        "Group",
        # secondary="project_shared_with_groups",
        foreign_keys=[shared_with_groups_id],
        backref=backref("shared_projects_with_group"),
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

    projects_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    projects = relationship(
        "Project",
        # secondary="runner_projects",
        foreign_keys=[projects_id],
        backref=backref("runners"),
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
    commit = relationship(
        "Commit", foreign_keys=[commit_id], backref=backref("jobs_commits")
    )

    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    pipeline = relationship(
        "Pipeline", foreign_keys=[pipeline_id], backref=backref("jobs_pipeline")
    )

    runner_id = Column(Integer, ForeignKey("runners.id"), nullable=True)
    runner = relationship("Runner", backref=backref("jobs_runner"))

    runner_manager_id = Column(Integer, ForeignKey("runner_managers.id"), nullable=True)
    runner_manager = relationship(
        "RunnerManager",
        foreign_keys=[runner_manager_id],
        backref=backref("jobs_runner_manager"),
    )

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = relationship("Project", backref=backref("jobs_projects"))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", foreign_keys=[user_id], backref=backref("jobs_users"))

    downstream_pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    downstream_pipeline = relationship(
        "Pipeline",
        foreign_keys=[downstream_pipeline_id],
        backref=backref("jobs_downstream"),
    )

    artifacts_file_id = Column(Integer, ForeignKey("artifacts_files.id"), nullable=True)
    artifacts_file = relationship(
        "ArtifactsFile", backref=backref("jobs_artifact_file")
    )

    artifacts_id = Column(Integer, ForeignKey("artifacts.id"), nullable=True)
    artifacts = relationship("Artifact", backref=backref("jobs_artifacts"))


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
    user = relationship(
        "User", foreign_keys=[user_id], backref=backref("pipelines_user")
    )

    detailed_status_id = Column(
        Integer, ForeignKey("detailed_status.id"), nullable=True
    )
    detailed_status = relationship(
        "DetailedStatus",
        foreign_keys=[detailed_status_id],
        backref=backref("pipelines_status"),
    )

    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)
    jobs = relationship("Job", foreign_keys=[job_id], backref=backref("pipeline_jobs"))


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

    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    pipelines = relationship(
        "Pipeline",
        foreign_keys=[pipeline_id],
        backref=backref("pipeline_package_versions"),
    )
    package_id = Column(Integer, ForeignKey("packages.id"), nullable=True)
    packages = relationship(
        "Package",
        foreign_keys=[package_id],
        backref=backref("package_versions_package"),
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
    links = relationship(
        "PackageLink", foreign_keys=[links_id], backref=backref("packages_links")
    )

    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    pipelines = relationship(
        "Pipeline", foreign_keys=[pipeline_id], backref=backref("packages")
    )
    versions_id = Column(Integer, ForeignKey("package_versions.id"), nullable=True)
    package_versions = relationship(
        "PackageVersion",
        foreign_keys=[versions_id],
        backref=backref("packages_versions"),
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
    author = relationship("User", foreign_keys=[author_id], backref=backref("comments"))

    commits_id = Column(Integer, ForeignKey("commits.id"), nullable=True)
    commits = relationship(
        "Commit", foreign_keys=[commits_id], backref=backref("commit_comments")
    )


# Commit Model
class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True)
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
    author = relationship(
        "User", foreign_keys=[author_id], backref=backref("commits_author")
    )

    stats_id = Column(Integer, ForeignKey("commit_stats.id"), nullable=True)
    stats = relationship(
        "CommitStats", foreign_keys=[stats_id], backref=backref("commits_stats")
    )

    last_pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=True)
    last_pipeline = relationship(
        "Pipeline",
        foreign_keys=[last_pipeline_id],
        backref=backref("commits_last_pipeline"),
    )

    signature_id = Column(Integer, ForeignKey("commit_signatures.id"), nullable=True)
    signature = relationship(
        "CommitSignature",
        foreign_keys=[signature_id],
        backref=backref("commits_signatures"),
    )

    notes_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    notes = relationship(
        "Comment", foreign_keys=[notes_id], backref=backref("commit_notes")
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
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
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
    author = relationship(
        "User", foreign_keys=[author_id], backref=backref("authored_issues")
    )

    milestone_id = Column(Integer, ForeignKey("milestones.id"), nullable=True)
    milestone = relationship(
        "Milestone", foreign_keys=[milestone_id], backref=backref("issues")
    )

    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assignee = relationship(
        "User", foreign_keys=[assignee_id], backref=backref("assigned_issues")
    )

    closed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    iteration_id = Column(Integer, ForeignKey("iterations.id"), nullable=True)
    epic_id = Column(Integer, ForeignKey("epics.id"), nullable=True)
    closed_by = relationship(
        "User", foreign_keys=[closed_by_id], backref=backref("closed_issues")
    )
    iteration = relationship("Iteration", backref=backref("issues"))
    epic = relationship("Epic", backref=backref("issues"))


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
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    state = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    start_date = Column(String, nullable=True)
    due_date = Column(String, nullable=True)
    web_url = Column(String, nullable=True)

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship(
        "Group", foreign_keys=[group_id], backref=backref("iterations")
    )


# Identity Model
class Identity(Base):
    __tablename__ = "identities"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="Identity")
    provider = Column(String, nullable=True)
    extern_uid = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", foreign_keys=[user_id], backref=backref("identities"))


# GroupSamlIdentity Model
class GroupSamlIdentity(Base):
    __tablename__ = "group_saml_identities"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="GroupSamlIdentity")
    extern_uid = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    saml_provider_id = Column(Integer, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", name="fk_group_saml_identity_user_id"),
        nullable=True,
    )
    user = relationship(
        "User", foreign_keys=[user_id], backref=backref("group_saml_identities_user")
    )


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
    user_id = Column(
        Integer, ForeignKey("users.id", name="fk_created_by_user_id"), nullable=True
    )

    user = relationship(
        "User", foreign_keys=[user_id], backref=backref("created_by_user")
    )


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    base_type = Column(String, default="User")
    username = Column(String, nullable=True)
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

    created_by_id = Column(
        Integer,
        ForeignKey("created_by.id", name="fk_user_created_by_id"),
        nullable=True,
    )
    created_by = relationship(
        "CreatedBy", foreign_keys=[created_by_id], backref=backref("users")
    )

    group_saml_identity_id = Column(
        Integer,
        ForeignKey("group_saml_identities.id", name="fk_user_group_saml_identity_id"),
        nullable=True,
    )
    group_saml_identity = relationship(
        "GroupSamlIdentity",
        foreign_keys=[group_saml_identity_id],
        backref=backref("users"),
    )

    namespace_id = Column(
        Integer, ForeignKey("namespaces.id", name="fk_user_namespace_id"), nullable=True
    )
    namespace = relationship(
        "Namespace", foreign_keys=[namespace_id], backref=backref("users")
    )


# Namespace Model
class Namespace(Base):
    __tablename__ = "namespaces"

    id = Column(
        Integer, ForeignKey("namespaces.id", name="fk_namespace_id"), primary_key=True
    )
    base_type = Column(String, default="Namespace")
    name = Column(String, nullable=True)
    path = Column(String, nullable=True)
    kind = Column(String, nullable=True)
    full_path = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    web_url = Column(String, nullable=True)

    parent_id = Column(
        Integer,
        ForeignKey("namespaces.id", name="fk_namespace_parent_id"),
        nullable=True,
    )
    parent = relationship("Namespace", foreign_keys=[parent_id], remote_side=[id])

    user_id = Column(
        Integer, ForeignKey("users.id", name="fk_namespace_user_id"), nullable=True
    )
    user = relationship("User", foreign_keys=[user_id], backref=backref("namespaces"))


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

    merge_request_id = Column(Integer, ForeignKey("merge_requests.id"), nullable=True)
    merge_request = relationship(
        "MergeRequest", foreign_keys=[merge_request_id], backref=backref("diffs")
    )


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

    approvers_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approvers = relationship(
        "User",
        # secondary="merge_approval_approvers",
        foreign_keys=[approvers_id],
        backref=backref("merge_approvals"),
    )

    approver_groups_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    approver_groups = relationship(
        "Group",
        # secondary="merge_approval_approver_groups",
        foreign_keys=[approver_groups_id],
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
    total = relationship(
        "TestReportTotal", foreign_keys=[total_id], backref=backref("test_reports")
    )

    test_suites_id = Column(Integer, ForeignKey("test_suites.id"), nullable=True)
    test_suites = relationship(
        "TestSuite",
        # secondary="test_report_test_suites",
        foreign_keys=[test_suites_id],
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

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    groups = relationship("Group", foreign_keys=[group_id], backref=backref("epics"))


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

    test_cases_id = Column(Integer, ForeignKey("test_cases.id"), nullable=True)
    test_cases = relationship(
        "TestCase", foreign_keys=[test_cases_id], backref=backref("test_suites")
    )


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
