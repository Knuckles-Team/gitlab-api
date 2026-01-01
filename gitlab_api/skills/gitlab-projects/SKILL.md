---
name: gitlab-projects
description: "Manages GitLab projects. Use for listing, editing, archiving, sharing projects. Triggers: repo management."
---

### Overview
Handles project lifecycle.

### Key Tools
- `get_projects` / `edit_project` / `archive_project` / `unarchive_project` / `delete_project`.
- `get_nested_projects_by_group` / `get_project_contributors` / `get_project_statistics` / `get_project_groups` / `share_project`.

### Usage Instructions
1. Use visibility for updates.

### Examples
- Edit: `edit_project` with project_id="123", visibility="public".
- Share: `share_project` with project_id="123", group_id="group", group_access="maintainer".

### Error Handling
- Deletion permanent: Confirm first.