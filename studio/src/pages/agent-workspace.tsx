import { Link, useParams } from "react-router-dom";

import { PageChrome, StudioMark } from "../components/page-chrome";
import { agentStatusLabel, getAgent } from "../lib/agents";
import { useDocumentTitle } from "../lib/use-document-title";
import { NotFoundPage } from "./not-found";

export function AgentWorkspacePage() {
  const { agentSlug = "" } = useParams();
  const agent = getAgent(agentSlug);
  useDocumentTitle(agent ? `${agent.name} workspace` : "Not found");

  if (!agent) {
    return <NotFoundPage />;
  }

  return (
    <main className="workspace-page">
      <PageChrome
        left={<StudioMark />}
        right={<Link to={`/agents/${agent.slug}/paper`}>Read paper</Link>}
      />
      <div className="workspace">
        <div className="workspace-empty">
          <div className={`project-status status-${agent.status}`}>
            {agentStatusLabel(agent.status)}
          </div>
          <h1 className="workspace-title">{agent.name}</h1>
          <p className="lede">{agent.tagline}</p>
          <div className="runtime-boundary">
            <strong>{agent.number === 1 ? "Agent runtime comes next." : "This project is planned."}</strong>
            <p>
              This route is the interface boundary. No model response is simulated, and no agent
              service is running yet.
            </p>
          </div>
          <ul className="concept-list" aria-label="Project concepts">
            {agent.concepts.map((concept) => (
              <li key={concept}>{concept}</li>
            ))}
          </ul>
        </div>
      </div>
    </main>
  );
}
