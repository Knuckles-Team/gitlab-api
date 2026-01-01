---
name: gitlab-deploy-tokens
description: "Manages GitLab deploy tokens. Use for creating, listing, or deleting tokens at instance, project, or group levels. Triggers: deploy keys, access tokens."
---

### Overview
Handles deploy tokens for CI/CD access.

### Key Tools
- `get_deploy_tokens`: Instance-wide list.
- `get_project_deploy_tokens` / `create_project_deploy_token` / `delete_project_deploy_token`: Project-level.
- `get_group_deploy_tokens` / `create_group_deploy_token` / `delete_group_deploy_token`: Group-level.

### Usage Instructions
1. Specify scopes as list (e.g., ["read_repository"]).
2. Use expires_at for time-bound tokens.

### Examples
- Create project token: `create_project_deploy_token` with project_id="123", name="ci-token", scopes=["read_registry"].
- List group tokens: `get_group_deploy_tokens` with group_id="group/path".

### Error Handling
- Duplicate names: Use unique names.
- Revocation: Delete to revoke.