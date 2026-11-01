# Contract: delivery classes

Provider: medulla MEDULLA-SDLC-R019.1
Consumer: gitlab-api CONN-GITLAB-API-R004.13

The engine declares the delivery classes. The connector references them in its mapping and never redeclares them.

## Wire shape

- `schema_mappings` entries map merge requests, approvals, discussions, pipelines and jobs to `:MergeRequest`, `:Review`, `:ReviewThread`, `:PipelineRun` and `:PipelineJob`.

## Refusal codes

- `PACK_CLASS_UNROOTED`: a mapped class does not reach an engine core class.
- A null `ontology_class` fails the connector certification.

## Authoritative types

- Engine vocabulary: `crates/medulla-core/ontology/sdlc_lifecycle-v1.ttl` in medulla.
- Connector mapping: `gitlab_api/ontology/mappings/source.yaml`.

## Test vectors

- `tests/test_merge_request_tools.py::test_delivery_records_map_to_shared_classes`.
