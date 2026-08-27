import { Link, useParams } from "react-router-dom";

import { PageChrome, StudioMark } from "../components/page-chrome";
import { agentStatusLabel, getAgent } from "../lib/agents";
import { useDocumentTitle } from "../lib/use-document-title";
import { NotFoundPage } from "./not-found";

export function AgentOverviewPage() {
  const { agentSlug = "" } = useParams();
  const agent = getAgent(agentSlug);
  useDocumentTitle(agent?.name);

  if (!agent) {
    return <NotFoundPage />;
  }

  return (
    <main className="shell">
      <PageChrome left={<StudioMark />} right={<span>Project {agent.number} of 8</span>} />
      <div className="shell-center">
        <div className="stack overview-stack">
          <div className={`project-status status-${agent.status}`}>
            {agentStatusLabel(agent.status)}
          </div>
          <header className="doorway-header">
            <h1>{agent.name}</h1>
            <p className="tagline">{agent.tagline}</p>
          </header>
          <dl className="project-details">
            <div>
              <dt>Pattern</dt>
              <dd>{agent.pattern}</dd>
            </div>
            <div>
              <dt>Deliverable</dt>
              <dd>{agent.deliverable}</dd>
            </div>
          </dl>
          <nav aria-label="Agent project" className="action-list">
            <Link className="action-link" to={`/agents/${agent.slug}/paper`}>
              Read project paper
            </Link>
            <Link className="action-link" to={`/agents/${agent.slug}/workspace`}>
              Enter workspace
            </Link>
          </nav>
        </div>
      </div>
    </main>
  );
}
