---
name: gitlab-merge-rules
description: "Manages GitLab merge approval rules. Use for approvals, rules at project/group levels. Triggers: code reviews, approvals."
---

### Overview
Handles approval configurations.

### Key Tools
- Project: `get_project_level_merge_request_approval_rules` / create/update/delete.
- MR-specific: `merge_request_level_approvals` / approve/unapprove.
- Group/Project settings: get/edit rules.

### Usage Instructions
1. Use approvals_required, user/group IDs.

### Examples
- Create rule: `create_project_level_rule` with project_id="123", name="review", approvals_required=2.
- Approve MR: `approve_merge_request` with project_id="123", merge_request_iid=1.

### Error Handling
- Insufficient approvals: Check state.