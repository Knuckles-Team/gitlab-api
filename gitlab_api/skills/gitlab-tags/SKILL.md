---
name: gitlab-tags
description: "Manages GitLab tags. Use for creating, deleting, protecting tags. Triggers: versioning."
---

### Overview
Handles tags and protection.

### Key Tools
- Get/create/delete tags.
- Protect/unprotect.

### Usage Instructions
1. Ref for creation.

### Examples
- Create: `create_tag` with project_id="123", name="v1.0", ref="main".
- Protect: `protect_tag` with create_access_level="maintainer".

### Error Handling
- Tag exists: Delete first.