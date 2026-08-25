# OpenFDE Studio — Master Project Planner

> An open-source curriculum, reference architecture, and full-stack studio for learning how to build production AI agents with the OpenAI Agents SDK.

## 1. Project Thesis

OpenFDE Studio teaches agent engineering through eight complete builds rather than isolated examples. Every build includes a real product scenario, backend, interface, tools, skills, memory, safety boundaries, traces, datasets, evaluations, and progressively harder exercises.

OpenFDE is implemented with the **OpenAI Agents SDK**. NVIDIA NeMo Agent Toolkit is architectural inspiration for composing tool-calling, ReAct, reasoning, ReWOO, routing, sequential, and multi-agent workflows. OpenFDE does not depend on or reimplement NVIDIA's toolkit.

> Agents are interchangeable workers. OpenFDE provides the operating layer, learning environment, and reliability system around them.

## 2. End-State Learning Outcomes

After completing OpenFDE, a developer should be able to:

1. Build agents with typed outputs and validated tools.
2. Connect trusted local and remote MCP servers.
3. Create, select, and invoke reusable skills and SOPs.
4. Manage conversation state and durable memory.
5. Decide when to use an agent loop versus deterministic code.
6. Implement ReAct-style investigation.
7. Separate planning, execution, and synthesis.
8. Route requests and hand off to specialists.
9. Coordinate multiple agents without losing control of state, cost, or quality.
10. Add approval gates around consequential actions.
11. Trace and debug agent decisions.
12. Build datasets for routing, tools, memory, workflow, policy, and voice.
13. Evaluate decisions rather than only final prose.
14. Build a realtime voice agent with tools, interruptions, and safety checks.
15. Ship the complete system with a frontend, API, database, workers, tests, and CI.
16. Build direct-context, file-search, vector, filtered, and agentic retrieval paths.
17. Generate validated JSON, HTML, PDF, and Word artifacts.
18. Load-test agent workloads and introduce queues, workers, caching, and backpressure only when justified.

## 3. Product Layers

### OpenFDE Runtime

The shared Python runtime contract used by every agent service. It loads skills, tools, MCP servers, memory, policies, and workflows, then emits normalized run events.

### OpenFDE Control Plane

A lightweight FastAPI platform service that owns authentication context, service registration, run routing, approvals, and aggregated traces/evaluations. It never becomes a second agent framework.

### Independent Agent Services

Each reference project is a standalone FastAPI backend service built on the shared runtime contract. A developer can run only the service they are learning, or start all completed services for routing and multi-agent demos.

### OpenFDE Studio

The web application for:

- Browsing agents, skills, tools, and MCP connections
- Starting and monitoring runs
- Inspecting traces and handoffs
- Editing evaluation scenarios
- Comparing agent versions
- Reviewing approvals
- Viewing datasets and confusion matrices
- Exploring the architecture graph

### Nexus Operations

The reference business backend gives agents normal application state:

- Accounts and contacts
- Implementations and integrations
- Environments and deployments
- Incidents and tasks
- SOPs, decisions, and approvals

V1 uses FastAPI, PostgreSQL, and seeded data. A later adapter can connect the same agents to Twenty CRM or another system of record.

## 4. Recommended Technology Stack

| Area | Technology | Purpose |
| --- | --- | --- |
| Agent runtime | OpenAI Agents SDK for Python | Agents, tools, sessions, handoffs, guardrails, approvals, tracing |
| Control Plane | FastAPI and Pydantic | Registry, routing, approvals, aggregate run APIs |
| Agent services | FastAPI and Pydantic | Independently deployable project backends |
| Database | PostgreSQL | Business state, projects, runs, scenarios, memory, approvals |
| ORM | SQLAlchemy and Alembic | Data access and migrations |
| Frontend | Next.js, React, TypeScript | Studio product interface |
| Visualization | React Flow | Traces, routing, plans, and agent graphs |
| Streaming | Server-Sent Events first | Live run progress |
| Initial concurrency | Python asyncio | Understandable local fan-out |
| Durable workflow stretch | Temporal | Resumability, timers, retries, compensation |
| Cache/coordination stretch | Redis | Caching, rate limits, distributed coordination |
| Local environment | Docker Compose | Reproducible services |
| Tests | Pytest, Vitest, Playwright | Unit, integration, and browser coverage |
| CI | GitHub Actions | Test and evaluation gates |
| Voice client | OpenAI Agents SDK for TypeScript Realtime APIs | Browser WebRTC voice agent |
| Voice control plane | FastAPI | Auth, short-lived credentials, secure tools, persistence |

Introduce Temporal, Redis, and distributed workers only after the simple version demonstrates a concrete limitation.

### The Golden Path

All eight projects share the same technology choices while remaining independently deployable:

~~~text
One React/Next.js Studio
          |
OpenFDE Control Plane API
          |
Agent Service Registry
          |
Eight independent FastAPI agent services
          |
Nexus Operations API/MCP + PostgreSQL
~~~

Each agent project owns a FastAPI service. It can be started, tested, deployed, and load-tested independently. The single Next.js Studio presents them as one coherent product.

The Control Plane owns authentication, project registration, run routing, service discovery, approvals, and aggregated traces/evaluations. It does not contain agent-specific reasoning.

### Backend Service Boundary

Every agent service includes:

- FastAPI application
- OpenAI Agents SDK configuration
- Agent-specific skills
- Function and MCP tools
- Request and result schemas
- Run lifecycle endpoints
- Trace and evaluation hooks
- Tests and datasets
- Dockerfile
- Optional worker process

For local development, all services may share one PostgreSQL server while owning separate schemas and migrations. Services do not read each other's tables directly. They communicate through typed APIs, MCP, or later event messages.

Nexus Operations is its own ordinary backend service. Agent services consume it through its API or custom MCP server rather than importing its database models.

### Optional Infrastructure Profiles

| Profile | Runtime shape | Learning purpose |
| --- | --- | --- |
| Local | Studio, Control Plane, Nexus, and one selected agent service | Build one project without starting the world |
| Integrated | Studio plus all completed agent services in Docker Compose | Test routing and cross-agent behavior |
| Worker | Selected agent API plus its workers and optional Redis | Background jobs, retries, isolation, backpressure |
| Durable | Selected service plus Temporal workers | Long-running resumable workflows and compensation |
| Load | Replicas of one agent API/worker and a load generator | Throughput, concurrency, rate limits, cost |

The same run contract works across profiles. A service receives a run request, streams events, supports cancellation or approval, and returns a typed result. Infrastructure is introduced per service only when its workload justifies it.

### Core Full-Stack Responsibilities

OpenFDE remains a full-stack project:

