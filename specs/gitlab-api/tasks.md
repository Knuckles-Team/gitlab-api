# CONN-GITLAB-API — Implementation tasks

Governing spec: [spec.md](spec.md). Design: [plan.md](plan.md). Rows: [requirements.md](requirements.md).

Each task line reads `- [ ] T001 [P] [US1] <ID>-R012.4 description`. Order is producer first.

- [x] T001 [US1] CONN-GITLAB-API-R001 Declare the `projects` and `issues` sources.
- [x] T002 [US1] CONN-GITLAB-API-R002 Fleet name.
- [x] T003 [US1] CONN-GITLAB-API-R003 Shared GraphQL client.
- [ ] T004 [US1] CONN-GITLAB-API-R004 Merge-request delivery tools (rollup).
- [ ] T005 [US1] CONN-GITLAB-API-R004.1 Read one merge request as a change-proposal record.
- [ ] T006 [US1] CONN-GITLAB-API-R004.2 List the discussions of a merge request.
- [ ] T007 [US1] CONN-GITLAB-API-R004.3 Resolve one discussion.
- [ ] T008 [US1] CONN-GITLAB-API-R004.4 Reply to a discussion.
- [ ] T009 [US1] CONN-GITLAB-API-R004.5 List the pipelines of a merge request.
- [ ] T010 [US1] CONN-GITLAB-API-R004.6 List the jobs of a pipeline.
- [ ] T011 [US1] CONN-GITLAB-API-R004.7 Set auto-merge for an expected head commit.
- [ ] T012 [US1] CONN-GITLAB-API-R004.8 Cancel auto-merge.
- [ ] T013 [US1] CONN-GITLAB-API-R004.9 Close a merge request without merging.
- [ ] T014 [US1] CONN-GITLAB-API-R004.10 Mark a draft merge request ready.
- [ ] T015 [US1] CONN-GITLAB-API-R004.11 Read the approval state of a merge request.
- [ ] T016 [US1] CONN-GITLAB-API-R004.12 Normalize webhook events to feedback events.
- [ ] T017 [US1] CONN-GITLAB-API-R004.13 Map delivery records to the shared ontology classes.
- [ ] T018 [US1] CONN-GITLAB-API-R004.14 Hot-path proof: served merge-request tools.
- [ ] T019 [US1] CONN-GITLAB-API-R005 Optional input fields stay optional in served tool schemas.
- [ ] T020 [US1] CONN-GITLAB-API-R006 GraphQL operation failures explain themselves.
- [ ] T021 [US1] CONN-GITLAB-API-R007 Every GitLab request has a timeout.
