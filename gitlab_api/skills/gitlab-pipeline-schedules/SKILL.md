---
name: gitlab-pipeline-schedules
description: "Manages GitLab pipeline schedules. Use for creating, editing, running scheduled pipelines. Triggers: cron jobs, automation."
---

### Overview
Covers scheduled CI.

### Key Tools
- Get/create/edit/delete schedules.
- Run/take ownership/variables.

### Usage Instructions
1. Cron format for schedules.

### Examples
- Create: `create_pipeline_schedule` with project_id="123", ref="main", cron="0 0 * * *".
- Run: `run_pipeline_schedule` with pipeline_schedule_id=1.

### Error Handling
- Invalid cron: Validate format.