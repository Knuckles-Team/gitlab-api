# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
