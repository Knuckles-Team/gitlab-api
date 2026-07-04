# Concept Registry — gitlab-api

> **Prefix**: `CONCEPT:GL-*`
> **Version**: 25.27.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:GL-OS.governance.gl` | Branches Operations | MCP tool domain `branches` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-2` | Commits Operations | MCP tool domain `commits` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-3` | Custom Api Operations | MCP tool domain `custom_api` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-4` | Deploy Tokens Operations | MCP tool domain `deploy_tokens` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-5` | Environments Operations | MCP tool domain `environments` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-6` | Epics Operations | MCP tool domain `epics` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-7` | Graphql Operations | MCP tool domain `graphql` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-8` | Group Management | MCP tool domain `groups` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-9` | Issues Operations | MCP tool domain `issues` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-10` | Jobs Operations | MCP tool domain `jobs` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-11` | Labels Operations | MCP tool domain `labels` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-12` | Members Operations | MCP tool domain `members` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-13` | Merge Requests Operations | MCP tool domain `merge_requests` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-14` | Merge Rules Operations | MCP tool domain `merge_rules` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-15` | Milestones Operations | MCP tool domain `milestones` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-16` | Misc Operations | MCP tool domain `misc` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-17` | Notes Operations | MCP tool domain `notes` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-18` | Packages Operations | MCP tool domain `packages` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-19` | Pipeline Schedules Operations | MCP tool domain `pipeline_schedules` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-20` | Pipelines Operations | MCP tool domain `pipelines` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-21` | Projects Operations | MCP tool domain `projects` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-22` | Protected Branches Operations | MCP tool domain `protected_branches` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-23` | Releases Operations | MCP tool domain `releases` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-24` | Runners Operations | MCP tool domain `runners` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-25` | Snippets Operations | MCP tool domain `snippets` — Action-routed dynamic tool registration |
| `CONCEPT:GL-OS.governance.gl-26` | Tags Operations | MCP tool domain `tags` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | agent-utilities |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | agent-utilities |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `gitlab_api` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all GL-* concepts.
