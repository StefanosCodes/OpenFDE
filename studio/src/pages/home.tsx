import { Link } from "react-router-dom";

import { NexusStatus } from "../components/nexus-status";
import { agents, agentStatusLabel } from "../lib/agents";
import { useDocumentTitle } from "../lib/use-document-title";

export function HomePage() {
  useDocumentTitle();

  return (
    <main className="shell shell-center">
      <div className="stack curriculum-stack">
        <header className="home-header">
          <h1>OpenFDE.studio</h1>
          <p className="tagline">eight projects for building reliable agents</p>
        </header>
        <nav aria-label="Agent projects" className="nav-list">
          {agents.map((agent) => (
            <Link className="nav-link project-link" to={`/agents/${agent.slug}`} key={agent.slug}>
              <span>
                <span className="project-number">{String(agent.number).padStart(2, "0")}</span>
                {agent.shortName}
              </span>
              <span className={`project-status status-${agent.status}`}>
                {agentStatusLabel(agent.status)}
              </span>
            </Link>
          ))}
        </nav>
        <footer className="home-footer studio-footer">
          <div className="footer-links">
            <Link to="/paper">paper</Link>
            <a
              href="https://github.com/StefanosCodes/OpenFDE"
              rel="noreferrer"
              target="_blank"
            >
              source
            </a>
          </div>
          <NexusStatus />
        </footer>
      </div>
    </main>
  );
}
