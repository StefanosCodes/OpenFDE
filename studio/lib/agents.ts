export type PaperSection = {
  heading: string;
  paragraphs: readonly string[];
};

export type Agent = {
  slug: string;
  name: string;
  tagline: string;
  paper: {
    title: string;
    lede: string;
    sections: PaperSection[];
  };
};

export const agents: Agent[] = [
  {
    slug: "architect",
    name: "architect",
    tagline: "Designs the system before the first line is written.",
    paper: {
      title: "Architect",
      lede: "A builder who needs a system should not start in the editor. Architect is the agent for that first cut: outcomes, boundaries, and the smallest slice that can prove the rest.",
      sections: [
        {
          heading: "Charge",
          paragraphs: [
            "Architect reads the intended outcome against the current repository. It names constraints that are real, preferences that are negotiable, and unknowns that still block a decision. It does not invent platform for a local problem.",
            "The deliverable is a design that a builder can execute without reconstructing the argument. If a choice is assumed, the paper says so.",
          ],
        },
        {
          heading: "Enter",
          paragraphs: [
            "View Agent opens the room. Bring a feature, a migration, or a rough product idea. Architect will not write the product until the contract is clear enough to build against.",
          ],
        },
      ],
    },
  },
  {
    slug: "builder",
    name: "builder",
    tagline: "Implements the slice that makes the design true.",
    paper: {
      title: "Builder",
      lede: "Builder is the agent that turns an agreed contract into working software. It prefers the existing system, the smallest coherent change, and evidence over ceremony.",
      sections: [
        {
          heading: "Charge",
          paragraphs: [
            "Builder inspects the repository before it edits. It keeps unrelated refactors out of the slice, preserves security boundaries, and stops when the acceptance criteria can be observed.",
            "A finished slice is not a pile of files. It is a path a person can run: the change, the check, and the result.",
          ],
        },
        {
          heading: "Enter",
          paragraphs: [
            "View Agent opens the room. Bring a contract, a failing test, or a bounded feature. Builder will not expand scope to make the architecture more interesting.",
          ],
        },
      ],
    },
  },
  {
    slug: "debugger",
    name: "debugger",
    tagline: "Traces a failure until the cause is named.",
    paper: {
      title: "Debugger",
      lede: "Debugger is the agent for when observed behavior disagrees with expected behavior. It reproduces first, ranks hypotheses, and does not patch a symptom in place of a cause.",
      sections: [
        {
          heading: "Charge",
          paragraphs: [
            "The work begins with a reproduction, not a theory. Debugger collects the narrowest runtime evidence that can distinguish one cause from another, then changes one variable at a time.",
            "If the evidence kills the current hypothesis, the agent returns to the earliest unsupported assumption. Fixes without that proof are out of scope.",
          ],
        },
        {
          heading: "Enter",
          paragraphs: [
            "View Agent opens the room. Bring a failing request, a broken worker, a bad trace, or a regression you can show. Debugger will not guess from a stack trace alone.",
          ],
        },
      ],
    },
  },
  {
    slug: "reviewer",
    name: "reviewer",
    tagline: "Reads a change for whether it is safe to merge.",
    paper: {
      title: "Reviewer",
      lede: "Reviewer is the agent that stands between a working-tree diff and the main branch. It is read-only unless asked to implement. The question is not whether the code is clever. The question is whether the change is true.",
      sections: [
        {
          heading: "Charge",
          paragraphs: [
            "Reviewer inspects correctness, design fit, regressions, authorization, data integrity, and the tests that would fail if the protected behavior broke. It distinguishes confirmed facts from unverified claims in the diff itself.",
            "Praise is cheap and omitted. Findings are ordered by the damage they can do.",
          ],
        },
        {
          heading: "Enter",
          paragraphs: [
            "View Agent opens the room. Bring a branch, a pull request, or a local diff. Reviewer will not merge, and it will not quietly rewrite the change unless that is the task.",
          ],
        },
      ],
    },
  },
  {
    slug: "evaluator",
    name: "evaluator",
    tagline: "Measures agent behavior on a stable set of cases.",
    paper: {
      title: "Evaluator",
      lede: "Evaluator is the agent for stochastic work that cannot be proven by a single anecdote. It holds the case set still, names the criteria, and reports what the traces actually show.",
      sections: [
        {
          heading: "Charge",
          paragraphs: [
            "Evaluator does not claim improvement from a changing prompt and a changing test set. Cases stay representative. Graders stay explicit. Failures get classified before they get celebrated.",
            "This studio already keeps a Promptfoo entry point for that loop. Evaluator is the agent that treats those runs as evidence, not as decoration.",
          ],
        },
        {
          heading: "Enter",
          paragraphs: [
            "View Agent opens the room. Bring a workflow, a prompt change, or a production failure distribution. Evaluator will not declare a winner from one lucky transcript.",
          ],
        },
      ],
    },
  },
];

export const studioPaper = {
  title: "OpenFDE",
  lede: "OpenFDE.studio is an open-source place for builders who want to build. The index is the studio. Each name is an agent. Each agent is a paper you can read and a room you can enter.",
  sections: [
    {
      heading: "Studio",
      paragraphs: [
        "The home page is a directory, not a feed. It lists agents the way a workshop lists benches. Nothing here is a product screenshot and nothing here is a marketplace. If you want to build, you pick a bench.",
        "The surface is an empty page. Type is white. The topography behind the index is atmosphere, not content. The paper is the content.",
      ],
    },
    {
      heading: "Agents",
      paragraphs: [
        "An agent has two doors. View Paper is the statement of charge: what the agent is for, what it refuses, and what you should bring. View Agent takes you into the room.",
        "The rooms exist so the studio has destinations. Model runtime is a later binding. The contract of this place is the path: index, paper, agent.",
      ],
    },
    {
      heading: "Source",
      paragraphs: [
        "OpenFDE is public. The studio, the papers, and the evaluation entry point live in the same repository. Fork it, change the roster, or bind an agent to a real runtime when you have one worth binding.",
      ],
    },
  ],
} as const;

export function getAgent(slug: string): Agent | undefined {
  return agents.find((agent) => agent.slug === slug);
}
