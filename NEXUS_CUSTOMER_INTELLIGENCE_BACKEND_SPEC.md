# Nexus Customer Intelligence — Lightweight Backend Specification

> A deliberately small FastAPI and PostgreSQL backend that gives OpenFDE agents realistic customer-call data, documents, and actions without becoming a second product build.

**Status:** Simplified architecture — replaces the original 113-endpoint design  
**Stack:** Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic  
**Primary objective:** Spend the engineering time on agents  
**Related plan:** `OPENFDE_STUDIO_MASTER_PROJECT_PLANNER.md`

---

## 1. The Correction

The original specification overbuilt Nexus.

Nexus does not need to be a complete customer-operations SaaS. It does not need 113 endpoints, dozens of entities, a dedicated Control Plane, a complicated approval service, a workflow engine, or a distributed event system before the first agent works.

The correct definition is:

> **Nexus is a lightweight customer-call sandbox that gives OpenFDE agents something realistic to read, analyze, investigate, and act on.**

Nexus exists to support the agent curriculum. The agents are the project.

The new limits are:

- One FastAPI application
- One PostgreSQL database
- Six core tables
- Twelve product endpoints plus one health endpoint
- Eight function tools
- Seven MCP tools
- Seed scripts instead of ingestion infrastructure
- No frontend
- No Redis
- No Temporal
- No separate Nexus worker
- No Nexus-owned LLM loop
- No speculative enterprise infrastructure

We add a capability only when a specific OpenFDE agent cannot be built properly without it.

---

## 2. What Nexus Actually Does

Nexus represents a small B2B SaaS company's customer-call data.

It stores:

- Customer accounts
- Customer calls
- Stable transcript turns
- SOP and rubric documents
- Follow-up tasks
- Final agent-generated results

That is enough to support requests such as:

- “Find Acme's recent calls.”
- “Analyze the latest sales call against our discovery rubric.”
- “What objections are appearing across lost deals?”
- “Why does this account appear to be at risk?”
- “Create a follow-up task after I approve it.”
- “Build a sourced customer briefing.”
- “Route this request to the right specialist.”
- “Let several specialists investigate an escalation.”

The open-source project ships with synthetic data. Optimus A or another real backend can later load the same small schema through a private adapter.

### What Nexus is not

Nexus is not:

- Salesforce
- Gong
- Zendesk
- Calendly
- A data warehouse
- An agent framework
- The OpenFDE Control Plane
- A standalone startup that must be finished before OpenFDE

---

## 3. The Entire Architecture

~~~text
Synthetic seed script or private Optimus A adapter
                         |
                         v
              Nexus FastAPI + PostgreSQL
                  /                 \
                 v                   v
       Agent function tools      Nexus MCP
                  \                 /
                   v               v
             OpenFDE agent services
                         |
                 traces + evals + files
~~~

### Nexus owns

- Data validation
- Database queries
- Stable IDs
- Pagination and limits
- Task writes
- Idempotency for writes
- Simple service authentication

### OpenFDE agent services own

- Agent instructions and skills
- Model loops
- Sessions and memory
- Tool selection and handoffs
- Approval before write tools
- Structured outputs
- RAG experiments
- Artifact generation
- Tracing and evaluations
- Background execution only when an agent needs it

### MCP owns

- A standardized agent-facing version of selected Nexus capabilities
- Tool schemas and descriptions
- Transport and authentication

MCP does not contain separate business logic. It calls the same Nexus service layer or small REST API.

---

## 4. Repository Shape

~~~text
openfde/
  services/
    nexus/
      app/
        api.py
        database.py
        models.py
        schemas.py
        services/
          accounts.py
          calls.py
          documents.py
          tasks.py
          results.py
        settings.py
        main.py
      migrations/
      seed/
        generate.py
        fixtures/
      tests/
      Dockerfile

    agents/
      01-structured-tool/
      02-sop-analysis/
      03-react-investigator/
      04-planner-executor/
      05-rewoo-researcher/
      06-router-handoff/
      07-multi-agent-command/
      08-realtime-voice/

  mcp-servers/
    nexus/
      server.py
      tools.py
      tests/

  packages/
    nexus-client/
    openfde-runtime/
    openfde-evals/

  skills/
  datasets/
  artifacts/
  docker-compose.yml
