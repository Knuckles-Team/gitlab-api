---
name: gitlab-runners
description: "Manages GitLab runners. Use for registering, updating, deleting runners at various levels. Triggers: CI infrastructure."
---

### Overview
Covers runner setup.

### Key Tools
- Get/register/update/delete runners.
- Project/group specifics.
- Token resets.

### Usage Instructions
1. Use tokens for registration.

### Examples
- Register: `register_new_runner` with token="abc123".
- Enable: `enable_project_runner` with runner_id=1.

### Error Handling
- Token invalid: Reset.