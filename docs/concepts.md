# Concept Registry — gitlab-api

> **Prefix**: `CONCEPT:GL-*`
> **Version**: 25.27.0
> **Bridge**: [`CONCEPT:ECO-4.0`](../../agent-utilities/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:GL-001` | Branches Operations | MCP tool domain `branches` — Action-routed dynamic tool registration |
| `CONCEPT:GL-002` | Commits Operations | MCP tool domain `commits` — Action-routed dynamic tool registration |
| `CONCEPT:GL-003` | Custom Api Operations | MCP tool domain `custom_api` — Action-routed dynamic tool registration |
| `CONCEPT:GL-004` | Deploy Tokens Operations | MCP tool domain `deploy_tokens` — Action-routed dynamic tool registration |
| `CONCEPT:GL-005` | Environments Operations | MCP tool domain `environments` — Action-routed dynamic tool registration |
| `CONCEPT:GL-006` | Epics Operations | MCP tool domain `epics` — Action-routed dynamic tool registration |
| `CONCEPT:GL-007` | Graphql Operations | MCP tool domain `graphql` — Action-routed dynamic tool registration |
| `CONCEPT:GL-008` | Group Management | MCP tool domain `groups` — Action-routed dynamic tool registration |
| `CONCEPT:GL-009` | Issues Operations | MCP tool domain `issues` — Action-routed dynamic tool registration |
| `CONCEPT:GL-010` | Jobs Operations | MCP tool domain `jobs` — Action-routed dynamic tool registration |
| `CONCEPT:GL-011` | Labels Operations | MCP tool domain `labels` — Action-routed dynamic tool registration |
| `CONCEPT:GL-012` | Members Operations | MCP tool domain `members` — Action-routed dynamic tool registration |
| `CONCEPT:GL-013` | Merge Requests Operations | MCP tool domain `merge_requests` — Action-routed dynamic tool registration |
| `CONCEPT:GL-014` | Merge Rules Operations | MCP tool domain `merge_rules` — Action-routed dynamic tool registration |
| `CONCEPT:GL-015` | Milestones Operations | MCP tool domain `milestones` — Action-routed dynamic tool registration |
| `CONCEPT:GL-016` | Misc Operations | MCP tool domain `misc` — Action-routed dynamic tool registration |
| `CONCEPT:GL-017` | Notes Operations | MCP tool domain `notes` — Action-routed dynamic tool registration |
| `CONCEPT:GL-018` | Packages Operations | MCP tool domain `packages` — Action-routed dynamic tool registration |
| `CONCEPT:GL-019` | Pipeline Schedules Operations | MCP tool domain `pipeline_schedules` — Action-routed dynamic tool registration |
| `CONCEPT:GL-020` | Pipelines Operations | MCP tool domain `pipelines` — Action-routed dynamic tool registration |
| `CONCEPT:GL-021` | Projects Operations | MCP tool domain `projects` — Action-routed dynamic tool registration |
| `CONCEPT:GL-022` | Protected Branches Operations | MCP tool domain `protected_branches` — Action-routed dynamic tool registration |
| `CONCEPT:GL-023` | Releases Operations | MCP tool domain `releases` — Action-routed dynamic tool registration |
| `CONCEPT:GL-024` | Runners Operations | MCP tool domain `runners` — Action-routed dynamic tool registration |
| `CONCEPT:GL-025` | Snippets Operations | MCP tool domain `snippets` — Action-routed dynamic tool registration |
| `CONCEPT:GL-026` | Tags Operations | MCP tool domain `tags` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:OS-5.2` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:OS-5.3` | Guardrail Engine | agent-utilities |
| `CONCEPT:OS-5.4` | Audit Logging | agent-utilities |
| `CONCEPT:KG-2.0` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:ECO-4.0` (Unified Toolkit Ingestion). The `gitlab_api` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all GL-* concepts.
