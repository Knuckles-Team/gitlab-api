---
name: gitlab-protected-branches
description: "Manages protected branches in GitLab. Use for protecting/unprotecting branches, code owner approvals. Triggers: branch protection."
---

### Overview
Secures branches.

### Key Tools
- `get_protected_branches` / `protect_branch` / `unprotect_branch`.
- `require_code_owner_approvals_single_branch`.

### Usage Instructions
1. Access levels: push/merge.

### Examples
- Protect: `protect_branch` with project_id="123", branch="main", push_access_level="maintainer".
- Code owners: `require_code_owner_approvals_single_branch` with code_owner_approval_required=true.

### Error Handling
- Already protected: Update instead.