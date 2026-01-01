---
name: gitlab-releases
description: "Manages GitLab releases. Use for creating, updating, deleting releases and assets. Triggers: versioning, deployments."
---

### Overview
Handles release artifacts.

### Key Tools
- Get/create/update/delete releases.
- Evidences/assets.

### Usage Instructions
1. Tag-based.

### Examples
- Create: `create_release` with project_id="123", tag_name="v1.0", name="Version 1".
- Delete: `delete_release` with tag_name="v1.0".

### Error Handling
- Tag missing: Create tag first.