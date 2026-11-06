---
name: gitlab-vulnerabilities
skill_type: skill
description: >-
  Dependency and security-vulnerability review on GitLab via the gitlab-api MCP server — the GitLab counterpart to GitHub Dependabot. Read a project's Dependency List, review a project's or group's security vulnerabilities/findings, and fetch a single vulnerability by ID. Use when the agent must audit a project's dependencies for known vulnerabilities, review the security posture of a project or group, or inspect one vulnerability. Do NOT use for package publishing or registry reads (gitlab-packages), pipelines/CI (gitlab-pipelines), or issues (gitlab-issues); prefer those.
license: MIT
tags: []
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Gitlab Vulnerabilities

Typed gitlab_* tools take project_id (id or URL-encoded path) explicitly; resolve it before acting.

## Rules

- Resolve project_id (and the merge request or issue iid) before any call.
- Read first, then change, then read the object back.
- Delete, erase and merge-class tools need an explicit request; ask first.

## Task workflows

### triage-vulnerabilities

Read vulnerabilities of a project, group or one finding. Contract steps, in order:

1. `gitlab_get_group_vulnerabilities`(; optional project_id, group_id, vulnerability_id, package_manager, max_pages, per_page)
2. `gitlab_get_project_vulnerabilities`(; optional project_id, group_id, vulnerability_id, package_manager, max_pages, per_page)
3. `gitlab_get_vulnerability`(; optional project_id, group_id, vulnerability_id, package_manager, max_pages, per_page)
