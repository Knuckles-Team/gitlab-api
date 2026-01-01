---
name: gitlab-members
description: "Manages GitLab members. Use for listing members in groups or projects. Triggers: user access, permissions."
---

### Overview
Handles membership queries.

### Key Tools
- `get_group_members`: Group members.
- `get_project_members`: Project members.

### Usage Instructions
1. Filters: query, user_ids.

### Examples
- Group members: `get_group_members` with group_id="mygroup", query="john".
- Project: Similar for projects.

### Error Handling
- No members: Empty list is valid.