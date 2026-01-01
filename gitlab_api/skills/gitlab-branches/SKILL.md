---
name: gitlab-branches
description: "Manages GitLab branches. Use for listing, creating, deleting, or querying branches in projects. Triggers: branch operations, git branching."
---

### Overview
This skill handles branch-related tasks in GitLab via MCP tools. Focus on one operation per call for efficiency.

### Key Tools
- `get_branches`: List or get a specific branch. Params: project_id (required), search/regex/branch (filters).
- `create_branch`: Create a new branch. Params: project_id, branch, ref (required).
- `delete_branch`: Delete a branch or all merged branches. Params: project_id (required), branch or delete_merged_branches.

### Usage Instructions
1. Identify the project_id (e.g., from query or prior context).
2. Call the appropriate tool with minimal params.
3. Handle pagination if results exceed limits (use MCP's built-in support).

### Examples
- List branches: Call `get_branches` with project_id="my/project" and search="feature".
- Create: `create_branch` with project_id="123", branch="new-feature", ref="main".
- Delete merged: `delete_branch` with project_id="123", delete_merged_branches=true.

### Error Handling
- Missing params: Retry with required fields.
- 404: Branch/project not found—verify IDs.
- Rate limits: Wait and retry.
