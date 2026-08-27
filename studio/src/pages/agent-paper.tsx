import { Link, useParams } from "react-router-dom";

import { PageChrome, StudioMark } from "../components/page-chrome";
import { PaperDocument } from "../components/paper-document";
import { getAgent } from "../lib/agents";
import { useDocumentTitle } from "../lib/use-document-title";
import { NotFoundPage } from "./not-found";

export function AgentPaperPage() {
  const { agentSlug = "" } = useParams();
  const agent = getAgent(agentSlug);
  useDocumentTitle(agent ? `${agent.name} paper` : "Not found");

  if (!agent) {
    return <NotFoundPage />;
  }

  return (
    <main className="shell">
      <PageChrome
        left={<StudioMark />}
        right={<Link to={`/agents/${agent.slug}/workspace`}>Enter workspace</Link>}
      />
      <div className="paper-shell">
        <PaperDocument {...agent.paper} />
      </div>
    </main>
  );
}
