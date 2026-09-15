# Agent organization

Each implemented OpenFDE agent owns one numbered, kebab-case directory:

```text
agents/<number>-<agent-slug>/
  README.md
  backend/
    tests/
  ui/
  evals/
  datasets/
  docs/
```

An agent directory owns its model instructions, runtime, tools, API entry point, agent-specific UI,
tests, evaluation configuration, datasets, and learning material. Add only the directories an agent
actually uses; do not create empty Agent 2–8 implementations in advance.

Shared systems remain outside agent directories:

- `services/nexus/` owns business data, migrations, authentication, and domain operations.
- `studio/` owns application bootstrap, routing, global styles, and reusable UI infrastructure.
- root scripts, Compose, CI, and environment examples orchestrate the repository.
- the master planner and Nexus specification describe project-wide architecture.

Agent-specific code may depend on shared systems. Shared systems must not import an individual
agent implementation.