- Authentication, tenancy, and RBAC
- CRUD APIs for Nexus Operations
- File uploads and artifact storage
- Run scheduling and cancellation
- Streaming progress
- Approval/resume UX
- Dataset and rubric management
- Background workers
- Rate limits and quotas
- Observability and cost accounting
- Deployment and CI

## 5. OpenFDE Skills

### Skills Versus Tools

- A **skill** teaches the agent how to perform a type of work.
- A **tool** gives the agent access to data or an action.
- An **MCP server** exposes a standardized collection of tools and context.

Example:

- Skill: incident-investigation procedure
- Tool: retrieve incident events
- MCP: GitHub or Sentry operations
- Agent: apply the procedure and decide what to do next

OpenFDE skills are a first-class OpenFDE abstraction loaded into OpenAI agents through instructions, context, resources, tool policies, and output contracts.

### Skill Package

~~~text
skills/
  integration-debugging/
    SKILL.md
    manifest.yaml
    references/
      investigation-checklist.md
      error-classification.md
    schemas/
      investigation-result.json
    evals/
      scenarios.yaml
      rubric.yaml
~~~

### Skill Manifest

~~~yaml
name: integration-debugging
version: 1.0.0
compatible_agents: [react_investigator, multi_agent_command]
required_capabilities: [customer_records.read, incidents.read]
optional_capabilities: [sentry.read, github.read]
output_schema: investigation_report
policies:
  allow_writes: false
  require_evidence: true
success_criteria:
  - identify_affected_environment
  - establish_failure_timeline
  - compare_recent_deployments
  - cite_supporting_evidence
  - report_confidence
~~~

### Skill Execution

1. Router classifies the request.
2. Skill Registry returns compatible skills.
3. Runtime selects an agent and skill.
4. Skill instructions and resources are loaded.
5. Tool Gateway exposes only allowed capabilities.
6. Agent executes.
7. Trace records the selected skill and tool surface.
8. Evaluator checks whether the correct skill was selected and followed.

## 6. Shared Agent OS Services

| Service | Responsibility |
| --- | --- |
| Agent Registry | Definitions, versions, capabilities, compatibility |
| Skill Registry | Discovery, loading, versioning, resources |
| Tool Gateway | Function tools and least-privilege capability policies |
| MCP Gateway | Connections, filtering, caching, failures, approvals |
| Memory Service | Sessions, summaries, facts, preferences, provenance |
| Workflow Engine | Steps, branches, retries, checkpoints, timers |
| Policy Engine | Permissions, invariants, and human approval |
| Trace Service | Model, tool, MCP, handoff, guardrail, audio, custom events |
| Evaluation Engine | Dataset runs, graders, comparison, release gates |
| Run Store | Inputs, outputs, state, events, artifacts, costs, status |

### Responsibility Map

| Component | Owns |
| --- | --- |
| Studio | User experience, feature modules, streaming views, approvals, comparisons |
| Control Plane | Auth context, agent registry, run routing, approvals, aggregate traces/evals |
| Agent Service | Agent logic, local skills/tools, execution, service-specific datasets |
| Agent Worker | Long-running execution using the same Agent Service code |
| Nexus Operations | Business entities and transactional rules |
| Shared Python packages | Stable contracts and proven cross-service infrastructure |
| PostgreSQL | Separate schemas owned by each service |
| Redis/Temporal | Optional execution infrastructure for selected services |

## 7. Required Learning Loop for Every Agent

Each project follows the same progression:

1. **Build the naive version:** one prompt and one happy path.
2. **Instrument it:** capture tools, arguments, events, timing, cost, skill, result.
3. **Break it:** ambiguous inputs, bad tools, conflicting evidence, policy attacks.
4. **Build the dataset:** convert failures into versioned scenarios.
5. **Evaluate it:** deterministic graders first; model graders where necessary.
6. **Harden it:** improve schemas, skills, routing, guardrails, memory, approvals.
7. **Compare it:** run baseline and candidate against the same dataset.
8. **Extend it:** complete one challenge that changes the architecture.

## 8. Required Specification for Every Agent

Every agent folder must document:

1. Problem, target user, user stories, and non-goals
2. Architecture and execution lifecycle
3. OpenAI primitives being tested
4. NVIDIA pattern correlation
5. Tools, MCP servers, skills, and SOPs
6. Backend data model and APIs
7. Context and memory strategy
8. Permissions and approval policy
9. Failure modes and recovery behavior
10. Dataset design and evaluation metrics
11. Unit, integration, model-behavior, and end-to-end tests
12. MVP acceptance criteria and advanced challenges
13. Learning objectives, demo script, and retrospective

## 8.1 Core Concept Coverage

The curriculum is organized around transferable concepts, not eight unrelated demos.

| Concept | Introduced | Deepened |
| --- | --- | --- |
| Structured outputs and tools | Agent 1 | Every later agent |
| Skills and SOP execution | Agent 1 | Agents 2, 3, 4, 7, 8 |
| Retrieval and RAG | Agent 2 | Agents 3 and 5 |
| Artifact generation | Agent 2 | Agents 4, 5, and 7 |
| Agent loops | Agent 3 | Agents 6 and 7 |
| Deterministic workflows | Agent 4 | Agents 7 and 8 |
| Parallel execution | Agent 5 | Agent 7 |
| Routing and handoffs | Agent 6 | Agents 7 and 8 |
| Multi-agent orchestration | Agent 7 | Agent 8 handoff |
| Voice/realtime | Agent 8 | Capstone |
| Memory | Agent 1 sessions | Progressively across all agents |
| Evaluation | Agent 1 | Every later agent |
| Scale/workers | Agent 1 load baseline | System-wide performance track |

## 8.2 Retrieval and RAG Learning Ladder

The project deliberately implements retrieval several ways and compares them on the same tasks:

1. **Direct context:** load a few small stable documents.
2. **Hosted file search:** use OpenAI File Search for a managed baseline.
3. **PostgreSQL retrieval:** use pgvector so the open-source stack can run locally.
4. **Metadata filtering:** customer, document type, date, permission, and version.
5. **Hybrid retrieval:** semantic plus keyword results.
6. **Reranking:** reorder candidates before model use.
7. **Agentic retrieval:** allow a bounded agent to reformulate or repeat searches.
8. **Evaluation:** retrieval recall, relevance, grounding, latency, and cost.

Each step must answer: what failure in the previous approach justified the new complexity?

## 8.3 Memory Learning Ladder

Memory is separated into distinct problems:

1. **Run context:** dependencies and state available during one run.
2. **Conversation session:** prior turns for the current conversation.
3. **Summary memory:** compressed conversation history.
4. **Durable facts:** user, account, or project facts stored in PostgreSQL.
5. **Preference memory:** explicitly approved user preferences.
6. **Episodic memory:** previous runs and outcomes.
7. **Semantic recall:** retrieve relevant prior facts or lessons.
8. **Multi-agent state:** decide what specialists share and what remains isolated.
9. **Memory hygiene:** provenance, correction, deletion, tenancy, privacy, and expiration.

