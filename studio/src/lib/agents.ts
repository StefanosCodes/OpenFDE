export type AgentStatus = "ready-next" | "planned";

export type PaperSection = {
  heading: string;
  paragraphs: readonly string[];
};

export type AgentProject = {
  number: number;
  slug: string;
  name: string;
  shortName: string;
  status: AgentStatus;
  pattern: string;
  tagline: string;
  deliverable: string;
  concepts: readonly string[];
  paper: {
    title: string;
    lede: string;
    sections: readonly PaperSection[];
  };
};

export const agents: readonly AgentProject[] = [
  {
    number: 1,
    slug: "01-structured-tool",
    name: "Structured Tool Agent",
    shortName: "structured tool",
    status: "ready-next",
    pattern: "Tool-calling loop",
    tagline: "Resolve customer context, retrieve bounded evidence, and prepare an approved action.",
    deliverable: "Account and call resolution with an approval-gated follow-up task.",
    concepts: ["function tools", "typed output", "guardrails", "approval", "tracing"],
    paper: {
      title: "Structured Tool Agent",
      lede: "The first project proves that a narrow tool surface, typed context, and deterministic approval can support useful agent behavior without hiding the system.",
      sections: [
        {
          heading: "Build",
          paragraphs: [
            "The agent resolves an account, searches compact call records, retrieves only the transcript evidence it needs, and proposes one follow-up task. Nexus remains the source of truth.",
            "Application code derives idempotency and pauses for approval before the write tool is exposed. The model never receives credentials, arbitrary SQL, or a generic Nexus client.",
          ],
        },
        {
          heading: "Foundation",
          paragraphs: [
            "This room is intentionally not bound to a model yet. The React route and Nexus contract are ready; the run service, tools, traces, and evaluation set are the next milestone.",
          ],
        },
      ],
    },
  },
  {
    number: 2,
    slug: "02-sop-analysis",
    name: "SOP Analysis and Artifact Agent",
    shortName: "sop analysis",
    status: "planned",
    pattern: "Grounded analysis pipeline",
    tagline: "Score a call against a versioned SOP and produce evidence-backed artifacts.",
    deliverable: "Typed JSON and HTML analysis with transcript-turn citations.",
    concepts: ["direct context", "structured output", "evidence validation", "artifacts"],
    paper: {
      title: "SOP Analysis and Artifact Agent",
      lede: "The second project turns retrieved evidence into a reviewable analysis without treating a fluent answer as proof.",
      sections: [
        {
          heading: "Build",
          paragraphs: [
            "The agent loads one small versioned rubric, scores a selected call, and cites stable transcript turns. Deterministic validation rejects evidence that does not exist in the source.",
          ],
        },
        {
          heading: "Measure",
          paragraphs: [
            "Direct context is the baseline. File Search or pgvector earns a place only after the reviewed evaluation set shows that direct context is insufficient.",
          ],
        },
      ],
    },
  },
  {
    number: 3,
    slug: "03-react-investigator",
    name: "ReAct Investigation Agent",
    shortName: "react investigator",
    status: "planned",
    pattern: "Bounded adaptive loop",
    tagline: "Form hypotheses, gather evidence, recover from failed tools, and stop deliberately.",
    deliverable: "A grounded diagnosis with a visible hypothesis ledger.",
    concepts: ["multi-turn loops", "dynamic tools", "failure recovery", "stopping conditions"],
    paper: {
      title: "ReAct Investigation Agent",
      lede: "The third project studies adaptive investigation while keeping tool access, turns, and claims bounded.",
      sections: [
        {
          heading: "Build",
          paragraphs: [
            "The agent records hypotheses, selects evidence, reacts to missing or failed tools, and stops when the evidence supports a conclusion or the investigation budget is exhausted.",
          ],
        },
        {
          heading: "Boundary",
          paragraphs: [
            "Nexus stays unchanged unless measured cases prove a missing narrow query. The investigation loop belongs to the agent service, not the business sandbox.",
          ],
        },
      ],
    },
  },
  {
    number: 4,
    slug: "04-planner-executor",
    name: "Planner and Executor Agent",
    shortName: "planner executor",
    status: "planned",
    pattern: "Plan then execute",
    tagline: "Create a typed dependency plan, then execute approved steps deterministically.",
    deliverable: "A resumable plan with checkpoints and explicit approval boundaries.",
    concepts: ["structured planning", "code orchestration", "checkpoints", "resumability"],
    paper: {
      title: "Planner and Executor Agent",
      lede: "The fourth project separates probabilistic planning from deterministic execution.",
      sections: [
        {
          heading: "Build",
          paragraphs: [
            "The model proposes a typed plan with dependencies. Application code validates it, pauses at consequential actions, and executes known ordering instead of asking the model to remember control flow.",
          ],
        },
        {
          heading: "Recovery",
          paragraphs: [
            "Persisted checkpoints make interruption visible and resumption deliberate. A failed step does not silently replay completed side effects.",
          ],
        },
      ],
    },
  },
  {
    number: 5,
    slug: "05-rewoo-researcher",
    name: "ReWOO Research Agent",
    shortName: "rewoo researcher",
    status: "planned",
    pattern: "Plan, retrieve, synthesize",
    tagline: "Plan evidence needs once, retrieve independently, and synthesize with provenance.",
    deliverable: "A normalized research result with source attribution and cost comparison.",
    concepts: ["agents as tools", "concurrency", "normalization", "context control"],
    paper: {
      title: "ReWOO Research Agent",
      lede: "The fifth project tests whether separating planning from retrieval reduces repeated reasoning and context growth.",
      sections: [
        {
          heading: "Build",
          paragraphs: [
            "The planner identifies independent evidence needs once. Application code retrieves them concurrently, normalizes failures and provenance, and supplies a bounded packet for synthesis.",
          ],
        },
        {
          heading: "Compare",
          paragraphs: [
            "The project compares quality, cost, and latency against a sequential baseline using the same stable cases.",
          ],
        },
      ],
    },
  },
  {
    number: 6,
    slug: "06-router-handoff",
    name: "Router and Handoff Agent",
    shortName: "router handoff",
    status: "planned",
    pattern: "Classification and delegation",
    tagline: "Select the right capability and compare routing, tools, and handoffs.",
    deliverable: "A measured routing layer with explicit session ownership.",
    concepts: ["classification", "conditional tools", "handoffs", "input filters"],
    paper: {
      title: "Router and Handoff Agent",
      lede: "The sixth project makes delegation semantics explicit instead of treating every specialist call as equivalent.",
      sections: [
        {
          heading: "Build",
          paragraphs: [
            "The project compares deterministic code routing, a manager invoking a specialist as a tool, and a true handoff where the specialist owns the next interaction.",
          ],
        },
        {
          heading: "Registry",
          paragraphs: [
            "This is the first point where a tiny agent registry may be justified. It contains discoverable contracts, not agent reasoning or another orchestration framework.",
          ],
        },
      ],
    },
  },
  {
    number: 7,
    slug: "07-multi-agent-command",
    name: "Multi-Agent Command Agent",
    shortName: "multi-agent command",
    status: "planned",
    pattern: "Manager with specialists",
    tagline: "Run specialists concurrently, reconcile typed recommendations, and enforce a budget.",
    deliverable: "A command workflow with conflict handling and nested traces.",
    concepts: ["specialist agents", "concurrency", "shared context", "budget guardrails"],
    paper: {
      title: "Multi-Agent Command Agent",
      lede: "The seventh project tests coordination only after the individual agent contracts are understood.",
      sections: [
        {
          heading: "Build",
          paragraphs: [
            "A manager delegates bounded work to specialists, receives typed results, identifies disagreement, and produces a final recommendation within a fixed tool and token budget.",
          ],
        },
        {
          heading: "Observe",
          paragraphs: [
            "Nested traces show which specialist contributed each claim, what failed, and where concurrency actually reduced latency.",
          ],
        },
      ],
    },
  },
  {
    number: 8,
    slug: "08-realtime-voice",
    name: "Realtime Voice Operations Agent",
    shortName: "realtime voice",
    status: "planned",
    pattern: "Realtime conversational workflow",
    tagline: "Handle interruptions, tool calls, confirmation, and safe voice handoff.",
    deliverable: "A realtime workflow that confirms consequential actions before execution.",
    concepts: ["streaming audio", "interruptions", "realtime tools", "confirmation", "handoffs"],
    paper: {
      title: "Realtime Voice Operations Agent",
      lede: "The final project applies the earlier safety and orchestration lessons to a realtime interface.",
      sections: [
        {
          heading: "Build",
          paragraphs: [
            "The agent identifies an account, answers bounded questions, checks availability, confirms a consequential action, and hands off without losing verified context.",
          ],
        },
        {
          heading: "Realtime",
          paragraphs: [
            "The evaluation covers interruption, partial speech, tool latency, cancellation, and confirmation—not merely whether a demo conversation sounds natural.",
          ],
        },
      ],
    },
  },
];

