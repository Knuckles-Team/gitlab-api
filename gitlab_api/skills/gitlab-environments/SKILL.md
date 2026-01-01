---
name: gitlab-environments
description: "Manages GitLab environments. Use for creating, updating, deleting, or protecting deployment environments. Triggers: CI/CD environments, deployments."
---

### Overview
Covers environment lifecycle and protection.

### Key Tools
- `get_environments` / `create_environment` / `update_environment` / `delete_environment` / `stop_environment`: Basic ops.
- `stop_stale_environments` / `delete_stopped_environments`: Cleanup.
- `get_protected_environments` / `protect_environment` / `update_protected_environment` / `unprotect_environment`: Protection.

### Usage Instructions
1. Use name and external_url for creation.
2. Protection: Set required_approval_count.

### Examples
- Create: `create_environment` with project_id="123", name="prod", external_url="https://prod.example.com".
- Protect: `protect_environment` with project_id="123", name="prod", required_approval_count=2.

### Error Handling
- State conflicts: Check status before ops.