~~~

Do not extract packages until a second consumer proves the shared abstraction is useful. The first function tools may live directly inside Agent 1.

---

## 5. The Six Core Tables

### `accounts`

~~~text
id                  UUID primary key
name                text
domain              text nullable
segment             text nullable
health_status       text nullable
owner_name          text nullable
metadata            jsonb default {}
created_at          timestamptz
updated_at          timestamptz
~~~

Do not create separate contacts, subscriptions, opportunities, teams, and account-insight tables yet. Optional synthetic attributes stay in `metadata` until an agent requires a real query or invariant.

### `calls`

~~~text
id                  UUID primary key
account_id          UUID foreign key -> accounts.id
external_id         text nullable unique
call_type           text
title               text
started_at          timestamptz
duration_seconds    integer
outcome             text nullable
participants        jsonb default []
summary             text nullable
metadata            jsonb default {}
created_at          timestamptz
~~~

Participants remain JSON because they are analysis context, not a product domain in V1.

### `transcript_turns`

~~~text
id                  UUID primary key
call_id             UUID foreign key -> calls.id
turn_index          integer
speaker             text
started_ms          integer nullable
ended_ms            integer nullable
text                text
metadata            jsonb default {}
~~~

Unique constraint: `(call_id, turn_index)`.

Stable turn IDs matter because analyses cite exact evidence.

### `documents`

~~~text
id                  UUID primary key
name                text
document_type       text
version             text
content             text
metadata            jsonb default {}
created_at          timestamptz
~~~

V1 documents are plain text or Markdown loaded directly into context. Do not build document-version tables, chunks, embeddings, or pgvector until the direct-context experiment fails.

### `tasks`

~~~text
id                  UUID primary key
account_id          UUID foreign key -> accounts.id
source_call_id      UUID nullable foreign key -> calls.id
title               text
description         text nullable
status              text
due_at              timestamptz nullable
idempotency_key     text nullable unique
created_by_run_id   text nullable
created_at          timestamptz
updated_at          timestamptz
~~~

This gives the agents one real write action. The approval pause happens in the OpenFDE run before the tool is called. V1 does not need a separate approval table.

### `agent_results`

~~~text
id                  UUID primary key
agent_name          text
agent_version       text
skill_name          text nullable
source_type         text
source_id           UUID nullable
result_type         text
result              jsonb
artifact_paths      jsonb default []
trace_id            text nullable
created_at          timestamptz
~~~

This stores final structured outputs without inventing separate analysis, score, evidence, artifact, review, and job tables. When a result type develops real query requirements, it may earn its own table later.

---

## 6. The Complete V1 REST API

There are twelve product endpoints and one health endpoint.

### System

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Verify Nexus and PostgreSQL are available |

### Accounts

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v1/accounts` | Search/filter accounts |
| GET | `/v1/accounts/{account_id}` | Retrieve one account |

Account filters: `q`, `health_status`, `segment`, `limit`, and `cursor`. Limit defaults to 20 and cannot exceed 50.

### Calls

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v1/calls` | Search/filter compact call records |
| GET | `/v1/calls/{call_id}` | Retrieve one call and participant metadata |
| GET | `/v1/calls/{call_id}/transcript` | Retrieve bounded transcript turns |

Call filters: `q`, `account_id`, `call_type`, `outcome`, `started_after`, `started_before`, `limit`, and `cursor`.

Transcript filters: `start_turn`, `end_turn`, and `limit`. The maximum is 250 turns. Search results never include full transcripts.

### Documents

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v1/documents` | List/filter SOP and rubric documents |
| GET | `/v1/documents/{document_id}` | Retrieve one complete small document |

Document filters: `q`, `document_type`, `version`, and `limit`.

### Tasks

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v1/tasks` | List/filter tasks |
| POST | `/v1/tasks` | Create one approved follow-up task |
| PATCH | `/v1/tasks/{task_id}` | Update task status or due date |

The agent service supplies `Idempotency-Key` for task creation. Nexus validates allowed status transitions.