Every memory experiment must test false recall, stale facts, cross-tenant leakage, context growth, and correction behavior.

### Memory Assignments by Agent

| Agent | Memory experiment |
| --- | --- |
| Structured Tool | SDK session history plus tenant-safe run context |
| SOP Analysis | Job state, document/rubric versions, reviewer corrections |
| ReAct Investigator | Hypothesis ledger and evidence accumulated during a run |
| Planner/Executor | Durable plan checkpoints and resumable workflow state |
| ReWOO Researcher | Evidence cache with provenance and freshness |
| Router/Handoff | Conversation history filtering across handoffs |
| Multi-Agent Command | Shared case state versus private specialist context |
| Voice | Realtime session history, post-call summary, approved durable facts |

## 8.4 Orchestration and Handoff Ladder

OpenFDE explicitly teaches all three common coordination styles:

| Style | Use when | Reference build |
| --- | --- | --- |
| Agent as tool | A manager retains the user conversation | Multi-Agent Command Agent |
| Handoff | A specialist takes ownership of the conversation | Router and Voice Agents |
| Deterministic code | Ordering, policy, or business invariants must be predictable | Planner/Executor |

The Router project compares these styles on the same dataset. The Multi-Agent project adds typed contracts, parallel specialists, conflict resolution, and budgets. The Voice project demonstrates a realtime handoff without losing context.

## 8.5 Artifact Learning Ladder

Artifacts use one canonical structured result:

1. Agent produces validated Pydantic/JSON data.
2. Deterministic code validates citations and calculations.
3. Templates render HTML.
4. HTML becomes PDF.
5. A separate template renders DOCX.
6. Artifact metadata records source, skill, rubric, agent, and dataset versions.
7. Visual regression tests verify layout.

Agents do not directly improvise binary files. They produce structured content that deterministic renderers turn into reliable artifacts.

## 8.6 Performance and Scale Track

Every agent first runs locally. After the core behavior passes evaluations, selected agents enter the shared performance track.

### Load Stages

1. One request at a time
2. Ten concurrent runs
3. Fifty requests per minute
4. One hundred requests per minute
5. Five hundred requests per minute target experiment

### Concepts

- Async I/O and connection pools
- API and model-provider rate limits
- Worker concurrency
- Queues and backpressure
- Idempotency and deduplication
- Retry safety
- Timeouts and cancellation
- Redis caching where justified
- Horizontal worker scaling
- Per-tenant quotas
- Cost budgets
- Trace sampling
- Graceful degradation

### Success Measures

- Throughput
- p50, p95, and p99 latency
- Queue wait time
- Failure and retry rate
- Model and tool saturation
- Database connection use
- Cost per successful task
- Quality under load

The purpose is not to claim 500 requests per minute automatically. The purpose is to run a reproducible load test, find the bottleneck, change the architecture, and publish the evidence.

# 9. The Eight Agent Projects

## Agent 1 — Skill-Aware Structured Tool Agent

### Product

**Nexus Account Operations Agent**

It answers account questions and performs controlled CRM operations:

- Show Acme's active implementation.
- List its unresolved incidents.
- Create a follow-up task for tomorrow.
- Update the incident owner after approval.

### Why It Comes First

Tool calling is the foundation of every later project. This agent teaches that reliability depends on schema design, descriptions, validation, permissions, and error handling—not only prompting.

### Pattern and OpenAI Scope

- **NVIDIA correlation:** Tool Calling Agent
- **OpenAI features:** Agent, Runner, function tools, MCP tools, Pydantic outputs, guardrails, sessions, approval, tracing

### Skills

- account-lookup
- task-creation
- incident-update
- approval-required-write

The runtime records the chosen skill. The agent does not receive every skill for every request.

### Tools

- get_account
- list_implementations
- list_incidents
- create_task
- update_incident

Start with FastAPI-backed function tools. Expose the same operations through a custom Nexus MCP server as the advanced exercise.

### Execution Lifecycle

1. Validate user identity and tenant.
2. Select a skill.
3. Expose the minimum tool set.
4. Read required records.
5. Produce a structured result or proposed action.
6. Pause if the action modifies state.
7. Resume after approval.
8. Persist the run and trace.

### MVP

- One seeded account
- Three read tools and one write tool
- Two skills
- Structured result schema
- Approval before writes
- Trace view with arguments and results
- Twenty-five evaluation scenarios

### Dataset

Include clear single-tool requests, similar tools, missing identifiers, ambiguous account names, invalid dates, confirmation-required actions, no-tool requests, cross-tenant attempts, timeouts, and not-found responses.

### Evaluation

- Tool-selection accuracy
- Argument exactness
- Schema validity
- Unauthorized-action rate
- Approval compliance
- Unnecessary-call rate
- Recovery rate
- Latency and cost

### What You Learn

- How descriptions affect tool choice
- How schemas constrain calls
- How to separate read and write capabilities
- How to pause and resume for approval
- How to test orchestration without real model calls
- Why authorization remains deterministic

### Push Yourself

- Build the Nexus MCP server.
- Add role-based dynamic tool filtering.
- Inject a deliberately misleading tool description and measure the failure.
- Compare one large tool with several narrow tools.
- Make write retries idempotent.

### Definition of Done

The agent passes at least 95 percent of deterministic tool and policy scenarios, never crosses tenant boundaries, and cannot write without approval.

---

## Agent 2 — SOP-Grounded Analysis and Artifact Agent

### Product

**Call Quality Analysis Agent**

The user supplies a transcript, SOP documents, a scoring rubric, compliance rules, and coaching guidance. The agent produces:

- Overall and category scores
- Evidence linked to transcript turns
- Missed behaviors and compliance findings
- Positive behaviors
- Coaching recommendations
- Follow-up actions
- Validated JSON
- Rendered HTML, PDF, and Word reports

The reusable pattern is broader than calls:

- Interview transcript to candidate assessment
- Incident timeline to postmortem
- Contract to risk report
- Support case to QA review
- Meeting transcript to action plan
- Research packet to executive brief

### Why It Matters

This is one of the most common production-agent jobs: analyze source material against reference documents and generate a professional artifact. It teaches retrieval, long-document processing, evidence grounding, rubric evaluation, structured output, and file generation.

### Pattern and OpenAI Scope

- **NVIDIA correlation:** combines Tool Calling, Reasoning, and Sequential Executor patterns
- **OpenAI features:** FileSearchTool, function tools, structured Pydantic output, agents as tools, guardrails, tracing, optional audio transcription, optional sandbox/file capabilities

