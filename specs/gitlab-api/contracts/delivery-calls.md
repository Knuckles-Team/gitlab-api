# Contract: delivery calls from arbora

Provider: gitlab-api CONN-GITLAB-API-R004.7
Consumer: arbora ARBORA-OPS-R896.10

Arbora calls the merge-request tools through `fleet.call`. It sets auto-merge only under an owner approval receipt (ARBORA-OPS-R896.10). It calls the normalizer of CONN-GITLAB-API-R004.12 from its intake (ARBORA-OPS-R896.8).

## Wire shape

- `gitlab_set_merge_request_auto_merge{project_id, merge_request_iid, sha, approval_ref}` returns `{armed, sha}`.
- `gitlab_cancel_merge_when_pipeline_succeeds{project_id, merge_request_iid}` returns `{armed: false}`.

## Refusal codes

- `approval_required`: the call carries no approval reference.
- `head_mismatch`: the head differs from `sha`; nothing is armed.
- `unauthorized`, `not_found`: the typed SDK refusals.

## Authoritative types

- `gitlab_api/api/api_client_merge_requests.py`.

## Test vectors

- `tests/test_merge_request_tools.py::test_auto_merge_needs_approval_ref_and_matching_sha`.
