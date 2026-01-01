---
name: gitlab-merge-requests
description: "Manages GitLab merge requests. Use for creating, listing MRs across projects or groups. Triggers: PRs, code reviews."
---

### Overview
Covers MR creation and queries.

### Key Tools
- `create_merge_request`: Create MR.
- `get_merge_requests`: All MRs.
- `get_project_merge_requests`: Project MRs.

### Usage Instructions
1. For creation: source/target branches, title.

### Examples
- Create: `create_merge_request` with project_id="123", source_branch="feature", target_branch="main", title="New feature".
- List: `get_project_merge_requests` with project_id="123", state="opened".

### Error Handling
- Conflicts: Resolve before creation.