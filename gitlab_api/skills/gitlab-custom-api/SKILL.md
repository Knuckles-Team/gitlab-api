---
name: gitlab-custom-api
description: "Handles custom GitLab API requests. Use for any endpoint not covered by other skills. Triggers: advanced API calls, extensions."
---

### Overview
Fallback for arbitrary requests.

### Key Tools
- `api_request`: Custom HTTP calls.

### Usage Instructions
1. Specify method, endpoint, data/json.

### Examples
- GET: `api_request` with method="GET", endpoint="projects/123/issues".
- POST: With data={"title": "New issue"}.

### Error Handling
- Validate endpoints.