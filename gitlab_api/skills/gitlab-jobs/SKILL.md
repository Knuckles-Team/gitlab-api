---
name: gitlab-jobs
description: "Manages GitLab CI jobs. Use for listing, logs, canceling, retrying, or erasing jobs. Triggers: CI builds, job status."
---

### Overview
Covers job execution and logs.

### Key Tools
- `get_project_jobs` / `get_project_job_log` / `cancel_project_job` / `retry_project_job` / `erase_project_job` / `run_project_job`: Project jobs.
- `get_pipeline_jobs`: Pipeline-specific.

### Usage Instructions
1. Use job_id for actions.
2. Filters: scope, status.

### Examples
- Get log: `get_project_job_log` with project_id="123", job_id=456.
- Retry: `retry_project_job` with project_id="123", job_id=456.

### Error Handling
- Job not found: Verify IDs.