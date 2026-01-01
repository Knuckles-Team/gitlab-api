---
name: gitlab-pipelines
description: "Manages GitLab pipelines. Use for listing, running pipelines. Triggers: CI triggers."
---

### Overview
Handles pipeline execution.

### Key Tools
- `get_pipelines`: List/get.
- `run_pipeline`: Trigger.

### Usage Instructions
1. Use ref for branch/tag.

### Examples
- Run: `run_pipeline` with project_id="123", ref="main".
- List: `get_pipelines` with project_id="123", status="running".

### Error Handling
- Failed triggers: Check config.