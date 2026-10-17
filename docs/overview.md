# gitlab-api — Concept Overview

> Built on [`agent-connector-sdk`](https://github.com/Knuckles-Team/agent-connector-sdk) — the unified AGI Harness.

## Description

GitLab API + MCP Server

## Enterprise Readiness

All agents in the ecosystem inherit enterprise-grade infrastructure from `agent-connector-sdk`:

| Feature | Status | Source |
|:--------|:-------|:-------|
| **JWT/OIDC Authentication** | ✅ Built-in | `agent-connector-sdk` — Authlib JWKS + API key middleware |
| **OpenTelemetry Instrumentation** | ✅ Built-in | `agent-connector-sdk` — OTLP export, FastAPI auto-instrumentation |
| **HashiCorp Vault Integration** | ✅ Built-in | `agent-connector-sdk` — `secret://`, `env://`, `vault://` URI schemes |
| **Audit Logging** | ✅ Built-in | Append-only compliance trail with 30+ action types (CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox) |
| **Token Usage Analytics** | ✅ Built-in | 4-bucket tracking with budget alerting (CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox) |
| **Prompt Injection Defense** | ✅ Built-in | 25+ pattern scanner + jailbreak taxonomy (CONCEPT:AU-OS.config.secrets-authentication) |
| **Guardrail Engine** | ✅ Built-in | Input/output interception with block/redact/warn (CONCEPT:AU-OS.governance.reactive-multi-axis-budget) |
| **Action Execution Pipeline** | ✅ Built-in | Token, cost, duration, and node transition limits Dry-run / commit / rollback phases (CONCEPT:AU-ORCH.adapter.kg-graph-materialization) |
| **Resource Scheduling** | ✅ Built-in | Priority queuing + preemption limits (CONCEPT:AU-OS.state.cognitive-scheduler-preemption) |
| **Session Concurrency** | ✅ Built-in | Enqueue/reject/interrupt/rollback (CONCEPT:AU-OS.governance.reactive-multi-axis-budget) |

## Concept Registry

This project implements or inherits the following ecosystem concepts:

| Concept ID | Description | Source |
|:-----------|:------------|:-------|
| ECO-4.1 | MCP & Universal Skills | `agent-connector-sdk` (inherited) |

> 📖 **Full Registry**: See [`agent-connector-sdk/docs/overview.md`](https://github.com/Knuckles-Team/agent-connector-sdk/blob/main/docs/overview.md) for the complete 5-Pillar concept index.

## Architecture

This project follows the standardized agent-package pattern:

## MCP Configuration

### stdio Mode
```json
{
  "mcpServers": {
    "gitlab-api": {
      "command": "uv",
      "args": ["run", "--with", "gitlab-api", "gitlab-mcp"],
      "env": {}
    }
  }
}
```

### Streamable HTTP Mode
```bash
gitlab-mcp --transport streamable-http --port 8001
```