### Agent Results

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v1/agent-results` | Persist a final typed agent result |
| GET | `/v1/agent-results/{result_id}` | Retrieve a result for demos or later synthesis |

`POST /v1/agent-results` is called by application code after a run. It is not exposed to the model as a general-purpose tool.

### Development seeding

Seeding is a CLI command, not another API:

~~~bash
python -m app.seed.generate --reset --calls 1000
~~~

This keeps destructive development operations out of the server surface.

---

## 7. The Eight Agent Function Tools

| Tool | Nexus endpoint | Purpose |
| --- | --- | --- |
| `search_accounts` | `GET /v1/accounts` | Resolve an account from a name or filter |
| `get_account` | `GET /v1/accounts/{id}` | Retrieve authoritative account context |
| `search_calls` | `GET /v1/calls` | Find relevant calls without loading transcripts |
| `get_call` | `GET /v1/calls/{id}` | Retrieve call metadata |
| `get_call_transcript` | `GET /v1/calls/{id}/transcript` | Retrieve bounded stable turns |
| `list_documents` | `GET /v1/documents` | Find the correct SOP or rubric |
| `get_document` | `GET /v1/documents/{id}` | Load one selected document |
| `create_task` | `POST /v1/tasks` | Create one approved follow-up task |

Application code, not the model, calls `save_agent_result` and `update_task`.

### Tool rules

1. The model never supplies credentials.
2. The model never supplies an arbitrary URL or HTTP method.
3. Every list has a strict maximum.
4. Transcript retrieval is bounded.
5. Tool inputs and outputs are typed Pydantic models.
6. `create_task` is unavailable until the run receives approval.
7. The idempotency key is derived outside the model.
8. Only tools required by the selected skill are exposed.

### Example

~~~python
@function_tool
async def search_calls(
    ctx: RunContextWrapper[AgentContext],
    query: str | None = None,
    account_id: UUID | None = None,
    outcome: str | None = None,
    limit: int = 20,
) -> CallSearchResult:
    """Find customer calls using compact metadata and text filters."""
    return await ctx.context.nexus.search_calls(
        query=query,
        account_id=account_id,
        outcome=outcome,
        limit=min(limit, 50),
    )
~~~

`AgentContext` supplies authentication, correlation ID, and the Nexus client. Those are application dependencies, not model arguments.

---

## 8. The Seven-Tool Nexus MCP

| MCP tool | Underlying capability |
| --- | --- |
| `search_accounts` | Search accounts |
| `get_account` | Retrieve account |
| `search_calls` | Search calls |
| `get_call` | Retrieve call metadata |
| `get_call_transcript` | Retrieve bounded transcript turns |
| `list_documents` | Find SOPs and rubrics |
| `get_document` | Retrieve one document |

`create_task` stays a local approval-gated function tool in the first MCP exercise. This deliberately compares shared read capabilities through MCP with a consequential local write capability.

After approval/resume is reliable, `create_task` may become the eighth MCP tool as an advanced exercise.

### Transport order

1. Local `stdio`
2. Streamable HTTP only when another deployed service needs it
3. Hosted/public MCP only when real authentication work is justified

Use function tools first because they are the shortest path to a working agent. Build MCP second to learn portability.

---

## 9. No Generic Query Endpoint

Do not add `execute_sql`, `query_database`, `call_api`, `run_graphql`, or `search_everything`.

For the 1,000-call dataset, the agent:

1. Calls `search_calls` with filters.
2. Receives compact call IDs and summaries.
3. Selects relevant calls.
4. Retrieves only necessary transcript turns.
5. Uses ordinary Python/PostgreSQL aggregation when exact counting is required.

If Agent 5 repeatedly needs one exact aggregation, add one narrow query for Agent 5. Do not create a general analytics API in advance.

---

## 10. Minimal Agent Service Contract

Start every agent service with only:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Service health |
| POST | `/run` | Run the agent and return a typed result |

Initially, `/run` may be synchronous.

Only add asynchronous run, status, SSE, cancellation, and resume endpoints when a real run needs them. Do not build the OpenFDE Control Plane during Agent 1 or Agent 2. Add the smallest registry/router when Agent 6 requires it.

---

## 11. How Tiny Nexus Supports All Eight Agents

### Agent 1 — Structured Tool Agent

Uses account, call, and task tools. Build function tools first, approval-gate `create_task`, then expose the read tools through MCP and compare both paths.

### Agent 2 — SOP Analysis and Artifact Agent

Uses call, transcript, and document tools.

The agent service:

1. Loads one transcript.
2. Loads the applicable SOP and rubric.
3. Produces typed analysis JSON.
4. Validates evidence turn IDs in Python.
5. Calculates totals in Python.
6. Renders HTML/PDF/DOCX locally.
7. Saves the final result through `POST /v1/agent-results`.

No analysis-job API is required. When hundreds of calls become an exercise, add a worker inside Agent 2.

### Agent 3 — ReAct Investigator

Uses the same accounts, calls, transcripts, and documents. External evidence comes from GitHub/Sentry MCPs or simulated tools. The new work is the ReAct loop, hypotheses, recovery, stopping, and grounded diagnosis—not Nexus endpoints.

### Agent 4 — Planner and Executor

Reads existing context and creates an approved task. Plan state, dependency validation, pause/resume, retry, and compensation belong to Agent 4.

### Agent 5 — ReWOO Researcher

Queries existing accounts, calls, and documents concurrently, then retrieves selected evidence. Add at most one narrow aggregate query if measurement proves it is needed.

### Agent 6 — Router and Handoff

Primarily reads agent/skill metadata, not Nexus data. This is the earliest point to introduce a tiny registry or Control Plane.

### Agent 7 — Multi-Agent Command

Specialists share existing Nexus read tools. Nexus remains unchanged unless the approved final recommendation creates a task.

### Agent 8 — Realtime Voice

Starts with existing read tools for account status. Scheduling adds only when Agent 8 is built:

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v1/availability/search` | Return synthetic available slots |
| POST | `/v1/meetings` | Create a meeting after explicit confirmation |

