---
name: gitlab-groups
description: "Manages GitLab groups. Use for listing, editing groups, subgroups, projects, or merge requests. Triggers: group management, namespaces."
---

### Overview
Handles group structures and contents.

### Key Tools
- `get_groups` / `edit_group`: Groups.
- `get_group_subgroups` / `get_group_descendant_groups`: Hierarchy.
- `get_group_projects` / `get_group_merge_requests`: Contents.

### Usage Instructions
1. Use group_id for specifics.
2. Filters: search, sort, owned.

### Examples
- List subgroups: `get_group_subgroups` with group_id="mygroup".
- Get projects: `get_group_projects` with group_id="mygroup", include_subgroups=true.

### Error Handling
- Access denied: Check permissions.