This is intentionally a controlled pipeline rather than an unrestricted ReAct loop. The model analyzes evidence; deterministic code validates schemas, computes totals, and renders artifacts.

### Skills

- sales-call-analysis
- support-call-quality
- compliance-review
- coaching-recommendations
- executive-call-summary
- artifact-generation

Each skill identifies required documents, rubric version, evidence rules, output schema, and allowed artifact formats.

### Inputs

- Transcript with stable speaker and turn IDs
- Call metadata
- SOP and rubric documents
- Compliance requirements
- Output template and branding
- Optional audio recording

### Retrieval Progression

1. Load four short documents directly through the skill.
2. Move the same documents into OpenAI File Search.
3. Add metadata filtering by customer, call type, and rubric version.
4. Build a PostgreSQL/pgvector retrieval adapter.
5. Compare semantic, keyword, hybrid, and reranked retrieval.

RAG is introduced only when the direct-context baseline exposes a real limitation.

### Execution Lifecycle

1. Validate transcript, metadata, and document versions.
2. Select the analysis skill and rubric.
3. Segment the transcript by turn and topic.
4. Retrieve applicable rubric sections.
5. Extract evidence for every category.
6. Score categories with typed output.
7. Run a critic agent against unsupported conclusions.
8. Calculate aggregate scores deterministically.
9. Validate all cited turn IDs.
10. Produce the canonical JSON result.
11. Render HTML from the JSON.
12. Generate PDF and DOCX from the validated representation.
13. Persist artifact, skill, rubric, dataset, and agent versions.

### Data Model

- analysis_job
- source_document
- document_version
- transcript
- transcript_turn
- rubric
- rubric_category
- evidence_span
- category_score
- analysis_result
- artifact
- reviewer_correction

### MVP

- Four SOP/rubric documents
- Twenty synthetic transcripts
- One sales-call-analysis skill
- Five rubric categories
- Structured JSON output
- Evidence linked to turn IDs
- Deterministic total score
- HTML report
- PDF export
- Human correction screen
- Baseline evaluation report

DOCX generation follows after the canonical JSON and HTML/PDF path is stable.

### Dataset

Include excellent, average, and poor calls; short and long transcripts; multiple speakers; missing labels; emotional users; jargon; partial compliance; conflicting evidence; not-applicable categories; rubric-version changes; prompt injection inside transcripts; sensitive information; and cases where evidence is insufficient.

Ground-truth records should contain:

- Human category scores
- Supporting turn IDs
- Missing required behaviors
- Compliance violations
- Expected coaching themes
- Acceptable score ranges when reviewers can reasonably disagree

### Evaluation

- Human-score agreement
- Evidence precision and coverage
- Rubric completeness
- Unsupported-claim rate
- Score consistency
- Rubric-version correctness
- Citation validity
- JSON schema validity
- Artifact generation success
- Cost and latency

### What You Learn

- Direct context versus RAG
- Chunking, metadata filters, hybrid retrieval, and reranking
- Long-transcript segmentation
- Evidence-first analysis
- Rubric and grader design
- Structured outputs as canonical data
- JSON-to-HTML/PDF/DOCX artifact pipelines
- Human review and correction capture

### Push Yourself

- Generate a candidate rubric from SOP documents and require approval.
- Compare full-context and chunked analysis.
- Run two independent analyst agents and measure agreement.
- Add a reviewer agent that can reject unsupported scores.
- Analyze hundreds of calls for organizational trends.
- Support customer-defined and versioned rubrics.
- Add transcription and speaker diarization.
- Generate branded PDF and Word templates.

### Definition of Done

Every score is tied to a rubric version and evidence, deterministic totals match the category scores, artifacts render from validated data, and the agent abstains when the transcript cannot support a conclusion.

---

## Agent 3 — ReAct Investigation Agent

### Product

**Customer Integration Investigator**

It investigates why a customer integration or deployment is failing.

### Why It Matters

Real investigations are not predictable single calls. The agent must form hypotheses, gather evidence, react to results, recover from dead ends, and stop when it has enough support.

### Pattern and OpenAI Scope

- **NVIDIA correlation:** ReAct Agent
- **OpenAI features:** multi-turn loop, function/MCP tools, dynamic filtering, error handling, maximum turns, run context, sessions, guardrails, tracing

### Skills

- integration-debugging
- incident-investigation
- root-cause-analysis
- evidence-citation

### Tools and Integrations

- Nexus Operations
- GitHub MCP
- Sentry MCP or simulated observability
- Documentation search
- Deployment diff tool

Begin with Nexus and GitHub. Add Sentry after the basic investigation loop is reliable.

### Execution Lifecycle

1. Establish account, integration, and environment.
2. Load the investigation skill.
3. Build an initial timeline.
4. Form at least two plausible hypotheses.
5. Select evidence-gathering actions.
6. Observe results and revise hypotheses.
7. Stop when one is sufficiently supported or evidence is exhausted.
8. Return diagnosis, evidence, confidence, alternatives, and next steps.

### MVP

- One broken-integration scenario
- Four read-only tools
- One investigation skill
- Bounded tool-call loop
- Evidence-linked report
- Trace timeline
- Fifty evaluation scenarios

### Dataset

Include deployment regressions, expired credentials, rate limits, bad configuration, unrelated simultaneous errors, contradictory records, missing monitoring, broken MCP servers, malformed tool results, unknowable causes, and prompt injection embedded in tool output.

### Evaluation

- Correct root-cause category
- Evidence precision and recall
- Unsupported-claim count
- Relevant-tool ratio
- Dead-end recovery
- Correct abstention
- Confidence calibration
- Call-limit compliance
- Cost and time to diagnosis

### What You Learn

- Agent loops versus deterministic workflows
- Tool-surface design
- Untrusted tool-output handling
- Trace-driven debugging
- Stopping criteria
- Evidence-calibrated confidence

### Push Yourself

- Compare several tool-description variants.
- Add stale data and require provenance checking.
- Implement a hypothesis ledger in application state.
- Add a critic pass that challenges the diagnosis.
- Compare ReAct with a deterministic checklist.

### Definition of Done

The agent produces an evidence-backed diagnosis or explicitly abstains, remains within limits, and never presents an unsupported hypothesis as fact.

---

## Agent 4 — Reasoning Planner and Deterministic Executor

### Product

**Customer Implementation and Migration Planner**

It turns goals, requirements, and SOP documents into an executable plan.

### Why It Matters

Many tasks should not be improvised step by step. Planning first makes dependencies, approvals, risks, and completion criteria inspectable before actions begin.

### Pattern and OpenAI Scope

- **NVIDIA correlation:** Reasoning Agent plus Sequential Executor
- **OpenAI features:** structured outputs, agents as tools, code orchestration, context, sessions, guardrails, approval, custom trace spans

### Skills

