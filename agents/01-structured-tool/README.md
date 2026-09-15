# Agent 1 — Structured Tool

Agent 1 is a narrow account assistant and the first OpenFDE agent-engineering course. It teaches
how a model chooses among typed tools while application code owns execution and side effects.

## Current checkpoint

The agent has five deterministic mock tools and can sequence them:

```text
message -> model -> answer
message -> model -> search_accounts -> answer
message -> model -> search_accounts -> account details, calls, documents, or task proposal -> answer
```

`propose_task` stores a temporary in-memory proposal. Agent 1 does not yet call Nexus, persist a
task, use trusted tenant context, or pause for human approval. Each message is an independent run.

## Owned files

- `backend/` contains the Agents SDK definition, runtime, function tools, FastAPI entry point, CLI,
  container, dependencies, and Python tests.
- `ui/` contains the Studio chat feature, browser client, agent-specific styles, component tests,
  and browser test.
- `evals/` contains the Promptfoo runner and its Python provider.
- `datasets/` records the current scenario status and will own versioned cases.
- `docs/first-principles.md` explains the staged learning path.

Nexus remains a shared dependency in `services/nexus`. Root configuration and scripts orchestrate
Agent 1 but are not owned by it.

## Run locally

From the repository root:

```bash
uv sync --project agents/01-structured-tool/backend --locked
cp .env.example .env
pnpm dev
```

Add a valid `OPENAI_API_KEY` to `.env`. Studio runs at <http://localhost:5173> and the Agent 1 API
runs at <http://localhost:8010>. The UI distinguishes a plain answer from the ordered tools used,
for example `used search_accounts, search_calls`.

Useful commands:

```bash
pnpm learn:agent1:section1 "What happened in Acme's latest call?"
pnpm eval:agent1:section1
cd agents/01-structured-tool/backend && .venv/bin/python -m pytest
```

The Promptfoo command makes live model requests. The Python tests use a fake runner and make no
paid requests.

## Next milestone

Keep the public tool names and replace the mock implementations with authenticated Nexus HTTP
adapters. Structured output, trusted context, persistent writes, approval-resume, and the larger
evaluation dataset follow as separate observable checkpoints.
