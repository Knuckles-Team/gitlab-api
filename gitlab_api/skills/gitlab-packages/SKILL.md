---
name: gitlab-packages
description: "Manages GitLab packages. Use for listing, publishing, or downloading packages. Triggers: artifact registry."
---

### Overview
Covers package repository ops.

### Key Tools
- `get_repository_packages` / `publish_repository_package` / `download_repository_package`.

### Usage Instructions
1. Specify package_name/version/file_name.

### Examples
- Publish: `publish_repository_package` with project_id="123", package_name="mypkg", package_version="1.0".
- Download: Similar with file_name.

### Error Handling
- Version conflicts: Use unique versions.