- customer-onboarding
- api-migration
- implementation-planning
- rollback-planning
- risk-review

### Tools

- Read customer requirements
- Read SOPs
- Inspect current integration configuration
- Search documentation
- Create proposed tasks
- Validate dependencies

### Plan Contract

Every plan contains:

- Objective and assumptions
- Required information
- Ordered steps and dependencies
- Parallelizable groups
- Tools and owners
- Approval points
- Risks and rollback
- Completion criteria

### Execution Lifecycle

1. Gather requirements and constraints.
2. Select the planning skill.
3. Generate a typed plan.
4. Run schema and dependency validation.
5. Ask for missing information.
6. Present the plan for approval.
7. Execute approved steps through code or worker agents.
8. Check completion criteria after each stage.
9. Pause, retry, compensate, or escalate.
10. Produce a final implementation record.

### MVP

- One API migration scenario
- One SOP
- Typed plan model
- Dependency validator
- Approval before execution
- Three deterministic steps
- Plan/execution trace
- Forty planning scenarios

### Dataset

Include incomplete requirements, conflicts, hidden dependencies, parallel steps, required approvals, rollback cases, impossible deadlines, unsupported versions, mid-execution failure, and requirement changes after approval.

### Evaluation

- Required-step coverage
- Dependency correctness
- Invalid-order rate
- Approval placement
- Risk coverage
- Feasibility
- Execution completion
- Recovery and compensation
- Plan stability

### What You Learn

- Upfront reasoning versus ReAct
- Executable model contracts
- Deterministic orchestration
- Resumable workflows
- Plan drift
- Plans versus answers

### Push Yourself

- Add Temporal as durable executor.
- Add parallel branches and compensation.
- Visualize dependencies.
- Add a reviewer agent.
- Compare planning with and without SOP retrieval.

### Definition of Done

The system cannot execute an invalid or unapproved plan, resumes after interruption, and verifies completion instead of assuming it.

---

## Agent 5 — ReWOO Research and Synthesis Agent

### Product

**Customer 360 and Technical Briefing Agent**

It collects information from independent systems and produces a sourced customer or implementation brief.

### Why It Matters

Enterprise agent workloads are often evidence-synthesis problems. Planning once and executing independent lookups concurrently can reduce repeated reasoning, latency, and token use.

### Pattern and OpenAI Scope

- **NVIDIA correlation:** ReWOO planning, execution, and solution phases
- **OpenAI features:** structured planner, agents as tools, concurrent execution, normalized tool results, context, custom tracing, synthesis agent

### Skills

- customer-health-brief
- account-research
- technical-due-diligence
- executive-summary
- evidence-synthesis

### Sources

- Nexus account and implementation data
- GitHub release data
- Sentry incidents
- Product analytics
- Documentation and support records

### Execution Lifecycle

1. Define the decision the brief supports.
2. Create an evidence plan.
3. Assign stable evidence identifiers.
4. Run independent retrieval concurrently.
5. Normalize and validate results.
6. Mark missing or conflicting evidence.
7. Synthesize only from collected evidence.
8. Return citations, uncertainty, and recommendations.

### MVP

- Three independent data sources
- Structured evidence plan
- Concurrent retrieval
- Normalized evidence objects
- Sourced brief
- Latency/token comparison with ReAct
- Forty research scenarios

### Dataset

Include full evidence, missing sources, duplicate facts, conflicting status, stale data, irrelevant retrievals, noisy outputs, time-sensitive facts, negative findings, and unavoidable uncertainty.

### Evaluation

- Evidence coverage
- Citation correctness
- Unsupported-claim count
- Conflict detection
- Staleness awareness
- Retrieval relevance
- Parallel speedup
- Token and call efficiency
- Decision usefulness

### What You Learn

- Planning versus reacting
- Async fan-out and aggregation
- Evidence normalization
- Context-window management
- Provenance and citations
- Architectural efficiency measurement

### Push Yourself

- Weight sources by quality.
- Add freshness-aware caching.
- Use different models for planning and synthesis.
- Trim large tool results.
- Compare sequential, parallel, ReAct, and ReWOO versions.

### Definition of Done

Important claims point to evidence, conflicts are visible, missing sources do not become silent assumptions, and parallelism measurably improves latency.

---

## Agent 6 — Router, Skill Selector, and Handoff Agent

### Product

**OpenFDE Front Door**

It decides what work is being requested, which skill applies, and whether to retain control or transfer to a specialist.

### Why It Matters

As the catalog grows, routing becomes a system reliability problem. A bad route creates failure before a specialist begins.

### Pattern and OpenAI Scope

- **NVIDIA correlation:** Router Agent
- **OpenAI features:** structured classification, handoffs, conditional availability, input filters, agents as tools, sessions, guardrails, handoff tracing

### Skill Metadata

The router reads summaries rather than loading all skill contents:

- Name and description
- Compatible agents
- Required capabilities
- Trigger and exclusion examples
- Risk level

### Routes

- Account operations
- Incident investigation
- Implementation planning
- Customer briefing
- Multi-agent escalation
- Voice follow-up
- Human escalation
- Out of scope

### Execution Lifecycle

1. Normalize request and conversation context.
2. Detect authorization or safety concerns.
3. Retrieve candidate skill metadata.
4. Classify intent, risk, and confidence.
5. Clarify when confidence is insufficient.
6. Select agent plus skill.
7. Use an agent-as-tool when the front door retains ownership.
8. Use a handoff when the specialist owns the conversation.
9. Record the route and reason.

### Handoff Laboratory

Implement the same support workflow three ways:

1. **Manager pattern:** front-door agent calls specialists as tools and keeps the conversation.
2. **Handoff pattern:** front-door agent transfers ownership and filtered history to the specialist.
3. **Code router:** application code selects the specialist from structured classification.

Compare route accuracy, context passed, user experience, tool availability, latency, cost, and trace complexity. Include a second handoff back to the front door or to a human escalation path.

### MVP

- Four destinations
- One out-of-scope route
- Skill metadata registry
- Structured router output
- One manager-style agent-as-tool path
- One true specialist handoff with typed reason and filtered history
- One deterministic code route
- One human escalation path
- Studio confusion matrix
- One hundred routing examples

### Dataset

Include clear intents, similar intents, multi-intent requests, implicit intents, contextual follow-ups, mid-conversation changes, clarification cases, out-of-domain requests, adversarial wording, unseen skills, and mandatory escalation.

### Evaluation

- Route and skill accuracy
- Per-class precision and recall
- Confusion matrix
- Clarification quality
- False-handoff rate
- Out-of-scope detection
- Confidence calibration
- Latency and cost

### What You Learn

- Handoffs versus agents as tools
- Intent taxonomy design
- Dataset balance
- Context-dependent classification
- Skill discovery
- Confidence and fallback

### Push Yourself