export const studioPaper = {
  title: "OpenFDE",
  lede: "OpenFDE.studio is an open-source workshop for learning how reliable agents are actually built. Each project isolates one pattern, makes its boundaries visible, and measures the result.",
  sections: [
    {
      heading: "Studio",
      paragraphs: [
        "The index is a curriculum rather than a marketplace. Each project has an overview, a paper, and a workspace route. The interface stays quiet so the engineering evidence remains the content.",
        "The Studio is one React application. Route-driven projects share the shell without sharing agent runtime or backend business logic.",
      ],
    },
    {
      heading: "Nexus",
      paragraphs: [
        "Nexus is the deliberately small customer-intelligence sandbox beneath the projects: one FastAPI service, one PostgreSQL database, six tables, and thirteen routes.",
        "Nexus owns data integrity, bounded retrieval, authentication, and idempotent writes. Agents own model loops, skills, tools, memory, approval, traces, and evaluations.",
      ],
    },
    {
      heading: "Sequence",
      paragraphs: [
        "The projects are built in order. Complexity is introduced only when the current exercise needs it and its evaluation can show what the added mechanism changed.",
      ],
    },
  ],
} as const;

export function getAgent(slug: string): AgentProject | undefined {
  return agents.find((agent) => agent.slug === slug);
}

export function agentStatusLabel(status: AgentStatus): string {
  return status === "ready-next" ? "Ready next" : "Planned";
}
