# CONN-GITLAB-API — Test specification

Governing spec: [spec.md](spec.md).

| Requirement | Test | Observation |
|---|---|---|
| `CONN-GITLAB-API-R001` | `tests/test_ingest_sources.py::test_declares_ingestible_sources` | The declaration validates and its tools are the read operations `get_projects` and `get_issues`. |
| `CONN-GITLAB-API-R002` | `tests/test_fleet_name.py::test_connector_name_is_the_fleet_name` | Every connector name in the package is `gitlab-mcp`. |
| `CONN-GITLAB-API-R003` | `tests/test_gitlab_gql.py::test_wrapper_delegates_to_shared_graphql_client` | The wrapper uses the endpoint, bearer header, TLS profile and schema fetch of the shared client. |
| `CONN-GITLAB-API-R004` | `tests/test_merge_request_served.py::test_served_tools_and_normalizer_round_trip` | Merge-request delivery tools (rollup). |
| `CONN-GITLAB-API-R004.1` | `tests/test_merge_request_tools.py::test_get_merge_request_maps_to_change_proposal_ref` | Read one merge request as a change-proposal record. |
| `CONN-GITLAB-API-R004.2` | `tests/test_merge_request_tools.py::test_discussions_map_to_review_threads` | List the discussions of a merge request. |
| `CONN-GITLAB-API-R004.3` | `tests/test_merge_request_tools.py::test_resolve_discussion_is_idempotent` | Resolve one discussion. |
| `CONN-GITLAB-API-R004.4` | `tests/test_merge_request_tools.py::test_discussion_reply_bounds_the_body` | Reply to a discussion. |
| `CONN-GITLAB-API-R004.5` | `tests/test_merge_request_tools.py::test_merge_request_pipelines_map_to_check_runs` | List the pipelines of a merge request. |
| `CONN-GITLAB-API-R004.6` | `tests/test_merge_request_tools.py::test_pipeline_jobs_map_to_check_runs` | List the jobs of a pipeline. |
| `CONN-GITLAB-API-R004.7` | `tests/test_merge_request_tools.py::test_auto_merge_needs_approval_ref_and_matching_sha` | Set auto-merge for an expected head commit. |
| `CONN-GITLAB-API-R004.8` | `tests/test_merge_request_tools.py::test_cancel_auto_merge_needs_no_approval` | Cancel auto-merge. |
| `CONN-GITLAB-API-R004.9` | `tests/test_merge_request_tools.py::test_close_merge_request_is_destructive_and_idempotent` | Close a merge request without merging. |
| `CONN-GITLAB-API-R004.10` | `tests/test_merge_request_tools.py::test_mark_ready_is_idempotent` | Mark a draft merge request ready. |
| `CONN-GITLAB-API-R004.11` | `tests/test_merge_request_tools.py::test_approvals_map_to_review_records` | Read the approval state of a merge request. |
| `CONN-GITLAB-API-R004.12` | `tests/test_scm_events.py::test_each_event_maps_to_one_feedback_kind` | Normalize webhook events to feedback events. |
| `CONN-GITLAB-API-R004.13` | `tests/test_merge_request_tools.py::test_delivery_records_map_to_shared_classes` | Map delivery records to the shared ontology classes. |
| `CONN-GITLAB-API-R004.14` | `tests/test_merge_request_served.py::test_served_tools_and_normalizer_round_trip` | Hot-path proof: served merge-request tools. |
| `CONN-GITLAB-API-R005` | `tests/test_bug_002_005.py::test_no_tool_schema_requires_an_optional_field` | Optional input fields stay optional in served tool schemas. |
| `CONN-GITLAB-API-R006` | `tests/test_bug_002_005.py::test_graphql_failure_names_message_and_expected_kwargs` | GraphQL operation failures explain themselves. |
| `CONN-GITLAB-API-R006.1` | `tests/test_graphql_error_category.py::test_missing_merge_request_update_is_not_found_without_server_text` | Typed GraphQL tools return a typed failure category. |
| `CONN-GITLAB-API-R007` | `tests/test_bug_002_005.py::test_rest_session_applies_a_default_timeout` | Every GitLab request has a timeout. |
