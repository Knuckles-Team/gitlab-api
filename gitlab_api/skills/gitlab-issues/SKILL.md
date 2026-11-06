---
name: gitlab-issues
skill_type: skill
description: >-
  Issue review and tracking on GitLab via the gitlab-api MCP server — review a project's issues, review issues across a whole group/organization, and read, create, update, or close an issue with the domain-typed tool. Use when the agent must triage a project's issues, see every issue affecting a group, open a new issue, update labels/assignee/state, or delete one. Do NOT use for merge requests (gitlab-merge-request-review / gitlab-merge-request-create), pipelines (gitlab-pipelines), or repo/branch reads (gitlab-repositories); prefer those.
license: MIT
tags: []
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Gitlab Issues

Typed gitlab_* tools take project_id (id or URL-encoded path) explicitly; resolve it before acting.

## Rules

- Resolve project_id (and the merge request or issue iid) before any call.
- Read first, then change, then read the object back.
- Delete, erase and merge-class tools need an explicit request; ask first.

## Task workflows

### work-issues

Read, open, change and comment on issues, epics, labels and milestones. Contract steps, in order:

1. `gitlab_create_epic`(; optional group_id, epic_iid, title, description, state_event, data)
2. `gitlab_create_issue`(; optional project_id, group_id, title, description, labels, state)
3. `gitlab_create_label`(; optional project_id, name, color, new_name, description, data)
4. `gitlab_create_milestone`(; optional project_id, milestone_id, title, description, state_event, data)
5. `gitlab_create_note`(; optional project_id, issue_iid, note_id, body, data)
6. `gitlab_delete_epic`(; optional group_id, epic_iid, title, description, state_event, data) (destructive: pass confirm=true only after the person agrees)
7. `gitlab_delete_issue`(; optional project_id, group_id, title, description, labels, state) (destructive: pass confirm=true only after the person agrees)
8. `gitlab_delete_label`(; optional project_id, name, color, new_name, description, data) (destructive: pass confirm=true only after the person agrees)
9. `gitlab_delete_milestone`(; optional project_id, milestone_id, title, description, state_event, data) (destructive: pass confirm=true only after the person agrees)
10. `gitlab_delete_note`(; optional project_id, issue_iid, note_id, body, data, confirm) (destructive: pass confirm=true only after the person agrees)
11. `gitlab_get_epic`(; optional group_id, epic_iid, title, description, state_event, data)
12. `gitlab_get_epics`(; optional group_id, epic_iid, title, description, state_event, data)
13. `gitlab_get_group_issues`(; optional project_id, group_id, title, description, labels, state)
14. `gitlab_get_issue`(; optional project_id, group_id, title, description, labels, state)
15. `gitlab_get_issues`(; optional project_id, group_id, title, description, labels, state)
16. `gitlab_get_label`(; optional project_id, name, color, new_name, description, data)
17. `gitlab_get_labels`(; optional project_id, name, color, new_name, description, data)
18. `gitlab_get_milestone`(; optional project_id, milestone_id, title, description, state_event, data)
19. `gitlab_get_milestones`(; optional project_id, milestone_id, title, description, state_event, data)
20. `gitlab_get_note`(; optional project_id, issue_iid, note_id, body, data)
21. `gitlab_get_notes`(; optional project_id, issue_iid, note_id, body, data)
22. `gitlab_update_epic`(; optional group_id, epic_iid, title, description, state_event, data)
23. `gitlab_update_issue`(; optional project_id, group_id, title, description, labels, state)
24. `gitlab_update_label`(; optional project_id, name, color, new_name, description, data)
25. `gitlab_update_milestone`(; optional project_id, milestone_id, title, description, state_event, data)
26. `gitlab_update_note`(; optional project_id, issue_iid, note_id, body, data)
