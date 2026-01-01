---
name: gitlab-commits
description: "Manages GitLab commits. Use for listing, creating, reverting, or querying commit details/diffs/comments. Triggers: commit history, changes, reversions."
---

### Overview
This skill covers commit operations via MCP. Use for code changes, diffs, or discussions.

### Key Tools
- `get_commits`: List or get a commit. Params: project_id (required), commit_hash/ref_name/since/until/path/all.
- `create_commit`: Create a commit. Params: project_id, branch, commit_message, actions (required).
- `revert_commit`: Revert a commit. Params: project_id, commit_hash, branch (required), dry_run?.
- `get_commit_diff`: Get diff. Params: project_id, commit_hash.
- `get_commit_comments` / `create_commit_comment`: Manage comments.
- `get_commit_discussions` / `get_commit_statuses` / `post_build_status_to_commit`: Discussions and statuses.
- `get_commit_merge_requests` / `get_commit_gpg_signature`: Associated MRs and signatures.

### Usage Instructions
1. Use project_id and commit_hash for specifics.
2. For creation, build actions list (e.g., [{"action": "create", "file_path": "file.txt", "content": "..."}]).
3. Async tools (e.g., delete) support progress via ctx.

### Examples
- List commits: `get_commits` with project_id="123", ref_name="main", since="2023-01-01".
- Create: `create_commit` with project_id="123", branch="feature", commit_message="Add file", actions=[...].
- Revert: `revert_commit` with project_id="123", commit_hash="abc123", branch="main".

### Error Handling
- Invalid ref: Check branch/SHA existence first.
- Conflicts: Use diff tools to resolve.

Reference `tools-reference.md` for schemas.