- Add hierarchical routing.
- Retrieve skills semantically before classification.
- Measure degradation as the catalog grows.
- Compare model routing with rules.
- Build a hybrid router.

### Definition of Done

The router meets per-class thresholds, clarifies instead of guessing, and escalates risky or unsupported requests.

---

## Agent 7 — Multi-Agent Command Agent

### Product

**Customer Escalation Command Center**

It coordinates specialists to investigate an escalation, assess business impact, review policy, plan recovery, and prepare communications.

### Why It Matters

Specialization can improve quality, but multi-agent systems can duplicate work, lose context, disagree, and become expensive. This project teaches disciplined coordination rather than agent count.

### Pattern and OpenAI Scope

- **NVIDIA correlation:** agents and tools as composable functions
- **OpenAI features:** agents as tools, handoffs, concurrent specialists, typed outputs, shared run context, guardrails, approval, nested traces, sessions

### Specialists and Skills

| Specialist | Skill |
| --- | --- |
| Technical Investigator | integration-debugging |
| Customer Impact Analyst | customer-impact-analysis |
| Policy Reviewer | security-and-policy-review |
| Recovery Planner | incident-recovery-planning |
| Communications Writer | customer-communications |
| Final Reviewer | evidence-and-consistency-review |

### Execution Lifecycle

1. Decompose the escalation.
2. Select only necessary specialists.
3. Run independent specialists concurrently.
4. Collect typed findings with evidence and confidence.
5. Identify agreement and conflict.
6. Perform one bounded follow-up if needed.
7. Run final consistency and policy review.
8. Produce one recommendation.
9. Pause tasks and messages for approval.

### MVP

- Three specialists
- Typed contracts
- Parallel execution
- Conflict-resolution step
- Final synthesis
- Approval before actions
- Hierarchical trace
- Thirty complex cases

### Dataset

Include one-specialist cases, all-specialist cases, contradictory conclusions, duplicate work, failed specialists, shared evidence, policy blocks, business-priority changes, and separate internal/customer communications.

### Evaluation

- Specialist selection
- Delegation completeness
- Duplicate-work rate
- Specialist evidence quality
- Conflict resolution
- Final consistency
- Policy compliance
- End-to-end success
- Total latency and cost

### What You Learn

- Manager versus decentralized orchestration
- Agent contracts
- Shared versus isolated context
- Parallel coordination
- Conflict resolution
- Cost control
- Nested trace design

### Push Yourself

- Add dynamic specialist discovery.
- Compare sequential and concurrent versions.
- Give the command agent a fixed budget.
- Add a red-team specialist.
- Allow controlled specialist-to-specialist requests.

### Definition of Done

Specialists must improve measured quality. The final answer reconciles conflicts and remains traceable to evidence.

---

## Agent 8 — Realtime Voice Operations Agent

### Product

**Voice FDE Concierge**

A user can report an issue, ask for implementation status, schedule a follow-up, or reach a specialist by speaking. The agent can use tools while talking and must confirm consequential actions.

### Why It Is the Capstone

Voice combines realtime streaming, sessions, interruption, tools, skills, routing, handoffs, confirmation, latency, transcripts, and audio evaluation.

The OpenAI Agents SDK supports realtime speech-to-speech agents and voice pipelines that combine speech-to-text, an agent workflow, and text-to-speech. OpenFDE starts with a browser-based realtime agent.

### Pattern and OpenAI Scope

- **NVIDIA correlation:** extension of the same composable agent architecture
- **OpenAI features:** RealtimeAgent, RealtimeSession, WebRTC, voice activity detection, interruption handling, function tools, hosted MCP where appropriate, realtime handoffs, session history, guardrails, audio/tool tracing

### Technologies

- React and TypeScript voice UI
- OpenAI Agents SDK TypeScript realtime client
- WebRTC
- FastAPI endpoint for authenticated short-lived credentials
- Secure server-side tool endpoints
- PostgreSQL transcript and run metadata
- Optional server WebSocket or telephony integration later

### Skills

- voice-incident-intake
- voice-status-update
- voice-scheduling
- voice-confirmation
- human-escalation

Voice skills must instruct the agent to keep responses short, confirm names/dates/identifiers, read back consequential actions, reject background speech as approval, handle interruption, and offer text confirmation for precision.

### Execution Lifecycle

1. Authenticate before session creation.
2. Mint short-lived credentials.
3. Start realtime session.
4. Detect speech and interruption.
5. Select a voice skill.
6. Gather identifiers conversationally.
7. Call secure tools.
8. Speak a concise result.
9. Read back proposed writes.
10. Require explicit confirmation.
11. Persist transcript, tool events, outcome, latency, and consent.

### MVP

- Browser microphone
- One realtime voice agent
- Live transcript
- One read tool
- One approval-required write tool
- Interruption support
- Session summary
- Trace view
- Twenty transcript cases and ten representative audio samples

### Datasets

**Transcript cases:** clear commands, ambiguous dates, corrections, interruption, contextual references, explicit/implicit confirmation, background speech, frustration, and handoffs.

**Audio cases:** varied microphones, noise, speech speed, accents, partial words, crosstalk, silence, pauses, barge-in, and easily confused names or IDs.

Use consented, synthetic, or licensed audio. Never publish private customer recordings.

### Evaluation

- Task success
- Critical-field understanding
- Tool and argument correctness
- Confirmation compliance
- False-confirmation rate
- Interruption recovery
- Turn latency and time to first audio
- Handoff accuracy
- Conversation length
- User-rated clarity

### What You Learn

- WebRTC and realtime lifecycle
- Speech-to-speech versus STT-agent-TTS
- Voice activity detection and barge-in
- Spoken UX
- Secure browser-to-tool architecture
- Audio testing and observability
- Latency-driven design

### Push Yourself

- Handoff to the Incident Investigator.
- Add telephony.
- Support another language.
- Compare realtime speech-to-speech with a voice pipeline.
- Add human takeover.
- Test network degradation and reconnect.
- Add pronunciation hints.

### Definition of Done

The agent completes one useful workflow naturally, survives interruption, calls tools safely, and never writes based on unclear or accidental confirmation.

# 10. Dataset Strategy

## Dataset Families

One aggregate score hides important failures, so OpenFDE maintains separate families.

| Dataset | What it measures |
| --- | --- |
| Skill selection | Correct SOP/capability package |
| Routing | Correct agent or workflow |
| Tool selection | Correct capability |
| Tool arguments | IDs, dates, enums, payloads |
| Retrieval | Recall, relevance, filtering, reranking, grounding |
| Analysis rubric | Human-score agreement and evidence support |
| Artifacts | Schema, citations, calculations, rendering, layout |
| Workflow | Required steps and ordering |
| Memory | Relevant retention without invented facts |
| Evidence | Grounding and provenance |
| Recovery | Missing data and tool failures |
| Policy | Authorization and approval |
| Efficiency | Calls, tokens, latency, cost |
| Voice transcript | Conversation and confirmation |
| Voice audio | Noise, accents, interruption, latency |
| Performance | Throughput, tail latency, failures, quality, and cost under load |

