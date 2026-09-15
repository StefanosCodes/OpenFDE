# Agent 1 From First Principles

This guide turns OpenFDE Agent 1 into a slow, observable learning path. The goal is to understand
one layer completely before adding the next layer.

It is a companion to:

- [Agent 1 in the master project planner](../../../OPENFDE_STUDIO_MASTER_PROJECT_PLANNER.md#agent-1--skill-aware-structured-tool-agent)
- [The Agent 1 guide](../README.md)

Active code has reached the mock multi-tool checkpoint described in Section 4. It lives in
`../backend/`, while the later sections remain the planned hardening path.

## 1. The two goals

Agent 1 has a product goal and a learning goal. Keeping them separate makes the project easier to
understand.

### Product goal

Build a narrow Nexus account-operations assistant that can:

1. Resolve the account the user means.
2. Retrieve only the customer evidence needed for the request.
3. Return a grounded answer.
4. Propose one follow-up task when the request and evidence justify it.
5. Require human approval before writing the task.

The current implementation uses accounts, calls, transcripts, documents, and tasks. It is narrower
than the master planner's original examples involving implementations and incidents, but it teaches
the same agent pattern.

### Learning goal

Learn how a model uses typed tools to interact with an application while ordinary code controls
data access, validation, identity, authorization, and side effects.

By the end of Agent 1, we should be able to explain:

- what an `Agent` defines;
- what the `Runner` does;
- how a model selects a tool;
- how a tool schema constrains arguments;
- how a Python function executes outside the model;
- how tool results return to the model;
- how structured output controls response shape;
- why trusted runtime context belongs to application code;
- why a requested write is not automatically an authorized write;
- how approval pauses and resumes the same run;
- how traces and evaluations reveal failures.

## 2. The smallest correct mental model

An SDK agent is primarily a configured unit of behavior:

```text
Agent
= model
+ instructions
+ tools
+ optional output type and controls
```

The surrounding web service, database, frontend, authentication, persistence, and evaluation
harness are part of the agent application. They are not the core agent loop.

The core loop is:

```text
User message
    |
    v
Runner sends the message, instructions, and tool definitions to the model
    |
    v
Model produces either a final answer or a tool request
    |
    +-- final answer -------------------------------> run ends
    |
    `-- tool request
            |
            v
        Application executes the Python tool
            |
            v
        Tool result returns to the Runner
            |
            `---------------------------------------> model continues
```

This matches the official OpenAI description of the runner loop: the runner calls the model,
inspects the result, executes requested tools, and continues until the model returns a final answer.

## 3. The build rule

Use this rule throughout the curriculum:

> Add one new source of complexity only after the previous layer is observable and explainable.

For every section, answer six questions:

1. What capability did we add?
2. Why is it needed now?
3. What information does the model receive?
4. What decision is the model allowed to make?
5. What remains controlled by deterministic application code?
6. What observable evidence proves the section works?

Do not move to the next section because the code merely runs. Move on when we can explain the
flow and recognize its main failure modes.

## 4. Learning path overview

| Section | Add one concept | Main question | Observable checkpoint |
| --- | --- | --- | --- |
| 0 | Behavioral contract | What job are we asking the agent to do? | Input and expected result are clear without architecture terms |
| 1 | One agent and one turn | What are `Agent` and `Runner`? | A model receives one message and returns one answer |
| 2 | One fake read tool | How does tool calling work? | We observe the tool name, arguments, result, and final answer |
| 3 | One real Nexus tool | Where does business data access live? | The same agent answers from real account data |
| 4 | Two read tools | How does the model choose and sequence tools? | The model resolves an account and then finds its calls |
| 5 | Structured output | How do we constrain the final response shape? | Every successful result validates against one small schema |
| 6 | Trusted run context | What must the application own? | Identity, tenant, time, and limits never come from model claims |
| 7 | One write proposal | How are reads different from side effects? | A task can be proposed without being executed |
| 8 | Human approval | How do we safely execute a write? | Approve executes once; reject executes nothing |
| 9 | Traces and scenarios | How do we inspect and improve behavior? | Failures are visible and converted into repeatable cases |
| 10 | Function tools versus MCP | When is a different tool transport justified? | Both variants run against the same cases and can be compared |

## 5. Section 0: define one behavior

### Goal

Describe the smallest useful job before choosing implementation details.

Use one request:

```text
Find the Acme account.
```

Expected behavior:

```text
The system resolves Acme to an account and reports a small, factual summary.
```

### Decide up front

- Input: one user message.
- Data needed: account name and status.
- Output: a concise answer.
- No side effects.
- No conversation memory.
- No web API or user interface is required for this lesson.

### Checkpoint

We can explain the request, required data, and expected answer without saying "agent," "tool," or
"SDK."

### Read

- [OpenAI Agents SDK overview](https://developers.openai.com/api/docs/guides/agents)

## 6. Section 1: one agent and one turn

The core introduced in Section 1 remains visible in
[`agent.py`](../backend/agent.py) and
[`runtime.py`](../backend/runtime.py). The CLI, tests, and Promptfoo
provider all call the same `run_once` path; the current files also include the later mock tools.

### Add

- one `Agent`;
- one name;
- one instruction;
- one model;
- one `Runner.run(...)` call;
- one printed final output.

Do not add tools yet.

### Learn

- The agent definition configures behavior.
- The runner performs the execution.
- A single run is one application-level turn.
- A fluent response is not yet grounded in Nexus data.

### Watch

```text
input message -> Runner -> model -> final output
```

### Leave out

- FastAPI;
- React;
- Nexus;
- Pydantic output models;
- sessions;
- approvals;
- custom traces;
- evaluations.

### Checkpoint

We can point to the exact line that defines the agent and the exact line that starts the run. We can
also explain why this is an assistant but not yet a useful account-data agent.

### Read

- [Agents SDK quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart)
- [Defining a focused agent](https://developers.openai.com/api/docs/guides/agents/define-agents)
- [Running agents and the runner loop](https://developers.openai.com/api/docs/guides/agents/running-agents)

## 7. Section 2: one fake read tool

### Add

One local function with deterministic fake data:

```python
def search_accounts(query: str) -> list[dict[str, str]]:
    return [{"name": "Acme Health", "status": "active"}]
```

Expose only this function to the agent.

### Learn

- A tool is a capability described to the model.
- A tool call is the model's request to use that capability.
- The model produces the tool name and arguments.
- Application code executes the Python function.
- The returned value becomes new input to the next model turn.
- The tool call itself is not the final answer.

### Watch the complete flow

```text
1. User: "Find Acme."
2. Model: search_accounts({"query": "Acme"})
3. Python: executes search_accounts
4. Tool: returns [{"name": "Acme Health", "status": "active"}]
5. Model: forms a final answer from the returned data
```

For this lesson, print or inspect:

- the original user input;
- the tool selected by the model;
- the exact arguments;
- the exact tool result;
- the final output.

### Experiment

Change only the tool description and observe whether the model's behavior changes. Then restore the
clear description. This demonstrates that tool descriptions are part of the agent's behavioral
interface.

### Checkpoint

We can narrate all five events without treating the model as if it executed Python itself.

### Read

- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)
- [Defining agent tools](https://developers.openai.com/api/docs/guides/agents/define-agents)

## 8. Section 3: connect one tool to Nexus

### Add

Replace the fake function body with a call to Nexus while keeping the model-visible capability
nearly unchanged:

```text
search_accounts(query)
    -> Nexus HTTP request
    -> Nexus database query
    -> bounded account result
```

### Learn

- The model chooses a business capability, not an HTTP endpoint or SQL query.
- The tool adapter owns credentials, networking, validation, and error translation.
- Nexus owns business data and persistence.
- The model only receives the bounded result that the tool returns.

### Watch

Separate the events into two layers:

```text
Model-visible layer: search_accounts({"query": "Acme"})
Application layer:   Python -> HTTP -> Nexus -> PostgreSQL -> Python
```

### Failure exercise

Make Nexus return a not-found result or a controlled error. Observe whether the tool and final
answer distinguish "no account exists" from "the dependency failed."

### Checkpoint

We can identify which facts the model selected, which facts application code supplied, and where
the real data originated.

### Read

- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)

### Compare later

This Nexus-backed layer is not implemented yet.

## 9. Section 4: add a second read tool

### Add

Add `search_calls` after `search_accounts` is understood.

Example request:

```text
What happened in Acme's latest call?
```

Possible flow:

```text
search_accounts(query="Acme")
    -> account_id
search_calls(account_id=account_id)
    -> latest call metadata
final answer
```

### Learn

- The model can choose more than one tool across runner turns.
- The result of one tool can supply an argument for the next tool.
- Narrow tools make choices and side effects easier to understand.
- Multiple available tools introduce routing and unnecessary-call failures.

### Test

- Clear account name.
- Ambiguous account name.
- Account not found.
- Account found with no calls.
- A request answerable without any tool.
- A request that should require both tools.

### Checkpoint

The model chooses the minimum sufficient read path on the small test set, and ambiguity produces an
honest clarification or no-action result rather than a guessed account.

### Read

- [Running agents and the agent loop](https://developers.openai.com/api/docs/guides/agents/running-agents)
- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)

## 10. Section 5: add structured output

### Add

Start with a deliberately small output type:

```python
class AgentOutput(BaseModel):
    summary: str
    account_id: UUID | None = None
```

### Learn

- Structured output constrains the shape of the model's answer.
- A valid schema does not prove the answer is factually correct.
- Application code can reliably consume a typed result.
- We should add fields only when a real consumer needs them.

### Watch

- the raw model result;
- parsed `AgentOutput`;
- schema validation failures;
- the difference between formatting validity and evidence validity.

### Checkpoint

Every successful run returns the same small contract, and we can explain what the schema guarantees
and what it does not guarantee.

### Read

- [OpenAI Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Defining agent output types](https://developers.openai.com/api/docs/guides/agents/define-agents)

## 11. Section 6: add trusted run context

### Add

Move trusted application facts into a run context:

- Nexus client;
- tenant identifier;
- actor identifier;
- current clock;
- business timezone;
- run identifier;
- evidence and tool-call records.

### Learn

- Context available to Python code is not automatically model-visible.
- User text and retrieved documents are untrusted input.
- Identity and tenant scope must come from verified application state.
- Limits and authorization are enforced by code, not by asking the model to behave.

### Test

- A user message that claims a different tenant.
- Retrieved text that instructs the agent to ignore its rules.
- A missing trusted tenant or actor.
- Excessive result limits.

### Checkpoint

Changing user text cannot change the server-owned tenant, actor, or authorization decision.

### Read

- [Defining agents and dynamic instructions](https://developers.openai.com/api/docs/guides/agents/define-agents)
- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)

### Compare later

This trusted-context layer is not implemented yet.

## 12. Section 7: add one write proposal

### Add

Introduce the arguments for one possible write:

```text
create_task(
    account_id,
    title,
    description,
    due_at
)
```

At first, treat this as a proposal and do not execute the database write.

### Learn

- Read tools retrieve information.
- Write tools produce side effects.
- A model request is a proposed action, not authorization.
- The exact proposed arguments must be reviewable.
- Application-controlled identifiers and idempotency values should not be supplied by the model.

### Checkpoint

The system can display the proposed task arguments, but no task can be created yet.

### Read

- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)
- [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)

## 13. Section 8: pause, approve, and resume

### Add

Require approval for `create_task` and preserve the paused run state.

```text
model requests create_task
    -> runner pauses before execution
    -> application displays exact arguments
    -> human approves or rejects

approve -> resume the stored run -> execute once -> return created task
reject  -> finish without executing the tool
```

### Learn

- Approval happens before the side effect.
- Approval applies to a specific stored tool call and its exact arguments.
- Resumption continues the original run rather than starting an unrelated new request.
- Duplicate approvals and retries require deterministic protection.

### Test

- Reject creates nothing.
- Approve creates exactly one task.
- Repeating the approval does not create a duplicate.
- A mismatched approval identifier fails.
- An expired approval fails.
- A resumed run cannot request a second unauthorized write.

### Checkpoint

There is no execution path that can create a task without a valid bound approval.

### Read

- [Guardrails and human-in-the-loop review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [Running and resuming agent workflows](https://developers.openai.com/api/docs/guides/agents/running-agents)

### Compare later

This approval-resume layer is not implemented yet.

## 14. Section 9: observe, break, evaluate, and harden

### Add

First inspect individual runs. Then turn important failures into a stable dataset.

Record or inspect:

- model turns;
- selected tools;
- tool arguments;
- tool results;
- approval interruptions;
- final output;
- latency and token usage;
- failures and recovery behavior.

### Learning loop

```text
Build one happy path
    -> inspect the trace
    -> deliberately break the behavior
    -> save the failure as a scenario
    -> add a deterministic check when possible
    -> compare the next change against the same scenarios
```

This is the repository's own required learning loop in smaller form: naive version, instrumentation,
failure discovery, dataset, evaluation, hardening, comparison, and only then extension.

### Start with these scenarios

- correct single-tool selection;
- correct two-tool sequence;
- exact argument extraction;
- ambiguous account;
- account not found;
- tool timeout;
- malformed tool result;
- unnecessary tool call;
- invalid structured output;
- task request without sufficient evidence;
- approval rejection;
- duplicate approval;
- cross-tenant claim;
- prompt injection inside retrieved text.

### Checkpoint

We can change a prompt, schema, or tool description and compare the candidate against the same cases
rather than judging it from one impressive demonstration.

### Read

- [Agents SDK integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability)
- [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)

### Compare later

The full scenario and trace layer is not implemented yet; only three starter scenarios exist.

## 15. Section 10: compare function tools with MCP

This is an advanced exercise, not part of the first tool-calling lesson.

### Add only after Section 9

Expose the same read capabilities through MCP without changing Nexus persistence ownership.

### Learn

- Function tools and MCP tools are different capability transports.
- A transport change should not silently change business semantics.
- The comparison needs the same dataset and acceptance criteria.
- MCP is justified by portability or integration needs, not because every agent needs it.

### Compare

- tool-selection accuracy;
- argument accuracy;
- response correctness;
- latency;
- trace shape;
- error behavior;
- implementation and operational cost.

### Checkpoint

Both adapters satisfy the same bounded read contract, and we can explain the practical tradeoff from
evidence.

### Read

- [Agents SDK integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability)

## 16. What to leave out until a failure requires it

Agent 1 does not initially need:

- multiple agents;
- handoffs;
- a planner/executor architecture;
- Redis or Temporal;
- background workers;
- semantic memory;
- vector retrieval;
- a large skill registry;
- dynamic tool search;
- a general control plane;
- distributed tracing infrastructure;
- Kubernetes or horizontal scaling.

These may be valid later. They are not part of learning the first tool-calling loop.

## 17. Reading order

Do not read every page before starting. Read the page that supports the current section.

1. [Agents SDK overview](https://developers.openai.com/api/docs/guides/agents)
2. [Agents SDK quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart)
3. [Defining agents](https://developers.openai.com/api/docs/guides/agents/define-agents)
4. [Running agents](https://developers.openai.com/api/docs/guides/agents/running-agents)
5. [Function calling](https://developers.openai.com/api/docs/guides/function-calling)
6. [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
7. [Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
8. [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability)
9. [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)

The official documentation itself recommends starting with one focused agent and adding additional
agents only when separate ownership, instructions, tool surfaces, or approval policies require it.
That is also the governing principle for this guide.

## 18. Immediate next milestone

The mock multi-tool loop is implemented. The next project milestone is Section 3: replace the mock
tool bodies with authenticated Nexus HTTP adapters while keeping the model-visible tool contracts
stable. New learners should still study Sections 1 and 2 first to understand the loop before tracing
the complete implementation.

The first real milestone is not "Agent 1 is production ready." It is:

> I can watch and explain every transition in one model-to-tool-to-model loop.
