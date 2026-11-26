---
name: gitlab-vulnerabilities
skill_type: skill
description: >-
  Dependency and security-vulnerability review on GitLab via the gitlab-api MCP server — the GitLab counterpart to GitHub Dependabot. Use when the agent must audit a project's dependencies for known vulnerabilities, review the security posture of a project or group, or inspect one vulnerability.
license: MIT
tags: []
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Gitlab Vulnerabilities

Scope: Dependency and security-vulnerability review on GitLab via the gitlab-api MCP server — the GitLab counterpart to GitHub Dependabot. Read a project's Dependency List, review a project's or group's security vulnerabilities/findings, and fetch a single vulnerability by ID. Use when the agent must audit a project's dependencies for known vulnerabilities, review the security posture of a project or group, or inspect one vulnerability. Do NOT use for package publishing or registry reads (gitlab-packages), pipelines/CI (gitlab-pipelines), or issues (gitlab-issues); prefer those.

Typed gitlab_* tools take project_id (id or URL-encoded path) explicitly; resolve it before acting.

## Rules

- Resolve project_id (and the merge request or issue iid) before any call.
- Read first, then change, then read the object back.
- Delete, erase and merge-class tools need an explicit request; ask first.

## Steps

1. Resolve the project or group with `gitlab_get_project`(project_id) or `gitlab_get_group`(group_id). Verify the id matches the target.
2. List findings with `gitlab_get_project_vulnerabilities`(project_id) or `gitlab_get_group_vulnerabilities`(group_id). Verify severity and state are shown per finding.
3. Inspect one with `gitlab_get_vulnerability`(vulnerability_id). Verify the response names the affected package or file.
4. Read the dependency list with `gitlab_get_project_dependencies`(project_id, package_manager). Verify versions are shown for vulnerable packages.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| Empty vulnerability list | Security scanning not enabled or no findings | Report that no scan data exists and confirm with `gitlab_get_project` |
| 403 on vulnerabilities | Token lacks the security role | Request a token with the required role; do not widen access yourself |
| Vulnerability not found | Wrong `vulnerability_id` | List ids again with `gitlab_get_project_vulnerabilities` and use the returned id |

## Task workflows

### triage-vulnerabilities

Read vulnerabilities of a project, group or one finding. Contract steps, in order:

1. `gitlab_get_group_vulnerabilities`(; optional project_id, group_id, vulnerability_id, package_manager, max_pages, per_page)
2. `gitlab_get_project_vulnerabilities`(; optional project_id, group_id, vulnerability_id, package_manager, max_pages, per_page)
3. `gitlab_get_vulnerability`(; optional project_id, group_id, vulnerability_id, package_manager, max_pages, per_page)