## Scenario Schema

~~~yaml
id: incident_deployment_regression_001
agent: react_investigator
skill: integration-debugging

input:
  message: Acme started failing after yesterday's release.

fixtures:
  account: acme
  deployment: v2.4
  incident: inc_104

expect:
  route: incident_investigation
  required_tools:
    - get_account
    - get_recent_deployments
    - get_incident_events
  forbidden_tools:
    - update_incident
  required_evidence:
    - deployment_v2_4
    - error_signature_17
  outcome:
    root_cause_category: deployment_regression

policies:
  read_only: true
  require_approval_before_write: true

limits:
  max_tool_calls: 8
  max_latency_ms: 15000
  max_cost_usd: 0.08

tags: [investigation, deployment, happy_path]
~~~

## How Data Is Created

1. Humans author seed scenarios for critical behavior.
2. Synthetic generation expands wording and edge cases.
3. Mutation generators remove fields, corrupt IDs, reorder events, and fail tools.
4. Red-team cases target prompt injection and policy boundaries.
5. Development failures become regression tests.
6. Production-derived cases require anonymization and permission review.

Synthetic generation proposes scenarios; it does not establish ground truth. Deterministic rules or human review must validate labels.

## Dataset Splits

- **Development:** visible cases used while building
- **Validation:** visible metrics used while tuning
- **Test:** held-out release cases
- **Challenge:** adversarial architecture stress
- **Regression:** every previously discovered failure

## Dataset Quality Rules

- Every scenario has a reason.
- Expected routes and tools are justified.
- Ambiguous cases explicitly allow clarification or multiple valid paths.
- Negative cases are included.
- Class balance is measured.
- Dataset and agent versions are linked.
- Model-generated labels are reviewed before becoming ground truth.

# 11. Evaluation Architecture

## Grader Selection

| Layer | Preferred grader |
| --- | --- |
| Schema validity | Deterministic code |
| Tool identity and arguments | Deterministic code |
| Route and skill | Deterministic code |
| Policy and approval | Deterministic code |
| Workflow order | Trace assertions |
| Evidence linkage | Deterministic plus optional model judge |
| Factual synthesis | Reference plus model-assisted grader |
| Communication quality | Rubric judge plus human review |
| Voice naturalness | Human rating and audio metrics |

## Release Gate

Do not promote a candidate when:

- Any critical policy case fails.
- A routing class falls below its threshold.
- Tool success improves while unauthorized actions increase.
- Quality improves only by violating cost or latency limits.
- Voice confirmation produces a false positive in the safety set.

## Test Layers

1. Unit tests for tools, policies, schemas, and skill loading.
2. Scripted SDK tests for tools, handoffs, guardrails, retries, sessions, Realtime events, and voice pipeline composition.
3. Integration tests against Nexus and MCP servers.
4. Model-behavior evaluations on versioned datasets.
5. Browser tests for Studio and approvals.
6. Audio and network tests for voice.

# 12. Open-Source Learning Experience

Every agent should feel like a compact course.

## Required Folder

~~~text
agents/<agent-name>/
  README.md
  architecture.md
  naive/
  production/
  skills/
  tools/
  datasets/
  evals/
  tests/
  exercises/
  failure-notes.md
  retrospective.md
~~~

## README Learning Path

1. Understand the problem and pattern.
2. Run the naive version.
3. Inspect its trace.
4. Run the failure dataset.
5. Fix one failure.
6. Compare the result.
7. Build or inspect the production version.
8. Complete an extension exercise.

## Teaching Artifacts

- Source walkthroughs
- Architecture decision records
- Intentionally broken examples
- TODO exercises
- Dataset-generation scripts
- Trace screenshots
- Failure postmortems
- Baseline/candidate reports
- Demo videos
- Copyable templates

The repository must teach why the code exists, not merely display finished code.

# 13. Build Order

## Foundation

- Monorepo
- FastAPI
- PostgreSQL
- Next.js Studio shell
- Nexus seed data
- Run and event models
- Agent and Skill Registries
- Basic tracing

## Curriculum Milestones

1. Skill-Aware Structured Tool Agent
2. SOP-Grounded Analysis and Artifact Agent
3. ReAct Investigation Agent
4. Reasoning Planner and Deterministic Executor
5. ReWOO Research and Synthesis Agent
6. Router, Skill Selector, and Handoff Agent
7. Multi-Agent Command Agent
8. Realtime Voice Operations Agent

## Final Integration

The OpenFDE Front Door accepts text or voice, selects the correct agent, skill, tools, workflow, and policy, and exposes the entire run in Studio.

# 14. First Public MVP

The first public release should include:

- Foundation services
- Structured Tool Agent
- SOP-Grounded Analysis Agent with JSON and HTML output
- ReAct Investigation Agent
- Router with three destinations
- Two complete skills
- One custom Nexus MCP server
- Session memory
- Approval before writes
- Trace Explorer
- Scenario runner
- Deterministic evaluation report
- One complete customer-incident demo
- Roadmap stubs for the remaining agents

This proves the architecture without requiring eight production implementations before release.

# 15. Suggested Repository Structure

~~~text
openfde/
  apps/
    studio/
      src/
        app/
          agents/
            [agent-slug]/
        features/
          structured-tool/
          sop-analysis-artifact/
          react-investigator/
          reasoning-planner/
          rewoo-researcher/
          router-handoff/
          multi-agent-command/
          realtime-voice/
        components/
          ui/
          traces/
          datasets/
          approvals/
        lib/
          api-client/
          auth/
          streaming/

  services/
    control-plane/
      app/
      migrations/
      tests/
      Dockerfile

    nexus-operations/
      app/
      migrations/
      seed/
      tests/
      Dockerfile

    agents/
      01-structured-tool/
        app/
          api/
          agent/
          domain/
          tools/
          skills/
          evals/
        migrations/
        tests/
        Dockerfile

      02-sop-analysis-artifact/
      03-react-investigator/
      04-reasoning-planner/
      05-rewoo-researcher/
      06-router-handoff/
      07-multi-agent-command/
      08-realtime-voice/

  packages/
    python/
      openfde-contracts/
      openfde-runtime/
      openfde-skills/
      openfde-mcp/
      openfde-memory/
      openfde-tracing/
      openfde-evals/
      openfde-artifacts/

    typescript/
      api-client/
      shared-types/
      ui/

  skills/
    account-operations/
    sales-call-analysis/
    support-call-quality/
    artifact-generation/
    integration-debugging/
    implementation-planning/
    customer-health-brief/
    customer-impact-analysis/
    security-policy-review/
    customer-communications/
    voice-incident-intake/

  mcp-servers/
    nexus/

  examples/
    nexus-operations/
      sop-documents/
      transcripts/

  artifacts/
    templates/
      html/
      docx/
    fixtures/

  datasets/
    skill-selection/
    routing/
    tool-use/
    retrieval/
    call-analysis/
    artifacts/
    workflow/
    memory/
    policy/
    performance/
    voice/

  infra/
    docker/
      compose.core.yaml
      compose.all.yaml
    temporal/
    load/

  tests/
    integration/
    end-to-end/
    load/

  docs/
    architecture/
    curriculum/
    decisions/
    tutorials/
