# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [27.3.15] - 2026-10-27

### Added
- Add the packaged GitLab API development skill, Pages spec dashboard, and focused contract tests.

## [27.3.13] - 2026-10-24

### Added
- Owner and assignee edges on the ingest sources (SDK 0.5.5 `EdgeSpec`): project to owner and namespace group,
  issue to author and assignees, with the `Person` record type (CONN-GITLAB-API-CONNECTOR-CONTENT-R005).

## [27.3.12] - 2026-10-24

### Fixed
- Requires `agent-connector-sdk>=0.5.3`: extra registrations receive a `RegistrationContext`, so `register_prompts` takes the context and reads the server from it.

## [27.3.11] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.2`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [Unreleased]

### Added
- Action-Routed pattern to `mcp_server.py` for advanced scalability.

### Changed
- Massively consolidated MCP tools (from 169 fragmented endpoints to 18 Action-Routed tools) to adhere to the IDE 100-tool hard cap and optimize LLM token consumption.
- Replaced `_` prefixed parameters with standardized `kwargs` driven arguments in `mcp_server.py`.
- Enforced `Field()` descriptions across all MCP endpoints for clarity.

### Fixed
- Fixed bug with legacy underscore-prefixed variables not mapping correctly in the validation pipelines.

## [25.15.56] - 2026-04-29

### Added
- Initial release
