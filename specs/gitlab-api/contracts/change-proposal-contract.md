# Contract: change-proposal records and the normalizer protocol

Provider: scion-sdk SCION-SCM-R003.2
Consumer: gitlab-api CONN-GITLAB-API-R004.12

The SDK defines the records and the normalizer protocol. The connector implements the protocol for GitLab webhooks and returns the records from its tools.

## Wire shape

- `ScmEventNormalizer.normalize(headers, body) -> ScmFeedbackEvent` after `verify_webhook` accepts the shared token.
- `ScmFeedbackEvent{event_id, provider, kind, proposal, actor, actor_kind, at, body_digest}` with `kind` from the closed set of SCION-SCM-R003.1.
- Tool replies map to `ChangeProposalRef`, `ReviewRecord`, `ReviewThreadRecord` and `CheckRunRecord` (SCION-SCM-R003.1).

## Refusal codes

- `SCM_SIGNATURE_INVALID`: the token does not match the shared secret.
- `SCM_EVENT_UNSUPPORTED`: the event type has no feedback kind.

## Authoritative types

- SDK records: `scion_sdk/scm/records.py` (SCION-SCM-R003.1).
- Connector normalizer: `gitlab_api/scm_events.py` (CONN-GITLAB-API-R004.12).

## Test vectors

- `tests/fixtures/scm_events/` in this repository: one recorded payload per event type.