~~~

### Repository Rules

1. One monorepo.
2. One Next.js frontend server with feature modules organized by agent project.
3. One FastAPI Control Plane with no agent-specific reasoning.
4. One independent FastAPI service per agent project.
5. One Nexus Operations backend consumed through API or MCP.
6. One shared run/event/result contract across services.
7. One PostgreSQL server locally; separate service-owned schemas and migrations.
8. No direct cross-service database reads.
9. Skills and datasets can be service-local first, then promoted to shared packages when reused.
10. Each agent service has naive and production implementations.
11. Each service can run alone with Control Plane, Nexus, and Studio.
12. Redis and Temporal remain optional, service-specific infrastructure.
13. Workers use the same service code and contracts as synchronous execution.
14. Shared libraries are extracted only after two services need the same abstraction.

### Frontend Feature Contract

Each agent feature contains:

~~~text
features/<agent-name>/
  api/
  components/
  hooks/
  schemas/
  state/
  views/
  tests/
  index.ts
~~~

Agent-specific UI remains inside its feature. Generic buttons, forms, tables, dialogs, trace primitives, dataset editors, and approval components live in shared folders. A feature may compose shared components but cannot import another feature's internal files.

The dynamic agent route loads the registered feature shell, while each project can still have custom screens:

- Structured Tool: tool-call inspector
- SOP Analysis: transcript evidence and artifact preview
- ReAct: hypothesis and investigation timeline
- Planner: dependency graph
- ReWOO: evidence fan-out
- Router: confusion matrix and handoff trace
- Multi-Agent: specialist tree and conflicts
- Voice: realtime audio, transcript, interruptions, and tools

### Real-World Product Categories Represented

| OpenFDE build | Common product category |
| --- | --- |
| Structured Tool Agent | Operations assistant and action copilot |
| SOP Analysis Agent | Conversation intelligence, QA, compliance, document analysis |
| ReAct Investigator | Incident and support investigation copilot |
| Planner/Executor | Implementation, migration, and onboarding automation |
| ReWOO Researcher | Account research and executive briefing |
| Router/Handoff | Support triage and specialist routing |
| Multi-Agent Command | Escalation, case management, and analyst team |
| Realtime Voice | Voice support, scheduling, and operations concierge |

OpenFDE teaches the reusable architecture beneath these marketplace categories rather than cloning one vendor's interface.

# 16. What Makes OpenFDE Stand Out

1. The same domain and data compare several architectures.
2. Skills, tools, MCP, memory, workflows, and approvals remain separate concepts.
3. Every agent ships with datasets and measurable completion criteria.
4. Intentionally broken implementations teach debugging.
5. Studio visualizes decisions, not just chat messages.
6. Voice is a production interaction mode, not a text-to-speech add-on.
7. The repository teaches when not to use an agent.
8. The final product demonstrates flexible AI under deterministic software control.

# 17. NVIDIA-to-OpenFDE Mapping

| NVIDIA NeMo Agent Toolkit | OpenFDE |
| --- | --- |
| Tool Calling Agent | Skill-Aware Structured Tool Agent |
| Tool Calling + Reasoning + Sequential Executor | SOP-Grounded Analysis and Artifact Agent |
| ReAct Agent | ReAct Investigation Agent |
| Reasoning Agent | Reasoning Planner |
| ReWOO Agent | Research and Synthesis Agent |
| Router Agent | Router, Skill Selector, Handoff Agent |
| Sequential Executor | Deterministic Python or Temporal workflow |
| Agent implemented as function | OpenAI agent exposed as tool |
| Automatic Memory Wrapper | OpenFDE Memory Service plus SDK sessions |
| Functions/function groups | Function tools, MCP tools, skills, agent tools |
| Workflow observability | SDK traces plus OpenFDE evaluations |
| Composable workflows | Agent, skill, tool, policy, workflow registries |

The Voice Agent is an OpenFDE capstone using OpenAI Realtime capabilities, not a claimed direct NVIDIA equivalent.

# 18. Official References

## OpenAI

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Agents](https://openai.github.io/openai-agents-python/agents/)
- [Tools](https://openai.github.io/openai-agents-python/tools/)
- [MCP](https://openai.github.io/openai-agents-python/mcp/)
- [Handoffs](https://openai.github.io/openai-agents-python/handoffs/)
- [Sessions](https://openai.github.io/openai-agents-python/sessions/)
- [Sandbox Agent Memory](https://openai.github.io/openai-agents-python/sandbox/memory/)
- [Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [Testing](https://openai.github.io/openai-agents-python/testing/)
- [Realtime Agents](https://openai.github.io/openai-agents-js/guides/voice-agents/)

## NVIDIA Inspiration

- [NVIDIA NeMo Agent Toolkit](https://docs.nvidia.com/nemo/agent-toolkit/latest/)
- [Building Workflows](https://docs.nvidia.com/nemo/agent-toolkit/latest/build-workflows/about-building-workflows.html)
- [ReAct Agent](https://docs.nvidia.com/nemo/agent-toolkit/latest/components/agents/react-agent/react-agent.html)
- [Reasoning Agent](https://docs.nvidia.com/nemo/agent-toolkit/latest/components/agents/reasoning-agent/reasoning-agent.html)
- [Memory](https://docs.nvidia.com/nemo/agent-toolkit/latest/build-workflows/memory.html)

# 19. Open-Source Description

> OpenFDE Studio is an open-source, full-stack learning platform where developers build, break, trace, evaluate, and compare eight production agent architectures using the OpenAI Agents SDK, MCP integrations, reusable skills, memory, retrieval, artifact generation, deterministic workflows, human approvals, multi-agent orchestration, and realtime voice.

# 20. Resume Version

> Built OpenFDE Studio, an open-source full-stack agent engineering platform featuring eight production agent architectures, a skill and MCP runtime, retrieval and artifact pipelines, durable workflows, human approval, trace visualization, versioned evaluation datasets, multi-agent orchestration, and a realtime voice experience using the OpenAI Agents SDK.