These are not V1 Nexus endpoints.

---

## 12. RAG and Memory Stay With the Agents

### RAG order

1. Store four small documents in `documents`.
2. Load selected documents directly into context.
3. Evaluate the baseline.
4. Try OpenAI File Search as a managed comparison.
5. Add pgvector only if the local experiment needs it.

Nexus does not need chunk, embedding, retrieval, reranking, and version APIs to teach RAG.

### Memory ownership

| Memory | Owner |
| --- | --- |
| Current account/call/task facts | Nexus |
| Run context | Agent service |
| Conversation history | Agents SDK session |
| Hypothesis ledger | Agent 3 |
| Plan checkpoint | Agent 4 |
| Evidence cache | Agent 5 |
| Handoff context | Agents 6/7 |
| Voice session summary | Agent 8 |

Do not create a Memory Service until two agents need the same persistent behavior.

---

## 13. Synthetic and Real Data

### Hand-authored development set

- 5 accounts
- 20 calls
- 4 SOP/rubric documents
- 10 tasks
- Reviewed ground truth for the first analysis cases

### Generated load set

- 50 accounts
- 1,000 calls
- 80–200 turns per transcript
- Multiple call types and outcomes
- Ambiguous, contradictory, and missing evidence
- Prompt injection inside selected transcripts
- Repeated objections and risk signals

### Optimus A

A private adapter later normalizes real calls into `accounts`, `calls`, and `transcript_turns`:

~~~python
class CallSourceAdapter(Protocol):
    async def fetch_calls(self, cursor: str | None) -> CallPage: ...
    async def fetch_transcript(self, external_call_id: str) -> Transcript: ...
~~~

Private Optimus A data and credentials never enter the open-source repository.

---

## 14. Testing and Evaluations

### Nexus tests

- Account search and pagination
- Call filtering
- Transcript ordering and limits
- Document filtering
- Task idempotency and transitions
- Agent-result persistence
- Service authentication

### Tool and MCP tests

- Pydantic validation
- Correct endpoint mapping
- Bounded results
- Stable not-found and timeout behavior
- `create_task` unavailable before approval
- MCP exposes only seven tools
- Function/MCP results have equivalent schemas
- MCP cannot call arbitrary Nexus endpoints

### Agent evaluations

- Correct skill
- Correct tool and arguments
- Evidence correctness
- Structured-output validity
- Unnecessary calls
- Missing-data recovery
- Approval compliance
- Route/handoff accuracy
- Cost and latency

The evaluation system grows from observed failures, not speculative platform requirements.

---

## 15. Ordered Build Plan

### Phase 1 — Tiny Nexus

Build one FastAPI service, six tables, thirteen routes, a seed CLI, five accounts, twenty calls, tests, and Docker Compose.

Done when calls can be searched, transcripts retrieved, documents loaded, and one task created idempotently.

### Phase 2 — Agent 1 Function Tools

Build Agent 1, `POST /run`, the account/call/task tools, one skill, typed output, approval, traces, and twenty-five eval cases.

### Phase 3 — Nexus MCP

Build seven read-only MCP tools over local stdio. Run the same Agent 1 read scenarios through function tools and MCP and publish the comparison.

### Phase 4 — Agent 2 Call Analysis

Build one analysis skill, four documents, typed JSON, evidence validation, deterministic scoring, HTML output, saved results, and twenty reviewed transcripts.

This is the first public MVP.

### Phase 5 — RAG Comparison

Compare direct context with managed File Search and optional pgvector. Add complexity only when the evaluation justifies it.

### Phases 6–11

Build Agents 3 through 8. Keep Nexus unchanged unless a particular exercise demonstrates a missing capability. Agent 6 may introduce a tiny registry; Agent 8 adds the two scheduling endpoints.

---

## 16. First Twenty Engineering Issues

1. Bootstrap Nexus FastAPI.
2. Add PostgreSQL, SQLAlchemy, and Alembic.
3. Create the six-table migration.
4. Implement the deterministic seed CLI.
5. Add account list/get.
6. Add call list/get/transcript.
7. Add document list/get.
8. Add task list/create/update with idempotency.
9. Add agent-result create/get.
10. Add Nexus integration tests.
11. Scaffold Agent 1 with health and run routes.
12. Implement four account/call function tools.
13. Implement the approval-gated task tool.
14. Add Agent 1 structured output and traces.
15. Create twenty-five eval cases.
16. Implement the local Nexus MCP.
17. Compare function tools and MCP.
18. Create four SOP/rubric documents.
19. Build typed call-analysis output.
20. Add evidence validation and HTML rendering.

Stop, publish the first MVP, and choose the next complexity from measured failures.

---

## 17. Complexity Budget

Before adding infrastructure, ask:

> Which current agent failure requires this component?

| Addition | Add only when |
| --- | --- |
| pgvector | The direct-context/local RAG goal fails |
| Redis | Measured cache, queue, or coordination pressure exists |
| Worker | A real agent run no longer fits a request lifecycle |
| Temporal | Durable recovery is the explicit Agent 4 exercise |
| Control Plane | Agent 6 needs discovery and routing |
| Nexus table | JSON cannot enforce/query an important invariant |
| Nexus endpoint | An agent cannot use an existing narrow endpoint |
| Frontend | OpenAPI/CLI cannot support the learning objective |
| Multitenancy | Real hosted users or Optimus A require isolation |

Every addition needs an observed failure, the smallest change, and an evaluation proving it helped.

---

## 18. Final Scope Check

| Item | Decision |
| --- | --- |
| Nexus | Lightweight customer-call sandbox |
| Backend | One FastAPI service |
| Database | One PostgreSQL database |
| Tables | Six |
| V1 routes | Thirteen including health |
| Function tools | Eight |
| MCP tools | Seven read tools initially |
| Frontend | None until voice |
| Worker | None until batch analysis needs it |
| Redis | No |
| Temporal | Agent 4 stretch only |
| Control Plane | Deferred until Agent 6 |
| RAG | Direct context first |
| Artifacts | Generated inside Agent 2 |
| Approvals | Agent pause/resume around write tool |
| Memory | Agent sessions and run state |
| Real data | Private Optimus A adapter later |
| Main work | Building, breaking, tracing, and evaluating agents |

> **Nexus should be boring. The agents should be impressive.**

---

## 19. Official OpenAI References

- [OpenAI Agents SDK tools](https://openai.github.io/openai-agents-python/tools/)
- [OpenAI Agents SDK MCP](https://openai.github.io/openai-agents-python/mcp/)
- [OpenAI Agents SDK handoffs](https://openai.github.io/openai-agents-python/handoffs/)

The official SDK exposes function tools, agents as tools, handoffs, and MCP connections as separate primitives. OpenFDE uses those primitives directly and keeps Nexus intentionally small.
